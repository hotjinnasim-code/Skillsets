"""Adapt prospective schema and resolve nearest plans before any generation."""
from pathlib import Path
import copy
import datetime
import hashlib
import json

TASK = Path(__file__).resolve().parents[1]
source = TASK / 'drafts/next-five-design/plan.json'
case_source = TASK / 'drafts/next-five-request.json'
original = json.loads(source.read_bytes())
case = json.loads(case_source.read_bytes())['cases'][0]
assert original['request'] == case['request'] and original['copy'] == case['copy']
plan = copy.deepcopy(original)
plan['common_constraints'] = [f'{key}: {value}' for key, value in original['common_constraints'].items() if key != 'workflow']
plan['common_constraints'].append('Reuse accumulated ideas without source artwork re-opening. This case supplies no client image or supporting guide; create a complete first native poster directly. Current central coordinates/line groups/optical choices are design choices, not new client preservation conditions. Preserve every literal actual requirement and the unchanged native-call bounds.')
for direction in plan['directions']:
    direction['role'] = direction.pop('role_id')
    assert ' '.join(direction['body_line_groups']) == case['copy'][3]['text']
d = plan['directions'][3]
d['working_name_not_printed'] = 'Botanical atlas: the explanation leads, ground becomes the visit ledger'
d['whole_relationship'] = 'A substantial three-line explanatory paragraph is the first verbal encounter among crossing specimen canopies. Independent drawn plants descend across the full width, and their stepped shared ground supports a horizontal visit row followed locally by access/care and invitation/URL. A compact identity stays beside the explanatory entry rather than a competing headline.'
d['positive_direction'] = '''Make a botanical editorial poster that takes the range from small pot to long-grown tree seriously. Draw independent specimens at different living scales: a small broad-leaf pot, a branching houseplant and a taller indoor tree, with gently descending ground heights across the whole landscape. Give leaves convincing attachments, articulated stems, actual pot rims, visible soil and a selectively visible root-ball section. The large canopy enters the upper crop and individual stems cross the field at uneven heights; this is an actively drawn atlas spread, not three little specimens decorating a text board. Work in observed colored-pencil and fine ink, mineral green, deep olive, warm bark brown and restrained blue, with richer leaf masses balanced by fine internal drawing. Do not add species names or technical labels.

Let the actual explanatory paragraph be the first verbal encounter in a broad, stable three-line area adjacent to the crossing canopy. Use a mature Korean book serif with generous open counters, sturdy thin strokes, controlled triangular terminals and calm, consistent word spaces. Give its full syllable body, width and dark weight enough optical presence to lead; at the assumed SNS view, a comfortable roughly18–20pixel body is a starting design choice, not a required native coordinate. Keep paragraph ink clean and planar. Place the Korean title, Latin companion and slogan as one compact, clearly quieter identifying group beside its entry. Their role is to name and reinforce the already intelligible offer, not make three additional headlines.

From the paragraph's final line, the nearby market-name start continues down its optical axis onto the drawn specimens' shared stepped ground. Date, hours and venue extend as one clear horizontal visit row along that ground. Access and the care offer form the next short local row; invitation and URL complete the same visible ledger immediately nearby. Vary leaf and pot scale rather than breaking useful strings around different specimens. Use aligned baselines, adequate numeral and dash forms, visible word boundaries and deliberate group spacing. The botanical field remains substantial around and between these reading relationships. The explanation-to-ground movement and horizontal practical ledger differ from a left paragraph with a separate right information column.'''
d['hierarchy'] = {
    'primary': {'entry': 4, 'role': 'The broad three-line explanation is the main verbal encounter: full readable book-serif body, strong ink and optical area.'},
    'support': [
        {'entry': 1, 'role': 'Compact identity beside the paragraph entry, clearly quieter than the explanatory block.'},
        {'entry': 2, 'role': 'Small companion joined to that identity.'},
        {'entry': 3, 'role': 'Supporting sentence in the same identifying group, with lower visual weight.'},
    ],
    'visit': {'entries': [5, 6, 7, 8], 'shape': 'Market name begins below the paragraph end; date/hours/venue continue horizontally on the actual stepped-ground ledger.'},
    'next_action': {'entries': [9, 10, 11, 12], 'shape': 'Nearby succeeding ledger rows: access/care pair, then invitation/URL, all one local horizontal family.'},
}
d['body_end_to_next_info'] = 'The paragraph end and nearby market-name start share one optical axis and short downward transition. The specimens share a stepped ground that carries date/hours/venue horizontally, with access/care and invitation/URL succeeding locally. There is no separate right-hand visit column or return across an image to find the URL.'
d['nearest_peer'] = {
    'role_id': 'R19-C1-M3',
    'structural_distinction': 'M4 begins with the broad explanation and continues to a horizontal practical ledger on the specimens ground. M3 enters through date/hours/venue before turning between two connected colony openings; its identity is encountered later.',
    'style_distinction': 'M4 uses observed colored-pencil/ink anatomy, independently articulated specimens and an open stepped-ground field. M3 uses interlocking large flat cut-paper silhouettes surrounding an internal passage.',
}
plan['design_provenance']['root_amendment'] = 'Original plan kept unchanged. ROOT adapted common-constraint/role schema and redesigned M4 before generation because M1/M2/M4 had near prose-to-right-ledger geometry. No source artwork or previous poster was opened and no native call made for this amendment.'
plan['status'] = 'Reviewed prospective central plan; no native generation yet'
destination = source.with_name('root-plan.json')
with destination.open('x', encoding='utf-8') as handle:
    json.dump(plan, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
record = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_plan_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'root_plan_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
    'request_exact': True, 'all_copy_exact': True, 'all_body_line_groups_rejoin_exactly': True,
    'schema_adaptations': ['common_constraints object to strings list', 'direction role_id key to role'],
    'design_change': 'M4 actual first copy role, practical arrangement and image/copy ground relationship redesigned before generation; other4 direction objects unchanged except role-key adaptation.',
    'misreading_correction': 'Decoded JSON check found exact request match. Apparent newline mismatch in escaped tool display was a ROOT reading error; no request correction was needed.',
    'limits': ['Central plan comparison is not image quality scoring or an extra mandatory quality gate.', 'No generated images or future critic scores are available for this prospective case.'],
}
with source.with_name('root-amendment-record.json').open('x', encoding='utf-8') as handle:
    json.dump(record, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps({'root_plan': str(destination), 'roles': len(plan['directions']), 'native_calls': 0}))
