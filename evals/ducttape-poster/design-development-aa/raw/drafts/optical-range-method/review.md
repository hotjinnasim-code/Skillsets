# 광학 숫자 범위의 작은 전향 구현 초안

기존 20-helper bundle을 현재 R22 prepared 핀과 비교하고 정규화 이름·함수·summary digest 및 전체 문맥 digest를 참조하는 위치를 파일별로 기록했다. 두 normalizer, adapter의 고정 summary SHA, 두 preparer의 packet/copy/helper 핀, reuse와 compact binding의 context, producer의 v1 검사 문장, 규칙·문서·역사 검증의 범위가 주요 연결점이다. 모든 기존 helper는 읽기만 했으며 바이트가 그대로다. 기존 원전사·점수·FAIL/NA를 읽어 다시 판단하지 않았다.

새 `numeric_range_normalization.py`는 독립 순수 함수와 선언 검증만 제공한다. 기존 함수의 일반 비교를 유지하면서 카피별 정확한 양끝/U+2013/명시적 nonfixed spacing 선언이 있는 각 숫자 범위에만 광학 예외를 적용한다. 미선언 range, 숫자 내부, 다른 기호·숫자·어절·URL, client-fixed spacing/newlines를 보존한다. source나 raw를 변경하거나 원문으로 관찰을 대체하지 않는다. 새 함수는 기존 helper·packet·case 어디에도 연결하지 않았다.

새 단위 검증 8개는 허용 간격의 동등성·idempotence·입력 불변, 72개 숫자 변형·다른 기호·역순, 미선언 range, 어절/숫자 내부 변화, 고정 공백/줄, URL, 잘못된 선언, 선언 없는 기존 v1의 실제 pure 함수와의 호환성을 확인했다. 허용 간격 변형은 서로 다른 다섯 수치 쌍에 25개씩 총 125개다. baseline 비교는 현재 summary의 normalize 함수 AST만 격리해 실행했으며 round helper의 CLI·packet·summary·critic을 실행하지 않았다. 실제 단위 검증은 exit 0, 8 tests OK였다. 테스트는 이미지 품질·평가 절차·actor 종료나 통합 성공을 증명하지 않는다.

숫자 범위의 실제 의미, 사용자 공백 고정의 해석과 메타데이터 공급 위치, shared module을 helper chain에 넣을지 두 함수에 동일하게 적용할지, actual summary digest와 의존성 핀, 새 버전의 rules/producer/preparer 문장 및 기존 역사 verification과의 구분은 남는 **선택적 통합 결정**이다. 새 구현은 완성된 평가 bundle이라고 주장하지 않는다. 현재 v1을 계속 쓰거나 숫자 범위가 없는 Title-only·Title+body를 먼저 설계하는 데 이 초안은 관문이 아니다.

R22의 두 단계에는 frozen v1을 유지하고 재점수·소급 정규화·평가자 교체·비교 재계산을 하지 않는다. 7항목 각 4 이상·세 다양성 각 4 이상은 그대로다. normalized equality가 typography 점수를 끌어올리거나 실제 서체/코드포인트 적용을 증명하지 않는다. 스타일·폰트 조화·본문의 읽기 흐름을 최초부터 구현하는 디자인 개선이 여전히 본 작업이다.

구체적인 계약은 [policy.md](policy.md), 전체 위치·현재 핀은 [integration-map.json](integration-map.json), 실제 검증과 남는 결정은 [status.json](status.json), 새 파일 목록·해시는 [changed-files.json](changed-files.json)에 기록한다. 쓰기는 이 새 초안 디렉토리뿐이며 기존 LIVE·R22 case/helper/raw/score·역사 기록·git을 변경하지 않았다. 새 render·native·critic·case/job을 만들지 않았다.
