"""Write a prospective plan only; no raster reads, rendering or image calls."""
from pathlib import Path
import json
from PIL import ImageFont

ROOT = Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster')
case = json.loads((ROOT / 'work/round19/planning/single-five-case.json').read_text())['cases'][0]
copy = case['copy']
OUT = ROOT / 'drafts/w-five-design'
SANS = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
SERIF = '/System/Library/Fonts/Supplemental/AppleMyungjo.ttf'

body3 = [
    '작은 화분부터 오래 키운 나무까지 만납니다.',
    '재배자의 이야기를 듣고,',
    '우리 집의 빛과 생활에 맞는 식물을 골라보세요.'
]
body_home = [
    '작은 화분부터 오래 키운 나무까지 만납니다.',
    '재배자의 이야기를 듣고, 우리 집의 빛과 생활에 맞는',
    '식물을 골라보세요.'
]

def region(entry, x, y, width, height, size, *, face=2, serif=False,
           lines=None, color='#202624', leading=None):
    return {
        'entry': entry,
        'copy': copy[entry - 1]['text'],
        'lines': lines or [copy[entry - 1]['text']],
        'fixed_newlines': copy[entry - 1]['fixed_newlines'],
        'x': x, 'y': y, 'align': 'left',
        'line_spacing': leading or round(size * 1.35),
        'area': {'width': width, 'height': height},
        'font': {'path': SERIF if serif else SANS, 'index': 0 if serif else face, 'size': size},
        'color': color,
    }

def guide(shapes, regions, background):
    return {
        'status': 'Concept only; no SVG, PNG or manifest rendered in this planning task',
        'canvas': {'width': 1600, 'height': 900, 'background': background},
        'image_geometry_concepts': shapes,
        'text_regions': regions,
        'limits': [
            'Coordinates and these installed font faces are current-case choices, not client preservation conditions or a universal layout.',
            'Image geometry describes substantive picture organization; it is not empty gray placeholders to adopt as final style.',
            'A later guide may show only newly authored shapes and actual copy. No source raster or generated poster is used as a bitmap input.',
            'The plan records installed-font measurements only. It neither renders a guide nor certifies that future native generation applies these font files.',
        ],
    }

