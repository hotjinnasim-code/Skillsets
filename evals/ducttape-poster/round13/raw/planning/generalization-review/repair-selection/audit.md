# 제작자 repair·selection 행동 감사

작성일: 2026-10-08. 독립 자문 감사이며 새 품질 평가가 아니다. R12의 닫힌 이미지·선택·원관찰·점수·게이트는 변경하지 않았다.

**권고는 계획에서 벗어난 수치를 결함으로 승격시키기 전에 실제 실패를 확인하고, 계획 일치만 늘어난 보정으로 이미 알려진 마감 퇴행을 정당화하지 못하게 하는 것이다.** L은 이미 계획의 비강제성과 전후 비교를 말한다. 부족했던 것은 제작자가 호출 직전과 선택 직전에 적용할 판별·중단 기준이다. 중앙 승인, 추가 생성, 고정 스타일·격자, 일반 제작의 새 외부 평가자는 필요하지 않다. 이 문서의 문구는 제안이며 Skillsets나 R12에 적용하지 않았다.

## 1. 실제 열람 범위

증거 기준 경로 `R`은 `/Users/nahyeonbin/Desktop/_Codex/ducttape-poster-round12`이다. 아래 문서 51개를 로컬에서 열었다. JSON은 필요한 필드를 투영해 읽었으며 모든 중복 메타데이터·정규화 전사 필드까지 정독했다고 주장하지 않는다. 최초 출력에서 잘린 관련 프롬프트·관찰은 더 작은 출력으로 다시 읽었다.

| 문서 | 실제 읽은 내용 |
| --- | --- |
| `R/report.md` | 전문: 단계별 선택, 전체 원점수 표, 게이트, 절차·한계 |
| `R/planning/final-evidence.json` | 상위 종료·횟수·한계, makers의 선택/호출 수, initial/selected 게이트, 원관찰 인벤토리. caller_records와 source/cache 하위 기록의 전문은 읽지 않음 |
| `R/raw-score-matrices.json` | 30개 presentation_records의 전체 일곱 점수, 단계/역할/평가자 연결과 기록 수 |
| `R/coordinator/R12-C1/plan.json` | 원문 요청, common_constraints, plan_authority, planning_checks; 다섯 방향의 내용/배치/읽는 경로/타이포그래피/대상 변형/가까운 방향 비교. M3·M5의 수량·좌표·카피 면적 계획. 폰트 측정 배열 전체나 모든 조사 출처 하위 필드를 정독하지 않음 |
| `R/checks/root-whole-five-visual-views.json` | ROOT의 보기 목록/수, notes와 limits. 이 기록의 27회를 내 열람으로 세지 않음 |
| `R/snapshots/candidate-l/SKILL.md` | 전문 |
| `R/snapshots/candidate-l/references/parallel-production.md` | 전문 |
| `R/snapshots/candidate-l/references/visual-research.md` | 전문. 링크된 웹 작품은 이번 감사에서 열지 않음 |
| `R/snapshots/candidate-l/references/art-direction.md` | 전문 |
| `R/snapshots/candidate-l/references/evaluation-loop.md` | 전문 |

제작 증거 35개는 다음 **각 역할의 세 단계 전부**다. 15개 `call-input.json`의 프롬프트 전문·참조 경로·투명 배경 값, 15개 `inspection.json`의 원시 읽기·보기/표시 한계·located_observations·residuals·mandatory의 서술/관계/비율 및 존재하는 선택 이유를 읽었다. 중복 `mandatory.transcriptions`의 전체 정규화 필드와 모든 view_pins를 하나씩 대조한 것은 아니다. 5개 `selection.json`에서는 selected_stage, selected_files, counts, 단계 연결, 종료 및 attestation 의미를 확인했다.

