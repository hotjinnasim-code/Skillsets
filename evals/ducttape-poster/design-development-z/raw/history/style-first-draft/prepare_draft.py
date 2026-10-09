from pathlib import Path
import hashlib
import shutil
import json
import difflib
import sys

ROOT = Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster')
SOURCE = ROOT / 'Skillsets/skills/ducttape-poster'
DRAFT = ROOT / 'drafts/candidate-style-first'
HISTORY = ROOT / 'history/style-first-draft'

def pins(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob('*')) if p.is_file()}

source_pins = pins(SOURCE)
assert len(source_pins) == 12
if '--resume-own-incomplete-draft' in sys.argv:
    assert DRAFT.exists()
    assert not (HISTORY / 'pins.json').exists(), 'Do not overwrite a completed draft.'
    assert set(pins(DRAFT)) == set(source_pins)
    for rel in source_pins:
        shutil.copy2(SOURCE / rel, DRAFT / rel)
else:
    assert not DRAFT.exists(), 'Do not overwrite an existing draft.'
    shutil.copytree(SOURCE, DRAFT)
edits = []

def paragraph(rel, prefix, replacement):
    p = DRAFT / rel
    lines = p.read_text().splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(hits) == 1, (rel, prefix, hits)
    lines[hits[0]] = replacement
    p.write_text('\n'.join(lines) + '\n')
    edits.append({'path': rel, 'original_prefix': prefix})

def phrase(rel, old, new):
    p = DRAFT / rel
    text = p.read_text()
    assert text.count(old) == 1, (rel, old, text.count(old))
    p.write_text(text.replace(old, new))
    edits.append({'path': rel, 'original_phrase': old})

paragraph('SKILL.md', '내용을 받으면 **서로 다른 스타일',
    '내용을 받으면 **서로 다른 스타일 다섯 개 × 독립된 완성 이미지 한 장 = 총 다섯 장**을 직접 만든다. **스타일의 차이를 우선한다:** 이미지 표현·편집, 색·대비, 타이포그래피의 목소리, 재질·마감과 정서가 함께 만드는 정체성을 현재 내용에 맞게 설계한다. 잘 읽히는 Title·body의 순서와 정렬 구조는 여러 방향에서 공유할 수 있으며 다섯 레이아웃을 전부 다르게 만들 필요는 없다. 축적한 디자인 아이디어, 내용에 맞는 시각적 발상, 카피를 읽게 하는 구조, 이미지와 글자의 마감을 함께 설계한다. 한 장의 후속 수정은 지정한 이미지에만 적용한다. 프롬프트 제공로 제작을 대신하지 않는다.'.replace('프롬프트 제공로', '프롬프트 제공으로'))
paragraph('SKILL.md', '중앙은 [축적한 구성 문법]',
    '중앙은 현재 내용에 맞는 다섯 스타일의 긍정적인 명세를 함께 설계한다. 이미지가 어떤 표현·편집으로 내용을 보여 주며 색·대비, 글자의 목소리, 재질·마감과 정서가 어떤 전체 인상을 만드는지 짧고 구체적으로 전달한다. [축적한 구성 문법](references/design-grammar.md)의 관계 아이디어는 필요할 때 선택적으로 참고하며 원본 작품 재열람을 의무로 만들지 않는다. 제작자는 배정된 스타일과 실제 카피에 맞는 좋은 읽기 구도를 자율적으로 구체화한다. 같은 읽기 순서·정렬·정보 묶음을 공유해도 스타일의 정체성이 뚜렷하면 독립된 방향이 될 수 있다. 고유한 다섯 레이아웃·첫 카피 역할·정보 순서·팔레트·서체 수량이나 고정 다섯 가족을 배정하지 않는다.')
phrase('SKILL.md', 'Title의 명확한 인지와 본문·안내의 읽힘을 유지하면서 전체 구성을 구별한다.',
    'Title의 명확한 인지와 본문·안내의 읽힘을 유지하면서 각 스타일의 정체성을 구현한다.')
