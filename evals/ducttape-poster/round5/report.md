# 덕테이프 포스터: 재질·자형·접점 전이 평가

선택 14장과 추가 제약 전이 1장의 **사전 핵심/다양성 기준은 PASS**다. 문구·사용자 조건을 먼저 확인하고 내용·형태, 타이포그래피, 이미지·재질, AI 슬롭은 모든 해당 평가자에게 각각 4 이상, 다중 이미지 세트 다양성도 각각 4 이상이어야 한다. 평균으로 낮은 점수를 상쇄하지 않았다. [선택 근거](raw/planning/final-delivery-evidence.json), [오프라인 갤러리](gallery.html), [정확한 바이트 대응표](archive-index.json)를 함께 제공한다.

이는 여러 버전의 검증된 선택 모음이다. 최신 G 전체를 14장 새로 생성한 시험이나 모든 미래 입력의 품질·인간 제작 여부·실제 제품 기능·인쇄 적합성의 보장이 아니다. 가장 최근 G는 서로 다른 새 원본 3개를 검사했다. 이전 전체 FAIL과 낮은 점수·평가 차이도 보존했다.

## 일반 사용과 변경

기본 요청은 중앙 조정자가 내용에서 다섯 방향을 정하고 제작자 다섯 명이 한 장씩 맡는다. 가용 자리가 다섯이면 동시에 시작하고, 자리가 적으면 5개 역할을 유지해 나누어 실행한다. 사용자 지정 수량·스타일·참조와 한 장의 후속 수정이 우선한다. 이 환경은 root 포함 4자리였으며 실제 정원 기본 5개 역할은 2+2+1로 실행했다. 정원 호출 구간의 최대 중첩은 2, 전체 기록의 최대 중첩은 3이다. 다섯 명의 실제 동시 실행을 주장하지 않는다. 협업 도구가 없으면 직접 동일 기준으로 만들고 에이전트 실행을 주장하지 않는다.

일반 생성에는 별도 세 평가자를 강제로 추가하지 않는다. 이번 개선 요청에서 생성·수정과 독립된 평가자 세 명의 루프를 실행했다. 기본 스타일은 고정 목록 대신 내용의 행동·구조·글자·매체에서 결정하며, 주제보다 효과가 먼저 보이는 범용 패키지의 우선순위를 낮춘다. 사용자가 지정한 네온·3D·거친 표현은 같은 완성도 기준으로 존중한다.

동결 D에 E/F/G의 일반 지침 6문단을 더했다. E는 카피·공간의 실제 관계를 먼저 정하고 생성 뒤 찾도록 한다. F는 표면의 세부가 대상 규모·빛·초점에 맞는지, 국소 보정 밖의 사진 표면·윤곽도 변했는지 비교한다. G는 긴 문자열·혼합 문자의 자형에 맞춰 폭과 크기를 확보하고, 압축 대신 면적·줄 묶음·간격을 조정하며, 실제 글자 끝과 대상 경계의 접점까지 설계한다. 스타일 금지·새로움 강요·평가 점수 인상으로 해결하지 않았다. [G 동결](raw/continuation-g/planning/phase-plan.json)에 실제 적용 6파일 해시와 호출 전 경계를 남겼다.

## 자료와 적용 판단

앞 단계에서 실제 확인한 공식 디자인 자료와 GitHub 경로 이력을 [고정된 조사 출처](raw/planning/research-provenance.json)로 재사용했다. 28개 디자인 이미지의 확인 이력이 있으며 이번 단계에 다시 열었다고 주장하지 않는다. 원작 픽셀·카피·로고·구도를 제작자나 저장소에 이식하지 않았다.