| 역할 디렉터리 | 읽은 세 단계 디렉터리: 각각 `call-input.json`, `inspection.json` | 읽은 선택 파일 |
| --- | --- | --- |
| `R/production/R12-C1-M1` | `stages/initial`, `stages/repair-1`, `stages/repair-2` | `selection.json` |
| `R/production/R12-C1-M2` | `stages/initial`, `stages/repair-1`, `stages/repair-2` | `selection.json` |
| `R/production/R12-C1-M3` | `stages/initial`, `stages/repair-1`, `stages/repair-2` | `selection.json` |
| `R/production/R12-C1-M4` | `stages/initial`, `stages/repair-1`, `stages/repair-2` | `selection.json` |
| `R/production/R12-C1-M5` | `stages/initial`, `stages/repair-1`, `stages/repair-2` | `selection.json` |

닫힌 평가 문서 6개도 읽었다. 각 문서에서 다섯 이미지의 일곱 점수와 필수 조건 상태, residuals, 세트 다양성/잔여 문제를 읽었고, M3·M5는 일곱 rating의 evidence를 모두 읽었다. 추가로 initial editorial M4의 NA 근거, selected editorial M4의 공간 근거, selected portfolio M2의 문자 간격 근거를 읽었다. 평가자의 모든 copy/layout 전사와 모든 다른 역할의 4점 evidence를 정독하거나 재판정한 것은 아니다.

- `R/reviews/R12-C1/initial/cli/craft/craft.observations.json`
- `R/reviews/R12-C1/initial/cli/editorial/editorial.observations.json`
- `R/reviews/R12-C1/initial/cli/portfolio/portfolio.observations.json`
- `R/reviews/R12-C1/selected/cli/craft/craft.observations.json`
- `R/reviews/R12-C1/selected/cli/editorial/editorial.observations.json`
- `R/reviews/R12-C1/selected/cli/portfolio/portfolio.observations.json`

**내가 실제로 본 이미지는 아래 12개 파일뿐이다.** 각각 `tools.view_image(detail="original")`의 반환 이미지를 표시해 보았다. original은 1672×941, usage는 720×405다. thumbnail-320, final.png, M1·M2·M4의 이미지는 이번 감사에서 직접 보지 않았다. M1·M2·M4에 관한 아래 내용은 문서 기록에 대한 분석이다.

| 실제 표시한 디렉터리 | 실제 표시한 파일 |
| --- | --- |
| `R/production/R12-C1-M3/stages/initial` | `original.png`, `usage-720.png` |
| `R/production/R12-C1-M3/stages/repair-1` | `original.png`, `usage-720.png` |
| `R/production/R12-C1-M3/stages/repair-2` | `original.png`, `usage-720.png` |
| `R/production/R12-C1-M5/stages/initial` | `original.png`, `usage-720.png` |
| `R/production/R12-C1-M5/stages/repair-1` | `original.png`, `usage-720.png` |
| `R/production/R12-C1-M5/stages/repair-2` | `original.png`, `usage-720.png` |

계획·요청·일부 점수를 읽은 뒤 이미지를 본 자문 감사다. blind review, 사용자 검색 실험, 실제 봉제 이력 인증, 제작 주체 판별은 아니다. 새 생성·API·Git 변경·다른 에이전트 메시지·하위 에이전트·새 점수 산출은 하지 않았다. 작업 결과는 이 디렉터리의 `audit.md`뿐이다. 초기 도구 호출에서 상위 `_Codex`의 AGENTS.md 파일명도 검색했으나 관련 지침 파일은 발견되지 않았고 그 검색 결과 파일들의 본문은 읽지 않았다.

## 2. 닫힌 all-five 결과를 유지한 해석

아래는 기존 점수와 게이트의 요약이다. 표에서 언급하지 않은 품질 점수는 4다. 30개 원점수 레코드/210개 점수 필드를 여섯 observations의 score 필드와 기계적으로 대조했으며 불일치는 없었다. 이는 새 scoring이나 판정 규칙 변경이 아니다.

