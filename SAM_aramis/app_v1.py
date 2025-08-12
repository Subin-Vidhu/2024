from flask import Flask, render_template,request,jsonify
import base64
import io
import nibabel as nib
import os

import numpy as np
import torch
from segment_anything import SamPredictor, sam_model_registry

app = Flask(__name__)

which_model = "vit_h"
sam = sam_model_registry[which_model](checkpoint= {"vit_b":"SAM_testing_only/SAM_models/fb_research/sam_vit_b_01ec64.pth", "vit_l":"SAM_testing_only/SAM_models/fb_research/sam_vit_l_0b3195.pth", "vit_h":"SAM_testing_only/SAM_models/fb_research/sam_vit_h_4b8939.pth"}[which_model])
sam.to(device='cuda')

@app.route("/")
def index():
    return render_template('viewer_v1.html')

@app.route('/imgEmbeddings', methods=['POST'])
def get_embeddings():
    print('called /imgEmbeddings')
    predictor = SamPredictor(sam)
    data = request.get_json()
    image_embeddings = list()
    print("os.getcwd()",os.getcwd())
    print("data['path']", data['path'])

    img = nib.load(os.path.join(os.getcwd(), data['path'][1:]))
    img = np.asanyarray(img.dataobj)
    min,max = img.min(),img.max()
    for slice in [481]:
        image = np.transpose(np.repeat((img[:,:,slice,np.newaxis].astype(np.float32) - min)/(max - min),3,axis = 2), (1,0,2))
        print("image.dtype",image.dtype)
        # image = torch.from_numpy(image).to(device="cuda")
        # image = np.array(Image.open(io.BytesIO(request.data)).convert("RGB"))
        predictor.set_image(image)
        image_embedding = predictor.get_image_embedding().cpu().numpy().tobytes()
        image_embeddings.append(base64.b64encode(image_embedding).decode('ascii'))
        print("done slice",slice)

    # convert the image embedding to bytes
    print("done all")
    return jsonify(image_embeddings)
    
if __name__ == "__main__":
    app.run(debug = True)