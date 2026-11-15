const test = require('node:test');
const assert = require('node:assert/strict');
const {solve}=require('../assets/thermal-model.js');
test('reproduces all twelve published rev C ambient thresholds',()=>{
 for(const [fan,grille,expected] of [[false,'holes',[11,-74,-15,-105]],[true,'holes',[44,32,34,22]],[true,'slots',[49,40,42,33]]]){
  const actual=[15,25].flatMap(watts=>[false,true].map(sun=>Math.round(60-solve({fan,grille,watts,sun,ambient:0}).rise)));
  assert.deepEqual(actual,expected);
 }
});
test('all selectable combinations respond physically throughout the slider range',()=>{
 for(const fan of [false,true]) for(const grille of ['holes','slots']) for(const sun of [false,true]){
  let previous=-1;
  for(let watts=0;watts<=40;watts+=.5){
   const r=solve({fan,grille,sun,watts,ambient:-10});
   assert.ok(Number.isFinite(r.temperature)&&r.rise>=0&&r.rise>=previous);
   assert.ok(Math.abs(solve({fan,grille,sun,watts,ambient:50}).temperature-r.temperature-60)<1e-9);
   previous=r.rise;
  }
 }
});
test('larger grille lowers rise; sun adds heat; zero heat gives no rise',()=>{
 for(const fan of [false,true]){
  assert.ok(solve({fan,grille:'slots'}).rise<solve({fan,grille:'holes'}).rise);
  assert.ok(solve({fan,sun:true}).rise>solve({fan,sun:false}).rise);
  assert.equal(solve({fan,watts:0}).rise,0);
 }
 assert.ok(Math.abs(solve().airflow-4.249212489858884)<1e-10);
 assert.throws(()=>solve({watts:-1}),RangeError);
 assert.throws(()=>solve({ambient:NaN}),RangeError);
 assert.throws(()=>solve({grille:'unknown'}),RangeError);
});