| 역할 | initial의 닫힌 결과 | selected의 닫힌 결과 |
| --- | --- | --- |
| M1 | 세 평가자 모두 일곱 항목 4; PASS | initial을 선택. 세 평가자 모두 4; PASS |
| M2 | 모두 4; PASS | portfolio 글자 3 및 text/style FAIL; 역할 FAIL |
| M3 | 모두 4; PASS | 세 평가자 모두 이미지·재질 3, AI 슬롭 3; 역할 FAIL |
| M4 | 품질 점수 모두 4이나 editorial 시간 구분 기호 불확실성으로 NA | editorial 공간 3; 역할 FAIL |
| M5 | editorial·portfolio 계층/공간 3, craft 모두 4; FAIL | editorial 계층/공간/정서 3, portfolio 공간/AI 슬롭 3, craft 모두 4; FAIL |

initial 전체는 PASS 3 / FAIL 1 / NA 1, 세트 NA다. selected 전체는 PASS 1 / FAIL 4 / NA 0, 세트 FAIL이다. 세트 다양성은 두 단계의 세 평가자 모두 4다. 모든 제작자는 최초 1회와 보정 2회를 사용했고, M1 외에는 repair-2를 선택했다. 전체 15회와 평가 6세션은 이미 종료돼 있었다.

이 결과는 “보정은 항상 악화한다”는 증거가 아니다. M4는 기존 NA가 selected에서 해소됐지만 공간의 낮은 항목이 남았고, M5 selected의 계층은 portfolio에서 4인 반면 editorial에서는 3이다. M2의 기호 간격 FAIL도 닫힌 판정 그대로 보존한다. 이 감사가 래스터 간격을 다시 판정해 그것을 지우지 않는다. M3의 공통 재질 퇴행은 특히 일관된 후속 관찰이며, 다른 역할의 서로 다른 실패를 같은 원인으로 합치지 않는다.

## 3. M3: 이미 대응하는 두 줄을 세 줄 계획의 실패로 분류

사용자 요청은 입던 티셔츠→파우치 제작과 완성품 나눔의 연결, 성인에게 친근한 안내, 지정된 카피/비율/수량이다. 줄무늬 세 개, 1:2:1.4 폭, 넓고 좁은 간격은 사용자 요구에 없다. `plan.json`의 `/directions/2/image/transformation/necessary_features`가 세 개를 설계했고, `/plan_authority`는 방향/좌표/타입이 제안임을 명시한다. `/planning_checks/repair_priority`도 제안 좌표가 보존 조건이 아니라고 한다. 같은 계획 안에서 “necessary_features”라는 명명과 수치가 관계의 목적을 대신하는 체크리스트로 사용될 여지가 있었다.

| 단계 | 프롬프트·자기 검수에서 읽은 사실 | 직접 본 픽셀 |
| --- | --- | --- |
| initial | 프롬프트는 정확히 세 개의 불균등한 바와 빨간 비대칭 모서리를 요구. residual은 **양쪽 모두 두 바**인데 “assigned three”와 다르다고 적음. 동시에 substantive_visual은 바/빨간 모서리로 티셔츠→파우치 관계가 보인다고 기록 | 티셔츠와 왼쪽 파우치에 같은 두 짙은 띠, 밝은 바탕, 빨간 삼각 봉제 모서리가 있다. 파우치 입구/옆선과 별도 두 손바닥, 다른 붉은 파우치가 구별된다. 720에서도 이 대응과 안내 블록이 보인다 |
| repair-1 | “Observed correction”을 두 줄→세 줄로 정의. narrow/broad/medium, 약 1:2:1.4와 간격 순서를 지시. 검수는 여전히 양쪽 두 줄이며 상단은 좁고 하단은 넓다고 기록. 원단이 initial보다 균일하게 주름졌다는 drift도 기록 | 양쪽 두 줄의 폭 변화는 같이 일어났다. 원본의 무지 붉은 파우치에도 initial보다 반복되는 구불거리는 세부가 더 보인다 |
| repair-2 | 두 객체에 새 세 번째 바를 추가하는 데 두 번째 호출을 사용. 검수는 세 줄 대응을 기록하면서 원본의 반복 raised/wavy loop 질감이 natural knit variation을 줄인다고 명시. selection은 이 inspection을 연결한 repair-2를 채택 | 양쪽 세 줄을 셀 수 있다. 티셔츠의 밝고 어두운 부분과 두 파우치 모두에 유사한 굴곡/루프형 세부가 퍼졌다. 720에서는 이 질감 차이가 원본보다 덜 드러난다. 제목·사실 블록과 큰 손 지지 관계는 대체로 유지된다 |

