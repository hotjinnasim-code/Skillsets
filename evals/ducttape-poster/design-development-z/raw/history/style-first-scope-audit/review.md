# Style-first 독립 범위·일관성 감사

현재 candidate-style-first 12파일과 LIVE Y 12파일을 비교했다. 미해결 범위 문제는 없다. 이 기록은 지침과 전향적 준비 코드의 정적 감사이며, 포스터 품질 PASS나 실제 운영 성공을 뜻하지 않는다.

## 지침 범위

9파일이 변경됐고 `scripts/make_layout_guide.py`, `references/layout-guide-contract.md`, `references/reference-catalog.json`은 바이트가 동일하다. 현재 24개 파일 해시는 작성 기록의 원본·초안 핀과 모두 일치한다.

초안은 선택한 스타일 정체성을 먼저 설계하고 이미지 표현·편집, 색 관계, 타이포그래피의 목소리, 재료 마감과 분위기를 함께 구현하도록 한다. 좋은 구도, Title/body 역할 순서와 정렬은 공유할 수 있다. 다섯 구도·서로 다른 첫 문구 역할·정보 순서·색 또는 폰트 개수의 강제 조건은 남아 있지 않다. 단순 필터·색·폰트 교체만으로 스타일 차이를 단정하지 않는 지침과도 모순되지 않는다. 모든 요소가 매번 달라야 한다는 의무도 추가하지 않았다.

Y의 Title 역할은 즉시 인지되는 강한 주 타이포그래피 앵커로 유지된다. 항상 첫 시선·중앙·최대 고정 픽셀·고정 비율을 요구하지 않는다. 폰트의 광학적 조화와 읽히는 body/footer, 실제 안내의 연결된 읽기 흐름, 내용이 있는 이미지의 전체 기능도 유지된다. 레이아웃 공유 허용은 단색 배경·고딕 정보판이나 빈 장면을 카피 받침으로만 쓰는 기본값의 제외를 해제하지 않는다.

역할은 공급된 실제 카피에만 매핑한다. 없는 eyebrow/subtitle/footer/일정/장소/URL을 만들지 않는다. Title-only는 Title만으로 완성하며, Title+body의 두 역할에 별도 실용 안내가 없으면 복합 행사 안내 스케치를 강요하지 않는다. 사용자 수량·좁은 스타일·자산·명시 배치·역할 순서·no-copy와 단순 작업 범위를 우선한다. 실제 복합 카피와 실용 안내가 있고 기존 렌더러가 사용 가능할 때의 최초 호출 전 실제 폰트·카피 및 실질적 이미지 관계 스케치는 유지된다. 자원이 없거나 단순한 경우의 native 긍정 명세 fallback, native 최종 출력, 기존 bounded 수리도 유지된다. 원본 레퍼런스 재열람·설치·승인을 새 의무로 만들지 않았다.

7개 개별 점수 표와 각 4 이상, 세 평가자 다양성 각 4 이상이라는 수치 조건은 바이트가 동일하다. `evaluation-loop.md`의 1개 표, `art-direction.md`의 2개 표와 해당 수치 문단도 그대로다. 다만 다양성의 설명은 최신 사용자의 ‘스타일 차이 우선·좋은 레이아웃 공유 가능’에 맞춰 전향적으로 바뀌었다. 전체 평가 방법이 완전히 동일하다고 주장하지 않는다. 기존 R21 및 이전 원점수·평가·보고를 다시 읽거나 소급 판정하지 않았다.

## 준비 스크립트 최초 발견과 root 수정

최초 검토 버전은 SHA-256 `2bd1f68406c9cdcd04762217344ed91e55bfe8ce1270330c3fb3006229bfd52d`, 6878바이트다. 두 구체 문제를 root에 먼저 전달했다. archive index와 human steering 핀이 LIVE 복사 뒤에 있어 전제 실패 시 이미 채택된 상태가 남을 수 있었고, archive 검증 플래그가 R21 종료 기록의 현재 바이트와 실제 보관본에 충분히 연결되지 않았다.

Root가 원버전을 [before.py](../style-first-preparation-amendment/before.py)에 보존하고 [after.py](../style-first-preparation-amendment/after.py)와 [수정 기록](../style-first-preparation-amendment/status.json)을 작성했다. 현재 준비 스크립트는 SHA-256 `c7ea99f391e263706707f08050aad3eba4b559fe03464ed47abe8cf98fe48dc5`, 7689바이트이며 수정 보관본과 정확히 같다.

현재 버전은 archive index/verification, human steering, old case, source closure 핀을 모든 복사·LIVE 변경 전에 만든다. index의 source_root가 R21인지 확인하고, closure의 단일 index row와 현재 source 및 실제 archived closure의 해시·바이트를 모두 일치시킨다. 이후 prepared/adoption 기록은 이미 만든 핀을 재사용한다. 두 최초 발견은 현재 정적 코드에서 해결됐다.

단일 이전 case의 실제 copy·count·ratio·style·asset 조건을 보존하며 사용자 스타일/레이아웃 요청의 한 문장과 대응 조건만 정확히 한 번씩 바꾸도록 확인한다. R21 전체 종료 및 archive 검증, 기존 Y runtime/helper 핀과 LIVE 일치, 독립 초안 감사 핀 검사가 새 R22 복사 전에 놓여 있다. 기존 frozen helper의 상대 경로를 유지해 copy2로 복사하고 실행하거나 새 평가 체계를 만들지 않는다. 이 감사는 정적 흐름만 확인했으며 R21 실제 closure/archive/helper/raw를 다시 열어 실제 20개 파일의 운영 상태를 재검증하지 않았다.

## 실제 확인과 한계

상대 Markdown 링크 32개와 anchor 9개가 모두 해소된다. 기존 venv에서 표준 quick_validate를 Python -B로 실행해 exit 0, `Skill is valid!`를 받았다. agent YAML도 읽을 수 있으며 default_prompt 형식이 유효하다. 현재 준비 스크립트의 AST 문법은 유효하고 root 수정 전·후·현재 핀이 맞는다. 형식 검증은 이미지 품질이나 실행 분기 검증이 아니다.

준비 스크립트와 분기를 실행하지 않았고 새 round22는 열람 시 존재하지 않았다. 이미지·critic·child·가짜 점수·새 테스트 사례를 만들지 않았다. 실제 native 스타일 차이·마감·다양한 내용으로의 품질 일반화와 준비 스크립트의 실제 운영은 미검증이다. 본 감사의 쓰기는 이 review.md와 status.json 두 새 파일뿐이며 draft·LIVE·코드·round21·기존 raw/history·git을 변경하지 않았다. 현재 초안 12개와 준비 스크립트의 정확한 핀, 최초 발견과 해결 내역은 [status.json](status.json)에 기록했다.
