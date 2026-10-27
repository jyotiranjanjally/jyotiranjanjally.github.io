/* Deterministic, dependency-free educational models. Exported for numerical tests. */
const HubMath = {
  soft: (z, threshold) => Math.sign(z) * Math.max(Math.abs(z) - threshold, 0),
  ridge: (z, lambda) => z / (1 + lambda),
  elastic: (z, lambda, rho) => Math.sign(z) * Math.max(Math.abs(z) - lambda * rho, 0) / (1 + lambda * (1-rho)),
  solve(matrix, target) {
    const a = matrix.map((r,i) => [...r,target[i]]), n = a.length;
    for (let k=0;k<n;k++) {
      let pivot=k;
      for(let i=k+1;i<n;i++) if(Math.abs(a[i][k])>Math.abs(a[pivot][k])) pivot=i;
      [a[k],a[pivot]]=[a[pivot],a[k]];
      if(Math.abs(a[k][k])<1e-13) throw new Error('Singular matrix');
      const d=a[k][k]; for(let j=k;j<=n;j++) a[k][j]/=d;
      for(let i=0;i<n;i++) if(i!==k) {const f=a[i][k]; for(let j=k;j<=n;j++) a[i][j]-=f*a[k][j];}
    }
    return a.map(r=>r[n]);
  },
  polynomial(xs,ys,degree) {
    const rows=xs.map(x=>Array.from({length:degree+1},(_,j)=>x**j));
    const gram=Array.from({length:degree+1},(_,j)=>Array.from({length:degree+1},(_,k)=>rows.reduce((s,r)=>s+r[j]*r[k],0)));
    const target=Array.from({length:degree+1},(_,j)=>rows.reduce((s,r,i)=>s+r[j]*ys[i],0));
    return this.solve(gram,target);
  },
  metrics(y,p) {
    const n=y.length, mean=y.reduce((s,v)=>s+v,0)/n;
    const mse=y.reduce((s,v,i)=>s+(v-p[i])**2,0)/n;
    const mae=y.reduce((s,v,i)=>s+Math.abs(v-p[i]),0)/n;
    const sst=y.reduce((s,v)=>s+(v-mean)**2,0);
    return {mae,mse,rmse:Math.sqrt(mse),r2:sst ? 1-n*mse/sst : NaN};
  }
};
if (typeof module !== 'undefined') module.exports=HubMath;
if (typeof document !== 'undefined') document.querySelectorAll('[data-chart]').forEach((lab,labIndex)=>{
  const kind=lab.dataset.chart, controls=lab.querySelector('.lab-controls'), svg=lab.querySelector('svg');
  const values={};
  function slider(key,label,min,max,step,value) {
    values[key]=value;
    const el=document.createElement('label');
    el.innerHTML=`<span>${label}: <output>${value}</output></span><input type="range" min="${min}" max="${max}" step="${step}" value="${value}" aria-label="${label}">`;
    el.querySelector('input').addEventListener('input',e=>{values[key]=Number(e.target.value);el.querySelector('output').textContent=e.target.value;draw();});
    controls.append(el);
  }
  if(kind==='line') slider('slope','Slope',0,4,.1,2);
  if(kind==='polynomial') {slider('degree','Polynomial degree',1,6,1,2);slider('noise','Noise amplitude',0,1,.05,.3);}
  if(['ridge','lasso','elastic','compare'].includes(kind)) slider('lambda','Penalty λ',0,4,.05,.5);
  if(kind==='elastic') slider('rho','L1 fraction ρ',0,1,.05,.5);
  if(kind==='metrics') slider('error','Third prediction error',0,10,.5,2);
  if(kind==='descent') slider('rate','Learning rate η',.05,2.2,.05,.3);
  if(kind==='residual') slider('curve','Unmodelled curvature',0,2,.1,1);
  const fmt=v=>Number.isFinite(v)?v.toFixed(3):'undefined';
  function draw(){
    let points=[],curves=[],summary='',xLabel='x',yLabel='y',xmin=0,xmax=4,ymin=0,ymax=10;
    if(kind==='line') {
      points=[[0,1],[1,2.7],[2,5.4],[3,6.8],[4,9.1]];
      curves=[points.map(([x])=>[x,1+values.slope*x])];
      summary=`Prediction = 1 + ${values.slope.toFixed(1)}x. Training MSE = ${fmt(HubMath.metrics(points.map(p=>p[1]),curves[0].map(p=>p[1])).mse)}. Intercept stays fixed; this control explores loss, not a refitted intercept.`;
      ymax=18;
    } else if(kind==='polynomial') {
      xmin=-1;xmax=1;ymin=-1;ymax=4;
      const xs=Array.from({length:15},(_,i)=>-1+2*i/14), ys=xs.map((x,i)=>.5+2*x*x+values.noise*Math.sin(i*2.4));
      const b=HubMath.polynomial(xs,ys,values.degree);
      const predict=x=>b.reduce((s,v,j)=>s+v*x**j,0);
      points=xs.map((x,i)=>[x,ys[i]]);curves=[Array.from({length:101},(_,i)=>{const x=-1+i/50;return[x,predict(x)];})];
      summary=`Degree ${values.degree}; ${b.length} coefficients. Training MSE ${fmt(HubMath.metrics(ys,xs.map(predict)).mse)}. Lower training error alone does not establish better generalization. Solid curve: fitted polynomial; dots: training samples.`;
    } else if(['ridge','lasso','elastic','compare'].includes(kind)) {
      xmax=4;ymin=-2;ymax=3;xLabel='penalty λ';yLabel='coefficient';
      const z=[2.5,-1.5,.4],lambda=values.lambda,rho=values.rho??.5;
      const shrink=kind==='ridge'?HubMath.ridge:kind==='lasso'?HubMath.soft:(v,l)=>HubMath.elastic(v,l,rho);
      if(kind==='compare') {
        curves=[HubMath.ridge,HubMath.soft,(v,l)=>HubMath.elastic(v,l,.5)].map(fn=>Array.from({length:81},(_,i)=>[i/20,fn(2.5,i/20)]));
        points=[HubMath.ridge(2.5,lambda),HubMath.soft(2.5,lambda),HubMath.elastic(2.5,lambda,.5)].map(v=>[lambda,v]);
        summary=`For OLS coefficient 2.5: ridge ${fmt(points[0][1])}, lasso ${fmt(points[1][1])}, elastic net ${fmt(points[2][1])}. Curves in order: solid ridge, dashed lasso, dotted elastic net (ρ = 0.5). Ridge uses MSE + λ L2; lasso and elastic net use half-MSE conventions from the text, so λ is not an equivalent penalty across these objectives.`;
      } else {
        curves=z.map(v=>Array.from({length:81},(_,i)=>[i/20,shrink(v,i/20)]));
        points=z.map(v=>[lambda,shrink(v,lambda)]);
        summary=`Centered orthonormal features XᵀX/n = I; OLS coefficients [2.5, −1.5, 0.4]. At λ = ${lambda}: [${points.map(p=>fmt(p[1])).join(', ')}]. Intercept is excluded. Solid, dashed, and dotted paths correspond to these three coefficients.`;
      }
    } else if(kind==='metrics') {
      const y=[1,2,3],p=[1,2,3+values.error],m=HubMath.metrics(y,p);
      xmin=1;xmax=3;ymax=14;xLabel='observation';yLabel='target / prediction';points=y.map((v,i)=>[i+1,v]);curves=[p.map((v,i)=>[i+1,v])];
      summary=`Actual [1, 2, 3]; predicted [1, 2, ${p[2]}]. MAE ${fmt(m.mae)}, MSE ${fmt(m.mse)}, RMSE ${fmt(m.rmse)}, R² ${fmt(m.r2)}. Dots are targets; the line connects predictions only to aid comparison.`;
    } else if(kind==='descent') {
      xmin=0;xmax=20;yLabel='half-MSE loss';xLabel='iteration';let b=0;const trace=[];
      for(let i=0;i<=20;i++){trace.push([i,.5*(b-2)**2]);b-=values.rate*(b-2);}
      ymax=Math.max(2.2,...trace.map(p=>p[1]))*1.05;curves=[trace];
      summary=`J(b) = ½(b − 2)², b₀ = 0. After 20 updates, loss ${fmt(trace[20][1])}. For this unit-curvature problem convergence requires 0 < η < 2. η = 2 oscillates; η > 2 diverges. The vertical axis rescales to show the loss.`;
    } else {
      xmin=-2;xmax=2;ymin=-2;ymax=5;xLabel='fitted value (centered)';yLabel='residual';
      const xs=Array.from({length:31},(_,i)=>-2+4*i/30),meanSquare=xs.reduce((s,x)=>s+x*x,0)/xs.length;
      points=xs.map((x,i)=>[x,values.curve*(x*x-meanSquare)+.18*Math.sin(i*2)]);
      curves=[[[-2,0],[2,0]]];
      summary=`Synthetic residual pattern with curvature strength ${values.curve}. Horizontal line: zero residual. A U-shape suggests missing nonlinear structure; a flat pattern is not proof that every modelling assumption holds.`;
    }
    const X=x=>60+(x-xmin)/(xmax-xmin)*610,Y=y=>285-(y-ymin)/(ymax-ymin)*255;
    let markup=`<title id="chart-title-${labIndex}">${kind} regression experiment</title><desc>${summary.replaceAll('&','&amp;').replaceAll('<','&lt;')}</desc><defs><clipPath id="clip-${labIndex}"><rect x="60" y="30" width="610" height="255"/></clipPath></defs>`;
    for(let i=0;i<=4;i++){const x=xmin+(xmax-xmin)*i/4,y=ymin+(ymax-ymin)*i/4;markup+=`<line class="axis" x1="60" x2="670" y1="${Y(y)}" y2="${Y(y)}"/><text x="52" y="${Y(y)+4}" text-anchor="end">${y.toFixed(ymax>100?0:1)}</text><text x="${X(x)}" y="305" text-anchor="middle">${x.toFixed(1)}</text>`;}
    markup+=`<text x="365" y="332" text-anchor="middle">${xLabel}</text><text x="16" y="155" transform="rotate(-90 16 155)" text-anchor="middle">${yLabel}</text><g clip-path="url(#clip-${labIndex})">`;
    curves.forEach((curve,i)=>{markup+=`<path class="curve" stroke-dasharray="${['none','7 4','2 4'][i%3]}" d="${curve.map(([x,y],j)=>`${j?'L':'M'}${X(x).toFixed(2)},${Y(y).toFixed(2)}`).join(' ')}"/>`;});
    points.forEach(([x,y])=>{markup+=`<circle class="point" cx="${X(x)}" cy="${Y(y)}" r="4"/>`;});
    svg.innerHTML=markup+'</g>';svg.setAttribute('aria-labelledby',`chart-title-${labIndex}`);lab.querySelector('.chart-summary').textContent=summary;
  }
  draw();
});
