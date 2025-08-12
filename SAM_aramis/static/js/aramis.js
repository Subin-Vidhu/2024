'use strict'
// ./nifti-reader-min.js of tagged release 0.6.3;
//https://github.com/rii-mango/NIFTI-Reader-JS/tree/v0.6.3

//This viewer accepts LPI images for axial
//This viewer accepts PIL images for sagittal
//This viewer accepts LIP images for coronal

class svg_drw{
    constructor(cvs, toastFunc = window.alert.bind(window)){
        this.cvs = cvs;
        this.svg = document.createElementNS('http://www.w3.org/2000/svg', "svg");
        this.svg.tabIndex = -1;
        this.svg.onmouseenter = (e) => e.currentTarget.focus();
        this.svg.onmouseleave = (e) => e.currentTarget.blur();
        this.svg.setAttribute('width', cvs.offcvs.width);
        this.svg.setAttribute('height', cvs.offcvs.height);
        this.svg.style.position = 'absolute';
        this.svg.style.top = 0;
        this.svg.style.left = 0;
        cvs.parentNode.appendChild(this.svg);

        this.destroy_evts = [['resize',(e) => {
                this.destroy();
                this.toast("Refrain from resizing the window while using this mode");
            }],
            ['keydown',(()=>{
                let label = 1;
                return (e) => {
                    switch(e.key.toUpperCase()) {
                        case " ":
                            label = label?0:1;
                            break;
                        case 'P':
                            if(this.svg.onclick?.set) {
                                this.toast("Finish ongoing annot before switching")
                                break;
                            }
                            this.svg.onclick = (evt) => this.new_point(evt.offsetX,evt.offsetY,label,label?"green":"red");
                            break;
                        case 'R':
                            if(this.svg.onclick?.set) break;
                            const onclick_func = (evt) => {
                                if(!this.new_rectangle(evt.offsetX,evt.offsetY,label,label?"green":"red")) return;
                                this.svg.onclick = (evt1) => {this.svg.onclick = onclick_func;}
                                this.svg.onclick.set = 1;
                            };
                            this.svg.onclick = onclick_func;
                            break;
                        case 'Z':
                            if(e.ctrlKey) this.destroy_child();
                            break;
                        case 'ESCAPE':
                            this.svg.onclick = null;
                            this.svg.onkeydown = null;
                            this.destroy();
                    }
                }
            })()]
        ]

        // window.addEventListener(...this.destroy_evts[0])
        for (let i=-1;++i<this.destroy_evts.length;)
            window.addEventListener(...this.destroy_evts[i]);
        
        // this.toast = toastFunc? toastFunc: alert;
        this.toast = toastFunc;
        this.annots=[];
        this.annots_map=[];
    }
    destroy(){
        if(!this.svg) return;
        this.svg.remove();
        for (;this.destroy_evts.length;)
            window.removeEventListener(...this.destroy_evts.pop());
        this.svg = null;
        this.toast("Finished or suspended annotations");
        return this.get_coords();
    }
    get_coords(){
        return structuredClone(this.annots.map((v) => {
            if(v.stats) return {ent:v.ent, val:v.val, label:v.label};
        }).filter((v)=>v))
    }
    get_coords_all(){
        return structuredClone(this.annots.map((v) => {
            return {ent:v.ent, val:v.val, label:v.label};
        }))
    }
    destroy_children(){
        this.toast("Removing all annotations for a restart.")
        for (;this.svg.children.length;)
            this.destroy_child();
    }
    destroy_child(msg, idx){
        if (!this.annots.length) return;
        this.svg.onmousemove = null;
        msg?this.toast(msg):0;
        idx = (idx!=undefined)? +idx : (this.annots.length - 1)
        this.annots[idx].tag.remove();
        this.annots[idx].stats?this.annots_map.splice(idx,1):0;
        this.annots.splice(idx,1);
    }
    push_annot(ent,tag,val,label = 1){
        const a = {ent:ent, tag: tag, val:val, stats:0, label:label};
        this.annots.push(a);
    }
    edit_last_annot(val,label){
        val?this.annots[this.annots.length-1].val = val:0;
        label?this.annots[this.annots.length-1].label = label:0;
        // finish ? this.finish_last_annot() : 0;
    }
    finish_last_annot(){
        const a= this.annots[this.annots.length-1],b = String([a.ent,a.val]);
        if(!this.annots_map.includes(b)) {
            this.annots_map.push(b);
            a.stats=1;
            return 1;
        }
        a.tag.remove();
        a.tag = null;
        this.toast(`Failed to add ${a.ent} - [${b}]`);
        this.annots.pop();
    }
    createSvgElement(tag, attributes) {
        const elem = document.createElementNS('http://www.w3.org/2000/svg', tag);
        this.setSvgAttributes(elem, attributes);
        this.svg.appendChild(elem);
        return elem;
    }
    setSvgAttributes(elem,attributes) {
        for (let attr in attributes) 
            elem.setAttribute(attr, attributes[attr]);
    }
    new_point( offsetX, offsetY, label, color = "white", radius = 2, fill = "transparent", stk_w = 1, type = 2){
        let coord = this.cvs.draw_prop.xyCoord(offsetX, offsetY, type)
        if(coord==null || coord.includes(null)){
            this.toast("Point should be on image!");
            return;
        }
        const circle = this.createSvgElement('circle', {
            cx: offsetX,
            cy: offsetY,
            r: radius,
            stroke: color,
            fill: fill,
            "stroke-width": stk_w
        });
        // this.svg.appendChild(circle);
        this.push_annot('pt', circle, coord, label)
        this.finish_last_annot();
    }
    append_point(){

    }
    new_line(){

    }
    add_line(){

    }
    end_line(){

    }
    new_rectangle(offsetX, offsetY, label, color = "white", fill = "#ffffff55", stk_w = 1, type = 2) {
        let coord = this.cvs.draw_prop.xyCoord(offsetX, offsetY, type)
        if(coord==null || coord.includes(null)) {
            this.toast("Point should be on image!");
            return;
        }
        const rect = this.createSvgElement('rect', {
            x: offsetX,
            y: offsetY,   
            width: 0,
            height: 0,
            stroke: color,
            fill: fill,
            "stroke-width": stk_w
        });
        [rect.x_ini, rect.y_ini] = [offsetX, offsetY];
        this.svg.onmousemove = (e) => {
            this.add_rectangle(rect, e.offsetX,e.offsetY, type)
        }
        rect.onclick = (e) => {
            this.svg.onmousemove = null;
            rect.onclick = null;
            this.add_rectangle(rect, e.offsetX,e.offsetY, type)
            this.end_rectangle(rect, type)
        }
        // svg.appendChild(rect);
        this.push_annot('rect', rect, [coord], label);
        return 1;
    }
    add_rectangle(rect, offsetX, offsetY, type) {
        const x1= Math.min(offsetX, rect.x_ini), y1= Math.min(offsetY, rect.y_ini), w= Math.abs(offsetX-rect.x_ini), h= Math.abs(offsetY-rect.y_ini);
        this.setSvgAttributes(rect, {
            x: x1,
            y: y1,
            width: w,
            height: h
        });
        this.edit_last_annot([...this.cvs.draw_prop.xyCoord(x1,y1,type),...this.cvs.draw_prop.xyCoord(x1+w,y1+h,type)])
    }
    end_rectangle(rect, type = 2) {
        const [x1,y1,x2,y2] = [+rect.getAttribute("x"), +rect.getAttribute("y"), +rect.getAttribute("x")+(+rect.getAttribute("width")), +rect.getAttribute("y")+(+rect.getAttribute("height"))];
        let coords = [this.cvs.draw_prop.xyCoord(x1, y1, type), this.cvs.draw_prop.xyCoord(x2, y2, type)];
        if(coords[1]==null || coords[1].includes(null) || coords[0]==null || coords[0].includes(null)) {
            this.destroy_child("Rectangle should be only on image!");
            return;
        }
        this.finish_last_annot();
    }
    new_polygon(){

    }
    add_polygon(){

    }
    end_polygon(){

    }
    new_circle(){

    }
    add_circle(){

    }
    end_circle(){

    }
    new_ellipse(){

    }
    add_ellipse(){

    }
    end_ellipse(){

    }
}

