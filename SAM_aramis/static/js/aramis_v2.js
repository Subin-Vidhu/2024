// ./nifti-reader-min.js of tagged release 0.6.3;
//https://github.com/rii-mango/NIFTI-Reader-JS/tree/v0.6.3

//This viewer accepts LPI images for axial
//This viewer accepts PIL images for sagittal
//This viewer accepts LIP images for coronal
let i_m = document.getElementsByTagName('canvas');
// let workerHandleCount = i_m.length;
var aaa = new Array(4);

document.body.onresize = () => {
    Object.keys(i_m).forEach((idx)=>{
        idx = +idx;
        i_m[idx].width = parseInt(window.getComputedStyle(i_m[idx]).width);
        i_m[idx].height = parseInt(window.getComputedStyle(i_m[idx]).height);
        if((idx%2) == 1)
            i_m[idx].draw_prop.reset = 0;
    });
};

const handleFinalSlices = new Array()

Object.keys(i_m).forEach((idx)=>{
    idx = +idx;
    i_m[idx].f_p = i_m[idx].getAttribute('f_p');
    i_m[idx].removeAttribute('f_p');
    i_m[idx].ctx = i_m[idx].getContext("2d");
    // i_m[idx].ctx.mozImageSmoothingEnabled = 0;
    // i_m[idx].ctx.webkitImageSmoothingEnabled = 0;
    // i_m[idx].ctx.msImageSmoothingEnabled = 0;
    i_m[idx].width = parseInt(window.getComputedStyle(i_m[idx]).width);
    i_m[idx].height = parseInt(window.getComputedStyle(i_m[idx]).height);
    i_m[idx].ctx.imageSmoothingEnabled = 0;
    if((idx%2) == 0){
        i_m[idx].who = [idx,'i'];
        i_m[idx].draw_prop = {
            get width(){
                return i_m[idx].width;
            },
            get height(){
                return i_m[idx].height;
            },
            get imageSmoothingEnabled(){
                if (this.imgSE != i_m[idx].ctx.imageSmoothingEnabled)
                    this.imgSE = i_m[idx].ctx.imageSmoothingEnabled,drawCanvas([i_m[idx],i_m[idx+1]]);
                return i_m[idx].imgSE;
            },
            scaleFac:0.10,
            multiplier:2,
            scale_curr:1,
            maxZoom:10.0,
            minZoom:0.05,
            imgSE:i_m[idx].ctx.imageSmoothingEnabled,
            set imageSmoothingEnabled(val){
                this.imgSE = val;
                i_m[idx].ctx.imageSmoothingEnabled = val;
                i_m[idx+1].ctx.imageSmoothingEnabled = val;
                drawCanvas([i_m[idx],i_m[idx+1]]);
            },
            set slcChange(newVal){
                if((newVal < i_m[idx].dim3) && (newVal >= 0)){
                    this.slc = newVal;
                    
                    if((i_m[idx].imgData[newVal].src !== '') && (i_m[idx+1].imgData[newVal].src !== '')){
                        drawCanvas([i_m[idx],i_m[idx+1]]);
                    }
                    else{
                        if(i_m[idx].imgData[newVal].src == ''){
                            i_m[idx].imgData[newVal].onload = () => {
                                i_m[idx].imgData[newVal].onload = null;
                                this.slc == newVal ? drawCanvas([i_m[idx]]):0;
                            }
                            sliceProcess_img(i_m[idx]);
                        }
                        if(i_m[idx+1].imgData[newVal].src == ''){
                            i_m[idx+1].imgData[newVal].onload = () => {
                                i_m[idx+1].imgData[newVal].onload = null;
                                this.slc == newVal ? drawCanvas([i_m[idx+1]]):0;
                            }
                            sliceProcess_mask(i_m[idx+1]);
                        }
                    }
                }
            },
            set reset(draw){
                this.dx = Math.max(0,(i_m[idx].width - (this.aspect_ratio*i_m[idx].height))/2);
                this.dy = Math.max(0,(i_m[idx].height - (i_m[idx].width/this.aspect_ratio))/2);
                this.dWidth = this.dx ? this.aspect_ratio*i_m[idx].height : i_m[idx].width;
                this.dHeight = this.dy ? i_m[idx].width/this.aspect_ratio : i_m[idx].height;
                this.orig_dWidth = this.dWidth;
                this.orig_dHeight = this.dHeight;
                i_m[idx].ctx.setTransform(1, 0, 0, 1, 0, 0);
                i_m[idx+1].ctx.setTransform(1, 0, 0, 1, 0, 0);
                this.scale_curr = 1;

                draw ? 0 : drawCanvas([i_m[idx],i_m[idx+1]]);
            },
            set pan(panFac){
                // let trsX = panFac.x/this.scale_curr, trsY = panFac.y/this.scale_curr;
                // i_m[idx].ctx.translate(trsX, trsY);
                // i_m[idx+1].ctx.translate(trsX, trsY);
                // this.translateX += trsX;
                // this.translateY += trsY;
                this.dx += panFac.x;
                this.dy += panFac.y;

                panFac.draw ? 0 : drawCanvas([i_m[idx],i_m[idx+1]]);
            },
            set scale(scale_p){
                let change = +((Math.max(Math.min(this.scale_curr + (this.scaleFac * scale_p.scroll),this.maxZoom),this.minZoom)).toFixed(this.multiplier));
                // let trsX = this.width*(change - this.scale_curr)*scale_p.x * (this.scale_curr/change), trsY = this.height*(change - this.scale_curr)*scale_p.y * (this.scale_curr/change);

                // i_m[idx].ctx.translate(-trsX,-trsY);
                // i_m[idx+1].ctx.translate(-trsX,-trsY);
                // i_m[idx].ctx.scale(change/this.scale_curr, change/this.scale_curr);
                // i_m[idx+1].ctx.scale(change/this.scale_curr, change/this.scale_curr);
                // let as1 = this.dWidth;
                // let as2 = this.dHeight;
                this.dWidth = this.orig_dWidth * change;
                this.dHeight = this.orig_dHeight * change;
                // this.dx = this.dx - ((i_m[idx].width * (change - this.scale_curr))*scale_p.x);
                // this.dy = this.dy - ((i_m[idx].height * (change - this.scale_curr))*scale_p.y);
                this.dx = scale_p.x - (((scale_p.x - this.dx) * change)/this.scale_curr);
                this.dy = scale_p.y - (((scale_p.y - this.dy) * change)/this.scale_curr);

                this.scale_curr = change;

                // let change = Math.max(Math.min(this.scale_curr + (this.scaleFac * scale_p.scroll),10.0),0.05);
                // this.dWidth = this.dWidth * change/this.scale_curr;
                // this.dHeight = this.dHeight * change/this.scale_curr;
                // this.scale_curr = change;

                scale_p.draw ? 0 : drawCanvas([i_m[idx],i_m[idx+1]]);
            }
        };
        handleFinalSlices.push(readFile(i_m[idx]));
    }
    else{
        i_m[idx].who = [idx,'m'];
        i_m[idx].color_map = JSON.parse(i_m[idx].getAttribute('color_map'));
        i_m[idx].xyCoord = (offsetX,offsetY) => {
            const coords = [(offsetX>=i_m[idx].draw_prop.dx && offsetX<(i_m[idx].draw_prop.dx+i_m[idx].draw_prop.dWidth)) ? Math.max(Math.min(Math.round((offsetX-i_m[idx].draw_prop.dx) * i_m[idx].dim1 / i_m[idx].draw_prop.dWidth),i_m[idx].dim1 - 1),0): null, (offsetY>=i_m[idx].draw_prop.dy && offsetY<(i_m[idx].draw_prop.dy+i_m[idx].draw_prop.dHeight)) ? Math.max(Math.min(Math.round((offsetY-i_m[idx].draw_prop.dy) * i_m[idx].dim2 / i_m[idx].draw_prop.dHeight),i_m[idx].dim2 - 1),0): null];
            return coords.every((val) => val!=null) ? coords: null;
            //demooo
            // i_m[1].onclick = (e) => {
            //     console.log("e.offsetX",e.offsetX);
            //     console.log("e.offsetY",e.offsetY);
            //     console.log("i_m[1].xyCoord",i_m[1].xyCoord(e.offsetX,e.offsetY));
            // }
        };
        i_m[idx].removeAttribute('color_map');

        i_m[idx].fast_color_map = {0:{r:0x00,g:0x00,b:0x00,a:0x00}}
        Object.keys(i_m[idx].color_map).forEach((val)=>{
            i_m[idx].fast_color_map[val] = hexToRgb(i_m[idx].color_map[val]);
            i_m[idx].fast_color_map[val].a = 0xFF;
        })

        Object.defineProperty(i_m[idx], 'draw_prop', {
            get: () => {
              return i_m[idx-1].draw_prop;
            }
        });
        handleFinalSlices.push(handleFinalSlices[idx-1]
            .then(() => readFile(i_m[idx])))
        // readFile(i_m[idx-1])
        //     .then(() => {
        //         readFile(i_m[idx]);
        //     });
    }
})
Promise.all(handleFinalSlices)
.then(() => {
    Object.keys(i_m).forEach((idx)=>{
        idx = +idx;
        if(i_m[idx].who[1] == 'i')
            get_embeddings(i_m[idx])

        // allSliceProcess(i_m[idx]);

        const fastWorker = new Worker("static/worker/worker.js",{type:'module'});
        fastWorker.onmessage = async ({data}) => {
            if(i_m[idx].imgData[data.slice].src == '')
                i_m[idx].imgData[data.slice].src = data.blob;
            else
                URL.revokeObjectURL(data.blob)
        }
        let worker_data = { choose:2, who:i_m[idx].who, f_p:i_m[idx].f_p, dim1:i_m[idx].dim1, dim2:i_m[idx].dim2, dim3:i_m[idx].dim3, sliceSize:i_m[idx].sliceSize, typedData:i_m[idx].typedData, fast_color_map:i_m[idx].fast_color_map, draw_prop:i_m[idx].draw_prop, minHU:i_m[idx].minHU, maxHU:i_m[idx].maxHU, scl_inter:i_m[idx].scl_inter, scl_slope:i_m[idx].scl_slope}
        fastWorker.postMessage(worker_data);
    });
})

