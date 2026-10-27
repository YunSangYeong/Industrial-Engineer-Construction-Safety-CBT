import {test,expect,type Page} from '@playwright/test';
async function open(page:Page){await page.getByRole('button',{name:'메뉴 열기',exact:true}).click();await expect(page.locator('.sidebar')).toHaveClass(/open/);await page.waitForTimeout(250);}
async function assertBottom(page:Page){
 expect(await page.locator('.sidebar').evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
 await expect(page.getByRole('button',{name:'학습 기록 백업',exact:true})).toBeInViewport();
 await expect(page.getByRole('button',{name:'데이터 초기화',exact:true})).toBeInViewport();
 const download=page.waitForEvent('download');await page.getByRole('button',{name:'학습 기록 백업',exact:true}).click();expect((await download).suggestedFilename()).toContain('construction-safety');
 await page.getByRole('button',{name:'데이터 초기화',exact:true}).click();await expect(page.getByRole('dialog')).toBeVisible();await page.getByRole('button',{name:'돌아가기',exact:true}).click();
}
async function assertTop(page:Page){
 await expect.poll(()=>page.locator('.sidebar').evaluate(el=>el.scrollTop)).toBe(0);
 const dashboard=page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true});
 await expect(dashboard).toBeInViewport();await dashboard.click();await expect(page.getByRole('heading',{name:'건설안전산업기사 필기 CBT',exact:true})).toBeVisible();await expect(page.locator('.sidebar')).not.toHaveClass(/open/);
}
for(const size of [{width:390,height:480},{width:740,height:360}]){
 test(`메뉴 실제 휠 상하 이동·하단 백업/초기화·상단 대시보드 ${size.width}x${size.height}`,async({page})=>{
  await page.setViewportSize(size);await page.goto('');await open(page);
  const menu=page.locator('.sidebar');expect(await menu.evaluate(el=>el.scrollHeight>el.clientHeight)).toBe(true);
  await page.mouse.move(120,Math.min(size.height-80,300));await page.mouse.wheel(0,5000);
  await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);await page.waitForTimeout(150);await assertBottom(page);
  await page.mouse.move(120,150);await page.mouse.wheel(0,-5000);await assertTop(page);
 });
 test(`메뉴 실제 터치 스와이프 상하 접근 ${size.width}x${size.height}`,async({page,context,isMobile})=>{
  test.skip(!isMobile,'터치 에뮬레이션 프로젝트에서만 수행');await page.setViewportSize(size);await page.goto('');await open(page);
  const session=await context.newCDPSession(page);
  async function swipe(from:number,to:number){
   await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:120,y:from}]});
   for(let step=1;step<=12;step++){await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:120,y:from+(to-from)*step/12}]});await page.waitForTimeout(18);}
   await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(250);
  }
  for(let i=0;i<5;i++)await swipe(size.height-60,70);
  await assertBottom(page);
  for(let i=0;i<5;i++)await swipe(80,size.height-60);
  await assertTop(page);await session.detach();
 });
}
test('글자 확대 메뉴와 뷰포트 높이 변경에서도 실제 휠 접근',async({page})=>{
 await page.setViewportSize({width:390,height:480});await page.goto('');
 await page.addStyleTag({content:'.sidebar nav button { font-size: 19px; min-height: 65px; } .sidebar .text-button { font-size: 18px; }'});
 await open(page);await page.setViewportSize({width:390,height:400});await page.mouse.move(120,220);await page.mouse.wheel(0,5000);await page.waitForTimeout(250);await assertBottom(page);
 await page.mouse.move(120,100);await page.mouse.wheel(0,-5000);await assertTop(page);
});
