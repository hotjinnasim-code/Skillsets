# Candidate U: 최초 생성의 일반화 가능한 설계 원인

이 문서는 동결한 U 런타임 12개 파일과 R18 **INITIAL** 세 평가자의 원시 관찰·호환 JSON을 읽은 구현 검토다. 이미지 재열람·생성·점수 부여·원시 기록 변경은 하지 않았다. SELECTED 자료는 읽지 않았다. 아래 판단은 기록된 시각 관찰의 공통 원인에 대한 가설이며 새 평가자나 통과 인증이 아니다.

평가 절차 자체는 NA다. INITIAL summary의 `procedure_gate`는 NA이며, 105개의 정수 점수는 모두 보존돼 있지만 최종 집계는 0 PASS / 0 FAIL / 5 NA다. compact binding audit은 세 프로필 모두 trace의 failed turn/error를 기록한다. editorial trace에는 WebSocket 재연결, HTTPS 전환, 응답 디코딩 오류가 실제로 남아 있다. 이를 디자인 실패나 낮은 점수의 근거로 해석하지 않는다. 세 평가자가 남긴 다양성 원점수는 모두 4이며, 이 값도 유효한 전체 PASS를 뜻하지 않는다.

- [INITIAL summary:578](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/summary.json:578>)
- [INITIAL binding audit:10](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/compact-binding-audit.json:10>)
- [editorial transport trace:20](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/editorial/trace.jsonl:20>)

## 공통 신호와 기존 U 지침

본문은 원시 기록상 대체로 충분한 크기와 연속된 문단으로 읽힌다. 공통 결함을 다시 ‘본문을 크게’라는 문제로 축소하면 실제 원인을 놓친다. M3와 M4는 세 평가자 모두 정보 계층 3이다. M2는 craft만 정보 계층 3이고 editorial/portfolio는 4지만, 세 기록 모두 제목·초대 문장·의미 문장 등이 여러 진입점으로 경쟁하는 잔여 문제를 적었다. 강한 첫 앵커를 다양화하는 것과 한 장 내부의 여러 카피를 동시에 헤드라인으로 만드는 것은 다른 결정이다.

U는 이미 첫 앵커, 문단 시작·끝, 다음 행동 정보, 보조 언어·의미 문장·행사 이름의 역할을 설계하라고 명시한다. 부족한 것은 이 개념의 부재가 아니라 **큰 제목 외 카피의 실제 강조가 맡은 역할을 유지하는 제작 명세**, 그리고 **정보 구역 사이의 실제 이동 단서**다. 아래 세 제안은 기존 긍정적인 제작 명세를 더 구체화하는 방식이며 체크리스트·새 승인 단계·추가 생성 상한을 요구하지 않는다.

- [U SKILL:30](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/snapshots/candidate-u/SKILL.md:30>), [U production brief:19](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/snapshots/candidate-u/references/production-brief.md:19>), [U parallel production:11](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/snapshots/candidate-u/references/parallel-production.md:11>)

## 제안할 최초 생성 지침: 최대 세 가지

### 1. 첫 역할과 보조 역할을 실제 광학 강약으로 구현한다

제목·보조 언어·의미 문장·초대 문장·날짜가 실제로 있는 경우, 선택한 첫 역할에 이어 **어느 문구가 그 역할을 보충하고 어느 문구가 다음 행동을 맡는지**를 정한다. 제작 명세에는 단순히 ‘상단/하단/크게’라고 배정하지 않고, 실제 문구 사이에서 크기·굵기·색 대비·고립된 여백 중 무엇으로 우선순위를 구현할지 짧게 연결한다. 보조 문구를 별도 모서리의 또 다른 헤드라인으로 강조하는 것은 현재 목적에 필요한 경우에 선택한다. 여러 진입점이 필요한 구성도 각 진입점이 어느 정보로 이어지는지 정한다. 한 장의 유용한 첫 역할은 방향마다 달라도 되며 고정 제목 우선, 한 개 헤드라인, 작은 보조 문구의 의무로 바꾸지 않는다.