근거 파일은 M3의 세 단계 `call-input.json` 및 `inspection.json`의 `/residuals`, `/located_observations`, `/mandatory/substantive_visual`, `/mandatory/material_edges`, 그리고 `selection.json`의 `/selected_stage`다. 선택 파일에는 독립된 선택 이유 문장이 없다. 따라서 “세 줄 복원 때문에 반드시 선택했다”는 내면의 동기를 확정하지 않는다. **기록에 이미 있는 대응 관계를 계획의 줄 수 부족으로 고치고, 자기 검수에서 알아낸 마감 퇴행이 있는 후보를 선택했다**는 실행 경로는 확인된다. 단순히 최신 파일을 무심코 골랐다고 단정할 근거도 없다.

여기서 필요한 질문은 “세 줄을 만들었나?”가 아니라 “현재의 두 줄과 비대칭 모서리가 원단 재사용 관계를 실제로 구별하게 하는가, 무엇이 아직 실패하는가?”다. initial 자기 검수와 세 초기 평가자는 그 관계를 인정했고, 내가 본 픽셀도 색 하나를 넘어 띠/모서리/새 봉제 구조의 대응을 제공한다. 따라서 **세 줄과의 불일치만을 이유로 한 두 호출은 생략 대상으로 판단할 근거가 충분하다.** 초기본에 다른 잔여 문제가 없었다거나 모든 관객에게 관계가 완벽했다는 뜻은 아니다.

후속 세 평가자는 선택본의 반복 표면을 각각 이미지·재질/AI 슬롭 3의 근거로 기록했다. 이는 내 새 점수가 아니다. 두 호출의 프롬프트에 realistic cotton/knit 유지 지시가 있었어도 반환물이 drift할 수 있었고, 사후 자기 검수도 그것을 알아봤다. 선택 단계가 “계획상의 세 줄 달성”과 “실제 사용자 목적의 개선”을 구분하지 못한 부분이 중요하다. 생성 모델의 왜곡 원인을 줄 수 지시 하나로 분리해 입증한 실험은 아니다.

## 4. M5: 좌표를 복원하는 것과 행사 안내·프레이밍을 해결하는 것

M5 계획 자체가 큰 English masthead를 허용했다. 사용자는 English 카피를 제공했고 스타일을 맡겼으므로 English-first, 강한 검정 글자, 두 안내 블록, stencil/cutout 표현은 그 자체로 위반이 아니다. 다만 주민에게 실제 행사가 무엇이고 어떻게 참여하는지 알려야 하는 맥락은 유지돼야 한다.

내가 본 initial은 English가 넓고 무겁고, Korean 두 줄도 큰 덩어리이며, 티셔츠·두 파우치가 중앙부터 오른쪽까지 뻗는다. 사용 보기에서 날짜/시간은 한 행, 장소/입장은 왼쪽 아래, 네 참여/준비 항목은 오른쪽 아래에 읽힌다. 문제를 검토할 단위는 이 앵커들의 경쟁과 필요한 정보로 이동하는 관계다. x243 대신 x397이어야 한다는 사실만으로 실패를 증명하지 못한다. initial 두 평가자는 계층·공간 3으로 이런 경쟁/분기 관계를 적었고 craft는 4로 인정했다.