let predWorker, sam_type;
set_model(0);
function set_model(model_num) {
    model_num = +model_num
    const model_workers = [["static/worker/worker_pred.js","vit_h"]];
    if( !Number.isInteger(model_num) || (model_num<0) || (model_num>=model_workers.length)) {
        alert("Invalid model");
        return;
    }
    else if(predWorker instanceof Worker)
        predWorker.terminate();
    predWorker = new Worker(model_workers[model_num][0],{type:'module'}), sam_type = model_workers[model_num][1];
}
// const predWorker = new Worker("static/worker/worker_pred2.js",{type:'module'});
let i_m = document.getElementsByTagName('canvas');
// let workerHandleCount = i_m.length;
var aaa = new Array(4);

// document.body.onresize = () => {
//     Object.keys(i_m).forEach((idx)=>{
//         idx = +idx;
//         i_m[idx].width = parseInt(window.getComputedStyle(i_m[idx]).width);
//         i_m[idx].height = parseInt(window.getComputedStyle(i_m[idx]).height);
//         if((idx%2) == 1)
//             i_m[idx].draw_prop.reset();
//     });
// };

const handleFinalSlices = new Array()

Object.keys(i_m).forEach((idx)=>{
    idx = +idx;
    i_m[idx].f_p = i_m[idx].getAttribute('f_p');
    i_m[idx].removeAttribute('f_p');
    i_m[idx].offcvs = i_m[idx].transferControlToOffscreen()
    i_m[idx].ctx = i_m[idx].offcvs.getContext("2d");
    // i_m[idx].ctx.mozImageSmoothingEnabled = 0;
    // i_m[idx].ctx.webkitImageSmoothingEnabled = 0;
    // i_m[idx].ctx.msImageSmoothingEnabled = 0;
    i_m[idx].offcvs.width = parseInt(window.getComputedStyle(i_m[idx]).width);
    i_m[idx].offcvs.height = parseInt(window.getComputedStyle(i_m[idx]).height);
    // i_m[idx].ctx.imageSmoothingEnabled = 0;
    if((idx%2) == 0){
        i_m[idx].who = [idx,'i'];
        i_m[idx].draw_prop = {
            get dimx(){
                return i_m[idx].niftiHeader.dims[this.x];
            },
            get dimy(){
                return i_m[idx].niftiHeader.dims[this.y];
            },
            get dimz(){
                return i_m[idx].niftiHeader.dims[this.z];
            },
            get pixDimx(){
                return i_m[idx].niftiHeader.pixDims[this.x];
            },
            get pixDimy(){
                return i_m[idx].niftiHeader.pixDims[this.y];
            },
            get pixDimz(){
                return i_m[idx].niftiHeader.pixDims[this.z];
            },
            get width(){    
                return i_m[idx].offcvs.width;
            },
            get height(){
                return i_m[idx].offcvs.height;
            },
            scaleFac:0.10,
            multiplier:2,
            scale_curr:1,
            maxZoom:10.0,
            minZoom:0.05,
            get imgSE(){
                return [i_m[idx].ctx.imageSmoothingEnabled,i_m[idx+1].ctx.imageSmoothingEnabled];
            },
            imageSmoothingToggle: function(chng){
                chng = chng?chng:"im";
                chng = [chng.includes("i"), chng.includes("m")];
                [i_m[idx].ctx.imageSmoothingEnabled, i_m[idx+1].ctx.imageSmoothingEnabled] = this.imgSE.map((val,i) => chng[i] ? !val: val);
                chng = chng.map((val,i)=>val?[i_m[idx],i_m[idx+1]][i]:0).filter((val)=>val);
                drawCanvas(chng);
            },
            slcChange: function(newVal){
                if(newVal == '+')
                    newVal = Math.min(i_m[idx].draw_prop.dimz-1,Math.max(0,this.slc+1));
                else if(newVal == '-')
                    newVal = Math.min(i_m[idx].draw_prop.dimz-1,Math.max(0,this.slc-1));

                if(this.slc == newVal) return;
                this.slc = newVal;
                drawCanvas([i_m[idx],i_m[idx+1]]);
            },
            alphChange:function(newVal){
                if((typeof(newVal) == "string") && newVal.includes("%"))
                    newVal = Math.min(100,Math.max(0,newVal.slice(0,--newVal.length)))*255/100;
                newVal = Math.min(255,Math.max(0,Math.round(newVal)));
                if(this.a == newVal) return;
                this.a = newVal;
                Object.values(this.fast_color_map).slice(1).forEach((val) => val.a = this.a)
                drawCanvas([i_m[idx+1]]);
            },
            reset: function(draw, min_max_reset, slc_reset, clr_reset, ornt_reset){
                ornt_reset? this.chng_ornt(this.init_ornt,[0]) : 0;
                this.sliceSize = this.dimx * this.dimy;
                this.aspect_ratio = (this.pixDimx * this.dimx)/(this.pixDimy * this.dimy);
                this.dx = Math.max(0,(this.width - (this.aspect_ratio*this.height))/2);
                this.dy = Math.max(0,(this.height - (this.width/this.aspect_ratio))/2);
                this.dWidth = this.dx ? this.aspect_ratio*this.height : this.width;
                this.dHeight = this.dy ? this.width/this.aspect_ratio : this.height;
                this.orig_dWidth = this.dWidth;
                this.orig_dHeight = this.dHeight;
                i_m[idx].ctx.imageSmoothingEnabled = 0;
                i_m[idx+1].ctx.imageSmoothingEnabled = 0;
                i_m[idx].ctx.setTransform(1, 0, 0, 1, 0, 0);
                i_m[idx+1].ctx.setTransform(1, 0, 0, 1, 0, 0);
                this.scale_curr = 1;

                min_max_reset? (this.min = +i_m[idx].niftiHeader.cal_min, this.max = +i_m[idx].niftiHeader.cal_max) : 0;
                slc_reset? this.slc = Math.floor(this.dimz/2) : 0;
                clr_reset?this.fast_color_map = structuredClone(i_m[idx+1].fast_color_map) : 0;
                draw ? 0 : drawCanvas([i_m[idx],i_m[idx+1]]);
            },
            pan: function(x,y){
                this.dx += x;
                this.dy += y;

                drawCanvas([i_m[idx],i_m[idx+1]]);
            },
            scale: function(x,y,scroll){
                let change = +((Math.max(Math.min(this.scale_curr + (this.scaleFac * scroll),this.maxZoom),this.minZoom)).toFixed(this.multiplier));
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
                this.dx = x - (((x - this.dx) * change)/this.scale_curr);
                this.dy = y - (((y - this.dy) * change)/this.scale_curr);

                this.scale_curr = change;

                // let change = Math.max(Math.min(this.scale_curr + (this.scaleFac * scale_p.scroll),10.0),0.05);
                // this.dWidth = this.dWidth * change/this.scale_curr;
                // this.dHeight = this.dHeight * change/this.scale_curr;
                // this.scale_curr = change;

                drawCanvas([i_m[idx],i_m[idx+1]]);
            },
            xyCoord: function(offsetX,offsetY, type=0){
                switch(+type){
                    case 0: let coords = [(offsetX>=this.dx && offsetX<(this.dx+this.dWidth)) ? Math.max(Math.min(Math.floor((offsetX-this.dx) * this.dimx / this.dWidth),this.dimx - 1),0): null, (offsetY>=this.dy && offsetY<(this.dy+this.dHeight)) ? Math.max(Math.min(Math.floor((offsetY-this.dy) * this.dimy / this.dHeight),this.dimy - 1),0): null];
                        return coords.every((val) => val!=null) ? coords: null;
                        //true points on the image else no points
                    case 1: return [(offsetX>=this.dx && offsetX<(this.dx+this.dWidth)) ? Math.max(Math.min(Math.floor((offsetX-this.dx) * this.dimx / this.dWidth),this.dimx - 1),0): null, (offsetY>=this.dy && offsetY<(this.dy+this.dHeight)) ? Math.max(Math.min(Math.floor((offsetY-this.dy) * this.dimy / this.dHeight),this.dimy - 1),0): null];
                        //true points on the image else no x or y coord
                    case 2: return [Math.max(Math.min(Math.floor((offsetX-this.dx) * this.dimx / this.dWidth),this.dimx - 1),0), Math.max(Math.min(Math.floor((offsetY-this.dy) * this.dimy / this.dHeight),this.dimy - 1),0)];
                        //nearest points on the image to offset
                    case 3: return [Math.floor((offsetX-this.dx) * this.dimx / this.dWidth), Math.floor((offsetY-this.dy) * this.dimy / this.dHeight)];
                        //points on the image plane but can be imaginary
                    default: return null;
                }
            },
            WW_WL: function(ww,wl){
                // if(ww<=0)
                //     return;
                // if(ww==0)
                //     return;
                this.min_max_set(Math.round(wl-(ww/2)), Math.round(wl+(ww/2)))
                // this.max = Math.round(wl+(ww/2));
                // this.min = Math.round(wl-(ww/2));
                // drawCanvas([i_m[idx]])
                return [this.min, this.max];
            },
            min_max_set: function(min,max){
                // if(max<=min)
                //     return;
                if(max==min)
                    return;
                this.max = max;
                this.min = min;
                drawCanvas([i_m[idx]])
            },
            chng_ornt: function(newOrnt){
                // if(!this.ornt){
                //     newOrnt = i_m[idx].orig_ornt.substr(0,2)
                // }
                this.ornt = newOrnt ? newOrnt :({a:'s', s:'c', c:'a'})[this.ornt];
                
                // let x,y,z;
                switch(this.ornt) {
                    case 'a': this.x = (this.orig_ornt.includes('R') ? this.orig_ornt.indexOf('R'): this.orig_ornt.indexOf('L'))+1, this.y = (this.orig_ornt.includes('A') ? this.orig_ornt.indexOf('A'): this.orig_ornt.indexOf('P'))+1, this.z = (this.orig_ornt.includes('S') ? this.orig_ornt.indexOf('S'): this.orig_ornt.indexOf('I'))+1;
                        break;
                    case 's': this.x = (this.orig_ornt.includes('A') ? this.orig_ornt.indexOf('A'): this.orig_ornt.indexOf('P'))+1, this.y = (this.orig_ornt.includes('S') ? this.orig_ornt.indexOf('S'): this.orig_ornt.indexOf('I'))+1, this.z = (this.orig_ornt.includes('R') ? this.orig_ornt.indexOf('R'): this.orig_ornt.indexOf('L'))+1;
                        break;
                    case 'c': this.x = (this.orig_ornt.includes('R') ? this.orig_ornt.indexOf('R'): this.orig_ornt.indexOf('L'))+1, this.y = (this.orig_ornt.includes('S') ? this.orig_ornt.indexOf('S'): this.orig_ornt.indexOf('I'))+1, this.z = (this.orig_ornt.includes('A') ? this.orig_ornt.indexOf('A'): this.orig_ornt.indexOf('P'))+1;
                }
                // [this.dimx, this.dimy, this.dimz] = [i_m[idx].niftiHeader.dims[x], i_m[idx].niftiHeader.dims[y], i_m[idx].niftiHeader.dims[z]];
                // [this.pixDimx, this.pixDimy, this.pixDimz] = [i_m[idx].niftiHeader.pixDims[x], i_m[idx].niftiHeader.pixDims[y], i_m[idx].niftiHeader.pixDims[z]];
                i_m[idx].imgData = new Array(this.dimz).fill().map(() => {return {}});
                i_m[idx+1].imgData = new Array(this.dimz).fill().map(() => {return {}});
                // reset_params ? this.reset(...reset_params):0;
            }
        };
        i_m[idx].draw_prop_typedData = (slice = i_m[idx].draw_prop.slc, ornt = i_m[idx].draw_prop.ornt) => {
            const tempFunc = (a) => i_m[idx].draw_prop.orig_ornt.indexOf(a[ornt]);
            const dim12_prod = i_m[idx].niftiHeader.dims[1] * i_m[idx].niftiHeader.dims[2];
            const fast_mov = tempFunc({'a':'L', 's':'P', 'c':'L'}), fast_mov_dim = i_m[idx].niftiHeader.dims[fast_mov+1], slow_mov = tempFunc({'a':'P', 's':'I', 'c':'I'}), slice_mov = 3-fast_mov-slow_mov;

            return function*(){
                let i,j;
                // let v = {};
                let v = {
                    get [fast_mov](){
                        return j;
                    },
                    get [slow_mov](){
                        return i;
                    },
                    get [slice_mov](){
                        return slice;
                    },
                };
                // Object.defineProperties(v,{
                //     [fast_mov]:{
                //         get: ()=>j
                //     },
                //     [slow_mov]:{
                //         get: ()=>i
                //     },
                //     [slice_mov]:{
                //         get: ()=>slice
                //     }
                // });
                for (i=0;;i++)
                    for (j=0;j<fast_mov_dim;j++)
                        yield i_m[idx].dvGet((v[0] + v[1] * i_m[idx].niftiHeader.dims[1] + v[2] * dim12_prod)*i_m[idx].bpv, i_m[idx].niftiHeader.littleEndian)*i_m[idx].scl_slope + i_m[idx].scl_inter;
                        // yield i_m[idx].dvGet.call( i_m[idx].dv, (v[0] + v[1] * i_m[idx].niftiHeader.dims[1] + v[2] * dim12_prod)*i_m[idx].bpv, i_m[idx].niftiHeader.littleEndian)*i_m[idx].scl_slope + i_m[idx].scl_inter;
            }()
        }
        handleFinalSlices.push(readFile(i_m[idx]));
    }
    else{
        i_m[idx].onmouseenter = (e) => e.currentTarget.focus();
        i_m[idx].onmouseleave = (e) => e.currentTarget.blur();
        i_m[idx].who = [idx,'m'];
        i_m[idx].color_map = JSON.parse(i_m[idx].getAttribute('color_map'));
        i_m[idx].removeAttribute('color_map');

        Object.defineProperty(i_m[idx], 'draw_prop', {
            get: () => {
              return i_m[idx-1].draw_prop;
            }
        });
        i_m[idx].draw_prop.a = 0xFF;
        i_m[idx].draw_prop.c = [];
        i_m[idx].fast_color_map = {0:{r:0x00,g:0x00,b:0x00,a:0x00}}
        Object.keys(i_m[idx].color_map).forEach((val)=>{
            i_m[idx].fast_color_map[val] = hexToRgb(i_m[idx].color_map[val]);
            i_m[idx].fast_color_map[val].a = i_m[idx].draw_prop.a;
        })

        i_m[idx].draw_prop_typedData = (slice = i_m[idx].draw_prop.slc, ornt = i_m[idx].draw_prop.ornt) => {
            const tempFunc = (a) => i_m[idx].draw_prop.orig_ornt.indexOf(a[ornt]);
            const dim12_prod = i_m[idx-1].niftiHeader.dims[1] * i_m[idx-1].niftiHeader.dims[2];
            const fast_mov = tempFunc({'a':'L', 's':'P', 'c':'L'}), fast_mov_dim = i_m[idx].niftiHeader.dims[fast_mov+1], slow_mov = tempFunc({'a':'P', 's':'I', 'c':'I'}), slice_mov = 3-fast_mov-slow_mov;

            return function*(){
                let i,j;
                // let v = {};
                let v = {
                    get [fast_mov](){
                        return j;
                    },
                    get [slow_mov](){
                        return i;
                    },
                    get [slice_mov](){
                        return slice;
                    },
                };
                // Object.defineProperties(v,{
                //     [fast_mov]:{
                //         get: ()=>j
                //     },
                //     [slow_mov]:{
                //         get: ()=>i
                //     },
                //     [slice_mov]:{
                //         get: ()=>slice
                //     }
                // });
                for (i=0;;i++)
                    for (j=0;j<fast_mov_dim;j++)
                        yield i_m[idx].dvGet((v[0] + v[1] * i_m[idx].niftiHeader.dims[1] + v[2] * dim12_prod)*i_m[idx].bpv, i_m[idx].niftiHeader.littleEndian);
                        // yield i_m[idx].dvGet.call( i_m[idx].dv, (v[0] + v[1] * i_m[idx].niftiHeader.dims[1] + v[2] * dim12_prod)*i_m[idx].bpv, i_m[idx].niftiHeader.littleEndian);
            }()
        };
        i_m[idx].set_draw_prop_typedData_slice = (newArr, slice = i_m[idx].draw_prop.slc, ornt = i_m[idx].draw_prop.ornt) => {
            const tempFunc = (a) => i_m[idx].draw_prop.orig_ornt.indexOf(a[ornt]);
            const dim12_prod = i_m[idx-1].niftiHeader.dims[1] * i_m[idx-1].niftiHeader.dims[2];
            const fast_mov = tempFunc({'a':'L', 's':'P', 'c':'L'}), fast_mov_dim = i_m[idx].niftiHeader.dims[fast_mov+1], slow_mov = tempFunc({'a':'P', 's':'I', 'c':'I'}), slow_mov_dim = i_m[idx].niftiHeader.dims[slow_mov+1], slice_mov = 3-fast_mov-slow_mov;
            if (newArr.length !=(fast_mov_dim*slow_mov_dim)) throw new Error("newArr.length = ", newArr.length, "\nfast_mov_dim = ", fast_mov_dim, "\nslow_mov_dim = ", slow_mov_dim);
            
            let i,j;
            // let v = {};
            let v = {
                get [fast_mov](){
                    return j;
                },
                get [slow_mov](){
                    return i;
                },
                get [slice_mov](){
                    return slice;
                },
            };
            // Object.defineProperties( v,{
            //     [fast_mov]:{
            //         get: ()=>j
            //     },
            //     [slow_mov]:{
            //         get: ()=>i
            //     },
            //     [slice_mov]:{
            //         get: ()=>slice
            //     }
            // });
            for (i=0;i<slow_mov_dim;i++)
                for (j=0;j<fast_mov_dim;j++)
                    i_m[idx].dvSet((v[0] + v[1] * i_m[idx].niftiHeader.dims[1] + v[2] * dim12_prod)*i_m[idx].bpv, newArr[i*fast_mov_dim+j], i_m[idx].niftiHeader.littleEndian);
        }

        handleFinalSlices.push(readFile(i_m[idx],handleFinalSlices[idx-1]))
        // readFile(i_m[idx-1])
        //     .then(() => {
        //         readFile(i_m[idx]);
        //     });
    }
    window.addEventListener("resize", (e) => {
        i_m[idx].offcvs.width = parseInt(window.getComputedStyle(i_m[idx]).width);
        i_m[idx].offcvs.height = parseInt(window.getComputedStyle(i_m[idx]).height);
        if((idx%2) == 1)
            i_m[idx].draw_prop.reset();
    })
})
// Promise.all(handleFinalSlices)
// .then(() => {
//     Object.keys(i_m).forEach((idx)=>{
//         idx = +idx;
//         if(i_m[idx].who[1] == 'i')
//             get_embeddings(i_m[idx])
//     });
// })

