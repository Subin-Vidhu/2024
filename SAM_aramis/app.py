from flask import Flask, render_template, request, jsonify, abort, send_from_directory
import base64
import io
import nibabel as nib
import os
import time

import numpy as np
import torch
from segment_anything import SamPredictor, sam_model_registry

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r"./user_files_nifti"
decode_files = {"code1":"CT_LPI.nii.gz","code2":"CT_LPI_mask.nii.gz"}

which_model = ["vit_h"]
sam = {model:sam_model_registry[model](checkpoint= {"vit_b":"SAM_testing_only/SAM_models/fb_research/sam_vit_b_01ec64.pth", "vit_l":"SAM_testing_only/SAM_models/fb_research/sam_vit_l_0b3195.pth", "vit_h":"SAM_testing_only/SAM_models/fb_research/sam_vit_h_4b8939.pth"}[model]) for model in which_model}
[sam[model].to(device='cuda') for model in sam]
# sam = sam_model_registry[which_model](checkpoint= {"vit_b":"SAM_testing_only/SAM_models/fb_research/sam_vit_b_01ec64.pth", "vit_l":"SAM_testing_only/SAM_models/fb_research/sam_vit_l_0b3195.pth", "vit_h":"SAM_testing_only/SAM_models/fb_research/sam_vit_h_4b8939.pth"}[which_model])
# sam.to(device='cuda')

@app.route("/")
def index():
    items = [["code1","code2",str({ "1":"#FF0000", "2":"#0000FF", "3":"#00FF00", "4":"#00F00F", "5":"#00F0F0", "6":"#FFFF00"}).replace("'",'"')]]
    return render_template('viewer.html',items=items)

@app.route("/getFile")
def getFile():
    file_name = decode_files.get(request.args.get('q'))
    print("file_name", file_name)
    if not (file_name and os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], file_name))):
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_name)

@app.route('/imgEmbeddings', methods=['POST'])
def get_embeddings():
    print('called /imgEmbeddings')
    # image_embeddings = list()
    data = request.get_json()
    print("os.getcwd()",os.getcwd())
    print("data['path']", data.get('path'), "\ndata['slice']",data.get('slice'), "\ndata['ndim']",data.get('ndim'), "\ndata['min']",data.get('min'), "\ndata['max']",data.get('max'), "\ndata['sam_type']",data.get('sam_type'))
    if not (data.get('path') and data.get('slice') and data.get('ndim') and data.get('min') and data.get('max') and data.get('sam_type') and sam.get(data.get('sam_type'))):
        abort(404)
    
    min,max = int(data['min']),int(data['max'])
    if min == max:
        abort(404)
    data = request.get_json()
    
    n_ax = int(data['ndim']) - 1
    if(n_ax not in range(0,3)):
        abort(404)
    
    slice = int(data['slice'])
    
    print("os.path.join(app.config['UPLOAD_FOLDER'], decode_files[data['path']])",os.path.join(app.config['UPLOAD_FOLDER'], decode_files[data['path']]))
    img = nib.load(os.path.join(app.config['UPLOAD_FOLDER'], decode_files[data['path']]))
    image = np.asanyarray(img.dataobj)
    print("np.asanyarray(img.dataobj).shape",image.shape)
    if(slice not in range(0,image.shape[n_ax])):
        abort(404)
    
    start = time.time()
    predictor = SamPredictor(sam[data['sam_type']])
    print("Time for SamPredictor %f sec" % (time.time() - start))

    transp = ''.join(nib.aff2axcodes(img.affine))
    print("transp", transp, type(transp))
    transp = (1,0,2) if (transp.replace(transp[n_ax],'') in ('LP','PI','LI')) else (0,1,2)
    print("transp", transp, type(transp))

    # img = np.asanyarray(img.dataobj).take(slice, axis = n_ax)
    start = time.time()
    image = image.take(slice, axis = n_ax)
    image = image[...,np.newaxis]
    image = image.astype(np.float32)
    print("image.shape",image.shape)
    image = (image - min)/(max - min)
    # image = np.clip(image, 0.0, 1.0)
    image = np.repeat(image,3,axis = 2)
    image = np.transpose(image, transp)
    # image = np.transpose(np.repeat(np.clip((np.asanyarray(img.dataobj).take(slice, axis = n_ax)[...,np.newaxis].astype(np.float32) - min)/(max - min), 0.0, 1.0),3,axis = 2), transp)
    print("image.dtype",image.dtype)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy().tobytes()
    print("type(image_embedding)",type(image_embedding))
    image_embedding = base64.b64encode(image_embedding).decode('ascii')
    print("type(image_embedding)",type(image_embedding))
    print("done slice",slice)
    print("Time for creating Embeddings %f sec" % (time.time() - start))

    return jsonify({'imgEmb':image_embedding})
    
if __name__ == "__main__":
    app.run(debug = True)