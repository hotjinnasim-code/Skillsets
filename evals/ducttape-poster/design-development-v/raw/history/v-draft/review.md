# Candidate V draft revision

V는 `drafts/candidate-u`의 12개 파일을 먼저 바이트 그대로 새 `drafts/candidate-v`에 복사한 뒤 작성한 **미채택·미시험 초안**이다. 이미지 생성·점수 부여·추가 평가·설치는 하지 않았다. U 원본, 현재 라이브 U, R18 동결 U의 파일 집합 해시는 작업 전후 동일하다. R18 제작·선택·평가 경로에는 쓰지 않았으며 SELECTED 자료도 읽지 않았다.

## 변경한 파일과 이유

1. [SKILL.md:32](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/SKILL.md:32>)는 실제 첫 역할과 보조 문구의 크기·굵기·대비·여백 관계를 명세하도록 구체화했다. [같은 파일:34](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/SKILL.md:34>)는 문단의 끝에서 실제 다음 안내 묶음의 시작을 찾는 연결과 이미지의 크롭·열림을 함께 설계하도록 바꿨다. [같은 파일:36](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/SKILL.md:36>)에는 실제 안내의 단어 경계와 기호 식별을 최초 조판 명세에 연결했다.
2. [production-brief.md:13](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/references/production-brief.md:13>)은 추상적인 ‘역할’ 배정을 실제 문구 사이의 광학 강약으로 구현한다. [본문 흐름:19](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/references/production-brief.md:19>)는 다음 정보의 시작과 이미지의 열림을 함께 선택한다. [조판:27](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/references/production-brief.md:27>)은 원문 기호의 구별되는 길이·위치·숫자 기준선과 의미 있는 단어 간격을 실제 표시 상황에 맞춰 명세한다. [도구 전달:51](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/references/production-brief.md:51>)은 이 세 결정을 기존 긍정적인 제작 명세에 포함한다.
3. [parallel-production.md:15](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-v/references/parallel-production.md:15>)는 중앙의 역할 배정에 같은 구체적인 강약·전환·조판 결정을 담아 제작자에게 전달한다. 다른 제작자의 이미지·전체 계획은 여전히 공유하지 않는다.

이 변경은 [INITIAL 읽기 전용 분석](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/history/u-general-failure-synthesis/review.md>)에서 찾은 경쟁 앵커와 실용 정보의 불연속을 겨냥한다. R18 INITIAL은 세 transport trace 오류로 절차 NA이며, 원시 낮은 점수와 판독의 평가자 간 차이는 그대로 남아 있다. 그 기록으로 만든 가설을 초안에 반영한 것이므로 성능 개선이나 전이 성공을 주장하지 않는다.

## 좁힌 범위와 다양성 보존

새 체크리스트·사후 점수·통과 문턱·출처 재열람·승인·추가 생성 단계는 만들지 않았다. 기존 최초 설계 문단을 구체화했다. 제목 우선·단일 진입점·한 열·한 패널·고정 정보 순서·본문 크기 숫자를 새 의무로 넣지 않았다. 여러 진입점은 필요한 다음 정보를 갖도록 설계할 수 있고 방향마다 날짜·제목·이미지 등 첫 역할을 다르게 선택할 수 있다. 보조 문구를 무조건 작게 만들거나 같은 하단에 모으지 않는다. 사용자 지정 스타일·배치·순서와 제목만/무문자 요청의 우선순위를 유지한다.

위계를 모든 방향의 제목→본문→일정→신청 열로 구현하면 공간과 읽는 경로의 차이를 다시 없앨 위험이 있다. V의 명시적인 비고정 범위와 기존 ‘서로 다른 큰 관계’ 지침을 함께 유지해야 한다. 실용 정보의 연결도 물리적으로 모두 인접해야 한다는 뜻이 아니며 선택한 이미지 방향·정렬·열림으로 분산된 정보를 이어 줄 수 있다.

## 복사와 정적 확인

복사 직후 U와 V는 12개 파일 모두 동일했다. 변경 후 파일 목록도 각각 12개이며 위 세 파일만 달라졌다. 다음 아홉 파일은 U와 SHA-256이 동일하다.

- `agents/openai.yaml`
- `references/art-direction.md`
- `references/design-grammar.md`
- `references/evaluation-loop.md`
- `references/layout-guide-contract.md`
- `references/layout-guide.md`
- `references/reference-catalog.json`
- `references/visual-research.md`
- `scripts/make_layout_guide.py`

따라서 helper·자료 색인·평가 루브릭과 절차·상한·기준·자산 조건·기본 제외 스타일은 수정하지 않았다. Markdown 상대 파일 링크 28개는 모두 존재한다. 이 확인은 파일 연결 확인이며 이미지 품질이나 렌더러 실행 검증이 아니다. 개별 U/V 해시와 보호한 U의 전후 파일 집합 해시는 [status.json](</Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/history/v-draft/status.json>)에 기록했다.