directions = [
    {
        'role': 'R20-C1-M1', 'ratio': '16:9',
        'working_name_not_printed': 'Choosing a plant at the scale of daily life',
        'whole_relationship': 'Two unequal photographic scales compare a hand-held nursery pot with a plant beside an ordinary domestic seat; the broader explanation follows their common lower ledge and opens into a full-size two-part visit ledger.',
        'positive_direction': """Design a precise photographic editorial poster about choosing the scale of a living plant for a home. Give the viewer two genuinely different distances. A broad, close, waist-height photograph at the upper left shows someone supporting a modest nursery pot, with its rim, stem attachment and leaves in believable relation to the hand. A taller photograph at the right shows a larger potted plant beside the cropped edge of an ordinary chair, with the floor and actual pot base visible. The second picture establishes lived scale; it is not an empty room for lettering. Crop both pictures decisively, with unequal widths and heights, clear botanical attachment, natural daylight and unembellished pottery. Keep the small pot distinct from the mature plant rather than suggesting an undocumented before/after transformation.

The modest Korean title and its smaller Latin companion share the upper-left photographic start. Use controlled mature Korean serif anatomy for the title, open inner counters, a restrained stroke contrast and intact word spaces. Their optical weight remains below the complete photographic comparison. Immediately beneath the left photograph, the slogan introduces a broad three-line explanation. Give the explanation a real editorial reading body, medium-weight Korean sans forms, balanced rectangular syllables, flat clean strokes and ordinary leading. Reserve its measured area before shaping the photographs. In a 720-wide planning view it should feel like readable prose, not a caption.

The paragraph ends on the same left start that begins the market name below. Date and hours stay near that name; the venue joins the hours baseline. Access and care occupy an adjoining, equally readable local group, with the invitation and URL directly beneath. The entire lower region is useful reading space, not a tiny footer. Use deep natural greens, warm gray ceramics, neutral photographic skin and quiet charcoal type. Finish with exact picture edges, controlled exposure, natural surfaces and crisp planar lettering. The comparison of plant scale determines the photographic edit and the broad prose-to-visit ledge.""",
        'hierarchy': {
            'primary': {'entry': 1, 'role': 'Modest serif identity at the first photographic start; strongest identifier without overtaking the photographic comparison.'},
            'support': [{'entry': 2, 'role': 'Close smaller Latin companion.'}, {'entry': 3, 'role': 'Visible explanation entry below the wide near photograph.'}],
            'explanation': {'entries': [4], 'shape': 'Broad three-line continuous paragraph under the nearer photographic crop.'},
            'visit': {'entries': [5, 6, 7, 8], 'shape': 'Lower-left market/date group; hours and venue share one nearby baseline.'},
            'next_action': {'entries': [9, 10, 11, 12], 'shape': 'Adjoining lower-right access/care group, then invitation and URL directly below.'},
        },
        'body_line_groups': body3,
        'body_end_to_next_info': 'The paragraph and market name keep the same left start with one local vertical gap. The market/date/hours/venue group shares its upper baseline with access/care; the invitation and URL continue immediately inside that neighboring group.',
        'nearest_peer': {
            'role_id': 'R20-C1-M4',
            'structural_distinction': 'M1 is simultaneous scale comparison through a broad near picture and one taller domestic context, followed by a common prose ledge. M4 sequences three actions through alternating horizontal crops and a descending zigzag of whole copy groups.',
            'style_distinction': 'M1 uses natural-color photographic distance, carefully exposed surfaces and quiet serif identity. M4 uses tight monochrome action crops, coarse graphic tonal separation and date-led sans typography.',
        },
        'guide_geometry_concept': guide([
            {'shape': 'broad upper-left photograph region', 'bounds': [64, 183, 860, 215], 'content': 'Hand supporting a small pot; genuine scale, attachment and hand contact.'},
            {'shape': 'taller right photograph region', 'bounds': [984, 42, 552, 628], 'content': 'Larger plant beside a cropped chair; floor and pot base give domestic scale.'},
            {'shape': 'shared lower photo edge and extended prose-to-market start', 'points': [[64, 398], [924, 398], [924, 670], [1536, 670]], 'content': 'Picture edit and paragraph/ledger relationship, not a decorative plant perimeter.'},
        ], [
            region(1, 64, 44, 850, 79, 62, serif=True),
            region(2, 64, 129, 850, 48, 34),
            region(3, 64, 413, 900, 58, 42, face=4),
            region(4, 64, 476, 900, 181, 42, lines=body3, leading=58),
            region(5, 64, 691, 690, 59, 42, face=4),
            region(6, 64, 754, 670, 55, 40),
            region(7, 64, 814, 358, 53, 38),
            region(8, 445, 814, 310, 53, 38),
            region(9, 830, 691, 706, 53, 38),
            region(10, 830, 744, 706, 53, 38),
            region(11, 830, 797, 706, 53, 38),
            region(12, 830, 850, 706, 46, 34),
        ], '#EEECE5'),
    },
    {
        'role': 'R20-C1-M2', 'ratio': '16:9',
        'working_name_not_printed': 'The plant and the light it will live with',
        'whole_relationship': 'One oblique field of domestic light and its attached pot-and-stem shadows forms the whole page; a large slogan and upright paragraph occupy its stable upper tone, and the sloping light edge lands at a wide visit crossbar.',
        'positive_direction': """Make a boldly reduced image about the relationship between a plant, its position and domestic light. Build one continuous spatial field, with the close edge of a window or sill at the upper right, a planted pot below it and the plant's attached shadow stretching obliquely toward the lower left. A second, smaller pot stands farther from that edge, visibly at a different position. Show stems connected to actual pots, daylight falling in one coherent direction and shadows belonging to those objects. This expresses consideration of light without labels, measurements, health comparisons or a claimed recommended position.

Translate the scene into controlled large graphic tonal shapes: a deep near-black wall tone, a muted warm apricot light plane, dense rust pottery and sharply selected botanical contours. Let the oblique boundary cross most of the image, rather than making foliage a border around a pale text hole. Combine a hard light edge with a limited, specifically observed shadow softness; leave the objects and their spatial attachment unambiguous. The composition should feel like an intentionally edited light study, with a substantive shadow structure and quiet surface, rather than a washed-out plant advertisement.

The slogan enters first, plainly stronger than the smaller Korean/Latin identity at the upper-left edge. The explanation begins beneath it in a broad upright three-line paragraph on a steady tonal portion of the light study. Use precise mature Korean sans anatomy, open counters, moderate medium weight, meaningful spaces and proportionate Latin/numeral forms. Keep the paragraph substantial at the adopted SNS view and keep every line free of shadow crossings. Its last line meets the descending light boundary; that edge directs the next start down-left to the market-name crossbar. Market name and date occupy one row, hours and venue the next. Access/care then form a close following row, with invitation and URL continuing underneath. The schedule is flat typesetting even while the picture is oblique. Coherent light, distinct range-dash forms and deliberately bounded tonal transitions provide the finish.""",
        'hierarchy': {
            'primary': {'entry': 3, 'role': 'Large clear slogan on the upper light-study tone.'},
            'support': [{'entry': 1, 'role': 'Smaller Korean identifier at the upper-left image edge.'}, {'entry': 2, 'role': 'Close Latin companion, subdued relative to slogan.'}],
            'explanation': {'entries': [4], 'shape': 'Three-line upright paragraph below the slogan, on one stable dark tone.'},
            'visit': {'entries': [5, 6, 7, 8], 'shape': 'Wide two-row crossbar reached by the descending light boundary; market/date then hours/venue.'},
            'next_action': {'entries': [9, 10, 11, 12], 'shape': 'Access/care pair immediately under the crossbar, then invitation and adjacent URL.'},
        },
        'body_line_groups': body3,
        'body_end_to_next_info': 'The actual descending light boundary leaves the paragraph’s last-line edge and reaches the beginning of the market/date crossbar. Hours/venue are the next local row, followed by access/care and invitation/URL without a detached corner caption.',
        'nearest_peer': {
            'role_id': 'R20-C1-M5',
            'structural_distinction': 'M2 is one diagonal light-and-shadow field and a lateral visit crossbar. M5 is a frontal architectural section with several different support heights, a broad invitation/body entry and a lower stepped identity seam.',
            'style_distinction': 'M2 uses extreme tonal reduction, an oblique light boundary and attached shadow contours. M5 uses dry drawn furniture/plant structure, restrained colored architectural planes and a wide frontal scale comparison.',
        },
        'guide_geometry_concept': guide([
            {'shape': 'large oblique light-plane polygon', 'points': [[1090, 0], [1600, 0], [1600, 900], [420, 900], [50, 570]], 'content': 'Light from the upper-right sill, with one coherent oblique direction.'},
            {'shape': 'plant/pot and attached shadow silhouettes', 'bounds': [1030, 338, 570, 562], 'content': 'Connected stems, upright pot and long shadow; major image structure, not foliage corners.'},
            {'shape': 'secondary pot farther from light edge', 'bounds': [40, 400, 300, 430], 'content': 'A distinct position in the same light field; no invented measurement or health state.'},
        ], [
            region(1, 64, 56, 340, 67, 46, face=2, color='#F2E3CC'),
            region(2, 64, 132, 340, 47, 34, color='#F2E3CC'),
            region(3, 450, 55, 1060, 81, 56, face=4, color='#F2E3CC'),
            region(4, 450, 205, 1040, 181, 42, lines=body3, leading=58, color='#F2E3CC'),
            region(5, 64, 477, 660, 58, 42, face=4),
            region(6, 828, 477, 690, 58, 42),
            region(7, 64, 542, 660, 56, 40),
            region(8, 828, 542, 690, 56, 40),
            region(9, 64, 617, 660, 53, 38),
            region(10, 828, 617, 690, 53, 38),
            region(11, 64, 738, 820, 58, 42),
            region(12, 828, 738, 690, 54, 38),
        ], '#292B28'),
    },
    {
        'role': 'R20-C1-M3', 'ratio': '16:9',
        'working_name_not_printed': 'Listen to the work behind the plant',
        'whole_relationship': 'A large cropped grower leans from the left into the foreground rootball and pot; the actual explanation is the main verbal entry above that work, and a compact but full-size visit group continues directly beneath it.',
        'positive_direction': """Make the grower's work the reason to look, rather than a decorative collection of healthy leaves. Draw one adult grower leaning from the left into an ordinary pot and exposed rootball near the lower foreground. Crop the torso and forearms closely, so body weight, hand support, pot rim and the attachment of stems are comprehensible. One hand supports the rootball from beneath while the other steadies the pot edge; simplify the rest of the body economically. Show a believable working posture and a few specific soil and cloth marks. Give plants enough attached foliage to identify the activity, while hands, rootball and pot carry the important image relationship.

Use a forceful observed ink-and-oxide painting: broad controlled dark strokes establish the cropped figure, dry thinner contours reveal fingers and pot contact, and a limited burnt-orange mass gives the root/soil area weight. Keep the anatomy readable, surfaces deliberately selective and edges resolved. Ordinary work clothing, uneven soil and one practical pot should have specificity without extra lettering, labels or a sentimental smiling mascot. The large figure crosses the lower image and approaches the text boundary, while the upper prose remains clear planar typesetting.

Treat the actual explanation as the first verbal voice. Set its complete three-line paragraph in a substantial mature Korean serif body with open counters, restrained stroke contrast, stable syllable proportions and normal readable leading. Its final sentence asks the viewer to choose for their home; the nearby slogan supports this reading. Directly below, the market name starts the visit group on the same axis, with date/hours paired, venue beneath, then access/care and invitation/URL following at full reading size. Align the group to the image's working direction without printing arrows or new headings. The Korean/Latin identity is a quieter lower-left imprint beside the cropped figure's grounded edge, not a competing large title. Keep the paragraph and practical information clean and upright, separate from the painting's rough image marks. The work and the readable narrative voice create the authored system.""",
        'hierarchy': {
            'primary': {'entry': 4, 'role': 'Complete explanation as substantial first verbal voice; deliberate prose entry rather than a giant headline.'},
            'support': [{'entry': 3, 'role': 'Slogan immediately after the explanation with lower weight.'}, {'entry': 1, 'role': 'Quiet lower-left Korean identity at the figure’s grounded edge.'}, {'entry': 2, 'role': 'Latin companion immediately below the identity.'}],
            'explanation': {'entries': [4], 'shape': 'Broad three-line substantial serif paragraph across the upper-right working direction.'},
            'visit': {'entries': [5, 6, 7, 8], 'shape': 'Market starts directly below prose/slogan; date/hours share the next baseline, venue follows.'},
            'next_action': {'entries': [9, 10, 11, 12], 'shape': 'Access/care share the next local row; invitation and URL remain immediately underneath.'},
        },
        'body_line_groups': body3,
        'body_end_to_next_info': 'The paragraph, smaller slogan and market name retain the same start. Date/hours and venue continue inside that nearby group; access/care and invitation/URL follow without returning to a distant corner. The figure’s forearm points toward this working-and-reading axis.',
        'nearest_peer': {
            'role_id': 'R20-C1-M4',
            'structural_distinction': 'M3 is a single close active figure and rootball, with the explanation itself leading one continuous prose-to-visit axis. M4 is a stepped three-action edit, date first and whole copy groups alternating between action crops.',
            'style_distinction': 'M3 uses forceful selective ink/oxide figure painting and substantial serif prose. M4 uses clipped monochrome photographic actions, exact image bands and a date-led sans hierarchy.',
        },
        'guide_geometry_concept': guide([
            {'shape': 'cropped torso and forearm mass', 'bounds': [0, 77, 418, 690], 'content': 'Leaning adult grower with a purposeful posture; shoulders and sleeve imply weight and work.'},
            {'shape': 'diagonal active forearm', 'points': [[220, 570], [535, 650], [995, 776], [720, 895], [145, 738]], 'content': 'Hands support the actual rootball and pot; clean readable contact, not floating ornamental hands.'},
            {'shape': 'rootball/pot foreground pair', 'bounds': [795, 680, 805, 220], 'content': 'Substantial visible work fills the foreground, rather than a leaf border around text.'},
        ], [
            region(4, 420, 55, 1100, 191, 44, serif=True, lines=body3, leading=62),
            region(3, 420, 267, 1090, 56, 40),
            region(5, 420, 330, 1090, 61, 44, face=4),
            region(6, 420, 397, 480, 58, 42),
            region(7, 972, 397, 548, 58, 42),
            region(8, 420, 461, 1090, 56, 40),
            region(9, 420, 523, 485, 56, 40),
            region(10, 972, 523, 548, 56, 40),
            region(11, 420, 585, 1090, 56, 40),
            region(12, 420, 647, 1090, 50, 36),
            region(1, 64, 771, 635, 66, 50, serif=True),
            region(2, 64, 840, 635, 49, 36),
        ], '#E5DED1'),
    },
    {
        'role': 'R20-C1-M4', 'ratio': '16:9',
        'working_name_not_printed': 'A repotting demonstration is an activity, not decoration',
        'whole_relationship': 'Three tightly cropped repotting actions descend through alternating horizontal photographic bands; date/visit begins at the first open start, the full explanation occupies the middle turn, and access/care then invitation/URL complete the lower turn.',
        'positive_direction': """Create an edited action poster for the promised repotting demonstration and continued care. Use three tightly observed views of the same ordinary plant/potting activity: hands lifting a supported rootball beside the pot, the relation of roots and soil at close distance, and the newly seated plant with the hands setting the pot down. Show a plausible continuous activity without a dramatic health transformation or added written instructions. Crop out faces, unrelated props and printed packages. The pots, hands, roots and surfaces must have coherent scale and actual contact; a few connected leaves identify the plant rather than decorating the perimeter.

Arrange the action images as unequal horizontal bands that alternate their open reading starts. The top action runs from the center toward the right crop; the middle close view enters from the left; the final pot-setting view occupies the lower right. Their stagger is visible at thumbnail size. Use crisp monochrome photography with dark stable blacks, controlled midtones and a restrained blue separation in the image shadows. Tight close focus and exact cuts give the work specificity. Coarse photographic tone is an image treatment only, never noise in the letters. Keep edges flat and controlled; avoid simulated folded paper, distressed caption lettering or added arrows.

The date is the first verbal anchor at the upper-left opening, with market name, hours and venue closely grouped. At the next turn, the slogan introduces the complete broad three-line explanation on the middle-right side. Set the paragraph in mature medium-weight Korean sans, generous open counters, meaningful spaces and comfortable leading, at full reading size rather than a photo caption. Access and care follow directly beneath its last line on that same start. The third action's edge brings the eye down-left to the modest Korean/Latin identity and the invitation/URL directly below it. That final group is a local invitation, not unrelated corner print. Give date dashes, hours colons and URL slashes distinct clean shapes. Activity sequence, changing close distance and whole copy-group turns determine the full system.""",
        'hierarchy': {
            'primary': {'entry': 6, 'role': 'Upper-left date; visible first entry into the first action and its visit group.'},
            'support': [{'entry': 3, 'role': 'Middle-right entry into the complete explanation.'}, {'entry': 1, 'role': 'Quiet lower-left Korean identity at the third action turn.'}, {'entry': 2, 'role': 'Smaller Latin companion in that same identity group.'}],
            'explanation': {'entries': [4], 'shape': 'Three-line broad paragraph at the middle-right turn, kept whole and upright.'},
            'visit': {'entries': [5, 6, 7, 8], 'shape': 'A complete upper-left visit cluster adjoining the top action band.'},
            'next_action': {'entries': [9, 10, 11, 12], 'shape': 'Access/care immediately below the explanation; invitation/URL form one local lower-left finish reached by the third action crop.'},
        },
        'body_line_groups': body3,
        'body_end_to_next_info': 'Access and care start immediately below the paragraph on the same middle-right axis. The third action crop’s descending left edge then ends beside the lower-left identity/invitation group, whose invitation and URL stay adjacent. Visit information already belongs to the initial date-led cluster.',
        'nearest_peer': {
            'role_id': 'R20-C1-M1',
            'structural_distinction': 'M4 is three actions edited in time through alternating horizontal bands and three whole reading turns. M1 compares two simultaneous scales in unequal photographs, with one broad prose ledge and one full-size bottom visit ledger.',
            'style_distinction': 'M4 is tightly cropped monochrome action and blue-separated tone with a date-led sans hierarchy. M1 is quiet natural-color domestic comparison with a restrained serif identity.',
        },
        'guide_geometry_concept': guide([
            {'shape': 'top horizontal action crop', 'bounds': [590, 0, 1010, 275], 'content': 'Hands lifting a supported rootball beside the actual pot.'},
            {'shape': 'middle closer action crop', 'bounds': [0, 305, 590, 280], 'content': 'Roots, soil and pot edge at a closer distance; coherent action, not decorative leaves.'},
            {'shape': 'lower horizontal action crop', 'bounds': [770, 640, 830, 260], 'content': 'Plant seated in pot and supported by hands; the contact is the action.'},
        ], [
            region(6, 64, 42, 472, 72, 52, face=4),
            region(5, 64, 119, 472, 56, 40),
            region(7, 64, 183, 472, 53, 38),
            region(8, 64, 239, 472, 53, 38),
            region(3, 650, 290, 886, 56, 40, face=4),
            region(4, 650, 354, 886, 179, 42, lines=body3, leading=58),
            region(9, 650, 536, 886, 53, 38),
            region(10, 650, 591, 886, 53, 38),
            region(1, 64, 649, 635, 71, 54, face=4),
            region(2, 64, 725, 635, 49, 36),
            region(11, 64, 783, 635, 53, 38),
            region(12, 64, 842, 635, 50, 36),
        ], '#ECEAE2'),
    },
    {
        'role': 'R20-C1-M5', 'ratio': '16:9',
        'working_name_not_printed': 'A plant has a place in lived space',
        'whole_relationship': 'A frontal drawn domestic section compares table, sill and floor support heights; a broad invitation and real paragraph begin above its first ledge, visit/access follow that horizontal ledge, and a quiet identity belongs to the lower stepped architectural seam.',
        'positive_direction': """Make a plant's fit within lived space the visual proposition. Draw a wide frontal domestic section in which an ordinary table edge, a window ledge and the floor support plants of genuinely different sizes. A small pot belongs on the ledge, a medium plant stands on the table and a slim taller plant is rooted in a floor pot. Show support contacts, pot bases, the furniture edge and plausible domestic scale. The wall, legs and floor form a descending stepped section across the whole image. It is an illustrative consideration of household positions, not a plan of the event venue, a miniature 3D room or a set of claimed recommended placements.

Use deliberate dry drawn contours, broad restrained clay-red and muted teal architectural planes, and dark irregular plant structures. Give the table leg, sill thickness, pottery contour and a few stem joints precise character. Keep foliage restrained and varied rather than filling every edge with lush generic fans. The section should have a wide authored rhythm: high left support, lower middle support and a floor-grounded right mass, with strong shared horizontal edges and clear upright structure. Furniture and pots carry the comparison; the section is substantive imagery rather than an empty room for words. Finish with selective line density, crisp plane boundaries and clean purposeful crops.

Let the invitation be the first verbal entry, large enough to welcome without becoming a huge gothic board. Beneath it, give the actual explanation a continuous broad three-line reading area, with mature medium-weight Korean sans forms, stable letter bodies, ordinary word spacing and comfortable leading. The slogan is a quieter bridge beneath that paragraph. The market-name row then begins at the same left start; date, hours and venue share the next nearby baseline, followed by an access/care pair and a local URL. This useful ledger belongs to the first architectural ledge. The Korean title and Latin companion remain a quieter identity on the lower-middle step, where their start shares the drawn support seam. All information stays planar and readable while the drawn section continues beneath and beside it. Domestic scale and real support heights determine the layout.""",
        'hierarchy': {
            'primary': {'entry': 11, 'role': 'Broad welcoming invitation first, clearly stronger than the quiet lower identity.'},
            'support': [{'entry': 3, 'role': 'Quiet bridge between substantial prose and the useful visit row.'}, {'entry': 1, 'role': 'Lower-middle Korean identity sharing the stepped support seam.'}, {'entry': 2, 'role': 'Latin companion directly below that identity.'}],
            'explanation': {'entries': [4], 'shape': 'Broad three-line continuous paragraph below the invitation.'},
            'visit': {'entries': [5, 6, 7, 8], 'shape': 'Market starts below prose/slogan; date, hours and venue share one wide next baseline.'},
            'next_action': {'entries': [9, 10, 12], 'shape': 'Access/care form the next useful row, URL local beneath care; invitation is already the first entry.'},
        },
        'body_line_groups': body_home,
        'body_end_to_next_info': 'The paragraph, quieter slogan and market row keep one left start. Date/hours/venue share the immediately following architectural ledge; access/care and local URL remain nearby. The lower identity is attached to the pictorial step and does not interrupt that functional reading chain.',
        'nearest_peer': {
            'role_id': 'R20-C1-M2',
            'structural_distinction': 'M5 is a frontal stepped support-height comparison with a broad invitation/body entry and a lower identity seam. M2 is one diagonal light/shadow field, slogan first and a wide crossbar reached by its oblique boundary.',
            'style_distinction': 'M5 uses dry furniture/plant contours and restrained architectural color planes. M2 is a strongly reduced light study with sharper tonal contrast and attached cast-shadow shapes.',
        },
        'guide_geometry_concept': guide([
            {'shape': 'frontally drawn stepped domestic section', 'points': [[0, 399], [550, 399], [550, 581], [1120, 581], [1120, 725], [1600, 725], [1600, 900], [0, 900]], 'content': 'Table, sill and floor support heights, with furniture thickness and rooted pots.'},
            {'shape': 'taller floor-grounded plant and right wall structure', 'bounds': [1238, 136, 362, 764], 'content': 'Slim mature plant with actual base and nearby wall/ledge; household scale, not leaf decoration.'},
            {'shape': 'smaller plant/support pairs', 'bounds': [46, 516, 1152, 384], 'content': 'Two distinct plants occupy the table and ledge; controlled frontal contours and support contacts.'},
        ], [
            region(11, 64, 44, 1420, 74, 52, face=4),
            region(4, 64, 145, 1360, 185, 42, lines=body_home, leading=60),
            region(3, 64, 330, 1120, 53, 38),
            region(5, 64, 393, 1080, 56, 40, face=4),
            region(6, 64, 454, 374, 56, 40),
            region(7, 474, 454, 352, 56, 40),
            region(8, 867, 454, 357, 56, 40),
            region(9, 64, 517, 525, 53, 38),
            region(10, 630, 517, 594, 53, 38),
            region(12, 630, 578, 594, 50, 36),
            region(1, 690, 684, 534, 61, 44, face=2),
            region(2, 690, 750, 534, 49, 36),
        ], '#E4DDD0'),
    },
]