phrase('SKILL.md', '새 카피나 역할 수를 다양성의 의무로 만들지 않고 동일한 대제목·중앙 오브젝트·하단 안내 틀을 적용하지 않는다.',
    '새 카피나 역할 수를 다양성의 의무로 만들지 않으며 내용과 무관한 대제목·중앙 오브젝트·하단 안내 틀을 자동 적용하지 않는다.')
phrase('SKILL.md', '무문자·제목만·간단한 카피에는 이를 의무로 늘리지 않으며,',
    '무문자·Title만·간단한 카피와 실용 안내가 없는 Title+body에는 이를 의무로 늘리지 않으며,')
paragraph('SKILL.md', '색·효과·재료 이름을 가린 뒤에도',
    '스타일의 차이는 실제 전체 이미지에서 판단한다. 같은 잘 읽히는 Title·body 순서와 정렬 구조를 재사용해도 이미지 표현·편집, 색·대비, 서체의 목소리·마감·정서가 설득력 있게 다른 체계를 만들면 독립 스타일이 될 수 있다. 색 필터나 글꼴 하나만 바꾼 변주를 완성된 스타일 설계로 대신하지 않되, 각 요소가 모두 서로 달라야 한다거나 레이아웃을 바꿔야 한다는 수량 조건은 두지 않는다. 사용자 지정 스타일·고정 구도·자산 보존 범위 안에서 가능한 차이를 설계한다. 실제 사용자 조건끼리 양립하지 않을 때만 기존 양립 불가 조건 확인 절차를 적용한다. 다섯 장 각각은 완성된 한 포스터이며 작품 안에 번호·스타일명·비교 설명을 넣지 않는다.')
phrase('SKILL.md', '실질적으로 다른 표현 체계와 레이아웃이 구현됐는지,',
    '실질적으로 다른 스타일의 정체성과 잘 읽히는 구도가 구현됐는지,')

paragraph('references/art-direction.md', '읽는 순서는 내용에 따라 달라진다.',
    '읽는 순서는 내용에 따라 달라진다. 제목이 첫 시선일 수도 있고 사진의 사건·날짜·반복되는 정보 구조가 첫 시선일 수도 있다. 실제 카피의 중요도, 제목의 단어 묶음과 폭, 장면의 식별, 안내의 판독을 함께 조정한다. 내용과 무관하게 큰 제목·중앙 오브젝트·하단 카피의 틀을 자동 적용하지 않으며, 내용에 맞는 좋은 읽기 순서와 정렬은 여러 스타일에서 공유할 수 있다. 의도를 장황하게 설명하는 것으로 화면에서 모호한 관계를 보완하지 않는다.')
paragraph('references/art-direction.md', '[구성 문법](design-grammar.md)의 다양한 관계를',
    '다섯 방향은 스타일의 정체성을 우선해 설계한다. 현재 내용을 보여 주는 이미지 표현·편집, 색·대비, 타이포그래피의 목소리, 재질·마감과 정서가 어떤 전체 인상으로 결합하는지 정한다. [구성 문법](design-grammar.md)은 필요할 때 쓰는 관계 아이디어이며 고유한 다섯 공간 구조를 고르는 메뉴가 아니다. 잘 읽히는 Title·body의 순서와 정렬 구조가 같아도 각각의 스타일이 뚜렷하면 독립된 방향이 될 수 있다. 중앙은 제작 가능한 긍정적인 스타일 명세를 주고 제작자는 그 스타일과 실제 카피에 맞는 구도를 선택한다.')
paragraph('references/art-direction.md', '- **표면을 가린 비교:**',
    '- **실제 스타일의 비교:** 이미지 표현·편집, 색·대비, 글자의 목소리, 재질·마감과 정서가 실제 화면에서 다른 정체성을 만드는가? 필터나 글꼴 하나의 교체만을 스타일 설계로 대신하지 않는다. 같은 좋은 레이아웃을 공유하는 것 자체는 겹친 스타일의 근거가 아니며 각 요소가 모두 달라야 하는 것도 아니다.')