function c_mousedown(e){
    e.preventDefault(); 
    let canvas = e.target;
    canvas.onmousemove = (e) => {
        if(e.ctrlKey){
            canvas.draw_prop.pan = {x:e.movementX, y:e.movementY};
    }
    };
    canvas.onmouseleave = () =>{
        canvas.onmouseleave = null;
        canvas.onmouseup = null;
        canvas.onmousemove = null;
    }
    canvas.onmouseup = () =>{
        canvas.onmouseup = null;
        canvas.onmousemove = null;
    }
}

function c_wheel(e){
    if(e.deltaMode)
    return new Error();
    e.preventDefault();
    if(e.ctrlKey){
        e.target.draw_prop.scale = {x: (e.offsetX), y: (e.offsetY), scroll:(e.deltaY<0? 1 : -1)};
    }
}

// const worker = new Worker('static/js/worker.js');

// worker.onmessage = function(e) {
//     if(--workerHandleCount == 0){
//         worker.onmessage=null;
//     }
//     i_m[e.data.who[0]].imgData = e.data.imgData;
//     drawCanvas(i_m[e.data.who[0]]);
// };

function readNIFTI(canvas, data, contWholeImgProcess = undefined) {
    // parse nifti
    if (nifti.isCompressed(data)) {
        data = nifti.decompress(data);
    }

    if (nifti.isNIFTI(data)) {
        canvas.niftiHeader = nifti.readHeader(data);
        canvas.niftiImage = nifti.readImage(canvas.niftiHeader, data);

        // canvas.style.width = `${canvas.niftiHeader.dims[1]}px`
        // canvas.style.height = `${canvas.niftiHeader.dims[2]}px`

        // canvas.style.width = `${900}px`
        // canvas.style.height = `${900}px`

        // canvas.width = parseInt(window.getComputedStyle(canvas).width);
        // canvas.height = parseInt(window.getComputedStyle(canvas).height);
    }


    if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT8) {
        canvas.typedData = new Uint8Array(canvas.niftiImage);
    } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT16) {
        canvas.typedData = new Int16Array(canvas.niftiImage);
    } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT32) {
        canvas.typedData = new Int32Array(canvas.niftiImage);
    } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT32) {
        canvas.typedData = new Float32Array(canvas.niftiImage);
    } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT64) {
        canvas.typedData = new Float64Array(canvas.niftiImage);
    } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT8) {
        canvas.typedData = new Int8Array(canvas.niftiImage);
    } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT16) {
        canvas.typedData = new Uint16Array(canvas.niftiImage);
    } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT32) {
        canvas.typedData = new Uint32Array(canvas.niftiImage);
    } else {
        return;
    }

    canvas.dim1 = canvas.niftiHeader.dims[1];
    canvas.dim2 = canvas.niftiHeader.dims[2];
    canvas.dim3 = canvas.niftiHeader.dims[3];

    if(canvas.who[1] == 'i'){
        canvas.draw_prop.aspect_ratio = (canvas.niftiHeader.pixDims[1] * canvas.niftiHeader.dims[1])/(canvas.niftiHeader.pixDims[2] * canvas.niftiHeader.dims[2]);
        
        canvas.minHU = +canvas.niftiHeader.cal_min
        canvas.maxHU = +canvas.niftiHeader.cal_max
        canvas.draw_prop.slc = Math.floor(canvas.niftiHeader.dims[3]/2);

        // let aspect_check = (canvas.draw_prop.aspect_ratio < (canvas.width/canvas.height));

        canvas.draw_prop.reset = true;

        // canvas.draw_prop.dx = aspect_check ? parseInt((aspect_ratio*canvas.height) - canvas.width) : 0;
        // canvas.draw_prop.dy = aspect_check ? 0 : parseInt((aspect_ratio*canvas.height) - canvas.width);
        // canvas.draw_prop.dWidth = canvas.width >= canvas.dim1 ? canvas.dim1 : canvas.width;
        // canvas.draw_prop.dHeight = canvas.height >= canvas.dim2 ? canvas.dim2 : canvas.height;

        // canvas.draw_prop.dx = aspect_check ? Math.floor((canvas.width - canvas.dim1)/2) : 0;
        // canvas.draw_prop.dy = aspect_check ? Math.floor((canvas.height - canvas.dim2)/2) : 0;
        // canvas.draw_prop.dWidth = canvas.width >= canvas.dim1 ? canvas.dim1 : canvas.width;
        // canvas.draw_prop.dHeight = canvas.height >= canvas.dim2 ? canvas.dim2 : canvas.height;
        if (canvas.niftiHeader.scl_slope == 0) {
            canvas.scl_slope = 1;
            canvas.scl_inter = 0;
        }
        else{
            canvas.scl_slope = canvas.niftiHeader.scl_slope;
            canvas.scl_inter = canvas.niftiHeader.scl_inter;
        }
    }

    // const tempCanvas = new OffscreenCanvas(canvas.dim1,canvas.dim2)
    // tempCanvas.ctx = tempCanvas.getContext("2d")
    // const canvasImageData = tempCanvas.ctx.createImageData(tempCanvas.width, tempCanvas.height)
    canvas.sliceSize = canvas.dim1 * canvas.dim2;

    canvas.imgData = new Array(canvas.dim3).fill().map(() => new Image(canvas.dim1,canvas.dim2));

    canvas.imgData[canvas.draw_prop.slc].onload = () => {
        canvas.imgData[canvas.draw_prop.slc].onload = null;
        drawCanvas([canvas]);
        contWholeImgProcess();
        // if (canvas.who[1] == 'm'){
        //     canvas.onmousedown = c_mousedown;
        //     canvas.onwheel = c_wheel;
        // }
        canvas.onmousedown = c_mousedown;
        canvas.onwheel = c_wheel;
        // requestAnimationFrame(() => {
        //     requestAnimationFrame(() => contWholeImgProcess());
        // });
    }

    // if(canvas.who[1] == 'i'){
    //     for (let slice = 0;slice<canvas.dim3; ++slice){

    //         const sliceOffset = sliceSize * slice;
    //         Array.from(Array(sliceSize).keys()).forEach((idx) => {
    //             const idx_4 = idx*4;
    //             let pix_val = (canvas.typedData[sliceOffset + idx] * canvas.scl_slope) + canvas.scl_inter;
    //             pix_val = ((pix_val - canvas.minHU)/(canvas.maxHU - canvas.minHU))*255
    //             canvasImageData.data[idx_4] = pix_val & 0xFF;
    //             canvasImageData.data[idx_4+1] = pix_val & 0xFF;
    //             canvasImageData.data[idx_4+2] = pix_val & 0xFF;
    //             canvasImageData.data[idx_4+3] = 0xFF;
    //         })
    //         tempCanvas.ctx.putImageData(canvasImageData,0,0)
    //         canvas.imgData[slice].src = URL.createObjectURL(await tempCanvas.convertToBlob());
    //     }
    // }
    // else{
    //     let fast_color_map = {0:{r:0x00,g:0x00,b:0x00,a:0x00}}
    //     Object.keys(canvas.color_map).forEach((val)=>{
    //         fast_color_map[val] = hexToRgb(canvas.color_map[val])
    //         fast_color_map[val].a = 0xFF
    //     })
    //     for (let slice = 0;slice<canvas.dim3; ++slice){
            
    //         const sliceOffset = sliceSize * slice;
    //         Array.from(Array(sliceSize).keys()).forEach((idx) => {
    //             const idx_4 = idx*4
    //             let fast_color_map_temp = fast_color_map[canvas.typedData[sliceOffset + idx]];
    //             canvasImageData.data[idx_4] = fast_color_map_temp.r & 0xFF;
    //             canvasImageData.data[idx_4+1] = fast_color_map_temp.g & 0xFF;
    //             canvasImageData.data[idx_4+2] = fast_color_map_temp.b & 0xFF;
    //             canvasImageData.data[idx_4+3] = fast_color_map_temp.a;
    //         })
    //         tempCanvas.ctx.putImageData(canvasImageData,0,0)
    //         canvas.imgData[slice].src = URL.createObjectURL(await tempCanvas.convertToBlob());
    //     }
    // }
    
    (canvas.who[1] == 'i') ? sliceProcess_img(canvas) : sliceProcess_mask(canvas);

    // const fastWorker = new Worker("static/worker/worker.js");
    // fastWorker.onmessage = async ({data}) => {
    //     fastWorker.onmessage = null;
    //     canvas.imgData[canvas.draw_prop.slc].src = data;
    // }
    // let worker_data = { choose:(canvas.who[0]%2), who:canvas.who, dim1:canvas.dim1, dim2:canvas.dim2, dim3:canvas.dim3, sliceSize:canvas.sliceSize, typedData:canvas.typedData, fast_color_map:canvas.fast_color_map, draw_prop:canvas.draw_prop, minHU:canvas.minHU, maxHU:canvas.maxHU, scl_inter:canvas.scl_inter, scl_slope:canvas.scl_slope}
    // fastWorker.postMessage(worker_data);

    // const slowWorker = new Worker("static/worker/worker.js");
    // slowWorker.onmessage = async ({data}) => {
    //     slowWorker.onmessage = null;
    //     data.map(async (val,idx)=>canvas.imgData[idx].src = val)
    // }
    // worker_data.choose = 2;
    // slowWorker.postMessage(worker_data);
}