repair-1은 작은 우상단 그림, Korean의 secondary 역할, sparse ink를 복원하려고 좌표와 font/visible height를 상세히 재지시한다. 제작자 자기 검수는 그림이 오른쪽으로 줄고 Korean은 작아졌지만 English는 약 71px로 더 커졌다고 기록했다. 내가 본 720 보기에서도 English는 거의 전체 상단 폭을 차지한다. “Korean이 English보다 작다”는 계획의 상대 역할을 맞추는 과정에서, 실제 행사 설명과 친근한 참여 안내의 비중이 더 좋아졌는지는 별도 판단이어야 한다.

repair-2 프롬프트는 “42% 대신 55%”, x397, 323×143, English visible height 약42/width505, Korean width150 등을 다시 정확한 목표로 만든다. 최종 자기 검수에도 그림 시작 x329, English 약62px, Korean 약49px, right facts x447처럼 계획과의 차이가 남는다. 이는 제작자의 래스터 추정치이며 내가 독립 측정해 인증한 수치가 아니다. 직접 본 selected는 그림이 줄고 오른쪽으로 이동했고, activity가 한 줄로 연결되며, attendance가 다소 가벼워졌다. 여전히 큰 English와 Korean, 작은 그림, 서로 다른 두 하단 그룹의 비중·경로 문제를 볼 수 있다. 계획상의 특정 픽셀로 되돌리는 것이 유일한 해결책은 아니다.

또한 initial부터 왼쪽 팔은 화면 내부에서 흐릿하게 끝나고, 오른쪽 팔은 화면 오른쪽 가장자리에서 들어온다. repair-1에서도 내부 종료가 남으며 repair-2에서는 내부 대각선 끝이 더 선명하다. 물체를 받치는 손바닥 접촉은 보인다. **경계가 더 선명해진 것과 팔의 페이지 안 프레이밍/소유 관계가 해결된 것은 서로 다른 관찰**이다. selected portfolio는 내부 절단과 반대 팔의 가장자리 진입의 비대칭을 공간·AI 슬롭 3으로 기록한다. 이 문제가 보정으로 처음 생겼다고 주장하지 않는다. 의도적인 잘라 붙인 형식 모두를 해부학 오류로 부르거나 모든 팔을 화면 가장자리에 연결하는 규칙도 제안하지 않는다.

M5 `/selection_consideration`은 실제로 smaller/further-right/flatter, 줄어든 English 높이, 가벼운 attendance, 한 줄 activity, firmer wrist termination을 장점으로 비교하고 작은 Korean/right-block 퇴행도 적었다. 즉 전후 비교를 전혀 하지 않은 사례가 아니다. 하지만 그 비교에서 **그림이 계획 영역에 가까워지는 것과 팔 끝이 단단해지는 것**이 실제 안내·공간 관계의 해결보다 큰 선택 근거가 될 수 있었다. selected editorial의 계층/공간/정서 3, portfolio의 공간/AI 슬롭 3 및 craft의 모두 4를 모두 남겨야 한다. 이 감사로 M5의 초기본이 무조건 더 낫다고 재선택하지 않는다.

향후 같은 상황이라면 “주민이 행사 내용과 전체 참여 정보를 찾는 경로의 어떤 경쟁을 줄일 것인가”와 “이 cutout 안에서 두 offering의 팔 경계가 왜 서로 다르게 끝나는가”를 먼저 정할 수 있다. 꼭 계획한 위치/높이로 복원할 필요는 없고, 보정을 한다면 그 실제 관계를 현재 한도 안의 목표로 삼을 수 있다. 이것은 다음 이미지 호출의 실행 지시가 아닌 문구 적용 예시다.

## 5. 다른 제작 기록이 보여 주는 한계와 반례

