"""Deterministic, original learning questions, not transcribed examination papers.
Decimal half-up generation; independent JS equations are in tests/bank.test.ts.
No statutory thresholds are asserted by these mathematical exercises.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json, hashlib, sys
ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT/'src/qualification.json').read_text())
SOURCE = 'https://github.com/YunSangYeong/Industrial-Engineer-Construction-Safety-CBT/blob/main/docs/question-review.md'
def decimal(x): return Decimal(str(x))
def rounded(x): return decimal(x).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
def fmt(x): return format(decimal(x).normalize(), 'f')
def base(id, subject, topic, question, choices, answer, explanation):
 return dict(id=id,subject=PROFILE['subjects'][subject],topic=topic,question=question,choices=choices,answer=answer,explanation=explanation,difficulty='중',year=None,session=None,type='original',sourceUrl=SOURCE,verificationStatus='reviewed',reviewNote='AI 자체 작성. 내부 문장·보기 검토. 계산형은 별도 JS 재계산 검사. 외부 전문가 검수 및 공식 출제기준 대조 미완료. 링크는 작성·검수 기록이며 외부 정답 증빙이 아님.',version='main',rights='자체 제작 · CC BY 4.0 · 건설안전산업기사 CBT 기여자 표시 및 변경사항 명시. 제3자 기출 전재 없음.')
questions=[]
for index,line in enumerate((ROOT/'scripts/concepts.txt').read_text().splitlines()):
 if not line or line.startswith('#'): continue
 subject,topic,question,correct,a,b,c,explanation=line.split('|')
 choices=[correct,a,b,c]; rotation=len(questions)%4; choices=choices[rotation:]+choices[:rotation]
 questions.append(base(f'CS-C-{len(questions)+1:03}',int(subject),topic,question,choices,choices.index(correct)+1,explanation))
# Each family is a distinct mathematical learning task. Forty input conditions
# are disclosed as variants, never as forty independent concepts or past papers.
def family(subject,kind,topic,unit,values,question,equation,compute):
 for i in range(40):
  v=[decimal(x) for x in values(i)]
  result=rounded(compute(v))
  candidates=[result,rounded(result*decimal('.5')),rounded(result*decimal('1.5')),rounded(result*2)]
  assert len(set(candidates))==4 and result>0,(kind,i)
  choices=[fmt(x)+' '+unit for x in candidates]; rotation=(i+subject)%4
  choices=choices[rotation:]+choices[:rotation]
  stem=question([fmt(x) for x in v])+' 다른 조건은 주어진 가정과 같으며, 필요하면 소수 셋째 자리에서 반올림한다.'
  exp=equation([fmt(x) for x in v])+f' 계산값을 소수 둘째 자리까지 반올림하면 {fmt(result)} {unit}이다. 보기에 쓰인 다른 수는 해당 조건의 답이 아니다. 이는 주어진 수학적 가정의 연습이며 법정 허용값이나 실제 설계 승인을 뜻하지 않는다.'
  q=base(f'CS-N-{kind}-{i+1:02}',subject,topic,stem,choices,choices.index(fmt(result)+' '+unit)+1,exp)
  q.update(family=kind,calculation=dict(kind=kind,values=[float(x) for x in v],result=float(result),unit=unit,precision=2))
  questions.append(q)
family(0,'frequency','재해 도수율','건/백만시간',lambda i:[2+i,400000+10000*i],lambda v:f'한 기간의 재해 건수가 {v[0]}건, 총 근로시간이 {v[1]}시간이다. 도수율을 재해 건수÷총 근로시간×1,000,000으로 정의할 때 도수율은?',lambda v:f'도수율 = 재해 건수 / 총 근로시간 × 1,000,000 = {v[0]} / {v[1]} × 1,000,000. ',lambda v:v[0]*1000000/v[1])
family(0,'severity','재해 강도율','일/천시간',lambda i:[20+3*i,120000+5000*i],lambda v:f'근로손실일수 {v[0]}일, 총 근로시간 {v[1]}시간일 때 강도율을 손실일수÷총 근로시간×1,000으로 정의하면 얼마인가?',lambda v:f'강도율 = 손실일수 / 근로시간 × 1,000 = {v[0]} / {v[1]} × 1,000. ',lambda v:v[0]*1000/v[1])
family(0,'incidence','재해자 비율','%',lambda i:[1+i,400+10*i],lambda v:f'같은 기간 근로자 {v[1]}명 중 재해자 {v[0]}명이다. 재해자 비율을 재해자 수÷근로자 수×100으로 정의하면?',lambda v:f'비율 = {v[0]} / {v[1]} × 100. 분모와 분자는 같은 기간의 인원이다. ',lambda v:v[0]*100/v[1])
family(0,'averageLoss','평균 손실일수','일/건',lambda i:[120+11*i,3+i],lambda v:f'재해 {v[1]}건에 의한 총 손실일수가 {v[0]}일이다. 건당 평균 손실일수는?',lambda v:f'건당 평균 = 총 손실일수 / 재해 건수 = {v[0]} / {v[1]}. ',lambda v:v[0]/v[1])
family(0,'reduction','위험 지표 감소율','%',lambda i:[100+4*i,30+i],lambda v:f'동일한 정의의 위험 지표가 개선 전 {v[0]}, 개선 후 {v[1]}이다. 감소율을 (개선 전−개선 후)÷개선 전×100으로 정의하면?',lambda v:f'감소율 = ({v[0]} − {v[1]}) / {v[0]} × 100. 개선 전 값을 분모로 쓴다. ',lambda v:(v[0]-v[1])*100/v[0])
family(0,'trainingCoverage','교육 이수율','%',lambda i:[30+i,90+2*(i%7)],lambda v:f'교육 대상 {v[1]}명 중 {v[0]}명이 교육을 이수했다. 이수율은? 중복 인원은 없다.',lambda v:f'이수율 = 이수자 / 대상자 × 100 = {v[0]} / {v[1]} × 100. 이 지표만으로 교육 효과 전체를 입증하지는 않는다. ',lambda v:v[0]*100/v[1])
family(1,'moment','정적 힘의 모멘트','N·m',lambda i:[100+5*i,decimal('.2')+decimal('.01')*i],lambda v:f'힘 {v[0]} N이 회전축에서 수직거리 {v[1]} m인 위치에 작용한다. 힘과 지레팔이 직각일 때 모멘트의 크기는?',lambda v:f'모멘트 M = F × d = {v[0]} N × {v[1]} m. d는 축에서 힘 작용선까지의 수직거리다. ',lambda v:v[0]*v[1])
family(1,'contactPressure','접촉 압력','kPa',lambda i:[50+3*i,decimal('.01')+decimal('.001')*i],lambda v:f'접촉면 {v[1]} m²에 수직하중 {v[0]} N이 균일하게 작용한다. 평균 압력은 몇 kPa인가?',lambda v:f'p = F/A = {v[0]} / {v[1]} Pa. 1 kPa = 1,000 Pa이므로 다시 1,000으로 나눈다. ',lambda v:v[0]/v[1]/1000)
family(1,'illuminance','평균 조도','lx',lambda i:[1000+100*i,10+i],lambda v:f'작업면 {v[1]} m²에 실제 도달한 광속 합계가 {v[0]} lm이고 균일 분포한다고 가정한다. 평균 조도는?',lambda v:f'평균 조도 E = 도달 광속 / 면적 = {v[0]} lm / {v[1]} m². 1 lx = 1 lm/m²이며 추가 이용률을 곱하지 않는다. ',lambda v:v[0]/v[1])
family(1,'cycleRate','반복 작업 빈도','회/시간',lambda i:[20+i],lambda v:f'한 작업 주기가 {v[0]}초이며 휴식 없이 같은 주기가 반복된다는 계산 가정이다. 시간당 반복 횟수는?',lambda v:f'1시간 = 3,600초이므로 시간당 반복 = 3,600 / {v[0]}. 실제 작업 계획은 피로·휴식을 별도로 고려해야 한다. ',lambda v:decimal(3600)/v[0])
family(1,'seriesReliability','직렬 시스템 신뢰도','%',lambda i:[decimal('.8')+decimal('.003')*i,decimal('.85')+decimal('.002')*i],lambda v:f'독립인 두 구성요소의 임무 성공 확률이 각각 {v[0]}, {v[1]}이다. 둘 모두 성공해야 하는 직렬 시스템의 성공 확률을 백분율로 나타내면?',lambda v:f'독립인 두 성공 사건의 교집합 확률 R = R₁ × R₂ = {v[0]} × {v[1]}. 백분율로 바꾸기 위해 100을 곱한다. 공통원인 고장은 없다고 가정한다. ',lambda v:v[0]*v[1]*100)
family(1,'parallelReliability','병렬 시스템 신뢰도','%',lambda i:[decimal('.6')+decimal('.004')*i,decimal('.7')+decimal('.003')*i],lambda v:f'독립인 두 구성요소의 성공 확률이 {v[0]}, {v[1]}이다. 하나 이상 성공하면 작동하는 이상적 병렬 시스템의 성공 확률은 몇 %인가?',lambda v:f'둘 다 실패할 확률 = (1−{v[0]}) × (1−{v[1]}). 하나 이상 성공 = 1 − 이 값이며 백분율로 바꾸어 100을 곱한다. 전환 실패와 공통원인 고장은 없다고 가정한다. ',lambda v:(1-(1-v[0])*(1-v[1]))*100)
family(2,'compressiveStrength','압축강도 계산','MPa',lambda i:[200+10*i,10000+100*i],lambda v:f'압축 파괴하중이 {v[0]} kN, 공시체 가압 단면적이 {v[1]} mm²이다. 평균 압축강도는 몇 MPa인가?',lambda v:f'압축강도 = 하중 / 단면적. {v[0]} kN = {fmt(decimal(v[0])*1000)} N이고, 1 N/mm² = 1 MPa이다. 따라서 {v[0]} × 1,000 / {v[1]}. ',lambda v:v[0]*1000/v[1])
family(2,'density','재료 밀도','kg/m³',lambda i:[18+i,decimal('.008')+decimal('.0002')*i],lambda v:f'시료의 질량이 {v[0]} kg, 부피가 {v[1]} m³이다. 밀도는?',lambda v:f'밀도 ρ = 질량 / 부피 = {v[0]} kg / {v[1]} m³. 질량밀도이며 단위중량과 구별한다. ',lambda v:v[0]/v[1])
family(2,'waterCement','물시멘트비','%',lambda i:[150+i,300+3*i],lambda v:f'배합에 쓰인 물의 질량이 {v[0]} kg, 시멘트의 질량이 {v[1]} kg이다. 물시멘트비를 질량 백분율로 표시하면? 다른 결합재는 없다.',lambda v:f'물시멘트비 W/C = 물 질량 / 시멘트 질량 × 100 = {v[0]} / {v[1]} × 100. 부피비가 아니며 임의 가수를 허용하는 값도 아니다. ',lambda v:v[0]*100/v[1])
family(2,'slabVolume','슬래브 체적','m³',lambda i:[4+decimal('.1')*i,3+decimal('.05')*i,decimal('.15')+decimal('.001')*i],lambda v:f'직육면체 슬래브의 길이 {v[0]} m, 폭 {v[1]} m, 두께 {v[2]} m이다. 개구부와 할증이 없을 때 체적은?',lambda v:f'체적 V = 길이 × 폭 × 두께 = {v[0]} × {v[1]} × {v[2]} m³. 개구부 공제와 시공 할증은 조건에서 제외했다. ',lambda v:v[0]*v[1]*v[2])
family(2,'strain','축방향 변형률','%',lambda i:[1+decimal('.1')*i,1000+20*i],lambda v:f'시험편의 원래 길이는 {v[1]} mm, 인장에 의한 늘어난 길이는 {v[0]} mm이다. 공학적 변형률을 백분율로 나타내면?',lambda v:f'변형률 ε = 늘어난 길이 / 원래 길이 = {v[0]} / {v[1]}. 두 길이의 단위가 같으므로 무차원이며 백분율 표시를 위해 100을 곱한다. ',lambda v:v[0]/v[1]*100)
family(3,'overturning','전도 안정 계산','배',lambda i:[120+7*i,40+i],lambda v:f'검토 단면에서 저항 모멘트 {v[0]} kN·m, 전도 모멘트 {v[1]} kN·m이다. 안전율을 저항 모멘트÷전도 모멘트로 정의하면? 요구 안전율은 묻지 않는다.',lambda v:f'안전율 = 저항 모멘트 / 전도 모멘트 = {v[0]} / {v[1]}. 같은 단위가 소거된다. 실제 안정 판정에는 적용 기준의 요구값과 모든 하중 조합을 따로 검토해야 한다. ',lambda v:v[0]/v[1])
family(3,'groundPressure','장비 지지 압력','kPa',lambda i:[80+6*i,decimal('.8')+decimal('.02')*i],lambda v:f'받침판에 수직력 {v[0]} kN이 작용하고 지반 접촉면적이 {v[1]} m²이다. 전면에 균등 분포한다고 가정한 평균 접지 압력은?',lambda v:f'q = 수직력 / 면적 = {v[0]} kN / {v[1]} m². 1 kN/m² = 1 kPa이다. 편심과 지반 지지력 검토는 별도로 필요하다. ',lambda v:v[0]/v[1])
family(3,'kineticEnergy','이동 물체 운동에너지','J',lambda i:[100+10*i,decimal('1')+decimal('.05')*i],lambda v:f'질량 {v[0]} kg인 운반 물체가 속력 {v[1]} m/s로 병진 운동한다. 회전 운동을 제외한 운동에너지는?',lambda v:f'운동에너지 E = ½mv² = 0.5 × {v[0]} × ({v[1]})² J. 속력의 제곱에 비례하며 실제 충돌력은 정지 거리 등 추가 조건이 필요하다. ',lambda v:v[0]*v[1]*v[1]/2)
family(3,'fallEnergy','낙하 위치에너지','J',lambda i:[2+i,decimal('1')+decimal('.1')*i],lambda v:f'질량 {v[0]} kg인 물체가 기준면 위 {v[1]} m 높이에 있다. 중력가속도 9.8 m/s²일 때 기준면에 대한 위치에너지는? 공기저항은 고려하지 않는다.',lambda v:f'위치에너지 E = mgh = {v[0]} × 9.8 × {v[1]} J. 위치에너지를 묻는 것이며 충돌 시 최대 힘이나 보호구의 허용값을 뜻하지 않는다. ',lambda v:v[0]*decimal('9.8')*v[1])
family(3,'slingTension','대칭 두 줄 줄걸이','kN',lambda i:[10+i,decimal('.6')+decimal('.005')*i],lambda v:f'하중 {v[0]} kN을 동일한 두 줄로 대칭 정지 지지한다. 각 줄이 수직선과 이루는 각 θ의 cosθ가 {v[1]}일 때 한 줄의 장력은? 자중·동하중·불균등은 무시한다.',lambda v:f'수직 힘 평형 2Tcosθ = W. 따라서 T = W/(2cosθ) = {v[0]}/(2×{v[1]}) kN. 각도는 수평선이 아니라 수직선 기준이다. 실제 용구 선정에는 허용하중과 추가 조건 검토가 필요하다. ',lambda v:v[0]/(2*v[1]))
family(3,'slopeGrade','경사 백분율','%',lambda i:[decimal('.2')+decimal('.02')*i,4+decimal('.1')*i],lambda v:f'통로의 높이차가 {v[0]} m, 수평거리가 {v[1]} m이다. 경사 백분율을 높이차÷수평거리×100으로 정의하면?',lambda v:f'경사 백분율 = {v[0]}/{v[1]} × 100. 수평거리를 분모로 쓰며 경사면 길이나 각도(도)와 혼동하지 않는다. 이 값만으로 법적 적합성을 판정하지 않는다. ',lambda v:v[0]/v[1]*100)
assert len(questions)==1000,len(questions)
assert len({q['id'] for q in questions})==1000
fingerprints=[''.join((q['question']+'|'+ '|'.join(sorted(q['choices']))).split()).lower() for q in questions]
assert len(set(fingerprints))==1000
text=json.dumps(questions,ensure_ascii=False,indent=2)+'\n'
path=ROOT/'src/data/questions.json'
if '--check' in sys.argv:
 assert path.read_text()==text,'Generated bank differs; regenerate explicitly.'
else:
 path.write_text(text)
 template=dict(questions[0],id='LOCAL-EXAMPLE-001',verificationStatus='pending',reviewNote='예제. 출처·권한·정답 확인 후 근거를 기록하세요.')
 (ROOT/'public/templates/questions.json').write_text(json.dumps([template],ensure_ascii=False,indent=2)+'\n')
 import csv
 with (ROOT/'public/templates/questions.csv').open('w',newline='') as f:
  row={k:v for k,v in template.items() if k!='choices'}
  for i,c in enumerate(template['choices'],1):row[f'choice{i}']=c
  writer=csv.DictWriter(f,fieldnames=list(row),lineterminator="\n");writer.writeheader();writer.writerow(row)
print(json.dumps({'registered':len(questions),'concept':80,'numericVariants':920,'families':23,'sha256':hashlib.sha256(text.encode()).hexdigest(),'subjects':{s:sum(q['subject']==s for q in questions) for s in PROFILE['subjects']}},ensure_ascii=False))