paragraph('references/art-direction.md', '- **실제 내용의 비교:**',
    '- **실제 내용의 비교:** 이 제목·문구·사건에 맞는 표현과 읽기 관계인가? 다른 행사 이름으로 바꿔도 대부분 그대로라면 현재 내용을 충분히 보여 주는지 다시 본다. 관련 내용에 재사용 가능한 격자나 시각 체계도 현재 요청을 충분히 해결하면 유효하다. 모든 요청에 유일한 은유나 인간의 행동을 강요하지 않는다.')
paragraph('references/art-direction.md', '구분을 만들려고 사용자 조건을 버리지 않는다.',
    '구분을 만들려고 사용자 조건을 버리지 않는다. 명시한 사진·3D·보색·클레이나 좁은 브랜드 표현을 유지하면서 허용된 표현·편집·색·글자·마감에서 가능한 차이를 찾는다. 요청하지 않은 캠페인 통일성을 추가하지 않으며, 반대로 다섯 개의 고유한 팔레트·서체·레이아웃·정보 순서를 의무로 요구하지 않는다.')
paragraph('references/art-direction.md', '제작 명세를 쓰기 전에 «이미지에 어떤 표현 문법',
    '제작 명세에는 이미지의 표현·편집이 현재 내용을 어떻게 보여 주고 글자·정보와 어떤 관계로 결합하는지 구체적으로 담는다. 기본 정보 판형에 들어갈 바탕 장면부터 만들지 않는다. 방·사물·시점이나 사진·그림의 명칭만 바꿨다는 설명은 스타일 차이의 증거가 아니다. 같은 카피 위치를 공유하더라도 실제 이미지 표현과 글자·색·마감이 다른 전체 정체성을 만들면 독립 스타일일 수 있으며, 위의 제외 구성은 같은 정의로 적용한다.')
paragraph('references/art-direction.md', '이를 피하려고 다섯 장 모두 사진 배경',
    '이를 피하려고 다섯 장 모두 사진 배경·세리프·빈티지 질감으로 통일하지 않는다. 축적한 아이디어를 바탕으로 현재 내용에 맞는 이미지 표현·편집, 색·대비, 글자의 목소리와 마감을 설계한다. 각 방향의 스타일이 만드는 전체 인상이 뚜렷해야 하며, 좋은 읽기 구도를 공유해도 기본 정보 판형과 효과만으로 전체 인상을 대신하지 않는다. 사용자가 비문자 요소를 제외하지 않은 경우에는 글자 판독을 보장하면서 비문자 시각 체계가 내용과 인상을 실질적으로 맡게 한다.')

phrase('references/design-grammar.md', '아래는 서로 다른 발상의 출발점이다.',
    '아래의 22개 관계는 필요할 때 선택적으로 쓰는 발상의 출발점이다.')
phrase('references/design-grammar.md', '## 재료보다 먼저 큰 관계를 설계',
    '## 스타일에 맞는 읽는 관계를 고르기')
paragraph('references/design-grammar.md', '다섯 방향을 ‘사진·판화·회화·콜라주·3D’로 먼저 나누면',
    '현재 내용에 맞는 스타일의 정체성을 먼저 구체화한다. 이미지의 표현·편집, 색·대비, 타이포그래피의 목소리, 재질·마감과 정서가 함께 만드는 전체 인상을 선택하고 실제 카피가 자연스럽게 읽히는 구도로 구현한다. 사진·판화·회화 같은 재료 이름만 나열하지 않고 무엇을 어떤 거리·크롭·형태·빛·표현으로 보여 줄지 적는다. 고급 레퍼런스의 이미지 표현·색·밀도·글자·재질·정서와 읽는 관계 모두가 아이디어가 될 수 있다. 아래의 연속 장면·여러 장면의 편집·반복·집합·도해·공유 경계는 선택 가능한 관계이며 모든 스타일의 공간 구조를 다르게 만드는 의무가 아니다.')
