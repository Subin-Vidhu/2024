function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
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
    
    tempCanvas.getContext("2d").putImageData(canvasImageData,0,0)
    return URL.createObjectURL(await tempCanvas.convertToBlob());
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

    tempCanvas.getContext("2d").putImageData(canvasImageData,0,0)
    return URL.createObjectURL(await tempCanvas.convertToBlob());
}

async function allSliceProcess(canvas){
    let tempCanvasArr = new Array(canvas.dim3);
    if(canvas.who[1] == 'i')
        for (let slice = 0; slice<canvas.dim3; ++slice)
            tempCanvasArr[slice] = sliceProcess_img(canvas,slice);
    else
        for (let slice = 0; slice<canvas.dim3; ++slice)
            tempCanvasArr[slice] = sliceProcess_img(canvas,slice);
    
    return tempCanvasArr;
}

self.onmessage = async function({data}) {
    self.postMessage(await [sliceProcess_img, sliceProcess_mask, allSliceProcess][data.choose](data))
  }