common = [
    'count: 5; ratio: 16:9; assets: []',
    'One complete flat opaque landscape native poster per role; no mockup, comparison sheet, final manual composition or overlay.',
    'Print each of the twelve supplied entries once, with exact Korean/Latin/numbers/meaningful spaces/punctuation. Internal indices, role names, working names and guide metadata are never printed. No extra label, logo, plant tag, QR, watermark or image lettering.',
    'Use current-content viewpoints to determine whole image editing and copy relationships. These five choices are not a permanent menu or required future style families.',
    'Source observations are accumulated ideas only. Do not reopen source artwork, copy a source layout, use source reputation/count as quality proof or promise universal quality.',
    'Plan a complete substantial body and practical information with actual available fonts before the first native image. A 720-wide view and a 1600x900 guide canvas are internal planning assumptions, not new user pixel requirements or thresholds.',
    'The optional new-code guide is a planning diagram with actual-font copy and substantive image-organization shapes. It is not client artwork or the final poster. No raster input/compositing/postprocessing; final native font-file application is not certified by guide fonts.',
    'Give stable mature Korean body anatomy, readable Latin/numerals and original punctuation adequate size and contrast. Preserve en dashes, colons, middle dots, ampersand, periods and URL, including exact word spaces.',
    'Exclude passive solid/near-solid/split-field gothic headline/date/info boards with subordinate imagery, and clay/toy/complementary packages or repeated big-object/big-title/tiny-footer structures. Substantive coherent scenes, quiet space and appropriate sans remain available.',
    'Meaningful line groups and geometry are prospective design choices. Do not alter a functioning result merely to fit planned coordinates or line count. Native initial/correction bounds remain unchanged; no score feedback, threshold change or friendly-repeat loop is part of this plan.',
]

