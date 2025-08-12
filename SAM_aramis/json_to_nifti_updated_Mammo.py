import os
import nibabel as nib
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import glob
import pydicom
from nipype.interfaces.dcm2nii import Dcm2niix
import json
import shutil

path_to_dicom = r"C:/Users/USER/Desktop/vertibrae_2/dicom_files"
path_to_nifti = r"C:/Users/USER/Desktop/vertibrae_2/nifti_files"
path_to_editor_files = r"C:/Users/USER/Desktop/vertibrae_2/editor_files"

editor_axcode = "LPI"

shutil.rmtree(path_to_nifti)
shutil.rmtree(path_to_editor_files)
os.makedirs(path_to_nifti)
os.makedirs(path_to_editor_files)

subp_result = subprocess.run(["C:/Users/USER/Desktop/vertibrae_2/dcm2niix/dcm2niix.exe","-9","-f","%j","-d","9","-z","y","-o", path_to_nifti, path_to_dicom], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# print(subp_result.stdout)
# print(subp_result.stderr)

#### alternative for Ubuntu
# converter = Dcm2niix()

# converter.inputs.source_dir = path_to_dicom
# converter.compress = 'y'
# converter.inputs.compression = 9
# converter.out_filename = '%j'
# converter.inputs.output_dir = path_to_nifti
# converter.cmdline

# converter.run() 

path_to_prediction = r"C:\Users\USER\Desktop\vertibrae_2\predictions\response_en.json"
with open(path_to_prediction) as f:
    pred = json.load(f)

if (not (subp_result.stderr == "")):
    raise FileNotFoundError("Could not convert dicom to nifti\n", subp_result.stdout, subp_result.stderr)

# coords_and_uniq_val = [((1200,1300),(2400,2000),1), ((1400,2500),(3000,4000),2)]

line_thickness = 5

annot_mapping = { "calcified vessels" : 1, "calcinates_benign" : 2, "fibrocystic_breast_changes" : 3, "mass_benign" : 4}
orient_mapping = [('R','L'),('A','P'),('S','I')]

for individual_dicom_path in glob.glob(path_to_dicom+'/*'):
    ds = pydicom.dcmread(individual_dicom_path)
    acq_dev_proc_descr= str(ds[0x0018,0x1400].value)
    image_laterality = str(ds[0x0020,0x0062].value)
    print(acq_dev_proc_descr)
    try:
        patient_orientation = list(ds[0x0020,0x0020].value)
        print("patient_orientation",patient_orientation)
        # patient_orientation = [i.replace('F', '') for i in patient_orientation[-1::-1]]
        # print("patient_orientation",patient_orientation)
        if(image_laterality == 'L'):
            patient_orientation = [{'R':'L','A':'P','S':'I','L':'R','P':'A','I':'S'}[i.replace('F', '')] for i in patient_orientation[-1::-1]]
        elif(image_laterality == 'R'):
            patient_orientation = [i.replace('F', '') for i in patient_orientation[-1::-1]]
        print("patient_orientation",patient_orientation)
    except:
        print("No patient_orientation found")
        img_orientation = str(ds[0x0020,0x0037].value)
    for indx,i in enumerate([any([j in patient_orientation for j in i]) for i in orient_mapping]):
        if(not i):
            patient_orientation.append(orient_mapping[indx][0])
    print("patient_orientation_new",patient_orientation)
    
    seriesUID = str(ds[0x0020,0x000E].value)
    print(seriesUID)
    phot_imp = str(ds[0x0028,0x0004].value)
    individual_nifti_path = path_to_nifti+'/'+seriesUID+'.nii.gz'
    if (not os.path.isfile(individual_nifti_path)):
        continue
    # individual_nifti_path = "C:/Users/USER/Desktop/vertibrae_2/nifti_files/1.2.392.200036.9125.3.3616513216822.64984518430.30202290.nii.gz"
    img = nib.load(individual_nifti_path)
    # nib.orientations.ornt_transform(nib.orientations.io_orientation(img.affine),a)
    # nib.orientations.axcodes2ornt("".join(patient_orientation))
    img = img.as_reoriented(nib.orientations.ornt_transform(nib.orientations.io_orientation(img.affine),nib.orientations.axcodes2ornt("".join(patient_orientation))))
    
    img_data = np.asanyarray(img.dataobj)
    mask_data = np.zeros_like(img_data, dtype=np.uint8)
    
    coords_and_uniq_val = list()
    
    for annot in pred[acq_dev_proc_descr[0]]["detected_objects"][acq_dev_proc_descr[1:]]:
        x1,x2 = (annot["orig_coordinates"][0],annot["orig_coordinates"][2]) if annot["orig_coordinates"][0]<annot["orig_coordinates"][2] else (annot["orig_coordinates"][2],annot["orig_coordinates"][0])
        y1,y2 = (annot["orig_coordinates"][1],annot["orig_coordinates"][3]) if annot["orig_coordinates"][1]<annot["orig_coordinates"][3] else (annot["orig_coordinates"][3],annot["orig_coordinates"][1])
        if(annot["object_type"] in annot_mapping.keys()):
            coords_and_uniq_val.append(((x1,y1),(x2,y2),annot_mapping[annot["object_type"]]))
        else:
            print("New Keys found")
            coords_and_uniq_val.append(((x1,y1),(x2,y2),len(annot_mapping)+1))
    
    for ((x1,y1),(x2,y2),uniq_val) in coords_and_uniq_val:
        # mask_data[x1:x2+1, y1:y2+1,:] = uniq_val
        # mask_data[x1+line_thickness:x2+1-line_thickness, y1+line_thickness:y2+1-line_thickness,:] = 0
        mask_data[x1-line_thickness:x1, y1-line_thickness:y2+1+line_thickness,:] = uniq_val
        mask_data[x2+1:x2+1+line_thickness, y1-line_thickness:y2+1+line_thickness,:] = uniq_val
        mask_data[x1-line_thickness:x2+1+line_thickness, y1-line_thickness:y1,:] = uniq_val
        mask_data[x1-line_thickness:x2+1+line_thickness, y2+1:y2+1+line_thickness,:] = uniq_val
    
    mask = nib.Nifti1Image(mask_data, img.affine)
    mask = mask.as_reoriented(nib.orientations.ornt_transform(nib.orientations.io_orientation(mask.affine),nib.orientations.axcodes2ornt(editor_axcode)))
    nib.save(mask,os.path.join(path_to_editor_files,f"mask_{acq_dev_proc_descr}.nii.gz"))
    
    if(phot_imp == 'MONOCHROME1'):
        img_data = img_data.min() + img_data.max() - img_data
    
    img = nib.Nifti1Image(img_data, img.affine)
    img = img.as_reoriented(nib.orientations.ornt_transform(nib.orientations.io_orientation(img.affine),nib.orientations.axcodes2ornt(editor_axcode)))
    img.header['cal_min']=img_data.min()
    img.header['cal_max']=img_data.max()
    nib.save(img,os.path.join(path_to_editor_files,f"img_{acq_dev_proc_descr}.nii.gz"))
    # plt.imshow(img_data, cmap= "gray")


# individual_dicom_path = r"C:/Users/USER/Desktop/vertibrae_2/dicom_files/17c4f1b9-1ae7-427d-8afc-25c639d3b356"
# ds = pydicom.dcmread(individual_dicom_path)
# phot_imp = ds[0x0028,0x0004].value    
# seriesUID = ds[0x0020,0x000E].value
# acq_dev_proc_descr= ds[0x0018,0x1400].value