function drawCanvas(canvas_mul) {
    requestAnimationFrame(() => {
        [...canvas_mul].forEach((canvas)=>{
            // canvas.ctx.save();
            // canvas.ctx.setTransform(1,0,0,1,0,0);
            // canvas.ctx.clearRect(0,0,canvas.width,canvas.height);
            // canvas.ctx.restore();
    
            canvas.ctx.clearRect(0,0,canvas.width,canvas.height);
    
            // canvas.ctx.imageSmoothingEnabled = 0;
            // canvas.ctx.mozImageSmoothingEnabled = 0;
            // canvas.ctx.webkitImageSmoothingEnabled = 0;
            // canvas.ctx.msImageSmoothingEnabled = 0;
            let prp = canvas.draw_prop;
            canvas.ctx.drawImage(canvas.imgData[prp.slc], prp.dx, prp.dy, prp.dWidth, prp.dHeight);
        });
        // requestAnimationFrame(() => {});
    })
}

function makeSlice(file, start, length) {
    var fileType = (typeof File);

    if (fileType === 'undefined') {
        return function () {};
    }

    if (File.prototype.slice) {
        return file.slice(start, start + length);
    }

    if (File.prototype.mozSlice) {
        return file.mozSlice(start, length);
    }

    if (File.prototype.webkitSlice) {
        return file.webkitSlice(start, length);
    }

    return null;
}