paragraph('references/design-grammar.md', '각 방향을 한 문장으로 그릴 수 있게 쓴다.',
    '각 방향의 명세는 실제 전체 인상이 그려질 만큼 구체적이면 된다. 같은 잘 읽히는 Title·body 순서와 정렬을 공유해도 이미지 표현·편집, 색·서체의 목소리·마감·정서가 뚜렷한 다른 체계로 결합하면 독립 스타일이 될 수 있다. 필터나 글꼴 하나의 교체로 그 차이를 대신하지 않되, 고유한 다섯 레이아웃·첫 카피 역할·정보 순서·팔레트·서체 수량을 요구하지 않는다. 제작자가 배정된 스타일과 실제 카피에 맞는 구도를 선택한다.')
phrase('references/design-grammar.md', '고정 글꼴 목록·공통 정보 패널·공통 다섯 레이아웃을 만들지 않는다.',
    '모든 요청에 고정 글꼴 목록·정보 패널·다섯 레이아웃 메뉴를 강요하지 않는다. 적합한 읽기 구도는 여러 스타일에서 공유할 수 있다.')

paragraph('references/parallel-production.md', '원문·전체 카피·조건과 사용자 자료를 확정한다.',
    '원문·전체 카피·조건과 사용자 자료를 확정한다. 현재 내용과 축적한 아이디어로 각 방향의 스타일 정체성을 설계한다. 이미지 표현·편집, 색·대비, 글자의 목소리, 재질·마감과 정서가 어떤 전체 인상을 만드는지 긍정적인 명세로 전달하고 제작자는 실제 카피에 맞는 좋은 읽기 구도를 자율적으로 선택한다. 잘 읽히는 Title·body 순서와 정렬은 여러 스타일에서 공유할 수 있다. 매 요청의 새 조사나 제작자별 원본 재열람을 기본 단계로 넣지 않는다. 열린 요청에 유명 스타일 하나를 임의로 공유하지 않으며 사용자 지정의 좁은 스타일·브랜드 표현은 공통 조건으로 전달한다. [아트디렉션](art-direction.md)의 실제 스타일·내용 비교를 참고한다.')
phrase('references/parallel-production.md', '같은 굵은 고딕 제목·날짜·안내 패키지를 모든 역할에 공유하지 않고,',
    '굵은 고딕 제목·날짜·안내 패키지만으로 전체 인상을 대신하지 않고,')
phrase('references/parallel-production.md', '**이미지와 실제 카피가 결합한 큰 관계 → 실제 문구의 역할과 명확한 Title·보조 위계 → 핵심 약속과 다음 행동 정보로 이어지는 관계 → 이를 구현할 편집·표현·서체·색·마감**',
    '**현재 내용에 맞는 스타일 정체성 → 구체적인 이미지 표현·편집·색·서체·마감·정서 → 실제 문구의 역할과 명확한 Title·보조 위계 → 존재하는 본문과 유용한 다음 정보로 이어지는 읽기 관계**')
phrase('references/parallel-production.md', '읽기 관계**을 짧게 적는다.', '읽기 관계**를 짧게 적는다.')
phrase('references/parallel-production.md', '명확한 제목 위계와 본문·안내의 판독을 유지한 채 다섯 방향의 큰 이미지와 실제 글자 덩어리의 위치·점유 면적·공유 경계를 함께 설계한다. 가까운 두 방향에 같은 위치의 큰 피사체와 같은 설명·안내 발판이 남으면 재료·첫 구절·주변 가구 대신 그 큰 관계부터 달리 설계한다. 제작자에게 전달하는 대비 조건도 실제 구도·정보 흐름의 차이를 담는다.',
    '명확한 제목 위계와 존재하는 본문·안내의 판독을 유지하면서 각 스타일의 전체 인상을 구현한다. 같은 좋은 읽기 구도는 공유할 수 있고, 다섯 레이아웃·첫 카피 역할·정보 순서·팔레트·서체 수량을 서로 다르게 만들 의무는 없다. 제작자에게는 자기 방향의 긍정적인 스타일 명세와 그 안에서 읽기를 해결할 여지를 준다.')
phrase('references/parallel-production.md', '가까운 방향과의 구분은 중앙이 작성한 큰 형태·글자 역할·공간·읽는 흐름의 짧은 대비 조건으로만 전달하며',
    '중앙은 자기 방향의 스타일 정체성을 짧고 구체적으로 전달하며')