function c_mousedown(e){
    e.preventDefault(); 
    const canvas = e.currentTarget;
    canvas.onmousemove = (e) => {
        if(e.ctrlKey)
            canvas.draw_prop.pan(e.movementX, e.movementY);
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
        e.currentTarget.draw_prop.scale(e.offsetX, e.offsetY, e.deltaY<0? 1 : -1);
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

function readNIFTI(canvas, data) {
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

    [canvas.typedData_type, canvas.dvSet, canvas.dvGet]= ({2:[Uint8Array, 'setUint8', 'getUint8'], 4:[Int16Array, 'setInt16', 'getInt16'], 8:[Int32Array, 'setInt32', 'getInt32'], 16:[Float32Array, 'setFloat32', 'getFloat32'], 64:[Float64Array, 'setFloat64', 'getFloat64'], 256:[Int8Array, 'setInt8', 'getInt8'], 512:[Uint16Array, 'setUint16', 'getUint16'], 768:[Uint32Array, 'setUint32', 'getUint32']})[canvas.niftiHeader.datatypeCode];
    canvas.typedData = new canvas.typedData_type(canvas.niftiImage);
    canvas.dv = new DataView(canvas.niftiImage);
    canvas.bpv = Math.round(canvas.niftiHeader.numBitsPerVoxel/8);
    // [canvas.dvSet, canvas.dvGet] = [DataView.prototype[canvas.dvSet], DataView.prototype[canvas.dvGet]];
    [canvas.dvSet, canvas.dvGet] = (canvas.who[1] == 'i')?[0, canvas.dv[canvas.dvGet].bind(canvas.dv)]:[canvas.dv[canvas.dvSet].bind(canvas.dv), canvas.dv[canvas.dvGet].bind(canvas.dv)];
    // if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT8) {
    //     canvas.typedData = new Uint8Array(canvas.niftiImage);
    // } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT16) {
    //     canvas.typedData = new Int16Array(canvas.niftiImage);
    // } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT32) {
    //     canvas.typedData = new Int32Array(canvas.niftiImage);
    // } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT32) {
    //     canvas.typedData = new Float32Array(canvas.niftiImage);
    // } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT64) {
    //     canvas.typedData = new Float64Array(canvas.niftiImage);
    // } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT8) {
    //     canvas.typedData = new Int8Array(canvas.niftiImage);
    // } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT16) {
    //     canvas.typedData = new Uint16Array(canvas.niftiImage);
    // } else if (canvas.niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT32) {
    //     canvas.typedData = new Uint32Array(canvas.niftiImage);
    // } else {
    //     return;
    // }    

    if(canvas.who[1] == 'i'){
        // canvas.minHU = canvas.draw_prop.min = +canvas.niftiHeader.cal_min
        // canvas.maxHU = canvas.draw_prop.max = +canvas.niftiHeader.cal_max
        // canvas.draw_prop.slc = Math.floor(canvas.niftiHeader.dims[3]/2);

        if (canvas.niftiHeader.scl_slope == 0)
            canvas.scl_slope = 1,canvas.scl_inter = 0;
        else
            canvas.scl_slope = canvas.niftiHeader.scl_slope,canvas.scl_inter = canvas.niftiHeader.scl_inter;
        canvas.draw_prop.orig_ornt = "LPI";
        canvas.draw_prop.init_ornt = {"LPI":'a', "PIL":'s', 'LIP':'c'}[canvas.draw_prop.orig_ornt];
        // canvas.draw_prop.dimx = canvas.niftiHeader.dims[1];
        // canvas.draw_prop.dimy = canvas.niftiHeader.dims[2];
        // canvas.draw_prop.dimz = canvas.niftiHeader.dims[3];
        // canvas.draw_prop.pixDimx = canvas.niftiHeader.pixDims[1];
        // canvas.draw_prop.pixDimy = canvas.niftiHeader.pixDims[2];
        // canvas.draw_prop.pixDimz = canvas.niftiHeader.pixDims[3];

        // canvas.draw_prop.chng_ornt(canvas.draw_prop.init_ornt);

        // canvas.draw_prop.sliceSize = canvas.draw_prop.dimx * canvas.draw_prop.dimy;
        // canvas.draw_prop.aspect_ratio = (canvas.niftiHeader.pixDims[1] * canvas.draw_prop.dimx)/(canvas.niftiHeader.pixDims[2] * canvas.draw_prop.dimy);
        

        // canvas.draw_prop_typedData = ({
        //     1:function*(slice){
        //         let slc_size = 0;
        //         let sliceOffset = (canvas.draw_prop.sliceSize*slice - 1)*canvas.bpv;
        //         while (1)
        //             yield canvas.dvGet.call( canvas.dv, sliceOffset+=canvas.bpv, canvas.niftiHeader.littleEndian)*canvas.scl_slope + canvas.scl_inter;
        //     },
        //     2:function*(slice){
        //         // let slc_size = 0;
        //         // let sliceOffset = slice-(canvas.draw_prop.dimy*canvas.draw_prop.dimx);
        //         for (let i=0;i<canvas.draw_prop.dimy;i++)
        //             for (let j=0;j<canvas.draw_prop.dimz;j++)
        //                 yield canvas.dvGet.call( canvas.dv, (slice + (i * canvas.draw_prop.dimx) + (j * canvas.draw_prop.dimx * canvas.draw_prop.dimy))*canvas.bpv, canvas.niftiHeader.littleEndian)*canvas.scl_slope + canvas.scl_inter;
        //     }
        // })[2];

        // let x = canvas.orig_ornt.indexOf('L')+1, y = canvas.orig_ornt.indexOf('P')+1, z = canvas.orig_ornt.indexOf('I')+1;

        // canvas.draw_prop.ornt_cycle = ({"LPI":['a','s','c','a'], "PIL":['s','-c','-a','s'], "LPI":['c','-s','a','c']})[canvas.orig_ornt]

        // canvas.draw_prop_typedData = () => {
        //     const tempFunc = (a) => canvas.draw_prop.orig_ornt.indexOf(a[canvas.draw_prop.ornt]);
        //     const dim12_prod = canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2];
        //     const fast_mov = tempFunc({'a':'L', 's':'P', 'c':'L'}), fast_mov_dim = canvas.niftiHeader.dims[fast_mov+1], slow_mov = tempFunc({'a':'P', 's':'I', 'c':'I'}), slice_mov = 3-fast_mov-slow_mov;

        //     return function*(){
        //         let i,j;
        //         let v = {};
        //         Object.defineProperties(v,{
        //             [fast_mov]:{
        //                 get: ()=>j
        //             },
        //             [slow_mov]:{
        //                 get: ()=>i
        //             },
        //             [slice_mov]:{
        //                 get: ()=>canvas.draw_prop.slc
        //             }
        //         });
        //         for (i=0;;i++)
        //             for (j=0;j<fast_mov_dim;j++)
        //                 yield canvas.dvGet.call( canvas.dv, (v[0] + v[1] * canvas.niftiHeader.dims[1] + v[2] * dim12_prod)*canvas.bpv, canvas.niftiHeader.littleEndian)*canvas.scl_slope + canvas.scl_inter;
        //     }()
        //     // return {
        //     //     a:function*(){
        //     //         for (let i=0;;i++)
        //     //             for (let j=0;j<canvas.niftiHeader.dims[1];j++)
        //     //                 yield canvas.dvGet.call( canvas.dv, (j + i * canvas.niftiHeader.dims[1] + canvas.draw_prop.slc * canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2])*canvas.bpv, canvas.niftiHeader.littleEndian)*canvas.scl_slope + canvas.scl_inter;
        //     //     },
        //     //     s:function*(){
        //     //         for (let i=0;;i++)
        //     //             for (let j=0;j<canvas.niftiHeader.dims[2];j++)
        //     //                 yield canvas.dvGet.call( canvas.dv, (canvas.draw_prop.slc + j * canvas.niftiHeader.dims[1] + i * canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2])*canvas.bpv, canvas.niftiHeader.littleEndian)*canvas.scl_slope + canvas.scl_inter;
        //     //     },
        //     //     c:function*(){
        //     //         for (let i=0;;i++)
        //     //             for (let j=0;j<canvas.niftiHeader.dims[1];j++)
        //     //                 yield canvas.dvGet.call( canvas.dv, (j + canvas.draw_prop.slc * canvas.niftiHeader.dims[1] + i * canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2])*canvas.bpv, canvas.niftiHeader.littleEndian)*canvas.scl_slope + canvas.scl_inter;
        //     //     }
        //     // }[canvas.draw_prop.ornt]()
        // }
        // canvas.draw_prop_typedData = new Float32Array(canvas.typedData.map((val)=>val*canvas.scl_slope+canvas.scl_inter))
        canvas.draw_prop.reset(1,1,1,1,1);
    }
    // else{
    //     // canvas.draw_prop_typedData = ()=>{
    //     //     return {
    //     //         a:function*(){
    //     //             for (let i=0;;i++)
    //     //                 for (let j=0;j<canvas.draw_prop.dimx;j++)
    //     //                     yield canvas.dvGet.call( canvas.dv, (j + i * canvas.niftiHeader.dims[1] + canvas.draw_prop.slc * canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2])*canvas.bpv, canvas.niftiHeader.littleEndian);
    //     //         },
    //     //         s:function*(){
    //     //             for (let i=0;;i++)
    //     //                 for (let j=0;j<canvas.draw_prop.dimy;j++)
    //     //                     yield canvas.dvGet.call( canvas.dv, (canvas.draw_prop.slc + j * canvas.niftiHeader.dims[1] + i * canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2])*canvas.bpv, canvas.niftiHeader.littleEndian);
    //     //         },
    //     //         c:function*(){
    //     //             for (let i=0;;i++)
    //     //                 for (let j=0;j<canvas.draw_prop.dimx;j++)
    //     //                     yield canvas.dvGet.call( canvas.dv, (j + canvas.draw_prop.slc * canvas.niftiHeader.dims[1] + i * canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2])*canvas.bpv, canvas.niftiHeader.littleEndian);
    //     //         }
    //     //     }[canvas.draw_prop.ornt]()
    //     // }
    //     canvas.draw_prop_typedData = () => {
    //         const tempFunc = (a) => canvas.draw_prop.orig_ornt.indexOf(a[canvas.draw_prop.ornt]);
    //         const dim12_prod = canvas.niftiHeader.dims[1] * canvas.niftiHeader.dims[2];
    //         const fast_mov = tempFunc({'a':'L', 's':'P', 'c':'L'}), fast_mov_dim = canvas.niftiHeader.dims[fast_mov+1], slow_mov = tempFunc({'a':'P', 's':'I', 'c':'I'}), slice_mov = 3-fast_mov-slow_mov;

    //         return function*(){
    //             let i,j;
    //             let v = {};
    //             Object.defineProperties(v,{
    //                 [fast_mov]:{
    //                     get: ()=>j
    //                 },
    //                 [slow_mov]:{
    //                     get: ()=>i
    //                 },
    //                 [slice_mov]:{
    //                     get: ()=>canvas.draw_prop.slc
    //                 }
    //             });
    //             for (i=0;;i++)
    //                 for (j=0;j<fast_mov_dim;j++)
    //                     yield canvas.dvGet.call( canvas.dv, (v[0] + v[1] * canvas.niftiHeader.dims[1] + v[2] * dim12_prod)*canvas.bpv, canvas.niftiHeader.littleEndian);
    //         }()
    //     }
    //     // canvas.draw_prop.fast_color_map = structuredClone(canvas.fast_color_map)
    // }
    // contWholeImgProcess();
    // canvas.imgData = new Array(canvas.draw_prop.dimz).fill().map(() => {return {}});

    drawCanvas([canvas]);
    if (canvas.who[1] == 'm') {
        canvas.onmousedown = c_mousedown;
        canvas.onwheel = c_wheel;
    }
}

function drawCanvas(canvas_mul) {
    requestAnimationFrame(() => {
        [...canvas_mul].forEach((canvas)=>{
            sliceProcess(canvas);
    
            canvas.ctx.clearRect(0,0,canvas.offcvs.width,canvas.offcvs.height);
    
            let prp = canvas.draw_prop;
            canvas.ctx.drawImage(canvas.imgData[prp.slc].img, prp.dx, prp.dy, prp.dWidth, prp.dHeight);
        });
        // requestAnimationFrame(() => {});
    })
}

function makeSlice(file, start, length) {
    const fileType = (typeof File);

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

async function readFile(canvas, prevRes = 0) {
    let data = await fetch('/getFile?q='+encodeURIComponent(canvas.f_p))
        .then(response => response.blob())
        .catch(error => console.error(error));
    const blob = makeSlice(data, 0, data.size);

    return new Promise((resolve) => {
        const reader = new FileReader();

        reader.onloadend = async (evt) => {
            prevRes ? await prevRes :0;
            resolve();
            if (evt.currentTarget.readyState === FileReader.DONE) {
                readNIFTI(canvas, evt.currentTarget.result);
            }
        };

        reader.readAsArrayBuffer(blob);
    });
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function sliceProcess(canvas, slice = canvas.draw_prop.slc){
    if(canvas.who[1] == "i"){
        if((canvas.draw_prop.min == canvas.imgData[slice].min) && (canvas.draw_prop.max == canvas.imgData[slice].max))
            return;
        canvas.imgData[slice].min = canvas.draw_prop.min;
        canvas.imgData[slice].max = canvas.draw_prop.max;
        var imgData_ipt = new Uint8ClampedArray(4 * canvas.draw_prop.dimx * canvas.draw_prop.dimy)
        const get_vox_val = canvas.draw_prop_typedData()
        for(let i=0; i<canvas.draw_prop.sliceSize; i++){
            // let pix_val = (canvas.draw_prop_typedData[sliceOffset+i] * canvas.scl_slope) + canvas.scl_inter;
            let pix_val = (get_vox_val.next().value - canvas.draw_prop.min)/(canvas.draw_prop.max - canvas.draw_prop.min)*255;
            let idx_4 = i*4;
            imgData_ipt[idx_4++] = imgData_ipt[idx_4++] = imgData_ipt[idx_4++] = pix_val;
            imgData_ipt[idx_4] = 255;
        }
    }
    else if(!(canvas.draw_prop.a == canvas.imgData[slice].a) || !canvas.draw_prop.c.includes(slice)){
        var imgData_ipt = new Uint8ClampedArray(4 * canvas.draw_prop.dimx * canvas.draw_prop.dimy)
        const get_vox_val = canvas.draw_prop_typedData()
        for(let i=0; i<canvas.draw_prop.sliceSize; i++){
            // const fast_color_map_temp = canvas.draw_prop.fast_color_map[canvas.draw_prop_typedData[sliceOffset+i]]
            const fast_color_map_temp = canvas.draw_prop.fast_color_map[get_vox_val.next().value]
            let idx_4 = i*4;
            imgData_ipt[idx_4++] = fast_color_map_temp.r;
            imgData_ipt[idx_4++] = fast_color_map_temp.g;
            imgData_ipt[idx_4++] = fast_color_map_temp.b;
            imgData_ipt[idx_4] = fast_color_map_temp.a;
        }
        canvas.imgData[slice].a = canvas.draw_prop.a;
        canvas.draw_prop.c.includes(slice) ? 0 : canvas.draw_prop.c.push(slice);
    }
    else
        return;
    const tempCanvas = new OffscreenCanvas(canvas.draw_prop.dimx,canvas.draw_prop.dimy)
    tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
    tempCanvas.getContext("2d").putImageData(new ImageData( imgData_ipt, canvas.draw_prop.dimx, canvas.draw_prop.dimy),0,0);
    canvas.imgData[slice].img = tempCanvas;
}

async function sliceProcess_img(canvas, slice = canvas.draw_prop.slc){
    // const tempCanvas = new OffscreenCanvas(canvas.draw_prop.dimx,canvas.dim2)
    if((canvas.draw_prop.min == canvas.imgData[slice].min) && (canvas.draw_prop.max == canvas.imgData[slice].max))
        return;
    const sliceOffset = canvas.draw_prop.sliceSize * slice;
    const imgData_ipt = new Uint8ClampedArray(4 * canvas.draw_prop.dimx * canvas.draw_prop.dimy)
    for(let i=0; i<canvas.draw_prop.dimx * canvas.draw_prop.dimy; i+=4){
        // let pix_val = (canvas.draw_prop_typedData[sliceOffset+i] * canvas.scl_slope) + canvas.scl_inter;
        let pix_val = (canvas.draw_prop_typedData[sliceOffset+i] - canvas.draw_prop.min)/(canvas.draw_prop.max - canvas.draw_prop.min)*255;
        let idx_4 = i*4;
        imgData_ipt[idx_4++] = imgData_ipt[idx_4++] = imgData_ipt[idx_4++] = pix_val;
        imgData_ipt[idx_4] = 255;
    }
    const tempCanvas = new OffscreenCanvas(canvas.draw_prop.dimx,canvas.draw_prop.dimy)
    tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
    tempCanvas.getContext("2d").putImageData(new ImageData( imgData_ipt, canvas.draw_prop.dimx, canvas.draw_prop.dimy),0,0);
    canvas.imgData[slice].img = tempCanvas;
}

async function sliceProcess_mask(canvas,slice = canvas.draw_prop.slc){
    if((canvas.min == canvas.imgData[slice].min) && (canvas.max == canvas.imgData[slice].max))
        return;
    const tempCanvas = new OffscreenCanvas(canvas.draw_prop.dimx,canvas.draw_prop.dimy)
    // tempCanvas.ctx = tempCanvas.getContext("2d")
    // const canvasImageData = tempCanvas.ctx.createImageData(tempCanvas.width, tempCanvas.height)

    const sliceOffset = canvas.draw_prop.sliceSize * slice;
    // Array.from(Array(canvas.draw_prop.sliceSize).keys()).forEach((idx) => {
    //     const idx_4 = idx*4
    //     let fast_color_map_temp = canvas.fast_color_map[canvas.draw_prop_typedData[sliceOffset + idx]];
    //     canvasImageData.data[idx_4] = fast_color_map_temp.r & 0xFF;
    //     canvasImageData.data[idx_4+1] = fast_color_map_temp.g & 0xFF;
    //     canvasImageData.data[idx_4+2] = fast_color_map_temp.b & 0xFF;
    //     canvasImageData.data[idx_4+3] = fast_color_map_temp.a;
    // })

    // tempCanvas.ctx.putImageData(canvasImageData,0,0)

    const canvasImageData = new ImageData(new Uint8ClampedArray([...canvas.draw_prop_typedData.subarray(sliceOffset, sliceOffset + canvas.draw_prop.sliceSize)].flatMap((val)=>{
        let fast_color_map_temp = canvas.draw_prop.fast_color_map[val];
        return [ fast_color_map_temp.r, fast_color_map_temp.g, fast_color_map_temp.b, fast_color_map_temp.a];
    })), canvas.draw_prop.dimx, canvas.draw_prop.dimy)

    tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").mozImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").webkitImageSmoothingEnabled = 0;
    // tempCanvas.getContext("2d").msImageSmoothingEnabled = 0;
    tempCanvas.getContext("2d").putImageData(canvasImageData,0,0)
    canvas.imgData[slice].src = URL.createObjectURL(await tempCanvas.convertToBlob());
}

function allSliceProcess(canvas){
    if(canvas.who[1] == 'i')
        for (let slice = 0;slice<canvas.draw_prop.dimz; ++slice)
            setTimeout(() => sliceProcess_img(canvas,slice),0);
    else
        for (let slice = 0;slice<canvas.draw_prop.dimz; ++slice)
            setTimeout(() => sliceProcess_mask(canvas,slice),0);
}

let model_pass_annotation;
function get_embeddings_new(canvas, label, label_color = {r:0, g:255, b:0, a:128}) {
    label=+label;
    let interval_pred_id;
    const {slc,min,max,z,dx,dy,dWidth,dHeight,dimx,dimy} = canvas.draw_prop, mask_cvs = i_m[(canvas.who[0]%2) == 0 ? canvas.who[0]+1: canvas.who[0]], embedding_controller = new AbortController;
    if(!Object.keys(canvas.draw_prop.fast_color_map).includes(label+"") || label == 0) return;
    
    model_pass_annotation = new svg_drw(canvas);
    embedding_controller.signal.onabort = (e) => {
        window.removeEventListener('resize',temp_func)
        predWorker.onmessage = null;
        clearInterval(interval_pred_id);
        embedding_controller.signal.onabort = null;
        model_pass_annotation.destroy();
    }
    const temp_func = (e) => embedding_controller.abort();
    window.addEventListener('resize',temp_func);
    
    const fetch_wait = fetch('/imgEmbeddings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            path:canvas.f_p,
            slice:slc,
            ndim:z,
            min:min,
            max:max,
            sam_type:sam_type
        })
    },{signal:embedding_controller.signal})
        .then((response) => response.json())
        .then((data) => {
            predWorker.onmessage = ({data:{imgData,final}}) => {
                if(final) {
                    predWorker.onmessage = null;
                    mask_cvs.set_draw_prop_typedData_slice(final,slc)
                    embedding_controller.abort();
                    return;
                }
                requestAnimationFrame(() => {                
                    const tempCanvas = new OffscreenCanvas(dimx,dimy)
                    tempCanvas.getContext("2d").imageSmoothingEnabled = 0;
                    tempCanvas.getContext("2d").putImageData(imgData,0,0);
                    mask_cvs.ctx.clearRect(0,0,mask_cvs.offcvs.width,mask_cvs.offcvs.height);
                    mask_cvs.ctx.drawImage(tempCanvas, dx, dy, dWidth, dHeight);
                })
            }
            predWorker.postMessage({embedding:data.imgEmb, coords: model_pass_annotation.get_coords_all(), dx, dy, dWidth, dHeight, w:dimx, h:dimy, color:label_color})
            // interval_pred_id = setInterval(() => predWorker.postMessage({coords: model_pass_annotation.get_coords_all()})
            //     ,4000);
            aaa = model_pass_annotation.get_coords_all;
            console.log("prediction is READY 😶");
        })
        .catch((e) => console.log(e));
    return {
        abort:()=>embedding_controller.abort(), 
        finish:()=>predWorker.postMessage({coords: model_pass_annotation.get_coords(),final:label}),
        once_more:()=>predWorker.postMessage({coords: model_pass_annotation.get_coords()})
    };
}