이 제안은 M3/M4의 반복된 경쟁 앵커와 M2의 같은 방향의 잔여 문제를 함께 겨냥한다. 단순히 모든 글자의 무게를 낮추거나 큰 제목을 금지하지 않는다. 현재 U의 역할 배정을 생성 도구가 구현할 수 있는 구체적인 강약 관계로 번역하는 것이다.

- [craft M2:476](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/craft/craft.observations.json:476>)
- [craft M3:742](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/craft/craft.observations.json:742>)
- [portfolio M3:857](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/portfolio/portfolio.observations.json:857>)
- [editorial M4:1197](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/editorial/editorial.observations.json:1197>)

### 2. 설명을 읽은 뒤 실제 행동에 필요한 정보의 연결을 먼저 설계한다

카피를 기능별로 묶은 뒤, 현재 목적을 실행하려는 독자가 설명의 끝에서 일정·장소·조건·신청 등 **실제로 주어진 관련 정보의 다음 시작을 어떻게 찾는지**를 명세에 담는다. 여러 구역으로 분산하는 경우 공유하는 시작축·인접·연속된 행·이미지 방향·대비 변화 중 현재 구성에 맞는 실제 단서를 고른다. 이미지가 두 정보 구역을 가로지르면 그 크롭·열림과 읽는 연결을 함께 결정한다. 공간의 남는 모서리에 각 묶음을 채운 다음 독자에게 왕복을 맡기지 않는다. 모든 정보를 한 패널이나 한 열에 모으거나 고정 순서를 강요하지 않으며 사용자 지정 배치·순서를 우선한다.

M3에서는 외곽 제목에서 중앙 본문으로 들어간 다음 안내 묶음을 찾는 연결이 약하고, M4에서는 오른쪽 일정에서 왼쪽 아래 신청으로 되돌아가는 경로가 세 기록에 반복된다. M4의 좁은 오른쪽 비용 마진과 큰 왼쪽 등록 간격도 이 접속을 큰 공간에서 해결하지 못한 현상으로 해석할 수 있다. 구체적인 한 포스터의 좌표 수정이 아니라 이미지의 면적과 정보 전환을 같은 설계 결정으로 다루는 지침이다. 이 해석의 인과효과는 아직 별도 확인되지 않았다.

- [editorial M3:920](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/editorial/editorial.observations.json:920>)
- [craft M4:1000](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/craft/craft.observations.json:1000>)
- [portfolio M4:1145](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/portfolio/portfolio.observations.json:1145>)
- [U production brief:21](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/snapshots/candidate-u/references/production-brief.md:21>), [U art direction:21](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/snapshots/candidate-u/references/art-direction.md:21>)

### 3. 작은 실행 정보도 글자·기호의 형태를 먼저 결정한다

날짜·시간 범위·조건·URL 등 실제 안내가 있다면, 본문 조판과 함께 그 묶음의 글자 골격·기호 형태·시각적 크기·어절 간격을 최초 명세에서 정한다. 원문이 구별한 하이픈/대시 같은 기호는 단순히 ‘정확한 텍스트’라고 맡기지 않고 그 글꼴·크기에서 구별되는 길이와 기준선 관계가 남는 형태로 지정한다. 짧은 강조 줄의 의미 있는 단어 간격을 좁혀 하나의 덩어리로 압축하지 않는다. 이는 인쇄 카피 한 벌과 함께 전하는 조판 선택이며 카피를 반복 붙이거나 문장부호를 바꾸는 절차가 아니다. 선택적인 가이드는 이 형태를 보여 주는 참고로 사용할 수 있으나 최종 폰트 적용·정확한 Unicode·판독을 보장하지 않는다.

