"""Recheck immutable whole-case reuse without changing a raw evaluation."""
import hashlib, json

PROFILES = ('editorial', 'craft', 'portfolio')
CONTEXT_KEYS = ('case_id', 'candidate_label', 'expected_count', 'full_request', 'literal_case_sha256', 'normalization', 'requirements', 'copy', 'review_rules', 'critic_rubric', 'ratio_policy', 'helper_pins', 'source_assets', 'protected_layouts', 'images')

def check_reuse(initial, selected, summary, reuse, initial_packet_pin, summary_pin, exact_pin):
    first = {k: initial[k] for k in CONTEXT_KEYS}
    later = {k: selected[k] for k in CONTEXT_KEYS}
    assert first == later, 'Whole-case reuse context differs'
    assert summary['raw_packet'] == initial and summary['procedure_gate'] == 'PASS' and not summary['procedure_errors']
    n = initial['expected_count']
    assert summary['counts']['observed_image_profile_records'] == 3*n
    assert summary['counts']['valid_integer_1_to_5_score_values'] == 21*n
    retained = {}; sessions = []
    for p in PROFILES:
        review = summary['reviews'][p]; prov = review['provenance']
        assert not review['procedure_errors'] and not review['set']['errors']
        assert set(review['images']) == {i['image_id'] for i in initial['images']}
        assert all(not row['errors'] for row in review['images'].values())
        session = prov['derived_session_id']; sessions.append(session)
        retained[p] = {'raw_report': exact_pin(review['raw_report']), 'launch': exact_pin(prov['launch_pin']), 'completion': exact_pin(prov['completion_pin']), 'trace': exact_pin(prov['trace_pin']), 'actual_session_id': session}
    assert len(set(sessions)) == 3
    expected = {'kind': 'complete_whole_case_reuse', 'initial_packet':initial_packet_pin, 'initial_summary':summary_pin, 'retained_critics':retained, 'mapping':[{'image_id':i['image_id'], 'role':i['role'], 'initial_stage':i['stage'], 'selected_stage':i['stage'], 'native_sha256':i['views']['native']['sha256']} for i in initial['images']], 'low_or_na_gates_retained':True, 'context_sha256':hashlib.sha256(json.dumps(first,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
    assert reuse == expected, 'Reuse mapping/pin/session inventory differs'
    return True
