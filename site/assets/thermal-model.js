/* BJ-STU-002 rev C: steady-state, mixed bay air. SI units internally. */
(function (root) {
  'use strict';
  const rho = 101325 / (287.05 * 303.15), cp = 1007;
  const holes = 37 * Math.PI * 1.75 ** 2, slots = 667.3;
  const ua = 0.052565 / (1 / 5 + 1 / (5 + 4 * .9 * 5.670e-8 * 308.15 ** 3));
  function solve({ambient = 25, watts = 15, grille = 'slots', fan = true, sun = false} = {}) {
    if (!Number.isFinite(ambient) || !Number.isFinite(watts) || watts < 0 || !['holes','slots'].includes(grille)) throw new RangeError('Invalid thermal inputs');
    const area = grille === 'holes' ? holes : slots, heat = watts + (sun ? 12 : 0);
    let flow, rise;
    if (fan) {
      const resistance = a => rho / 2 / (.61 * a * 1e-6) ** 2;
      const k = resistance(area) + resistance(holes + 970 + 1257.6);
      let lo = 0, hi = 8.9 / 3600;
      for (let i=0;i<70;i++) { const q=(lo+hi)/2; if (1.95*9.80665*(1-q/(8.9/3600))**2 > k*q*q) lo=q; else hi=q; }
      flow = (lo+hi)/2; rise = heat / (rho*cp*flow);
    } else {
      const effective = 1/Math.sqrt(1/(970+1257.6)**2 + 1/(holes+area)**2)*1e-6;
      const q = d => .61*effective*Math.sqrt(2*9.80665*.02*d/303.15);
      let lo=0, hi=1000;
      for(let i=0;i<80;i++){ const d=(lo+hi)/2; if((rho*cp*q(d)+(sun?0:ua))*d < heat) lo=d; else hi=d; }
      rise=heat===0?0:(lo+hi)/2; flow=q(rise);
    }
    return {temperature:ambient+rise, rise, airflow:flow*3600, heat, margin:60-ambient-rise};
  }
  const model={solve};
  if (typeof module === 'object' && module.exports) module.exports=model;
  else root.BlackjackThermal=model;
})(globalThis);