async function readFile(canvas) {
    let data = await fetch(canvas.f_p)
        .then(response => response.blob())
        .catch(error => console.error(error));
    const blob = makeSlice(data, 0, data.size);

    return new Promise((resolve) => {
        const reader = new FileReader();

        reader.onloadend = function (evt) {
            if (evt.target.readyState === FileReader.DONE) {
                readNIFTI(canvas, evt.target.result, resolve);
                // resolve();
            }
        };

        reader.readAsArrayBuffer(blob);
    });
}

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
    
    // tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").mozImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").webkitImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").msImageSmoothingEnabled = 0;
    tempCanvas.getContext("2d").putImageData(canvasImageData,0,0);
    canvas.imgData[slice].src = URL.createObjectURL(await tempCanvas.convertToBlob());
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
    canvas.imgData[slice].src = URL.createObjectURL(await tempCanvas.convertToBlob());
}

function allSliceProcess(canvas){
    if(canvas.who[1] == 'i')
        for (let slice = 0;slice<canvas.dim3; ++slice)
            setTimeout(() => sliceProcess_img(canvas,slice),0);
    else
        for (let slice = 0;slice<canvas.dim3; ++slice)
            setTimeout(() => sliceProcess_mask(canvas,slice),0);
}
function get_embeddings(canvas){

    fetch('/imgEmbeddings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({path:canvas.f_p})
    }).then((response) => response.json())
    .then((data) => {
        i_m[1].onclick = (e) => {
            let slice = i_m[1].draw_prop.slc;
            console.log("e.offsetX",e.offsetX);
            console.log("e.offsetY",e.offsetY);
            const clickcooords = i_m[1].xyCoord(e.offsetX,e.offsetY)
            console.log("i_m[1].xyCoord",clickcooords)
            if((!clickcooords.includes(null)) && ([481].includes(slice))){
                if(aaa.slice(0,2).includes())
                    aaa.splice(0,2,...clickcooords)
                else{
                    aaa.splice(2,2,...clickcooords)

                    const predWorker = new Worker("static/worker/worker_pred.js",{type:'module'});
                    predWorker.onmessage = async ({data}) => {
                        i_m[1].imgData[data.slice].onload = () =>{
                            i_m[1].imgData[data.slice].onload = null;
                            drawCanvas([i_m[1]])
                        }
                        i_m[1].imgData[data.slice].src = data.blob;
                    }
                    const worker_data = { embedding:({481:data[0]})[slice], xyxy: aaa, typedArray:i_m[1].typedData}
                    predWorker.postMessage(worker_data);
                    aaa = new Array(4);
                }
            }
            else{
                console.log("i_m[1].draw_prop.slc == 480 || i_m[1].draw_prop.slc == 481 || i_m[1].draw_prop.slc == 482",slice)
                aaa = new Array(4);
            }
        }
    })
}