function get_embeddings(canvas){

    fetch('/imgEmbeddings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            path:canvas.f_p,
            slice:canvas.draw_prop.slc,
            ndim:canvas.draw_prop.z,
            min:canvas.draw_prop.min,
            max:canvas.draw_prop.max,
            sam_type:sam_type
        })
    }).then((response) => response.json())
    .then((data) => {
        i_m[(canvas.who[0]%2) == 0 ? canvas.who[0]+1: canvas.who[0]].onclick = (e) => {
            let slice = e.currentTarget.draw_prop.slc;
            console.log("e.offsetX",e.offsetX);
            console.log("e.offsetY",e.offsetY);
            const clickcooords = i_m[1].draw_prop.xyCoord(e.offsetX,e.offsetY,2)
            console.log("i_m[1].xyCoord",clickcooords)
            if((!clickcooords.includes(null)) && ([481].includes(slice))){
                if(aaa.slice(0,2).includes())
                    aaa.splice(0,2,...clickcooords)
                else{
                    aaa.splice(2,2,...clickcooords)

                    // const predWorker = new Worker("static/worker/worker_pred.js",{type:'module'});
                    predWorker.onmessage = async ({data}) => {
                        i_m[1].imgData[data.slice].onload = () =>{
                            i_m[1].imgData[data.slice].onload = null;
                            drawCanvas([i_m[1]])
                        }
                        i_m[1].imgData[data.slice].src = data.blob;
                    }
                    const worker_data = { embedding:data.imgEmb, xyxy: aaa, typedArray:i_m[1].typedData}
                    predWorker.postMessage(worker_data);
                    aaa = new Array(4);
                }
            }
            else{
                console.log("i_m[1].draw_prop.slc == 480 || i_m[1].draw_prop.slc == 481 || i_m[1].draw_prop.slc == 482",slice)
                aaa = new Array(4);
            }
        }
        console.log("prediction is READY 😶");
    })
}