phrase('references/parallel-production.md', '제작자는 실제 전체 카피에 맞춰 이를 구체화하며 공통 정보 패널·폰트·격자를 새로 추가하지 않는다.',
    '제작자는 실제 전체 카피에 맞춰 이를 구체화하며 모든 역할을 통일할 정보 패널·폰트·격자를 임의의 새 조건으로 추가하지 않는다.')
phrase('references/parallel-production.md', '같은 이미지 둘레의 빈 정보 면에 첫 문구나 재료만 바꾼 계획은 큰 관계부터 달리 설계한다.',
    '스케치는 자기 방향의 실제 이미지·글자 관계를 설계하는 수단이며 다른 스타일과 좌표·읽기 순서를 다르게 만드는 의무가 아니다. 실용 안내가 없는 Title+body만으로 이 복잡한 안내 스케치 절차를 의무화하지 않는다.')
phrase('references/parallel-production.md', '나란히 놓인 실제 이미지에서 레이아웃·글자 역할·장면·공간까지 서로 다른지 확인한다.',
    '나란히 놓인 실제 이미지에서 스타일의 정체성이 뚜렷한지 확인한다. 같은 좋은 읽기 순서와 정렬 자체를 다양성 실패로 보지 않는다.')

phrase('references/production-brief.md', '## 전체 장의 조직을 먼저 선택',
    '## 스타일 정체성과 실제 읽기를 함께 설계')
paragraph('references/production-brief.md', '[축적한 구성 문법](design-grammar.md)을 현재 내용의 발상에 사용한다.',
    '현재 내용에 맞는 스타일의 정체성을 우선 설계한다. 이미지 표현·편집, 색·대비, 타이포그래피의 목소리, 재질·마감과 정서가 만드는 전체 인상을 구체화하고 실제 카피가 읽히는 구도로 구현한다. [축적한 구성 문법](design-grammar.md)은 필요할 때 선택적으로 참고하는 아이디어이며 단일 장면·연속 편집·반복·집합·도해·공유 경계를 각각 배정하는 고정 다섯 메뉴가 아니다.')
paragraph('references/production-brief.md', '자기 방향을 큰 덩어리와 다음 읽을 정보의 한 문장으로 구체화한다.',
    '자기 방향을 실제로 제작할 수 있는 표현으로 구체화한다. 현재 문구가 말하는 관계·상태·경험을 어떤 관객 거리·대상 크기·연결·크롭·빛·형태로 보여 주며 색·글자·마감이 어떤 정서를 만드는지 선택한다. 실제 카피의 면적과 위계를 그 표현에 맞게 확보한다. 같은 잘 읽히는 Title·body 순서와 정렬을 재사용해도 스타일의 정체성이 뚜렷하면 독립된 방향이 될 수 있다. 필터나 글꼴 하나의 교체만으로 스타일 명세를 대신하지 않되 모든 레이아웃·첫 카피 역할·정보 순서·팔레트·서체를 서로 다르게 할 의무는 없다. 제작자는 배정된 스타일과 실제 카피에 맞는 좋은 구도를 선택한다. 구체적인 장면이 없는 표현도 현재 내용과 글자 공간이 자연스럽게 결합하도록 설계한다.')
phrase('references/production-brief.md', '사용자 지정 역할·강조·배치·순서를 우선하며 무문자 요청에는 글자를 추가하지 않고 제목만 있으면 그 제목으로 완결한다.',
    '사용자 지정 역할·강조·배치·순서를 우선하며 무문자 요청에는 글자를 추가하지 않는다. **Title만 있으면 그 제목으로 완결하고, Title+body만 있으면 두 역할의 위계와 이어 읽기를 설계한다.** eyebrow·Subtitle·footer나 날짜·장소·URL을 새로 채우지 않는다.')
phrase('references/production-brief.md', '그 위계를 유지한 채 이미지 편집·큰 공간·읽는 관계를 다르게 설계한다.',
    '그 위계를 유지한 채 배정된 스타일의 이미지 표현·편집과 글자·색·마감을 구현한다.')
