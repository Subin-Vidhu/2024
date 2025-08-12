import * as ort from "/static/onnxruntime-web-1.18.0/package/dist/esm/ort.min.js";
ort.env.wasm.wasmPaths = "/static/onnxruntime-web-1.18.0/package/dist/"

console.log("Inside pred Worker");
const session = await ort.InferenceSession.create("/static/models/SAM_models/New folder/sam.onnx");
let controller = new AbortController;
let wk_cvs_w, wk_cvs_h, wk_embedding, wk_dx, wk_dy, wk_dWidth, wk_dHeight, wk_w, wk_h, wk_color={};
function segment(coords, embedding, dx, dy, dWidth, dHeight, w, h, color, cvs_w, cvs_h, oldMask, final) {
    if (color) wk_color = color;
    // if (a) wk_color.a = a;
    if (embedding) {
        wk_dx = dx, wk_dy = dy, wk_dWidth = dWidth, wk_dHeight = dHeight, wk_w = w, wk_h = h, wk_cvs_w = cvs_w, wk_cvs_h = cvs_h;
        // let uint8arr = Uint8Array.from(atob(embedding), (c) => c.charCodeAt());
        // embedding = new ort.Tensor("float32", new Float32Array(uint8arr.buffer), [1, 256, 64, 64]);
        wk_embedding = new ort.Tensor("float32", new Float32Array(Uint8Array.from(atob(embedding), (c) => c.charCodeAt()).buffer), [1, 256, 64, 64]);
    }
    if (!coords.length || !wk_color.hasOwnProperty('r'))
        return;
    controller.abort()
    controller = new AbortController;

    return new Promise((resolve, reject) => {
        controller.signal.onabort = () => {
            reject("Operation aborted");
        };
        const input = {}, point_labels = [], point_coords = [];
        input['low_res_embedding'] = wk_embedding;

        for (let ent of coords) {
            point_coords.push(...ent.val);
            point_labels.push(...(ent.ent === 'pt' ? [ent.label] : [2, 3]))
        }
        if (!coords.filter((v) => v.ent == 'rect').length) {
            point_coords.push(0.0, 0.0);
            point_labels.push(-1);
        }
        const num_points = point_labels.length

        input['point_coords'] = new ort.Tensor("float32", new Float32Array(point_coords), [1, num_points, 2]);

        input['point_labels'] = new ort.Tensor("float32", new Float32Array(point_labels), [1, num_points]);

        // original image size
        input['image_size'] = new ort.Tensor("float32", new Float32Array([wk_h, wk_w]));

        // empty mask
        input['last_pred_mask'] = new ort.Tensor("float32", new Float32Array(oldMask?oldMask:65536), [1, 1, 256, 256]); // 256 * 256 = 65536
        input['has_last_pred'] = new ort.Tensor("float32", new Float32Array([oldMask?1:0]));

        session.run(input).then((output) =>{
            console.log("output.output.data.length", output.output.data.length);
            if(final) {
                // const imgData_ipt = new Uint8ClampedArray(wk_w * wk_h);
                self.postMessage({final:Uint8Array.from(output.output.data, (v) => (v>0.0)?final:0)});
                resolve();
                wk_cvs_w = wk_cvs_h = wk_embedding = wk_dx = wk_dy = wk_dWidth = wk_dHeight = wk_w = wk_h = wk_color = 0;
                return;
            }
            const imgData_ipt = new Uint8ClampedArray(4 * wk_w * wk_h)
            for(let i=-1; ++i<imgData_ipt.length;){
                let idx_4 = i*4;
                if(output.output.data[i]>0.0)
                    imgData_ipt[idx_4++] = wk_color.r, imgData_ipt[idx_4++] = wk_color.g, imgData_ipt[idx_4++] = wk_color.b, imgData_ipt[idx_4] = wk_color.a;
                else
                    imgData_ipt[idx_4++] = imgData_ipt[idx_4++] = imgData_ipt[idx_4++] = imgData_ipt[idx_4] = 0;
            }
            
            const imgData = new ImageData( imgData_ipt, wk_w, wk_h);
            self.postMessage({imgData},[imgData.data.buffer])
            resolve();
        })
        .catch(reject);
    });
};

// function segment(embedding, height, width, x1, y1, x2, y2, oldMask) {


//     let input = {};

//     let uint8arr = Uint8Array.from(atob(embedding), (c) => c.charCodeAt(0));
//     embedding = new ort.Tensor("float32", new Float32Array(uint8arr.buffer), [1, 256, 64, 64]);
//     input['low_res_embedding'] = embedding;

