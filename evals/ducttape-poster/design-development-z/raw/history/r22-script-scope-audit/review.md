# R22 운영 스크립트의 정적 범위 감사

현재 세 스크립트의 미해결 범위 문제는 없다. 최초 freeze 비교 누락과 보고서 문장 순서 개선을 root에 전달했고, root가 원버전과 수정본을 별도 보존했다. 현재 freeze는 request·copy·conditions·assets·count·ratios·styles·roles 여덟 필드를 모두 case와 비교한다. 실제 준비 case와 plan도 여덟 필드가 모두 같다. 이는 기존 요청 보존 불변식의 보완이며 새 품질 기준이 아니다. 보고서 문장은 사용자의 스타일 우선 지시와 조건 변경이 R22 생성 전에 있었다고 분명히 정리됐다.

준비된 runtime 12개와 actor helper 20개의 현재 해시·바이트가 prepared 기록과 일치한다. 최초 호출 전 freeze는 이 핀과 case·이전 종료 기록을 확인하고, 자기 guide 입력을 공급하며 실제 view 기록의 guide 해시를 연결하도록 한다. 스타일 정체성 우선, 좋은 Title/body 순서·정렬 공유 허용, 실제 Title와 읽히는 body/footer, 추가 문구 금지와 native 최종 출력 원칙이 유지된다. 일반 Title-only·Title+body 범위는 채택된 지침에 남아 있고, 이 R22 case는 실제 12문구를 공급하므로 case 전용 guide의 12항목 조건이 없는 역할을 만드는 것은 아니다. 다섯 guide spec은 실제 12문구와 줄 재구성이 일치하고, native brief의 인쇄 tail도 각 정확한 12문구다. 원작 재열람·최종 overlay·폰트 적용 인증·새 시각 품질 floor가 추가되지 않았다.

Maker 종료는 원 frozen compact preparer의 terminal 검증을 그대로 재사용한다. 선택 또는 세 번 모두 실제 실패한 unavailable만 닫히며 unavailable의 선택은 null이다. 한 최초 호출과 최대 두 수리, 총 최대 15호출을 유지한다. 최초 실패 뒤 선택 반환이 있으면 최초 단계는 UNREADY이며 선택 단계는 별도의 fresh whole-three가 가능하다. 동일 최초본은 유효한 전체 문맥의 원 세 평가만 reuse한다. 불완전·절차 오류의 reuse는 UNREADY로 남고 새 critic으로 구제하지 않는다. 각 UNREADY 단계는 readiness 오류와 5 NA·새 점수 0·새 critic 0을 기록한다.

Full closure는 원 summary의 낮은 점수·NA·절차 오류·다양성을 그대로 옮긴다. 단계당 세 profile·15 image/profile·105점이라는 기대 수와 7항목 각 4 이상·세 critic 다양성 각 4 이상은 유지한다. 실제 프로세스 종료와 절차 유효성은 구분하고 nonzero critic exit도 completion/trace와 함께 남긴다. 새 critic process 수 0/3/6과 실제 trace session 수를 따로 집계하며, reuse·UNREADY를 새 점수·세션으로 세지 않는다. maker completion·terminal 핀을 확인하므로 평가 뒤 재선택을 감추지 않는다. 다양성 설명의 스타일 우선 해석만 최신 인간 지시에 따라 전향적으로 바뀌며 이전 점수는 소급하지 않는다.

현재 세 스크립트 모두 AST 문법이 유효하다. freeze 현재 SHA-256은 `71337dc5f98bfa59dc861b5cee9d314f3eae5984effab71ef9d1c6f32d8e2000`(8823바이트), full closure 현재 SHA-256은 `c5dd9c3777e72ac0a7d268d2ca980f81ed2b41dabfc64109b8c37301ca63b69b`(14697바이트)이며 각각 root 보존 after와 동일하다. 실제 코드·분기·render·native·critic은 실행하지 않았다. root의 guide 열람은 이 감사자가 이미지 품질을 검증했다는 뜻이 아니다. 최대 세 worker는 선언된 운영 제한이며 실제 동시 실행 증거로 인증하지 않는다. 새로운 품질 PASS나 모든 요청 성공도 주장하지 않는다. 쓰기는 이 review.md와 [status.json](status.json)뿐이며, 상태에 현재 세 코드와 case·plan·prepared 및 두 수정 기록의 정확한 핀을 보존했다.
