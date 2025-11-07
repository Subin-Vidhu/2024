import nibabel as nib
import numpy as np

# Load both masks
img1 = nib.load(r'C:/Users/Subin-PC/Downloads/Telegram Desktop/dice_run/dice_run/test/071/N-071_Updated_AS.nii')
img2 = nib.load(r'C:/Users/Subin-PC/Downloads/Telegram Desktop/dice_run/dice_run/test/071/N-071_Updated_GM.nii')

data1 = img1.get_fdata()
data2 = img2.get_fdata()

print('='*60)
print('LABEL ANALYSIS')
print('='*60)
print('Annotator 1 (AS) unique values:', np.unique(data1))
print('Annotator 2 (GM) unique values:', np.unique(data2))

print('\nAnnotator 1 (AS) label counts:')
for label in np.unique(data1):
    count = np.sum(data1 == label)
    print(f'  Label {int(label)}: {count:,} voxels')

print('\nAnnotator 2 (GM) label counts:')
for label in np.unique(data2):
    count = np.sum(data2 == label)
    print(f'  Label {int(label)}: {count:,} voxels')

# Check spatial locations
print('\n' + '='*60)
print('SPATIAL LOCATION CHECK')
print('='*60)

# For label 1 in annotator 1
label1_mask = (data1 == 1).astype(np.uint8)
if np.sum(label1_mask) > 0:
    coords = np.argwhere(label1_mask)
    center = coords.mean(axis=0)
    print(f'\nAnnotator 1 - Label 1:')
    print(f'  Center of mass: {center.astype(int)}')
    print(f'  X-coordinate (left-right): {center[0]:.1f}')
    
# For label 2 in annotator 1
label2_mask = (data1 == 2).astype(np.uint8)
if np.sum(label2_mask) > 0:
    coords = np.argwhere(label2_mask)
    center = coords.mean(axis=0)
    print(f'\nAnnotator 1 - Label 2:')
    print(f'  Center of mass: {center.astype(int)}')
    print(f'  X-coordinate (left-right): {center[0]:.1f}')

print('\nIn medical imaging (LPI orientation):')
print('  - Lower X values = Left side of patient')
print('  - Higher X values = Right side of patient')