[Everyday Practice 2025 한국 예술축제](https://everyday-practice.com/2025-korea-art-festival/)와 [2026 대한민국 문학축제](https://everyday-practice.com/2026-%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD-%EB%AC%B8%ED%95%99%EC%B6%95%EC%A0%9C/)의 실제 정보 위계, [HAY Backflip 공식 자료](https://www.hay.com/news/news-2026/backflip-chair-by-gudmundur-ludvik)의 접힘·접점, [2019 시민 민요축제](https://everyday-practice.com/the-1st-folk-song-festival-poster/)의 운영 정보 관계를 비교했다. 이는 새 구성에 적용한 해석이다. 2026 문학축제 페이지 게시일은 10월 6일이고 HAY의 정확한 게시일은 확인되지 않았다. [frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)와 [canvas-design](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md)의 실제 경로 커밋도 앞 단계 출처 기록에 고정했다.

## 독립 평가 이력

각 행은 그때의 전체 익명 패킷 결과이며 서로 다른 평가자의 원점수다. 사전 원본/너비720/장변320 세 보기를 실제 열고 각 카피를 수동 전사했다. 새 신청 포스터는 원문 패킷 전에 720에서 행사일·신청 기한·전체 URL·위치를 읽어 저장했다. 첫 보정의 craft는 저장 실패 뒤 원문을 열었음을 기록했고, 사전 선언한 추가 ordered craft를 포함해 **네 평가자의 점수를 모두 유지**했다. 그 절차 실패를 소급 해소하거나 불리한 점수를 버리지 않았다.

| 단계 | 패킷 이미지 | 평가자 | 핵심 <4 | 기타 <4 | 세트 다양성 <4 | 판정 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| D 초기 | 9 | 3 | 9 | 7 | 5 | FAIL |
| E/D 첫 보정 | 9 | 4 | 18 | 9 | 4 | FAIL |
| E/D 두 번째 보정 | 9 | 3 | 10 | 2 | 0 | FAIL |
| F 사진 전이·이전 짝 | 4 | 3 | 5 | 4 | 1 | FAIL |
| G 자형/접점 전이·F 짝 | 5 | 3 | 2 | 6 | 2 | FAIL |
| F/G 첫 보정 묶음 | 5 | 3 | 2 | 2 | 2 | FAIL |
| F/G 두 번째 보정 묶음 | 5 | 3 | 2 | 1 | 0 | FAIL |
| T01 마지막 자체 보정 후 전체 묶음 | 5 | 3 | 0 | 1 | 0 | PASS |

[G 전이 전체 리뷰](raw/blind-transfer-correction3/reviews/)에는 F P01 initial, F H01 repair-1, G P02 repair-1, G H02 repair-1, G T01 한 장 제약 선택본이 포함된다. 추가 T01은 글자와 여백만 사용하며 선택 14장의 대체물이 아니다. T01 실패도 최종 완료 기준에 포함하며 단일 결과에 없는 다양성/가까운 짝 점수를 만들지 않았다. 모든 7항목의 원점수·보이는 근거·불확실성과 가까운 짝의 비기준 점수를 유지했다.

F P01 자체 첫 보정은 글자의 역할을 바꾸면서 접힌 컵·뚜껑을 약85–90 원본 픽셀 이동시키고 미세 표면을 다소 부드럽게 했다. [보존 비교](raw/continuation-f/production/P01/repair-1/preservation-inspection.json)에 남겼으며 정확한 사진 보존을 주장하지 않는다. 보정 전후 중 최신이라는 이유만으로 채택하지 않았다.

## 선택 묶음의 기준

정원 5개는 닫힌 correction2의 완전한 세트 근거, 제품·모집 각2개는 최신 전이의 완전한 세트 근거다. 그대로 유지한 해안 정화2·명시 네온2·사진 독서대1은 [이전 5장 대응 근거](raw/planning/retained-five-bindings.json)의 원본·실제 보기·리뷰·절차 63개 파일과 해시로 연결한다. 전체 옛 FAIL을 새 선택 PASS로 복사하지 않았다. 아래는 각 사례의 모든 이미지/평가자 중 최저점이다.

| 사례 | 내용·형태 | 타이포 | 이미지·재질 | AI 슬롭 | 다양성 |
| --- | ---: | ---: | ---: | ---: | --- |
| title-only | 4 | 4 | 4 | 4 | 4 |
| product | 4 | 4 | 4 | 4 | 4 |
| invitation | 4 | 4 | 4 | 4 | 5 |
| coast-cleanup-dense-action | 4 | 4 | 4 | 4 | 4 |
| moonroll-explicit-3d-neon | 4 | 4 | 4 | 4 | 4 |
| heldout-fold-stand-photograph | 4 | 4 | 4 | 4 | 단일 |
| type-only-control (추가) | 4 | 4 | 4 | 4 | 단일 |

핵심 네 항목 외에 4 미만으로 남은 관찰은 다음과 같다. 위치·원인과 모든 점수 차이는 원본 근거에 있다.

| 역할 | 평가자 | 항목 | 점수 |
| --- | --- | --- | ---: |
| H01 | transfer-correction3/craft | space | 3 |

## 실제 파일과 닫힌 경계

| 역할 | 버전·단계 | 실제 원본 크기 | 파일 |
| --- | --- | --- | --- |
| G01 | E / repair-1 | 1024×1536 | [원본](images/native/be3826a83dcb46942cd8f8767c30e88fdd7094ae5f69f0e32bc522b31ccef6b6.png) · [720](images/qa/0bc6ef4b094217a2b6a622821cd5b42c5b6b3c612da095b23aaaeeef607d1eb4.png) · [320](images/qa/09d1013c69b3ba75647daae544be471d10e1a0a617cee788aaceb09ba57fad09.png) |
| G02 | D / initial | 1024×1536 | [원본](images/native/cb049b0b1893183618109381b268b9169cd7fc77786847bee8eeee546f2e285e.png) · [720](images/qa/1c675e08b33d4a435d236826620f4c18b11a8e623d1516e0237f909fe337f6fe.png) · [320](images/qa/d12366384a00f65e0454b364042dfc90b003b91ba3d2f09029b603a2b1a801e1.png) |
| G03 | D / repair-1 | 1024×1536 | [원본](images/native/91c4ef1ec433aee5e06e5f14d8ec1cc0bfb038f162d747fde1c1b23efe56efef.png) · [720](images/qa/2bd61169e0e0fba216209704172c4d70abfb43fc33e227cd9f04ef402bdc2a2d.png) · [320](images/qa/fec5c2872fb32033fbdded3894f8b3c8f30d342b7e11c5fe6135779dde9cedc1.png) |
| G04 | D / repair-1 | 1024×1536 | [원본](images/native/40e723612be8e1bc2235cae327e77cf1f01c39df0f4f6c2039250e8fb554fef8.png) · [720](images/qa/f5769c9fea6b7cfbca9120c0544d8000aca9f6d5aba2a8bfcdbe904a02bb14ed.png) · [320](images/qa/870b72a779551350cda3864878845e64b7a0ab033e6308d08d9447239b94c9f6.png) |
| G05 | D / initial | 1024×1536 | [원본](images/native/9312eb18556e5f0ae6a979bdc45e41c2407851090f75717bcb63df996665a707.png) · [720](images/qa/1bc068c53f1e0933a82e967bca076d7ab6293d50a8c3e2fca6391b6a4ef9cc17.png) · [320](images/qa/2482fcb3c16fa38209254c8cb638c87333603601e473ae83d3aef61854363824.png) |
| P01 | F / initial | 1122×1402 | [원본](images/native/c83e7dfe464e0d91d553280b8af336948f551bd1f29a29b8da5ab3e083eaa47a.png) · [720](images/qa/8bee799908ce1569d131018bbeb0d5ea425a09f42269e436deac57c03914f075.png) · [320](images/qa/d8ee47bb79eb5dbc1e1efebb759cf4985adc5e104d0243e4a327da4ca9f2aa4c.png) |
| P02 | G / repair-1 | 1122×1402 | [원본](images/native/0d8f04cfd80133777b10214e562bb4d21d7026e91bfc9c25be3a0b902be242bc.png) · [720](images/qa/d7cbc6cdfb822d2d315928e65e614374b23e4d54af30990d439f546d3c974aa0.png) · [320](images/qa/7c5be600cdbe319e4a301398a81b3ebac2f97da202cafb1ec02f805d1251d15b.png) |
| H01 | F / repair-1 | 1086×1448 | [원본](images/native/533a73254f33c20bbabe90d8988629de3d6b79558ab9362455f410af55f5aaf0.png) · [720](images/qa/774d515d85955016de50db29d8041d656e6f62dda04582de2e6f70e3027d3a88.png) · [320](images/qa/c2cc1ceadd43daeda589eb50dc7d630f51049ebcb77ead09e0773e2242baaa7a.png) |
| H02 | G / repair-1 | 1254×1254 | [원본](images/native/5e694d0c7522f61ebfef3ba87c196247209dae8c0eef8052599199765f803754.png) · [720](images/qa/5f11a78e80c1cdf0f1b0712d684dc32a8ecfc45f0ac2cd445a6cfc21f799a32a.png) · [320](images/qa/358c0057d40f0684bf494938433642e1a5dc93b1f6d12fb02b03163d128bd3d0.png) |
| C01 | 이전 / repair-2 | 1024×1536 | [원본](images/native/eb45e009c26cd1ebcb23e78c7e29dc83a86c74f9d4f18f910d1f4739f677d31b.png) · [720](images/qa/88bd3cfc388f17d97dbd4170b101939d11c29b7867da5691d2d981e17fcaec8f.png) · [320](images/qa/eeaa3410b0e067fcbc4d7e2af51b26d960da8b599eb999b5c51501036205b25c.png) |
| C02 | 이전 / repair-2 | 1536×1024 | [원본](images/native/fc639332d9ce3415dd7f0fb5581ba880290adede97684ebeb45b6e8fdb7add93.png) · [720](images/qa/cdaf8053d54e19ea925ce9477b9aa594c862e76cc928a3c760e64858c55eb64c.png) · [320](images/qa/0a38d3c7470f0cc419af822efe80fd05d5dd3e068fce078c752626bebd31933f.png) |
| N01 | 이전 / repair-1 | 1254×1254 | [원본](images/native/e18c07736614e2ac42b91da28f0be3ed736da6e6bf407777d9657ac220d81eb7.png) · [720](images/qa/db07ae4c413e53183bdff11fe7efd98c9d718ddd8ce7be521f00cb02584bd117.png) · [320](images/qa/c7e54101c969b30a0465ba740f69739a8710fb8eea7f18fa905779b78127d738.png) |
| N02 | 이전 / initial | 1254×1254 | [원본](images/native/9877d996f499455ab0d38197604617718d30338e09790ed5f5b1ad2b39ba8d99.png) · [720](images/qa/441358fcd4d3f51b050e73d93d2d33c82d5b17d9f0ea48af34bf5224b64547a5.png) · [320](images/qa/016df235732db464c9bb08883cb02c82fb450ef184b4bb2886448b8a7da16c30.png) |
| H03 | 이전 / repair-1 | 1536×1024 | [원본](images/native/28aa99c4b306148d2b6d6ebf8080b266e13376f8d784cddc56b4add5e853f701.png) · [720](images/qa/d57dcc47f9da51c1e6c04c9d2bb1dfc422fe4109bb73d1b3a20aa45ba72bd074.png) · [320](images/qa/1a736a37843cc9ed04b2b54b5fa860b0f55e4eb750a19d1d993e77669692e0b5.png) |

원본 바이트를 보존하고 확인용 720/320만 축소했다. 1122×1402의 4:5 상대 오차 0.035663%는 사전1% 허용 안이지만 수학적으로 정확한4:5라고 부르지 않는다. 내장 도구에 가능한 최대 해상도를 요청했으며 실제 크기는 위에 공개한다. 도구가 크기 설정을 제공하지 않아 최대 달성을 인증하지 않았다.

| 단계 | 실제 호출 | 변경하지 않은 상한 | 미사용 폐기 |
| --- | ---: | ---: | ---: |
| D | 16 | 24 | 8 |
| E | 5 | 6 | 1 |
| F | 5 | 6 | 1 |
| G | 7 | 9 | 2 |

앞서 닫힌95회를 포함한 전체 기록은 **128회**다. D/E 호출은116에서 닫아 미사용9회를 폐기했다. 일반 지침을 실제 바꾼 F/G는 각6/9의 별도 사전 경계에서 이전 장면을 참조하지 않는 새 발상을 검사했다. 닫힌 D/E의 숨긴 세 번째 보정이나 상한 초기화로 세지 않았다. 모든 원본은 재생성을 포함해 자체 보정 최대2회를 지켰다. 새 단계 전후의 계획125/122/131 최대값 스냅샷과 도중 INCOMPLETE도 그대로 보존했다. F 계획의 종료 설명에 이전24라는 문구가 남았으나 수치 상한6과 검증기는 처음부터6으로 고정됐으며 실제 호출과 폐기를 공개한다.

[닫힌 호출 검증](raw/planning/full-validation-closed.json), [별도 품질 조립](raw/planning/final-delivery-evidence.json), [이식 가능한 바이트 감사](portable-audit.json)를 구분한다. 저장소 대응표를 사용하는 감사는 옛 작업 폴더 없이 해시·PNG 치수·리뷰 원점수·보기·절차를 확인한다. 실제 보기/선행 순서/위치 근거는 평가자의 기록이며 코드가 시각 판단이나 시간 순서를 인증하지 않는다. 옛 전체 패킷·리뷰에 언급된 미선택 비교 원본 전체까지 보관했다고 주장하지 않는다. 브라우저 렌더링 검수를 수행했다고 주장하지 않으며 갤러리는 파일 대응으로 확인했다.


## 절차 오류와 보존 비교

transfer-correction1은 품질 FAIL이며 H02 제작 기록의 해시가 평가 묶음 고정 이후 변경돼 전체 출처 연결도 FAIL이다. 원본 이미지 바이트는 같았지만 옛 기록을 소급 통과시키지 않았다. [불일치 기록](raw/planning/transfer-correction1-manifest-drift.json)을 보존하고 다음 전체 묶음은 제작자의 저장 완료 뒤 새로 고정했다. 마감일 필드에서 “신청”을 제외한 관찰도 마감일로 읽도록 형식 어댑터를 수정했으며, 전체 문구 대조와 평가 원점수는 그대로 남겼다.

F P01은 자체 두 보정에서 남은 타이포 문제를 기록하고, 사전에 원본을 다시 선택해 변경된 짝과 함께 전체 사례를 새로 평가했다. 이전 짝의 다양성 점수를 빌려오지 않았다. F H01의 첫 보정은 렌즈·금속 미세 표면이, G P02의 첫 보정은 천의 미세 결이 바뀌었다. [H01 비교](raw/continuation-f/production/H01/repair-1/parent-comparison.json)와 [P02 비교](raw/continuation-g/production/P02/repair-1/parent-comparison.json)에 남겼으며 정확한 사진 보존을 주장하지 않는다.

[별도 사전 감사](raw/planning/pre-archive-independent-audit.md)는 G의 제약 사례 T01 근거를 빼도 조립기가 통과하던 결함을 발견했다. 수정 뒤 T01 누락을 거부하는지 확인했으며, 기존 FAIL의 점수·보기·해시는 보존했다.

transfer-correction2의 제품·모집 사례는 세 평가자 모두 핵심·다양성 기준을 통과했지만, T01에서 한 평가자가 희미한 이중 글자 윤곽에 이미지·재질 3과 AI 슬롭 3을 주어 전체는 FAIL이다. [마지막 자체 보정 사전 계획](raw/continuation-g/planning/T01-repair-2-plan.json)은 해당 원인만 고치도록 제한하고, 두 번째 보정 뒤에도 전체 다섯 이미지를 새 평가자 세 명이 판단하도록 정했다. 불리한 평가자를 제외하거나 점수를 평균내지 않았다.

T01 두 번째 보정은 검정 채움이 균일해졌지만 제작자는 희미한 윤곽과 바탕 얼룩의 완전 제거를 확인하지 못했다고 [검수](raw/continuation-g/production/T01/repair-2/inspection.json)에 남겼다. 마지막 독립 판정과 이 불확실성을 함께 보존하며, 통과를 모든 합성 흔적의 절대적 부재로 해석하지 않는다.