measurements = []
for d in directions:
    assert d['ratio'] == '16:9'
    assert ' '.join(d['body_line_groups']) == copy[3]['text']
    regions = d['guide_geometry_concept']['text_regions']
    assert sorted(r['entry'] for r in regions) == list(range(1, 13))
    for r in regions:
        assert r['copy'] == copy[r['entry'] - 1]['text']
        assert ' '.join(r['lines']) == r['copy']
        f = ImageFont.truetype(r['font']['path'], r['font']['size'], index=r['font']['index'])
        advances = [float(f.getlength(line)) for line in r['lines']]
        assert max(advances) <= r['area']['width'], (d['role'], r['entry'], advances, r['area'])
        ascent, descent = f.getmetrics()
        for line_i, line in enumerate(r['lines']):
            bx0, by0, bx1, by1 = f.getbbox(line, anchor='ls')
            baseline = r['y'] + ascent + line_i * r['line_spacing']
            assert r['x'] + bx0 >= 0 and r['x'] + bx1 <= 1600
            assert baseline + by0 >= 0 and baseline + by1 <= 900, (d['role'], r['entry'], baseline, by1)
        measurements.append({'role': d['role'], 'entry': r['entry'], 'font_family_style': list(f.getname()), 'line_advances': advances, 'planned_area': r['area']})

