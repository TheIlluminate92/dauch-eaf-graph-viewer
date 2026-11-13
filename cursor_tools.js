/* Coordinate math and up-to-ten pins. Pins belong to the current recordings and
 * axis definitions, not to reusable view presets. No sample values are invented. */
(function(root,factory){
 const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.EafCursor=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
 'use strict';
 function numeric(axis,value){
  if(axis.type!=='date')return Number(value);
  if(typeof value==='number')return value;
  const text=String(value).replace(' ','T');
  return Date.parse(/[zZ]$|[+-]\d\d:\d\d$/.test(text)?text:text+'Z');
 }
 function axisValue(axis,fraction){const a=numeric(axis,axis.range[0]),b=numeric(axis,axis.range[1]);return a+(b-a)*fraction;}
 function axisFraction(axis,value){const a=numeric(axis,axis.range[0]),b=numeric(axis,axis.range[1]);return b===a?NaN:(value-a)/(b-a);}
 function number(value){return Number.isFinite(value)?Number(value.toPrecision(7)).toLocaleString('en-US',{maximumFractionDigits:8}):'—';}
 function time(value,type){return type==='date'?new Date(value).toISOString().replace('T',' ').replace('Z',' UTC'):number(value)+(type==='signal'?'':' min');}
 function xLabel(point){return point.type==='signal'?'X ('+point.xLabel+')':'Time';}
 class PinStore{
  constructor(){this.pins=[];this.active=null;this.context=null;}
  setContext(context){const changed=this.context!==null&&this.context!==context;this.context=context;if(changed)this.clear();return changed;}
  add(point){
   if(this.pins.length>=10)return null;
   if(!Number.isFinite(point.x)||(!Number.isFinite(point.left)&&!Number.isFinite(point.right)))return null;
   const id=Array.from({length:10},(_,i)=>i+1).find(n=>!this.pins.some(p=>p.id===n));
   const pin=Object.freeze({...point,id});this.pins.push(pin);this.active=id;return pin;
  }
  remove(id){this.pins=this.pins.filter(p=>p.id!==id);if(this.active===id)this.active=this.pins.at(-1)?.id??null;}
  clear(){this.pins=[];this.active=null;}
 }
 // A delayed single click lets Plotly keep its double-click reset gesture.
 class ClickTracker{
  constructor(add,delay=360,timer=(fn,ms)=>setTimeout(fn,ms),cancel=id=>clearTimeout(id)){this.add=add;this.delay=delay;this.timer=timer;this.cancelTimer=cancel;this.start=null;this.pending=null;this.pendingValue=null;}
  cancel(){if(this.pending!==null)this.cancelTimer(this.pending);this.pending=null;this.pendingValue=null;this.start=null;}
  commit(){const value=this.pendingValue;if(this.pending!==null)this.cancelTimer(this.pending);this.pending=null;this.pendingValue=null;if(value)this.add(value.point,value.context);}
  down(event,point,context){if(event.button!==0)return;
   // A second click at a different position is another pin, not a reset gesture.
   if(this.pendingValue&&Math.hypot(event.clientX-this.pendingValue.x,event.clientY-this.pendingValue.y)>4)this.commit();
   if(event.detail>1){this.cancel();return;}this.start=point?{x:event.clientX,y:event.clientY,point,context,moved:false}:null;}
  move(event){if(this.start&&Math.hypot(event.clientX-this.start.x,event.clientY-this.start.y)>4)this.start.moved=true;}
  up(event,context){const start=this.start;this.start=null;if(event.button!==0||!start||start.moved||context!==start.context||Math.hypot(event.clientX-start.x,event.clientY-start.y)>4)return;
   if(this.pending!==null)this.cancelTimer(this.pending);
   this.pendingValue=start;this.pending=this.timer(()=>this.commit(),this.delay);
  }
 }
 function mount(gd,resize){
  const $=id=>document.getElementById(id),store=new PinStore();
  let pointer=null,frame=0,enabled=false,bound=false,axisInfo={kind:'elapsed',label:''};
  const create=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
  function geometry(){
   const l=gd._fullLayout;if(!l?.xaxis||!l.width||!l.height)return null;
   const y=Number.isFinite(l.yaxis?._length)?l.yaxis:l.yaxis2;if(!y||!Number.isFinite(y._length))return null;
   const rect=gd.getBoundingClientRect(),sx=rect.width/l.width,sy=rect.height/l.height;
   return {l,rect,left:l.xaxis._offset*sx,top:y._offset*sy,width:l.xaxis._length*sx,height:y._length*sy};
  }
  function visible(axis){return gd.data?.some(t=>(t.yaxis||'y')===axis&&t.visible!==false&&t.visible!=='legendonly');}
  function capture(point){
   const g=geometry();if(!enabled||!g||!point)return null;
   const px=point.x-g.rect.left,py=point.y-g.rect.top,fx=(px-g.left)/g.width,fy=1-(py-g.top)/g.height;
   if(fx<0||fx>1||fy<0||fy>1||!Number.isFinite(fx+fy))return null;
   const left=visible('y')?axisValue(g.l.yaxis,fy):null,right=visible('y2')&&g.l.yaxis2?axisValue(g.l.yaxis2,fy):null;
   if(left===null&&right===null)return null;
   return {x:axisValue(g.l.xaxis,fx),left,right,type:axisInfo.kind==='signal'?'signal':g.l.xaxis.type,xLabel:axisInfo.label,anchor:left!==null?'left':'right'};
  }
  function yPixel(g,point,side){const axis=side==='left'?g.l.yaxis:g.l.yaxis2;return axis&&Number.isFinite(point[side])?g.top+(1-axisFraction(axis,point[side]))*g.height:NaN;}
  function inY(g,y){return Number.isFinite(y)&&y>=g.top-0.5&&y<=g.top+g.height+0.5;}
  function hide(){ $('cursorOverlay').hidden=true;$('cursorReadout').textContent='Move to read coordinates · click to pin (up to 10).'; }
  function renderTable(){
   $('pinCount').textContent=store.pins.length+' / 10';$('pinList').replaceChildren();
   $('clearPins').disabled=!store.pins.length;$('liveCursor').disabled=store.active===null;
   for(const pin of store.pins){
    const row=create('div',undefined,'pin-row'+(store.active===pin.id?' active':''));
    const select=create('button',`P${pin.id} · ${xLabel(pin)}: ${time(pin.x,pin.type)}\nY left: ${number(pin.left)}  |  Y right: ${number(pin.right)}`,'pin-select');
    select.title='Show pinned crosshair P'+pin.id;select.onclick=()=>{store.active=pin.id;renderTable();schedule();};
    const remove=create('button','×','pin-remove');remove.setAttribute('aria-label','Remove pin '+pin.id);remove.onclick=()=>{store.remove(pin.id);$('pinNotice').textContent='';renderTable();schedule();};
    row.append(select,remove);$('pinList').append(row);
   }
  }
  function drawPins(g){
   $('pinMarkers').replaceChildren();if(!enabled||!g)return;
   for(const pin of store.pins){
    const fx=axisFraction(g.l.xaxis,pin.x),py=yPixel(g,pin,pin.anchor);if(fx<0||fx>1||!Number.isFinite(fx))continue;
    const px=g.left+fx*g.width,line=create('div',undefined,'pin-v'+(store.active===pin.id?' active':''));
    Object.assign(line.style,{left:px+'px',top:g.top+'px',height:g.height+'px'});$('pinMarkers').append(line);
    if(inY(g,py)){const dot=create('div','P'+pin.id,'pin-dot'+(store.active===pin.id?' active':''));Object.assign(dot.style,{left:px+'px',top:py+'px'});$('pinMarkers').append(dot);}
   }
  }
  function draw(){
   frame=0;const g=geometry();drawPins(g);const pin=store.pins.find(p=>p.id===store.active),point=pin||capture(pointer);
   if(!enabled||!g||!point){hide();return;}
   const fx=axisFraction(g.l.xaxis,point.x),px=g.left+fx*g.width,yl=yPixel(g,point,'left'),yr=yPixel(g,point,'right');
   const anchor=point.anchor==='left'?yl:yr,timeText=time(point.x,point.type);
   $('cursorReadout').textContent=`${pin?'Pinned P'+pin.id:'Cursor'} · ${xLabel(point)}: ${timeText}  |  Y left: ${number(point.left)}  |  Y right: ${number(point.right)}`;
   if(!Number.isFinite(fx)||fx<0||fx>1||!inY(g,anchor)){
    $('cursorOverlay').hidden=true;$('cursorReadout').textContent+=' · Outside current zoom';return;
   }
   $('cursorOverlay').hidden=false;
   Object.assign($('cursorVertical').style,{left:px+'px',top:g.top+'px',height:g.height+'px'});
   Object.assign($('cursorHorizontal').style,{left:g.left+'px',top:anchor+'px',width:g.width+'px'});
   // Independently zoomed left/right axes can put the two captured values at
   // different heights. Position each label on its own actual scale.
   for(const [side,py] of [['Left',yl],['Right',yr]]){
    const n=$('cursor'+side);n.hidden=!inY(g,py);n.textContent=number(point[side.toLowerCase()]);
    Object.assign(n.style,{left:(side==='Left'?g.left-3:g.left+g.width+3)+'px',top:py+'px'});
   }
   const extra=point.anchor==='left'?yr:yl;$('cursorOtherHorizontal').hidden=!inY(g,extra)||Math.abs(extra-anchor)<1;
   Object.assign($('cursorOtherHorizontal').style,{left:g.left+'px',top:extra+'px',width:g.width+'px'});
   $('cursorTime').textContent=(pin?'P'+pin.id+' · ':'')+(point.type==='signal'?'X: ':'')+timeText;const half=$('cursorTime').offsetWidth/2;
   Object.assign($('cursorTime').style,{left:Math.max(half,Math.min(g.rect.width-half,px))+'px',top:(g.top+g.height+2)+'px'});
  }
  function schedule(){if(!frame)frame=requestAnimationFrame(draw);}
  const clicks=new ClickTracker((point,context)=>{
   if(!enabled||context!==store.context)return;
   if(!store.add(point)){$('pinNotice').textContent='10 pins reached. Remove one or clear pins to add another.';return;}
   $('pinNotice').textContent='Pinned coordinates stay fixed while you zoom.';renderTable();schedule();
  });
  function bind(){
   if(bound)return;bound=true;
   gd.addEventListener('mousedown',e=>clicks.down(e,capture({x:e.clientX,y:e.clientY}),store.context),true);
   // Plotly places a temporary drag cover outside the chart. Window capture
   // observes release there, while movement threshold separates clicks/drags.
   window.addEventListener('mousemove',e=>clicks.move(e),true);
   window.addEventListener('mouseup',e=>clicks.up(e,store.context),true);
   gd.addEventListener('dblclick',()=>clicks.cancel(),true);
   gd.addEventListener('mousemove',e=>{pointer=e.buttons?null:{x:e.clientX,y:e.clientY};schedule();},true);
   gd.addEventListener('mouseleave',()=>{pointer=null;schedule();});
   gd.on('plotly_relayout',schedule);gd.on('plotly_afterplot',schedule);
   let resizeFrame=0;new ResizeObserver(()=>{if(resizeFrame)cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{resizeFrame=0;if(gd.clientWidth&&gd.clientHeight)resize();});}).observe($('plotShell'));
   $('clearPins').onclick=()=>{clicks.cancel();store.clear();$('pinNotice').textContent='';renderTable();schedule();};
   $('liveCursor').onclick=()=>{store.active=null;pointer=null;renderTable();schedule();};
  }
  renderTable();
  return {
   begin(){enabled=false;pointer=null;clicks.cancel();hide();$('pinMarkers').replaceChildren();},
   ready(context,info={kind:'elapsed',label:''}){axisInfo=info;const count=store.pins.length;const changed=store.setContext(context);if(changed&&count)$('pinNotice').textContent='Pins cleared because recordings, signals, or the X axis changed.';enabled=true;bind();renderTable();schedule();},
   fail(){store.clear();renderTable();enabled=false;hide();$('pinMarkers').replaceChildren();}
  };
 }
 return {PinStore,ClickTracker,axisValue,axisFraction,number,time,xLabel,mount};
});