paragraph('references/production-brief.md', '각 방향은 자체적으로 설득력 있는 전체 관계를 갖는다.',
    '각 방향은 자체적으로 설득력 있는 스타일과 읽는 관계를 갖는다. 다섯 방향은 이미지 표현·편집, 색·대비, 글자의 목소리·마감·정서가 만드는 정체성으로 구별한다. 좋은 Title·body의 순서와 정렬은 공유할 수 있으며 각 표현 요소 모두의 차이나 고유한 다섯 레이아웃을 의무로 삼지 않는다. 영구적인 다섯 스타일 목록을 쓰지 않는다.')
phrase('references/production-brief.md', '무문자·제목만·간단한 카피에는 스케치를 의무로 늘리지 않는다.',
    '무문자·Title만·간단한 카피와 실용 안내가 없는 Title+body에는 이 복잡한 안내 스케치를 의무로 늘리지 않는다. 도움이 될 때 선택적으로 사용할 수 있다.')

paragraph('references/visual-research.md', '중앙이 다섯 방향을 설계할 때 [구성 문법]',
    '중앙은 현재 내용·카피·언어·매체에 맞는 스타일을 설계하며, [구성 문법](design-grammar.md)의 22개 관계 아이디어는 필요할 때 선택적으로 참고한다. 이미지 표현·편집·색·대비·글자·재질·정서를 폭넓게 발상에 활용하고 레이아웃 차이를 우선 조건으로 삼지 않는다. 원본 한 작품을 한 결과의 답안으로 대응시키거나 원작의 사진·인물·로고·카피·배열을 이식하지 않는다. 반복 장면·사진 편집·도해·삽화·공유 경계 등은 열린 발상의 출발점이며 영구적인 다섯 가족이나 스타일 순위가 아니다.')
phrase('references/visual-research.md', '다섯 결과의 실제 전체 구분을 본다.',
    '다섯 결과의 실제 스타일 정체성을 본다. 좋은 읽기 순서와 정렬을 공유하는 것만으로 스타일 차이가 없다고 판단하지 않는다.')

paragraph('references/evaluation-loop.md', '다섯 방향은 레퍼런스의 전체 표현 체계와 실제 내용에서 설계한다.',
    '다섯 방향은 현재 내용에 맞는 스타일의 정체성을 우선해 설계한다. 각 평가자는 실제 전체 이미지의 표현·편집, 색·대비, 글자의 목소리, 재질·마감과 정서가 만드는 차이로 세트의 다양성을 판단한다. 같은 잘 읽히는 Title·body 순서와 정렬을 공유해도 뚜렷한 스타일이 구현됐다면 독립 스타일일 수 있다. 모든 레이아웃·첫 카피 역할·정보 순서·팔레트·서체 수량의 차이를 필수 조건으로 추가하지 않는다. 필터나 글꼴 하나의 교체만을 완성된 스타일 차이로 인정하지 않으며, 사용자가 명시한 스타일·배치·자산 조건을 함께 적용한다.')
phrase('references/evaluation-loop.md', '넓은 이미지, 다른 방·시점·소재, 글꼴 교체만으로 전체 구분이나 제외 해소를 인정하지 않는다.',
    '넓은 이미지, 다른 방·시점·소재, 글꼴 교체만으로 스타일 차이나 제외 해소를 인정하지 않는다. 같은 좋은 읽기 구도를 공유하는 것 자체는 제외 위반이나 다양성 실패의 근거가 아니다.')
paragraph('references/evaluation-loop.md', '전체 결과의 다양성은 별도로 판단한다.',
    '전체 결과의 다양성은 별도로 판단한다. 1은 색 필터나 단일 글꼴 교체에 머문 반복, 3은 스타일 차이가 보이지만 표현 선택이 범용 효과에 의존하거나 하나의 정체성으로 충분히 결합하지 못함, 5는 공통 조건 안에서 현재 내용에 맞는 각 스타일의 전체 인상이 설득력 있게 구별됨이다. 이미지 표현·편집, 색·대비, 글자의 목소리, 재질·마감과 정서를 함께 보며 각 요소 모두가 달라야 한다는 뜻은 아니다. 좋은 읽기 순서·정렬의 공유만으로 낮은 점수를 주지 않는다. 최고 시안뿐 아니라 최저 시안과 전체 분포를 본다.')