plan = {
    'schema_version': 1,
    'case_id': 'R20-C1',
    'status': 'NEW prospective matched-development all-five plan after closed R19 feedback; no rendering or native generation',
    'common_constraints': common,
    'directions': directions,
    'design_provenance': {
        'source_request': 'work/round19/planning/single-five-case.json',
        'source_case_id': 'R19-C1',
        'development_design': 'Matched development after feedback; not a held-out test or isolated causal experiment.',
        'source_use': 'Read current V grammar, production brief, layout-guide and renderer contract plus catalog observations only. No source raster, prior poster pixel, critic score or raw transcript opened.',
        'observed_idea_connections': [
            {'id': 'BP2024-077', 'idea': 'Comparison at unequal picture scales plus one stable long paragraph; no source objects or fixed grid copied.'},
            {'id': 'BP2024-078', 'idea': 'Different action views linked through purposeful image edits; no source trajectories, captions or overprinted lines copied.'},
            {'id': 'BP2024-038', 'idea': 'Activity and its open reading starts organize the overall field, without requiring a giant object or headline.'},
            {'id': 'BP2024-025', 'idea': 'Related spatial scales/supports can determine image and nearby information; no source models, measurements or places copied.'},
            {'id': 'BP2025-082', 'idea': 'Selective rough image treatment can coexist with exact stable practical typography.'},
        ],
        'font_measurement_only': 'Read installed font metrics via Pillow; no font binary copied, no SVG/PNG rendered, no image edited. These measurements are guide planning evidence, not poster readability or quality approval.',
        'measurements': measurements,
    },
    'request': case['request'],
    'copy': copy,
}

