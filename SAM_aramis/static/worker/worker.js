// import * as ort from "../onnxruntime-web-1.18.0/package/dist/esm/ort.min.js";
// ort.env.wasm.wasmPaths = "../onnxruntime-web-1.18.0/package/dist/"

// console.log("Inside Worker");

async function get_embeddings(f_p){

    await fetch('/imgEmbeddings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({path:f_p})
    })
}

async function sliceProcess_img(canvas, slice = canvas.draw_prop.slc){
    const tempCanvas = new OffscreenCanvas(canvas.dim1,canvas.dim2)
    // tempCanvas.ctx = tempCanvas.getContext("2d")
    // const canvasImageData = tempCanvas.ctx.createImageData(tempCanvas.width, tempCanvas.height)

    const sliceOffset = canvas.sliceSize * slice;
    // Array.from(Array(canvas.sliceSize).keys()).forEach((idx) => {
    //     const idx_4 = idx*4;
    //     let pix_val = (canvas.typedData[sliceOffset + idx] * canvas.scl_slope) + canvas.scl_inter;
    //     pix_val = ((pix_val - canvas.minHU)/(canvas.maxHU - canvas.minHU))*255
    //     canvasImageData.data[idx_4] = canvasImageData.data[idx_4+1] = canvasImageData.data[idx_4+2] = pix_val & 0xFF;
    //     canvasImageData.data[idx_4+3] = 0xFF;
    // })

    // tempCanvas.ctx.putImageData(canvasImageData,0,0)

    const canvasImageData = new ImageData(new Uint8ClampedArray([...canvas.typedData.subarray(sliceOffset, sliceOffset + canvas.sliceSize)].flatMap((val)=>{
        let pix_val = (val * canvas.scl_slope) + canvas.scl_inter;
        pix_val = (pix_val - canvas.minHU)/(canvas.maxHU - canvas.minHU)*255;
        return [ pix_val, pix_val, pix_val, 0xFF];
    })), canvas.dim1, canvas.dim2)
    
    // tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").mozImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").webkitImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").msImageSmoothingEnabled = 0;
    tempCanvas.getContext("2d").putImageData(canvasImageData,0,0)
    self.postMessage({blob:URL.createObjectURL(await tempCanvas.convertToBlob()), slice:slice});
    count++;
}

async function sliceProcess_mask(canvas,slice = canvas.draw_prop.slc){
    const tempCanvas = new OffscreenCanvas(canvas.dim1,canvas.dim2)
    // tempCanvas.ctx = tempCanvas.getContext("2d")
    // const canvasImageData = tempCanvas.ctx.createImageData(tempCanvas.width, tempCanvas.height)

    const sliceOffset = canvas.sliceSize * slice;
    // Array.from(Array(canvas.sliceSize).keys()).forEach((idx) => {
    //     const idx_4 = idx*4
    //     let fast_color_map_temp = canvas.fast_color_map[canvas.typedData[sliceOffset + idx]];
    //     canvasImageData.data[idx_4] = fast_color_map_temp.r & 0xFF;
    //     canvasImageData.data[idx_4+1] = fast_color_map_temp.g & 0xFF;
    //     canvasImageData.data[idx_4+2] = fast_color_map_temp.b & 0xFF;
    //     canvasImageData.data[idx_4+3] = fast_color_map_temp.a;
    // })

    // tempCanvas.ctx.putImageData(canvasImageData,0,0)

    const canvasImageData = new ImageData(new Uint8ClampedArray([...canvas.typedData.subarray(sliceOffset, sliceOffset + canvas.sliceSize)].flatMap((val)=>{
        let fast_color_map_temp = canvas.fast_color_map[val];
        return [ fast_color_map_temp.r, fast_color_map_temp.g, fast_color_map_temp.b, fast_color_map_temp.a];
    })), canvas.dim1, canvas.dim2)

    // tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").mozImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").webkitImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").msImageSmoothingEnabled = 0;
    tempCanvas.getContext("2d").putImageData(canvasImageData,0,0)
    self.postMessage({blob:URL.createObjectURL(await tempCanvas.convertToBlob()), slice:slice});
    count++;
}

function allSliceProcess(canvas){
    if(canvas.who[1] == 'i'){
        // return (new Array(canvas.dim3).fill().map((_,slice) => sliceProcess_img(canvas,slice)))//.concat([get_embeddings(canvas.f_p)])
        for (let slice = 0; slice<canvas.dim3; ++slice)
            sliceProcess_img(canvas,slice);
        // get_embeddings(canvas.f_p);
    }
    else
        // return new Array(canvas.dim3).fill().map((_,slice) => sliceProcess_mask(canvas,slice))
        for (let slice = 0; slice<canvas.dim3; ++slice)
            sliceProcess_mask(canvas,slice);
}

var count = 0;
self.onmessage = function({data}) {
    // Promise.all([sliceProcess_img, sliceProcess_mask, allSliceProcess][data.choose](data)).then(() => {
        // debugger;
        // self.close()
    // });

    [sliceProcess_img, sliceProcess_mask, allSliceProcess][data.choose](data)
    setInterval(() =>{
        (count == data.dim3) ? self.close(): 0;
    },2000);
}