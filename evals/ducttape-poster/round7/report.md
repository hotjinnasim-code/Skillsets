# Round 7 — 기존 H 포스터 20개 역할의 최종 기록

이미 생성된 7개 요청·20개 역할을 모두 닫고 보관했다. 이 마감 작업에서 새 이미지나 새 critic을 실행하지 않았다. **선택본은 PASS 5개·FAIL 10개·NA 5개이며 전체 묶음 판정은 NA다.** 아카이브 무결성·재현 검사의 PASS는 포스터 품질의 PASS를 뜻하지 않는다.

[선택본 20개 갤러리](raw/gallery.html) · [원점수와 전체 보고](raw/report.md) · [봉인된 증거](raw/planning/final-evidence.json) · [출처 인덱스](archive-index.json)

| 기록 | 실제 결과 |
| --- | --- |
| 완료된 포스터 역할 | 20 / 20 |
| 포스터 native 생성 시도 | 52 / 최대 60 |
| 별도 합성 참조 자산 생성 | 3회; 포스터 분모·예산과 별도 |
| 실제 독립 fresh critic 세션 | 39 / 최대 42 |
| 중복 없는 실제 평가 묶음 | 13개: 초기 7개 + 변경된 선택본 6개 |
| 실제 이미지×critic 기록 / 점수 슬롯 / 유효 원점수 | 117 / 819 / 819 |
| 초기 이미지 판정 | PASS 7 · FAIL 10 · NA 3 |
| 선택본 이미지 판정 | PASS 5 · FAIL 10 · NA 5 |
| 초기 / 선택본 전체 묶음 판정 | NA / NA |

| 요청 | 역할 수 | 초기 묶음 | 선택본 PASS / FAIL / NA | 선택본 묶음 |
| --- | ---: | --- | --- | --- |
| R7-D1 | 5 | FAIL | 3 / 2 / 0 | FAIL |
| R7-B02 | 3 | FAIL | 0 / 3 / 0 | FAIL |
| R7-B03 | 2 | NA | 0 / 2 / 0 | FAIL |
| R7-B04 | 5 | NA | 0 / 0 / 5 | NA |
| R7-B05 | 1 | FAIL | 0 / 1 / 0 | FAIL |
| R7-B06 | 1 | PASS | 1 / 0 / 0 | PASS |
| R7-B07 | 3 | FAIL | 1 / 2 / 0 | FAIL |

B06는 요청·파일·순서·단계·native SHA·문맥이 모두 동일하여 초기의 완전한 세 critic 평가를 선택본에도 재사용했다. 새 critic 세션이나 점수로 중복 계산하지 않았다. 각 단계에 표시되는 기록은 60개·점수 420개이며, 두 단계의 실제 고유 기록은 위의 117개·819개다. B07 초기의 이미지 세 개는 각각 PASS였지만 묶음 다양성은 FAIL이었다. 마지막 선택본의 실제 세 평가를 추가한 뒤에도 FAIL을 유지했다.

B04 선택본 portfolio critic은 같은 세션에서 네 번의 websocket 재연결 오류를 남기고 실제 완료했다. 고정된 v4 판정기가 모든 critic trace 오류를 절차 NA로 처리하므로 다섯 역할 전부 NA를 유지했다. 원래 관찰·낮은 점수·105개 점수값·오류 trace를 보존했고, critic을 교체하거나 규칙을 완화하지 않았다. [절차 기록](raw/planning/b04-selected-procedural-finding.json)

H는 **계측된 개발 증거**다. 실행 하네스가 매 native 호출 앞에 원래 사용자 요청 전문을 반복하도록 강제했고, 이는 runtime skill의 요구보다 강했다. 따라서 이 결과를 일반 사용의 프롬프트 구성으로 표현하거나 runtime 단독 효과로 해석할 수 없다. 이후 I runtime이나 미관측 요청의 품질을 인증하지도 않는다. [계측 범위 기록](raw/planning/instrumentation-scope-finding.md)

전체 초기·선택·중간·미사용 native 원본, 실패·NA 평가, 고정 입력과 helper, 실제 세션 완료 기록을 보관했다. 마감 전 기존 입력 1,245개는 마감 후에도 같은 바이트였고, 포스터 native 원본 52개와 raw critic JSON 39개를 유지했다. 외부 native cache 식별자는 바이트가 동일한 보관 원본에 인덱스로 연결했다. 실제 그림과 출처를 보았다는 판단은 원 critic의 의미적 확인이며, 이 마감·아카이브 검사에서 새 시각 평가를 수행하지 않았다.

검증은 1,380개 출처 매핑의 SHA를 확인하고, 고정 v4로 13개 실제 평가 묶음을 재현했다. 원래 출처의 파일 읽기·메타데이터 접근을 차단한 재현에서도 원래 출처 접근은 0회였다. 아카이브와 Python runtime의 공통 상위 경로 메타데이터만 허용했다. 외부 경로 5개와 symlink 탈출 경로 2개를 거부했고, 갤러리 이미지 20개·로컬 링크 80개와 원 보고서 링크 19개를 모두 확인했다.

[판정 재현 검사](verification.json) · [원래 경로 차단 및 링크 검사](portability-integration.json) · [기존 입력 보존 검사](checks/immutable-preservation.json) · [ROOT 검사기 수정 이력](checks/integration-checker-history.json)

다른 위치에 복사한 뒤 Python 3.12 환경에서 아카이브 디렉터리를 기준으로 실행할 수 있다. raw 파일이나 점수·문구·판정 기준은 바꾸지 않고 인덱스의 경로 식별자만 메모리에서 연결한다.

```sh
python3 raw/verify_archive.py --archive .
python3 checks/closure_archive_integration_v2.py --archive . --output /tmp/round7-portability-recheck.json
```

두 번째 명령의 출력 파일은 아직 존재하지 않는 경로를 지정한다. 유한한 관찰 결과는 이후의 모든 이미지 품질을 보장하지 않는다.