M1은 숫자 1의 작은 spur와 경쟁하는 식물 제거 후 반복 winding texture가 생겼고, 두 번째 natural-knit 복구도 개선하지 못했다고 기록했다. 최종 선택은 initial이다. 따라서 이전 결과로 되돌리는 권한이나 파일 보존이 없었던 것은 아니다. 이 역할의 픽셀은 이번에 직접 보지 않았으므로 기록 이상의 시각 주장은 하지 않는다.

M2는 flat fills/rays를 다듬는 과정에서 repair-1 비율이 선언 허용 밖이었다. 이는 사용자 비율에서 나온 실제 조건 문제이며 계획 불일치와 구분해야 한다. repair-2의 비율 회복과 마감 장점을 비교해 선택했지만 닫힌 portfolio의 문자 간격 FAIL이 남았다. 같은 감사 원리로 정당한 조건 복구까지 막으면 안 된다.

M4는 계획 줄바꿈/크기 복원과 실제 source-pouch stripe junction 비교를 함께 했다. 자기 검수상 대응 강화와 전체 티셔츠 hem 수용은 기록된 변화이나, selected editorial은 공간 관계 3을 남겼다. “복원된 계획 항목 수”가 전체 개선을 보장하지 않는다는 보조 기록이다. 모든 M4 호출을 불필요하다고 분류하지 않는다.

이 세 역할의 프롬프트·자기 검수까지 읽은 이유는 M3만 보고 “항상 초기본을 선택하라”는 규칙을 만들지 않기 위해서다. 핵심은 실제 결함과 계획 편차를 먼저 구별하고, 고친 기능과 새 퇴행을 같은 보기에서 비교하는 재사용 가능한 행동이다.

## 6. L에 이미 있는 지침과 작동하지 않은 단계

| 기존 위치 | 이미 있는 지침 | 이번 경로에서 부족한 점 |
| --- | --- | --- |
| `references/parallel-production.md:9` | 중앙 계획은 추가 사용자 조건이 아니며 제작자가 관계를 재설계할 수 있음 | 실제 결과가 계획과 달라도 성공이면 **수정 없이 채택**할 수 있다는 선택 분기가 덜 명시적. 수치/necessary_features가 도구 명세·검수의 “assigned/required”로 넘어감 |
| `references/art-direction.md:15` | 같은 색/질감만으로 대응을 인정하지 않고 핵심 특징을 실제 양쪽에서 비교 | 유효한 다중 특징 대응과 설계자가 고른 특정 수량의 재현을 구별하지 않으면 M3처럼 이미 대응하는 두 객체를 세 줄 부족으로 분류할 수 있음 |
| `references/art-direction.md:21` 및 `SKILL.md:54–56` | 계획 설명 없이 실제 앵커와 전체 정보 경로를 봄 | M5는 실제 경로도 적었지만 좌표/visible height 편차가 다시 “remaining faults”의 주된 제목이 됨. 계획 근접도는 검색 성공의 측정이 아님 |
| `references/art-direction.md:77` | 계획 좌표보다 실제 관계/정보 검색 실패를 우선, 전후 비교, 최신/매끈함 자동 채택 금지 | 원인 기록에 **사용자 근거 또는 기능 실패가 실제로 있는지** 먼저 판별하는 단계가 없음. 비교를 해도 계획 달성 자체를 이득으로 세면 M3의 알려진 마감 퇴행을 선택할 수 있음 |
| `SKILL.md:62`, `references/parallel-production.md:21` | 최대 두 보정, 전후 중 가장 적합한 결과 선택 | 상한을 채울 필요가 없다는 중단 분기와 계획만 개선된 후보의 명시적 기각 기준이 약함. 전부 2회를 썼다는 기록만으로 강제 소진의 원인을 확정하지는 않음 |
| `references/evaluation-loop.md:3,72` | 일반 제작에 외부 평가/승인을 추가하지 않음. 새 버전·보정본이 더 낫다는 전제 없이 비교 | 이 원칙은 유지하면 됨. closed critics를 다시 열거나 일반 제작의 의무 단계로 옮길 필요 없음 |

