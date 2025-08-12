//
// VISIT DANIELHAEHN.COM !
//
// Thanks to Alireza Seghi and Kevin Wang for all the help!
//
//
//

// GET EMBEDDING FOR CANVAS
element = cornerstone.getEnabledElements()[0];
canvas = element.canvas;
height = canvas.height;
width = canvas.width;

base64 = canvas.toDataURL('image/png')
base64 = base64.replace("data:image/png;base64,","")
uint8arr = Uint8Array.from(atob(base64), (c) => c.charCodeAt(0));

endpoint = 'https://model-zoo.metademolab.com/predictions/segment_everything_box_model';        

xhr = new XMLHttpRequest();
xhr.open("POST", endpoint);
xhr.onreadystatechange = function () {
  if (xhr.readyState === 4) {

    embedding = JSON.parse(xhr.response);

    // LOAD ONNX RUNTIME
    const script = document.createElement("script")
    script.type = "text/javascript"
    script.src = "https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js"
    document.head.appendChild(script)
    eval(script)


  // ENABLE ROI INTERACTION
  cornerstoneTools.setToolActive('RectangleRoi', { mouseButtonMask: 1 })


  }
}
xhr.send(uint8arr);

// SEGMENT
async function segment(embedding, height, width, x1, y1, x2, y2) {

  session = await ort.InferenceSession.create('https://cs666.org/onnx/sam.onnx');

  input = {};

  uint8arr = Uint8Array.from(atob(embedding[0]), (c) => c.charCodeAt(0));
  embedding = new ort.Tensor("float32", new Float32Array(uint8arr.buffer), [1, 256, 64, 64]);
  input['low_res_embedding'] = embedding;

  console.log(embedding)

  input['point_coords'] = new ort.Tensor("float32", new Float32Array([x1,y1,x2,y2]), [1, 2, 2]);


  // 2 and 3 mean top-left-bottom-right box
  input['point_labels'] = new ort.Tensor("float32", new Float32Array([2,3]), [1, 2]);

  // original image size
  input['image_size'] = new ort.Tensor("float32", new Float32Array([height, width]));

  // empty mask
  input['last_pred_mask'] = new ort.Tensor("float32", new Float32Array(256 * 256), [1, 1, 256, 256]);
  input['has_last_pred'] = new ort.Tensor("float32", new Float32Array([0]));

  return session.run( input ).then( output => {

    ctx = canvas.getContext('2d');

    image = ctx.getImageData(0,0,width,height)

    mask = arrayToImageData(output.output.data, image, width, height);
    
    ctx.putImageData(mask, 0, 0);

    return output.output.data;

  }).catch(err => {

    console.error(err);

  });

};

// CONVERT ARRAY TO IMAGEDATA
function arrayToImageData(mask, image, width, height) {
  // From: https://github.com/facebookresearch/segment-anything/blob/40df6e4046d8b07ab8c4519e083408289eb43032/demo/src/components/helpers/maskUtils.tsx
  // Copyright (c) Meta Platforms, Inc. and affiliates.
  // All rights reserved.

  // This source code is licensed under the license found in the
  // LICENSE file in the root directory of this source tree.
  [r, g, b, a] = [0, 114, 189, 255]; // the masks's blue color

  arr = image.data;//new Uint8ClampedArray(4 * width * height);
  for (var i = 0; i < mask.length; i++) {

    // Threshold the onnx model mask prediction at 0.0
    // This is equivalent to thresholding the mask using predictor.model.mask_threshold
    // in python
    if (mask[i] > 0.0) {
      arr[4 * i + 0] = r;
      arr[4 * i + 1] = g;
      arr[4 * i + 2] = b;
      arr[4 * i + 3] = a;
    }

  }
  
  return new ImageData(arr, width, height);

};

// REGISTER CALLBACK THAT TRIGGERS SAM
canvas.onmouseup = function(e) {
  
  state = cornerstoneTools.globalImageIdSpecificToolStateManager.saveToolState();

  topleft = state[Object.keys(state).pop()].RectangleRoi.data[0].handles.start;
  bottomright = state[Object.keys(state).pop()].RectangleRoi.data[0].handles.end;

  topleft_c = cornerstone.pixelToCanvas(element.element, topleft);
  bottomright_c = cornerstone.pixelToCanvas(element.element, bottomright);

  cornerstoneTools.clearToolState(element.element, 'RectangleRoi')
  cornerstone.renderGrayscaleImage(element, true)
  
  mask = segment(embedding, height, width, topleft_c.x, topleft_c.y, bottomright_c.x, bottomright_c.y);

}





