# D 스킬 지침 회귀 감사

판정: **지정된 읽기 범위에서 뚜렷한 blocker 없음.** 정적 지침 감사이며 실행·생성·수정 검증은 수행하지 않았다.

## 범위와 변경

C와 D의 동일한 여섯 스킬 파일, `phase-plan.json`, `candidate-d-hashes.json`만 읽었다. 실제 출력 점수, 다른 에이전트, production, 진단, 사례 카피, live 스킬, 호출 ledger는 읽지 않았다. 요청된 이 보고서 두 파일만 저장했으며 스킬을 수정하거나 추가 에이전트를 실행하지 않았다.

바이트 비교 결과 `references/art-direction.md`의 D 15행과 83행에 있는 두 문단만 변경되었다. 나머지 다섯 파일은 C와 D가 바이트 단위로 동일하다. D의 여섯 파일은 동결 manifest의 SHA-256과 바이트 수에 모두 일치한다.

15행은 핵심 카피·대상·안내가 구성 안에서 이어지는지 판단하고 필요할 때 전체 면적·인접·정렬을 다시 배분하도록 한다. 정보 역할과 판독을 돕는 별도 영역은 허용하며 직접적인 사진·그림·조용한 제목도 허용한다. 83행은 자동 보정에서 원인이 된 자체 배치를 고정하지 않고 재설계할 수 있게 하되, 사용자 조건·잘 작동하는 관계·전체 문구와 대상을 유지하고 후속 부분 수정은 지정한 보존 범위를 따르도록 구분한다.

## 필수 기준 대조

| 기준 | 판정과 근거 |
| --- | --- |
| 사용자 수량·스타일·참조 우선 | 충돌 없음. 수량·스타일·참조·배치 등 사용자 조건을 우선하는 원문은 그대로다. 변경 문단은 그 조건 안에서 정보 역할과 판독을 돕는 면적·인접·정렬 판단을 추가한다. 근거: `SKILL.md:17`, `SKILL.md:20`, `SKILL.md:21`, `references/art-direction.md:3`, `references/art-direction.md:15`, `references/art-direction.md:25`, `references/art-direction.md:83`. |
| 기본 다섯 독립 제작자·가용 슬롯 | 충돌 없음. 기본 다섯 역할의 독립 생성, 사용자 지정 수량, 가용 슬롯에 따른 분할 실행, 실행하지 않은 병렬성 주장 금지는 변경되지 않았다. 근거: `SKILL.md:10`, `SKILL.md:43`, `SKILL.md:47`, `references/parallel-production.md:3`, `references/parallel-production.md:7`, `references/parallel-production.md:11`, `references/evaluation-loop.md:13`. |
| 한 장 후속 부분 수정의 보존 범위 | 충돌 없음. 자동 보정에서 원인이 된 자체 배치를 재설계하는 범위와 사용자 후속 부분 수정의 보존 범위를 명시적으로 구분한다. 후속 수정은 지정 이미지·부분만 바꾸는 원문을 따른다. 근거: `SKILL.md:10`, `SKILL.md:68`, `references/art-direction.md:81`, `references/art-direction.md:83`. |
| 한 원본 계보당 자동 보정 최대 두 번 | 충돌 없음. 재생성도 이미지당 최대 두 번에 포함하고 중앙·제작자 호출 이력을 합산하는 기준이 유지된다. 변경 문단에 보정 한도 초기화나 추가 보정 허용은 없다. 근거: `SKILL.md:63`, `references/art-direction.md:83`, `references/parallel-production.md:17`, `references/parallel-production.md:23`, `phase-plan.json:corrections_per_new_output_max`. |
| 실제 도구 참조 방식 | 충돌 없음. 실제 참조를 열어 확인하고 현재 도구의 파일·대화 이미지 참조 방식으로 전달하는 의무는 유지된다. 사용자 참조를 누락하지 않는 원문도 그대로다. 계획의 신규 초기 호출에서 양쪽 참조 키를 생략하고 자체 수정은 검증한 자체 원본을 쓰는 구분은 현재 도구 지침과 일치한다. 근거: `SKILL.md:46`, `SKILL.md:47`, `SKILL.md:52`, `SKILL.md:53`, `references/art-direction.md:81`, `phase-plan.json:reference_policy`, `current_session:image_gen_schema_and_usage`. |
| 가능한 최대 해상도와 제어 한계 | 충돌 없음. 사용자 크기를 우선하고 지원 가능한 최대 해상도를 요청하되 프롬프트만으로 보장하지 않으며 실제 반환 크기와 제어 한계를 알리는 원문이 유지된다. 변경 문단은 도구 인자나 해상도 보장을 추가하지 않는다. 근거: `SKILL.md:48`, `SKILL.md:49`, `SKILL.md:50`, `SKILL.md:62`, `current_session:image_gen_schema_and_usage`. |
| 전체 카피 보존 | 충돌 없음. 전체 카피와 대상의 공간 관계를 재배분하는 변경이다. 문구 값·지정 순서·줄바꿈·전체 카피 보존과 삭제·발명 금지가 유지되고 변경 문단도 전체 문구 보존을 명시한다. 근거: `SKILL.md:44`, `SKILL.md:45`, `references/art-direction.md:15`, `references/art-direction.md:19`, `references/art-direction.md:49`, `references/art-direction.md:51`, `references/art-direction.md:59`, `references/art-direction.md:83`. |
| 장르 중립 | 충돌 없음. 사진·그림·조용한 제목·기능적 표나 목록을 허용하며 글자 변형·물리적 겹침·특이한 장면을 필수로 만들지 않는다. 특정 색·효과·사진·3D를 자동 탈락시키지 않는 기준은 유지된다. 근거: `SKILL.md:67`, `references/art-direction.md:15`, `references/art-direction.md:23`, `references/art-direction.md:25`, `references/art-direction.md:57`, `references/art-direction.md:61`, `references/art-direction.md:89`, `references/art-direction.md:101`, `references/evaluation-loop.md:37`. |