따라서 새 디자인 이론·점수표가 필요한 것이 아니다. 실제 픽셀을 이미 보는 제작자에게 **호출할 이유의 자격**과 **선택할 이득의 자격**을 짧게 확인하게 해야 한다. M3는 계획 수량 복원만 남았다면 no-op, M5는 계획 위치와 무관한 실제 안내/프레이밍 목표가 남았다면 그 목표로 보정한다. 관계가 좋다는 자기 설명을 그대로 믿으라는 규칙도 아니다. 같은 실제 보기에서 반대 근거를 찾는 기존 검수를 유지한다.

## 7. 최소 한국어 수정안 — 두 위치, 적용하지 않음

다음 두 군데만 바꾸는 안을 권고한다. 새 JSON 양식·평가 점수·사전 승인 단계는 만들지 않는다. 아래 한 문장의 원인 기록은 기존 자기 검수/작업 메모에 남기면 된다. 스냅샷의 줄 번호는 위치 식별용이고 원문 anchor를 함께 적었다.

### A. `SKILL.md`, §4, 현재 62행의 보정·선택 문단 전체 교체

정확한 anchor: `검수에서 원인을 골라 **이미지당 최초 생성 뒤 재생성을 포함한 자동 보정 최대 두 번**만 수행한다.`로 시작하는 문단.

> 보정 전에 실제 보기의 실패 위치, 사용자 조건의 근거 또는 깨진 목적·판독·관계·마감, 확인할 변화와 보존할 장점을 한 문장으로 정한다. 계획의 좌표·글자 크기·줄 수·무늬 수와 다르다는 사실만으로 결함을 만들지 않는다. 카피·사용자 조건과 필요한 대응·읽는 흐름·방향의 구분이 작동하면 계획을 맞추기 위한 호출은 생략한다. **이미지당 최초 생성 뒤 재생성을 포함한 자동 보정은 최대 두 번**이며 채울 의무는 없다. 중앙과 제작자 호출을 합산하고 실패한 시도도 센다. 국소 결함은 대상 이미지를 수정하고 발상·구성의 실패는 관계부터 재설계한다. 매번 전체 카피·조건을 재확인하고 같은 보기에서 전후를 직접 비교한다. 선택은 필수 조건을 먼저 대조한 뒤 실제로 해결된 실패와 새 퇴행을 함께 비교한다. 계획 일치만 늘고 이미 작동하던 관계·판독·마감이 나빠졌으면 이전의 적합한 결과를 유지한다. 관찰한 실익이 동등하거나 불확실해도 이전의 적합한 결과를 우선하며 최신 파일을 자동 채택하지 않는다. 문구 삭제·효과 추가로 결함을 가리지 않고, 한도 안에서 남은 결함과 선택의 이유를 알린다.

이 교체가 핵심 실행 수정이다. 기존 art-direction §실제 결과의 일곱 기준 마지막 보정 문단(77행)을 확장 복제하지 않고 상세 비교 방법으로 유지한다. 그 문단의 “핵심 특징”은 사용자 목적상 필요한 실제 대응의 기준으로 읽으며 maker 계획의 수량을 자동 필수화하지 않는다.

### B. `references/parallel-production.md`, §중앙에서 먼저 설계, 현재 9행 끝의 네 문장 교체

정확한 교체 범위: `중앙 계획은 실행을 위한 설계이며 추가 사용자 조건으로 취급하지 않는다.`부터 `바꾼 관계와 이유를 중앙에 알린다.`까지.