시간 범위의 스트로크는 M1/M3/M4/M5에서 한 명 이상 FAIL 또는 unresolved NA가 남고 다른 평가자는 PASS로 읽었다. 따라서 모든 이미지에 실제 문자가 틀렸다고 합의한 공통 실패는 아니다. 반복된 **기호 판독의 취약성**이 공통 신호다. M5의 마감 단어 간격은 portfolio FAIL, editorial 재열람 후 해소, craft PASS로 다르다. 이 차이를 지우지 않고 읽는 크기에서 단어 경계와 기호 식별을 함께 설계할 필요의 근거로만 사용한다. U art direction:91에 이미 있는 기호 원칙을 사후 확인보다 최초 조판 명세의 내용에 연결하는 것이 제안의 범위다.

- [editorial M1:378](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/editorial/editorial.observations.json:378>)
- [craft M1:134](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/craft/craft.observations.json:134>)
- [editorial M3:851](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/editorial/editorial.observations.json:851>)
- [editorial M5:1389](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/editorial/editorial.observations.json:1389>)
- [portfolio M5:1416](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/portfolio/portfolio.observations.json:1416>)
- [U art direction:91](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/snapshots/candidate-u/references/art-direction.md:91>), [U layout guide:9](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/snapshots/candidate-u/references/layout-guide.md:9>)

## 공통 원인으로 확대하지 않을 항목

M4의 중앙 손·도구 접촉은 editorial/portfolio의 image_material 및 ai_slop 3이지만 craft는 각각 4다. 다른 네 장에서 같은 낮은 점수가 반복됐다는 근거가 없다. 이를 이유로 사람·손·도구·회화의 기본 사용을 금지하거나 모든 장에 고정 접촉 연출을 추가하지 않는다. U art direction:89의 동작 소유·연결 설계는 이미 존재한다. 이 한 장의 구체적인 끝점·나사·손잡이 수정은 일반 스킬 변경과 구분한다. M1의 작은 의류 라벨은 craft의 추가 인쇄 판독 NA이며 다른 이미지의 공통 가짜 문자 결함으로 확대하지 않는다.

세 평가자의 다양성 4와 포스터별 매체 관계를 보존한다. M2/M5의 판화 계열과 M1/M3의 사진 계열이 가깝다는 잔여 문제는 있었지만 전체 공간·글자 역할·편집 차이를 모두 4로 기록했다. 새 고정 다섯 매체 메뉴나 매체 중복 금지로 해결할 근거는 없다. 레퍼런스 수·명성·원본 재열람을 추가 통과 조건으로 만드는 것도 이 기록의 반복 원인을 해결하지 않는다.

- [portfolio M4 contact:1185](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/portfolio/portfolio.observations.json:1185>)
- [craft M4 image material:1045](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/craft/craft.observations.json:1045>)
- [craft M1 literal conditions:140](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/craft/craft.observations.json:140>)
- [portfolio set diversity:1494](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/reviews/R18-C1/initial/cli/portfolio/portfolio.observations.json:1494>)

위계 지침을 늘릴 때 가장 큰 위험은 ‘제목 하나 → 본문 → 일정 → 신청’의 연속 열을 모든 방향에 강요하는 것이다. 이는 현재 확보한 다른 진입점·이미지 경계·멀티컬럼·날짜 우선 구조를 같은 레이아웃으로 되돌릴 수 있다. 제안 1은 각 방향에서 선택한 역할 사이의 광학 우선순위만 구체화하고, 제안 2는 현재 구성의 실제 전환 단서를 구체화한다. 제목 우선·한 열·한 패널·일정과 신청의 물리적 인접·단일 진입점의 의무로 구현하면 이 제안의 범위를 벗어난다. 고정 배치가 있는 사용자 요청에서는 그 배치 안의 글자 강약·이미지 방향·정렬 단서로 연결을 해결한다.

이 검토는 U에 변경을 적용하거나 현재 R18 이미지를 다시 만들도록 요구하지 않는다. 같은 개발 요청의 관찰로 얻은 설계 가설이며 보류된 새 요청의 전이 결과나 안정적인 성공률을 증명하지 않는다. 원시 낮은 점수, FAIL, NA, transport 오류와 평가자 간 차이는 그대로 남는다.
