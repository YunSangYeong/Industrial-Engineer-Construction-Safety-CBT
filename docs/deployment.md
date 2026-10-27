# 배포 진행 기록

## 대상과 최신 정책

- 대상은 `YunSangYeong/Industrial-Engineer-Construction-Safety-CBT`만이다. 기존 전기기능사 등 다른 프로젝트는 수정·푸시·재배포하지 않았다.
- 표준 스킬은 원본 최신 main `76b990b8720adfa85c22a0a8f699b17094aa357b`의 v1.4.0을 폴더 전체 복사했다. 앱 소스는 스킬 지정 기준 커밋 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`에서 재사용했다.
- 준비한 `.github/workflows/pages.yml`은 main push → validate(설치·단위·빌드·PC/모바일) → Pages 아티팩트 → deploy이다. PR은 validate만 한다. 수동 실행은 자동 실행과 중복 사용하지 않는다.
- Pages base는 `/Industrial-Engineer-Construction-Safety-CBT/`이다.

## 첫 차단과 중단

실행한 최초 배포 사전 API 확인:

```text
gh api repos/YunSangYeong/Industrial-Engineer-Construction-Safety-CBT --jq '{full_name,default_branch,private,permissions}'
Get "https://api.github.com/repos/YunSangYeong/Industrial-Engineer-Construction-Safety-CBT": Forbidden
exit code: 1
```

환경의 `GH_TOKEN` 이름이 설정되어 있는 것과 Git HTTPS 읽기가 가능한 것은 확인했다. 값은 읽거나 기록하지 않았다. 이 사실만으로 GitHub API 권한·네트워크 통과나 Pages 관리 권한이 보장되지는 않는다. 이 오류만으로 토큰 불량·만료·관리자 권한 부족·Pages 미설정을 단정하지 않는다.

**이 첫 차단에서 배포 진행을 중단했다.** API 재호출, 다른 인증·네트워크 경로, main push, workflow dispatch, workflow 재실행은 하지 않았다. 이 작업의 Actions 검증·Pages 파이프라인은 시작하지 않았다. Pages 설정과 기존 게시 여부는 미확인이다. 공개 URL에도 배포 성공 확인을 위해 접근하지 않았다.

코드는 자동 push 트리거가 없는 `feat/construction-safety-cbt` 브랜치에 보존한다. 이 브랜치 push는 배포 시도가 아니며 PR도 자동 작성하지 않는다. 원격 보존 성공 여부와 커밋은 작업 완료 보고에서 별도로 확인한다. main은 초기 커밋을 유지한다. 실패 후 main에 추가 push하여 자동 배포를 우회 실행하지 않는다.

## 사용자에게 넘기는 최소 확인

현재는 Pages 설정까지 확인하지 못했다. GitHub 저장소의 **Settings → Pages**를 열어 Source가 **GitHub Actions**인지 확인하는 것이 다음 한 단계다. 기존 설정을 확인하지 않고 이를 변경 완료했다고 말하지 않는다. 이후 반영·실행은 사용자 직접 마무리이며 에이전트는 새로운 명시적 시도 요청 없이는 재개하지 않는다.

예상 기본 주소(배포·공개 확인 완료 주소가 아님):
https://YunSangYeong.github.io/Industrial-Engineer-Construction-Safety-CBT/