//     console.log(embedding)

//     input['point_coords'] = new ort.Tensor("float32", new Float32Array([x1, y1, x2, y2]), [1, 2, 2]);


//     // 2 and 3 mean top-left-bottom-right box
//     input['point_labels'] = new ort.Tensor("float32", new Float32Array([2, 3]), [1, 2]);

//     // original image size
//     input['image_size'] = new ort.Tensor("float32", new Float32Array([height, width]));

//     // empty mask
//     input['last_pred_mask'] = new ort.Tensor("float32", new Float32Array(256 * 256), [1, 1, 256, 256]);
//     input['has_last_pred'] = new ort.Tensor("float32", new Float32Array([0]));

//     return session.run(input).then(async (output) => {
//         //     const canvas = new OffscreenCanvas(width, height)

//         //   const ctx = canvas.getContext('2d');

//         // //   image = ctx.getImageData(0,0,width,height)
//         //   console.log("output.output.data",typeof(output.output.data))

//         //   let mask = arrayToImageData(output.output.data, oldMask, width, height);
//         const tempCanvas = new OffscreenCanvas(width, height)
//         // tempCanvas.ctx = tempCanvas.getContext("2d")
//         // const canvasImageData = tempCanvas.ctx.createImageData(tempCanvas.width, tempCanvas.height)

//         const sliceOffset = 512 * 512 * 481;
//         // Array.from(Array(canvas.sliceSize).keys()).forEach((idx) => {
//         //     const idx_4 = idx*4
//         //     let fast_color_map_temp = canvas.fast_color_map[canvas.typedData[sliceOffset + idx]];
//         //     canvasImageData.data[idx_4] = fast_color_map_temp.r & 0xFF;
//         //     canvasImageData.data[idx_4+1] = fast_color_map_temp.g & 0xFF;
//         //     canvasImageData.data[idx_4+2] = fast_color_map_temp.b & 0xFF;
//         //     canvasImageData.data[idx_4+3] = fast_color_map_temp.a;
//         // })

//         // tempCanvas.ctx.putImageData(canvasImageData,0,0)

//         const canvasImageData = new ImageData(new Uint8ClampedArray([...oldMask.subarray(sliceOffset, sliceOffset + (512 * 512))].flatMap((val, idx) => {
//             // let [r, g, b, a] = [255, 31, 248, 255]
//             if (output.output.data[idx] > 0.0)
//                 return [255, 31, 248, 255];
//             return [0, 0, 0, 0];
//         })), width, height)

//         // tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
//         // tempCanvas.getContext("2d").mozImageSmoothingEnabled = 0;
//         // tempCanvas.getContext("2d").webkitImageSmoothingEnabled = 0;
//         // tempCanvas.getContext("2d").msImageSmoothingEnabled = 0;
//         tempCanvas.getContext("2d").putImageData(canvasImageData, 0, 0)
//         self.postMessage({ blob: URL.createObjectURL(await tempCanvas.convertToBlob()), slice: 481 });

//         //   ctx.putImageData(mask, 0, 0);

//         //   return output.output.data;

//     }).catch(err => {

//         console.error(err);

//     });

// };

// // CONVERT ARRAY TO IMAGEDATA
// function arrayToImageData(mask, image, width, height) {
//     // From: https://github.com/facebookresearch/segment-anything/blob/40df6e4046d8b07ab8c4519e083408289eb43032/demo/src/components/helpers/maskUtils.tsx
//     // Copyright (c) Meta Platforms, Inc. and affiliates.
//     // All rights reserved.

//     // This source code is licensed under the license found in the
//     // LICENSE file in the root directory of this source tree.
//     [r, g, b, a] = [255, 31, 248, 255]; // the masks's blue color

//     arr = image.data;//new Uint8ClampedArray(4 * width * height);
//     for (var i = 0; i < mask.length; i++) {

//         // Threshold the onnx model mask prediction at 0.0
//         // This is equivalent to thresholding the mask using predictor.model.mask_threshold
//         // in python
//         if (mask[i] > 0.0) {
//             arr[4 * i + 0] = r;
//             arr[4 * i + 1] = g;
//             arr[4 * i + 2] = b;
//             arr[4 * i + 3] = a;
//         }

//     }

//     return new ImageData(arr, width, height);

// };

self.onmessage = function ({ data: { embedding, coords, dx, dy, dWidth, dHeight, w, h, color, cvs_w, cvs_h, oldMask, final} }) {
    segment(coords, embedding, dx, dy, dWidth, dHeight, w, h, color, cvs_w, cvs_h, oldMask, final);
}