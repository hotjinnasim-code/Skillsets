# Style-first 아이디어 보강의 좁은 독립 범위 감사

미해결 범위 문제는 없다. 새 candidate-style-first-ideas는 이전 candidate-style-first에서 `references/visual-research.md`만 변경했으며 나머지 11파일이 바이트 동일하다. LIVE Y 대비 기존 9변경·3동일 범위도 유지된다. 이전 초안 12개와 독립 scope 기록 두 파일, LIVE Y 12개는 이전 감사 핀과 정확히 같다.

추가는 기존 관찰을 현재 내용의 표현 결정으로 옮기는 선택적 예시 네 묶음이다. 여섯 source ID의 catalog 관찰·facts 텍스트를 확인했다. BP2025-009/072는 명암·선택 색·초점 차이를, BP2024-086은 사진·그림·편집과 스케일의 관계를, east-FNT-02/04는 획·열림·평면 색·곡선 동작·이미지 경계를, east-SM-03은 큰 면·가는 선·중첩·미세 표면을 뒷받침한다. ‘사진의 거리’, ‘Title의 목소리’, ‘식별·해석·스케일의 역할’ 등 새 내용에 적용하는 말은 관찰에서 가능한 설계 해석이며 원작에서 확인된 모든 사실이라는 표현은 아니다.

예시는 현재 내용에 맞는 선택과 이유를 요구하되 모든 차원을 채우는 서식, 작품 하나당 결과 하나, 고정 스타일 메뉴, 다섯 레이아웃 차이, 새 카피 역할 또는 새 평가 기준으로 만들지 않는다. 원작 얼굴·베일·손글씨·정물·격자·로고·삼원색 조합·인물·제목 모양·원호 안내를 이식하지 않도록 명시한다. 색·형태·배열을 정답으로 복제하게 하지 않는다. 거친 표면을 실제 인쇄 공정으로 확정하거나, 극도로 가는 원작 활자를 긴 한글 본문의 정답으로 삼는 지침도 없다. 새 문단은 원작의 작은 글자·폰트 파일·인쇄 공정이 모두 확인됐다는 뜻이 아님을 직접 명시한다. native 품질 성공이나 폰트 파일 적용의 검증도 주장하지 않는다.

Title-only와 Title+body의 실제 역할만 사용하는 지침, 명확한 Title 및 조화로운 폰트와 읽히는 본문, 좁은 사용자 수량·스타일·자산·명시 배치의 우선, 복합 안내의 조건부 스케치와 자원 미사용 가능 시 fallback, native 최종 조건은 해당 문서 11개의 바이트 동일성으로 보존된다. 7개 기준·각 4 이상과 세 critic 다양성 각 4 이상 수치 문단도 평가 문서가 그대로라 보존된다. 이전 스타일 우선 감사가 명시한 다양성 설명의 전향적 해석 변경은 그대로이며 원점수·기존 기록에 소급하지 않았다.

준비 스크립트는 이전 감사본 7689바이트를 보존한 prepare-before.py에서 DRAFT와 scope_audit 두 경로만 새 초안·새 감사 경로로 바꿨다. 현재 7700바이트, SHA-256 `b01034669f518936debbdba2bc0c17996ed63a8c3bd49e9172cc3d45ba4d3849`이며 prepare-after.py와 정확히 같다. AST 문법은 유효하다. 이미 감사한 운영 흐름, 사전 핀 및 R21 closure/archive 바인딩·helper 보존 조건은 두 경로 외에 동일하다. 준비 코드와 분기는 실행하지 않았다.

상대 링크는 기존 32개에 catalog 링크 하나가 더해져 33개, anchor는 9개이며 모두 해소된다. 기존 검증된 SKILL.md와 YAML이 바이트 동일해 quick_validate를 다시 실행하지 않았다. 이는 기존 형식 검증의 보존이며 실제 생성 품질 검증이 아니다.

이번 감사는 여섯 출처의 기존 텍스트를 읽었고 새 source 이미지·웹·R21 raw/archive·Y development를 열지 않았다. 새 이미지·guide·critic·점수·child·R22를 만들지 않았으며 LIVE·초안·코드·이전 기록·git도 변경하지 않았다. R22는 확인 시 존재하지 않았다. 쓰기는 이 review.md와 [status.json](status.json)뿐이다. 상태에는 현재 초안 12개와 준비 스크립트의 정확한 핀을 기록했다. 실제 실행·native 표현 차이·마감·모든 내용의 품질 일반화는 이번 정적 감사로 인증하지 않는다.

기존 전체 감사: [review.md](../style-first-scope-audit/review.md) · [status.json](../style-first-scope-audit/status.json). 보강 근거: [idea-review](../style-first-idea-review/review.md) · [root amendment](../style-first-idea-amendment/status.json).