phrase('references/layout-guide.md', '무문자·제목만·간단한 카피에는 의무로 늘리지 않고 도움이 될 때만 사용한다.',
    '무문자·Title만·간단한 카피와 실용 안내가 없는 Title+body에는 이 복잡한 안내 스케치를 의무로 늘리지 않고 도움이 될 때만 사용한다.')
phrase('references/layout-guide.md', '가장 가까운 방향과는 이미지의 조직과 카피의 형태·연속 관계를 함께 달리 설계하며, 같은 이미지 둘레의 빈 정보 면에서 첫 문구나 재료만 바꾸지 않는다.',
    '스케치는 배정된 스타일과 양립하는 색·글자·큰 이미지 관계 속에서 실제 카피의 읽기를 설계한다. 다른 스타일과 같은 좋은 읽기 순서·정렬·카피 형태를 공유할 수 있으며, 스케치의 레이아웃 차이를 스타일 차이의 의무로 삼지 않는다.')
phrase('references/layout-guide.md', '명세에는 구현할 내용의 관계·시점·이미지 편집·색·마감과 참고할 읽는 관계·글자 형태를 함께 설명하고,',
    '가이드와 함께 전달하는 긍정적인 명세에는 선택한 스타일의 정체성, 구현할 내용의 관계·시점·이미지 편집·색·마감과 참고할 읽는 관계·글자 형태를 설명하고,')

phrase('agents/openai.yaml',
    'choose the whole spatial organization, image editing and reading route first, then the medium, color and typography to design five genuinely different whole poster styles for my actual content,',
    'prioritize five distinct style identities for my actual content through authored image expression and editing, color and contrast, typographic voice, material and finish, and mood; makers may share a good readable Title/body order and alignment while choosing a suitable composition for each style,')
phrase('agents/openai.yaml', 'for each style, and assign one to each maker within available concurrency.',
    'for each style. Assign one direction to each maker within available concurrency.')
phrase('agents/openai.yaml',
    'Preserve my full copy and conditions, then inspect the actual images for readability, visible defects and whole-style diversity.',
    'Design hierarchy among the copy roles actually present: Title-only needs only its Title, and Title plus body needs those two roles without invented eyebrow, subtitle, footer, dates or URLs. Preserve my full copy and conditions, then inspect the actual images for readability, visible defects and style diversity without requiring five unique layouts.')

draft_pins = pins(DRAFT)
assert set(draft_pins) == set(source_pins)
changed = [f for f in source_pins if source_pins[f] != draft_pins[f]]
unchanged = [f for f in source_pins if source_pins[f] == draft_pins[f]]
assert len(changed) == 9, changed
assert unchanged == ['references/layout-guide-contract.md', 'references/reference-catalog.json', 'scripts/make_layout_guide.py'], unchanged
assert pins(SOURCE) == source_pins
diff = ''.join(''.join(difflib.unified_diff((SOURCE / f).read_text().splitlines(True),
                                         (DRAFT / f).read_text().splitlines(True),
                                         fromfile='live-y/' + f, tofile='candidate-style-first/' + f))
               for f in changed)
(HISTORY / 'diff.patch').write_text(diff)
(HISTORY / 'pins.json').write_text(json.dumps({
    'source': str(SOURCE), 'source_version': 'Y', 'draft': str(DRAFT),
    'source_12_file_sha256': source_pins, 'draft_12_file_sha256': draft_pins
}, ensure_ascii=False, indent=2) + '\n')
(HISTORY / 'changed-files.json').write_text(json.dumps({
    'changed_files': [{'path': f, 'source_sha256': source_pins[f], 'draft_sha256': draft_pins[f]} for f in changed],
    'unchanged_files': unchanged, 'edit_locations': edits
}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'draft_files': len(draft_pins), 'changed_files': changed,
                  'unchanged_files': unchanged, 'live_unchanged': True}, ensure_ascii=False, indent=2))
