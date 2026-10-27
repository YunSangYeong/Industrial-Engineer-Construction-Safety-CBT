import { describe, it, expect } from 'vitest';
import { BASE_BANK, SUBJECTS, PROFILE, validateQuestion, fingerprint } from '../src/model';
import { execFileSync } from 'node:child_process';
// Independent JS equations. The generator uses Decimal; no generation function is imported.
const equations: Record<string, (v:number[])=>number> = {
 frequency: ([n,h])=>n/(h/1e6), severity: ([d,h])=>d/(h/1e3), incidence: ([n,p])=>100*n/p,
 averageLoss: ([d,n])=>d/n, reduction: ([before,after])=>100*(1-after/before), trainingCoverage: ([n,total])=>100*n/total,
 moment: ([f,d])=>d*f, contactPressure: ([f,a])=>f/(a*1000), illuminance: ([flux,area])=>flux/area,
 cycleRate: ([seconds])=>60*(60/seconds), seriesReliability: ([a,b])=>100*a*b,
 parallelReliability: ([a,b])=>100*(a+b-a*b), compressiveStrength: ([kn,mm2])=>kn/(mm2/1000),
 density: ([m,volume])=>m/volume, waterCement: ([water,cement])=>water/(cement/100),
 slabVolume: ([l,w,t])=>t*w*l, strain: ([change,length])=>change/(length/100),
 overturning: ([resist,overturn])=>resist/overturn, groundPressure: ([force,area])=>force/area,
 kineticEnergy: ([mass,speed])=>mass*(speed**2)/2, fallEnergy: ([mass,height])=>9.8*height*mass,
 slingTension: ([weight,cosine])=>(weight/2)/cosine, slopeGrade: ([rise,run])=>100*rise/run,
};
const units: Record<string,string> = {frequency:'건/백만시간',severity:'일/천시간',incidence:'%',averageLoss:'일/건',reduction:'%',trainingCoverage:'%',moment:'N·m',contactPressure:'kPa',illuminance:'lx',cycleRate:'회/시간',seriesReliability:'%',parallelReliability:'%',compressiveStrength:'MPa',density:'kg/m³',waterCement:'%',slabVolume:'m³',strain:'%',overturning:'배',groundPressure:'kPa',kineticEnergy:'J',fallEnergy:'J',slingTension:'kN',slopeGrade:'%'};
describe('문제은행 인수',()=>{
 it('중복 제거 후 1000개: 개념 80 + 숫자 변형 920 / 23유형, 기출·복원 0',()=>{
  expect(BASE_BANK).toHaveLength(1000);
  expect(new Set(BASE_BANK.map(q=>q.id)).size).toBe(1000);
  expect(new Set(BASE_BANK.map(fingerprint)).size).toBe(1000);
  expect(BASE_BANK.filter(q=>!q.family)).toHaveLength(80);
  expect(BASE_BANK.filter(q=>q.family)).toHaveLength(920);
  expect(new Set(BASE_BANK.flatMap(q=>q.family?[q.family]:[])).size).toBe(23);
  expect(SUBJECTS.map(s=>BASE_BANK.filter(q=>q.subject===s).length)).toEqual([260,260,220,260]);
  expect(PROFILE.questionCount).toBe(SUBJECTS.length*PROFILE.questionsPerSubject);
  expect(PROFILE.rulesVerificationStatus).toBe('pending-official-access');
 });
 it('생성 원고와 등록 JSON이 byte 단위로 재현된다',()=>{
  expect(execFileSync('python3',['scripts/generate_bank.py','--check'],{encoding:'utf8'})).toContain('"registered": 1000');
 });
 it('모든 문항의 필수 필드·출처 한계·보기·확인되지 않은 회차를 확인한다',()=>{
  for(const q of BASE_BANK){
   expect(()=>validateQuestion(q)).not.toThrow();
   expect(q.type).toBe('original');expect(q.year).toBeNull();expect(q.session).toBeNull();
   expect(q.verificationStatus).toBe('reviewed');expect(q.reviewNote).toContain('외부 전문가 검수');
   expect(q.rights).toContain('CC BY 4.0');expect(q.explanation.length).toBeGreaterThan(30);
  }
 });
 it('유형별 40개 입력은 서로 다르며 신뢰도·인원·단위의 가정을 만족한다',()=>{
  for(const family of Object.keys(equations)){
   const list=BASE_BANK.filter(q=>q.family===family);expect(list).toHaveLength(40);
   expect(new Set(list.map(q=>JSON.stringify(q.calculation!.values))).size).toBe(40);
   if(family.endsWith('Reliability'))list.forEach(q=>q.calculation!.values.forEach(p=>{expect(p).toBeGreaterThan(0);expect(p).toBeLessThan(1);}));
   if(family==='trainingCoverage')list.forEach(q=>expect(q.calculation!.values[0]).toBeLessThanOrEqual(q.calculation!.values[1]));
  }
 });
 for(const q of BASE_BANK.filter(q=>q.calculation)) it(`독립 재계산·단위·보기: ${q.id}`,()=>{
  const c=q.calculation!;expect(equations[c.kind]).toBeDefined();expect(c.unit).toBe(units[c.kind]);
  const n=equations[c.kind](c.values);const rounded=Math.round((n+Number.EPSILON*Math.max(1,n))*100)/100;
  expect(Number.isFinite(n)).toBe(true);expect(rounded).toBeCloseTo(c.result,8);
  const parsed=q.choices.map(choice=>{const m=choice.match(/^([\d.]+) (.+)$/)!;expect(m).not.toBeNull();expect(m[2]).toBe(units[c.kind]);return Number(m[1]);});
  expect(new Set(parsed).size).toBe(4);expect(parsed[q.answer-1]).toBe(c.result);
  expect(parsed.filter(x=>Math.abs(x-rounded)<1e-8)).toHaveLength(1);
  for(const v of c.values)expect(q.question).toContain(String(v));
  expect(q.explanation).toContain('법정 허용값');
 });
});