rationale = '''# Prospective matched-development five

This is a new all-five design proposal for the exact closed R19 plant-market request. It changes the prospective design, not an individual returned poster. It is matched development after feedback, not a held-out test, isolated causal experiment or proof of quality. All five remain independent complete 16:9 native posters, with the exact twelve entries once and no client assets.

The viewpoint changes the large image organization before it changes materials:

- **M1 — choosing scale:** a close supported nursery pot and a taller plant beside a domestic seat create unequal simultaneous photographic distances. A broad continuous paragraph occupies their common ledge; the full-size practical ledger follows it. Comparison determines the edit, rather than a leaf canopy surrounding text.
- **M2 — domestic light:** one oblique light/shadow field, two attached pot positions and the window edge explain consideration of light without measurements or recommendations. Its descending boundary hands prose to the broad visit crossbar. Strong tonal reduction and attached shadows determine the style.
- **M3 — grower’s work:** one large cropped working figure, supported rootball and actual pot contact make the story visible. The complete substantial serif explanation is the first verbal voice, with the useful visit group directly below. The image’s rough painting remains separate from clean reading typography.
- **M4 — repotting demonstration:** three close actions form a descending staggered edit. Date/visit, complete prose/access-care and the local invitation/URL turn with the action crops. The temporal edit differs from M1’s simultaneous scale comparison; no health transformation or new instruction is claimed.
- **M5 — lived space:** a frontal domestic section compares table, ledge and floor support heights. A welcoming entry and continuous explanation lead into the first ledge’s useful ledger, with a quieter lower identity seam. Support contacts and furniture/plant scale determine the picture; the room is not a blank text backdrop.

These are five current-content choices, not a fixed future menu. They vary the dominant shapes, image edits, first verbal roles and body-to-information handoffs. M1/M4 are the closest photographic peers but compare simultaneous scale versus serial actions, unequal mosaic versus alternating bands and one prose ledge versus three whole reading turns. M2/M5 both concern domestic position but use an oblique continuous light field versus a frontal stepped support section. M3’s active single figure and prose-first voice differ from either system.

The guide concepts use a 1600×900 internal canvas, explicit existing font paths/faces, actual copy, deliberate meaningful line groups and substantive image-geometry descriptions. They are planning data only; no guide or poster has been rendered here. Coordinates, faces and the adopted 720-wide display assumption are not new client preservation conditions or thresholds. A later guide should show the actual copy/shape relation, not carry blank geometry or provisional tones into the final style. Installed-font anatomy in a guide does not certify font-file application in the native poster.

Checks performed: exact source request and full copy were copied without normalization; five role IDs, five 16:9 directions and assets[] were conserved in scope; each direction has all twelve entries exactly once in its proposed text regions; every deliberate line array joins to the exact entry; both body line-group variants reconstruct the whole source sentence with original spaces and punctuation; all requested installed font files exist; actual font metrics were read without raster rendering to confirm line advances fit their planned widths and painted text bounds stay on the proposed canvas. No source raster, old poster pixel, critic score or raw transcript was read. No source reputation or count establishes quality, and no poster scores or expected pass result are assigned.
'''

for name, text in [('plan.json', json.dumps(plan, ensure_ascii=False, indent=2) + '\n'), ('rationale.md', rationale)]:
    with (OUT / name).open('x', encoding='utf-8') as f:
        f.write(text)
print(json.dumps({'directions': len(directions), 'copy_regions': len(measurements), 'body_reconstruction': 'exact', 'guides_rendered': 0, 'native_calls': 0, 'outputs': ['plan.json', 'rationale.md']}, ensure_ascii=False))
