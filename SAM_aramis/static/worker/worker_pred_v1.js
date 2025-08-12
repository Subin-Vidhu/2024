import * as ort from "/static/onnxruntime-web-1.18.0/package/dist/esm/ort.min.js";
ort.env.wasm.wasmPaths = "/static/onnxruntime-web-1.18.0/package/dist/"

console.log("Inside pred Worker");

async function segment(embedding, height, width, x1, y1, x2, y2, oldMask) {

    let session = await ort.InferenceSession.create("/static/models/SAM_models/New folder/sam.onnx");
  
    let input = {};
  
    let uint8arr = Uint8Array.from(atob(embedding), (c) => c.charCodeAt(0));
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
  
    return session.run( input ).then( async (output) => {
    //     const canvas = new OffscreenCanvas(width, height)
  
    //   const ctx = canvas.getContext('2d');
  
    // //   image = ctx.getImageData(0,0,width,height)
    //   console.log("output.output.data",typeof(output.output.data))
  
    //   let mask = arrayToImageData(output.output.data, oldMask, width, height);
      const tempCanvas = new OffscreenCanvas(width, height)
    // tempCanvas.ctx = tempCanvas.getContext("2d")
    // const canvasImageData = tempCanvas.ctx.createImageData(tempCanvas.width, tempCanvas.height)

    const sliceOffset = 512*512 * 481;
    // Array.from(Array(canvas.sliceSize).keys()).forEach((idx) => {
    //     const idx_4 = idx*4
    //     let fast_color_map_temp = canvas.fast_color_map[canvas.typedData[sliceOffset + idx]];
    //     canvasImageData.data[idx_4] = fast_color_map_temp.r & 0xFF;
    //     canvasImageData.data[idx_4+1] = fast_color_map_temp.g & 0xFF;
    //     canvasImageData.data[idx_4+2] = fast_color_map_temp.b & 0xFF;
    //     canvasImageData.data[idx_4+3] = fast_color_map_temp.a;
    // })

    // tempCanvas.ctx.putImageData(canvasImageData,0,0)

    const canvasImageData = new ImageData(new Uint8ClampedArray([...oldMask.subarray(sliceOffset, sliceOffset + (512*512))].flatMap((val,idx)=>{
        // let [r, g, b, a] = [255, 31, 248, 255]
        if(output.output.data[idx]>0.0)
            return [255, 31, 248, 255];
        return [0,0,0,0];
    })), width, height)

    // tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").mozImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").webkitImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").msImageSmoothingEnabled = 0;
    tempCanvas.getContext("2d").putImageData(canvasImageData,0,0)
    self.postMessage({blob:URL.createObjectURL(await tempCanvas.convertToBlob()), slice:481});
      
    //   ctx.putImageData(mask, 0, 0);
  
    //   return output.output.data;
  
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
    [r, g, b, a] = [255, 31, 248, 255]; // the masks's blue color
  
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

self.onmessage = function({data}) {
    // Promise.all([sliceProcess_img, sliceProcess_mask, allSliceProcess][data.choose](data)).then(() => {
        // debugger;
        // self.close()
    // });
    segment(data.embedding, 512, 512, data.xyxy[0], data.xyxy[1], data.xyxy[2], data.xyxy[3], data.typedArray)
}