> 중앙 계획은 실행을 위한 설계이며 추가 사용자 조건이 아니다. 좌표·크기·줄 수·특징 수는 사용자 지시나 사용자 자산의 보존 요구에 근거한 경우에만 고정 조건으로 삼는다. 실제 결과가 계획과 달라도 사용자 조건·필요한 관계·다른 방향과의 실질적 구분을 충족하면 제작자가 중앙 승인 없이 그대로 채택할 수 있다. 실제 실패가 있으면 같은 조건 안에서 관계를 재설계하고 스킬 §4의 보정·선택 기준을 적용한다. 계획에서 달라진 관계와 이유는 결정 뒤 중앙에 알린다.

이는 기존의 중앙 보고를 없애지 않는다. 보고를 선택의 사전 허가로 바꾸지 않으며, 자유롭게 만든 계획 수치가 다음 호출의 client constraint로 승격되지 않게 한다.

### 적용 예외와 보존할 범위

- 사용자가 수량·좌표·픽셀 크기·줄바꿈·스타일·정확한 패턴/로고를 지정했거나 사용자 참조의 위치/비례/특징 보존을 요구했다면 그 근거가 우선이다. 그런 수치 불일치를 no-op로 넘기지 않는다. R12에는 client asset이 없으므로 이 예외의 실제 성공은 검증되지 않았다.
- 관계를 보여 주는 구성에서는 핵심 구조 대응을 계속 비교한다. 무늬가 두 개든 세 개든 **양쪽에서 대응하지 않거나 결과 식별이 안 되면** 실제 실패다. 색 하나가 같다는 이유로 통과시키지 않는다. 관계가 필요 없는 주제에 새 변형 과정·손·물리 장면을 만들지 않는다.
- 강한 English, 여러 진입점, 비대칭 블록, 거친 질감, 내부 cutout은 일괄 금지하지 않는다. 사용자 목적 안에서 실제 판독·그룹 이동·접촉/프레이밍이 작동하는지 본다. 한국어-first, 한 안내 열, 고정 격자, 양팔 모두 edge crop 같은 기본값을 만들지 않는다.
- 이전 결과가 사용자 필수 조건을 어겼고 보정이 그것을 해결했다면 단순한 미적 장점만으로 이전을 우선하지 않는다. 조건 충족 후보에서 비교하고 부수 퇴행을 기록한다. 모든 후보에 실패가 남으면 그것을 공개하며 완성/통과로 바꾸지 않는다.
- 일반 제작에는 maker/중앙의 기존 실제 보기만 쓴다. 평가 루프의 세 외부 평가자는 개선·비교를 명시한 기존 범위에서만 유지한다. 두 번은 상한이며 새 critic, 추가 generation 또는 중앙 approval의 자격 요건이 아니다.

## 8. 이 감사가 지지하는 것과 남는 불확실성

관찰 경로는 “자유롭게 설계한 수치 → 보정 대상의 required/assigned 항목 → 계획 달성에 유리한 선택”이라는 실패 가능성을 지지한다. 특히 M3는 실제로 대응하는 두 줄을 양쪽에서 확인한 뒤 두 호출을 세 줄에 썼고, native 마감 퇴행을 기록한 selected 후보가 세 평가자에게 같은 낮은 항목을 받았다. M5는 좌표 복원에 몰린 상세 지시와 별개로 실제 headline/context와 내부 팔 경계의 문제가 남았으며 평가자 차이도 남았다.

제안문을 적용한 새 이미지 실험은 하지 않았다. 이 문구가 불필요한 호출을 차단할 **구체적인 결정 분기**는 제공하지만, 모든 요청의 regression을 예방하거나 새로운 전이 품질을 보장한다고 말할 수 없다. 모델의 편집 drift, maker의 실제 관계 판단, 서로 다른 내용/스타일/사용자 자산 보존은 여전히 별도의 불확실성이다. 닫힌 R12 선택을 바꾸거나 유리한 후보만 합쳐 새 성공 세트를 만들지 않았다. 다음 테스트도 시작하지 않았다.