한 장의 자동 보정에서 자체 결정한 배치를 바꿀 수 있다는 문장을 사용자 후속 부분 수정의 구도·빛·질감 변경 허가로 해석하지 않는다. 후속 변경은 `SKILL.md:68`과 변경 문단의 명시적 구분을 따른다. 재설계·재생성도 기존 이미지 보정 이력에 합산하므로 지침 변경만으로 해당 원본의 두 번 한도를 초기화하지 않는다.

## 파일 무결성

| 파일 | C SHA-256 | D SHA-256 | D 바이트 | 동결 기록 |
| --- | --- | --- | ---: | --- |
| `SKILL.md` | `da8c7b2762a5e138d07ad64529f90c3f33448e523b8210903cbf8b7bb47c47ea` | `da8c7b2762a5e138d07ad64529f90c3f33448e523b8210903cbf8b7bb47c47ea` | 18003 | 일치 |
| `agents/openai.yaml` | `c5984a5895d0ea97b7cb29db14ab7bb6d0ab7fa437625a192a9b9b8eedb09460` | `c5984a5895d0ea97b7cb29db14ab7bb6d0ab7fa437625a192a9b9b8eedb09460` | 476 | 일치 |
| `references/art-direction.md` | `f8f03ef6076c337358dff7de0fda0f457ac8c19ef12c5b944a2496a2c9ed0e95` | `b76c20018075f06c790384d16ef5868d675cce7e17f6188df27994bef183c8bb` | 17038 | 일치 |
| `references/evaluation-loop.md` | `cbb7c3c8412363cc0549a5009ba6e8e48a35714375d688545c4c400433719dda` | `cbb7c3c8412363cc0549a5009ba6e8e48a35714375d688545c4c400433719dda` | 7493 | 일치 |
| `references/parallel-production.md` | `afb373eb4789a55e2de322ea2702472be06331588c906ba1b44db3ae197bb657` | `afb373eb4789a55e2de322ea2702472be06331588c906ba1b44db3ae197bb657` | 4390 | 일치 |
| `references/visual-research.md` | `8b72b1dc0dc3fa1234bc6b4c4fe3943a9cb1e6bbe84a82cfb05db2c6adfa8d7a` | `8b72b1dc0dc3fa1234bc6b4c4fe3943a9cb1e6bbe84a82cfb05db2c6adfa8d7a` | 11842 | 일치 |

로컬 상대 Markdown 링크는 C 6개, D 6개로 모두 실제 파일로 해석되고 각 사본 안에 남는다. `SKILL.md`의 27·33·35·43·76행과 `references/evaluation-loop.md`의 39행이 대상이다. `art-direction.md:83`의 코드 표기 `SKILL.md`는 링크가 아니라 루트 문서 이름 참조이며 두 사본의 루트 파일이 존재한다. 외부 URL의 최신 내용은 이 감사 범위에 포함하지 않았다.

## 계획 기록 일관성

`phase-plan.json`의 C 종료 기록은 32회이며 예상값과 같다. unused C 호출 폐기와 종료 이후 C native 호출 금지가 선언되어 있다. 이는 허용된 계획 기록 확인이며 ledger를 독립 검증했다는 뜻은 아니다.

D의 선언 범위는 새 출력 3개(`D-C02`, `D-P01`, `D-H02`)와 각 새 원본당 최대 보정 2회다. 산술은 `3 × (1 + 2) = 9`, `C 32 + D 최대 9 = 41 ≤ round4 42`, `round3 34 + 41 = 75 ≤ 전체 76`으로 일치한다. 최종 요청 14개는 새 D 3개와 보존 C 11개로 구성하는 계획이며 14개의 새 D 출력을 선언하지 않는다. 원본 계보가 다른 새 D 초기 생성과 C의 세 번째 자동 보정을 구별하는 계획은 두 번 보정 기준과 충돌하지 않는다.

## 판정의 한계

blocker는 0개다. 변경 D가 아직 live 스킬에 설치되지 않았다는 점은 전달받은 전제로 기록했으며 live 파일을 읽어 확인하지 않았다. 실제 실행·출력·평가 점수·call ledger를 읽거나 테스트하지 않았으므로 다섯 명 동시 실행, D 14장 실제 검증, 실제 생성 호출 수, 실제 결과 품질을 검증했다고 주장하지 않는다. 변경 두 문단과 보존된 지침의 정적 일관성만 통과한 감사다.
