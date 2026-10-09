"""Root-only report of closed historical H evidence; never invent missing scores."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIMS = ('content_form', 'hierarchy', 'typography', 'space', 'image_material', 'emotion_control', 'ai_slop')
PROFILES = ('editorial', 'craft', 'portfolio')


def main():
    final = json.loads((ROOT/'planning/final-evidence.json').read_bytes())
    corpus = json.loads((ROOT/'planning/corpus20.json').read_bytes())
    assert final['poster_calls_closed'] is True and final['poster_role_denominator'] == 20
    lines = ['# Historical H: closed twenty-role evidence', '',
             'These images were already generated. This closes their original bounded experiment; it launches no new twenty-image campaign.', '',
             f"Native poster attempts: {final['poster_native_attempts']}; fixture native attempts separately: {final['fixture_native_attempts_separate']}.",
             f"Actual unique fresh critic sessions: {final['actual_unique_review_sessions']}; actual unique records/score slots/valid values: {final['actual_review_counts']}.", '',
             '[Selected gallery](gallery.html) · [Closed evidence](planning/final-evidence.json) · [Native source coverage](planning/native-source-inventory.json)', '',
             'H is instrumented development evidence. Its maker harness forced the full literal request before the printed-copy specification on every native call, beyond the runtime skill. Do not claim ordinary-use prompting or isolate the runtime as the cause of these results. [Scope finding](planning/instrumentation-scope-finding.md).', '',
             'All seven quality categories, mandatory conditions, per-critic floor4 and whole-set diversity remain unchanged. Low scores, unresolved copy/action ambiguity and procedural NA are retained. One selected critic has recovered transport errors; frozen v4 still invalidates its whole case. [Recorded procedure finding](planning/b04-selected-procedural-finding.json). No critic was replaced.', '',
             '| Case | Requested roles | Initial image gates | Initial set | Selected image gates | Selected set |',
             '| --- | ---: | --- | --- | --- | --- |']
    for case in corpus['cases']:
        cid = case['case_id']
        first = final['stages']['initial']['cases'][cid]
        last = final['stages']['selected']['cases'][cid]
        counts = lambda wave: {g:sum(final['stages'][wave]['image_gates'][r['role_id']]==g for r in case['roles']) for g in ('PASS','FAIL','NA')}
        lines.append(f"| {cid} | {case['count']} | {counts('initial')} | {first['gate']} | {counts('selected')} | {last['gate']} |")
    lines += ['', f"Initial whole-corpus gate: **{final['stages']['initial']['whole_corpus_gate']}**; selected whole-corpus gate: **{final['stages']['selected']['whole_corpus_gate']}**.", '',
              'This finite historical evidence does not certify the later I runtime or unseen requests. I closes a separate single-five development request; its subsequent landscape request is a separate transfer observation. Source viewing and visual judgment remain semantic attestations, while native bytes and actual CLI identities have explicit provenance.', '']
    for wave in ('initial','selected'):
        lines += ['## '+wave+' raw scores', '', '| Case / image | Critic | Content | Hierarchy | Type | Space | Material | Emotion | AI slop |', '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
        for case in corpus['cases']:
            item = final['stages'][wave]['cases'][case['case_id']]
            if 'summary' not in item:
                lines.append(f"| {case['case_id']} | unready; retained NA | | | | | | | |")
                continue
            data = json.loads(Path(item['summary']['path']).read_bytes())
            for role in case['roles']:
                for profile in PROFILES:
                    scores = data['reviews'][profile]['images'].get(role['role_id'],{}).get('scores',{})
                    values = [str(scores[d]) if d in scores else 'missing' for d in DIMS]
                    lines.append('| '+role['role_id']+' | '+profile+' | '+' | '.join(values)+' |')
        lines += ['', 'Complete readings, located evidence, all unfavorable records and provenance:', '']
        for case in corpus['cases']:
            item = final['stages'][wave]['cases'][case['case_id']]
            if 'summary' in item:
                rel = Path(item['summary']['path']).relative_to(ROOT).as_posix()
                reuse = ' (complete initial three retained; no new critic)' if item['reused_complete_initial_three'] else ''
                lines.append(f"- [{case['case_id']}]({rel}){reuse}")
        lines.append('')
    with (ROOT/'report.md').open('x',encoding='utf-8') as handle:
        handle.write('\n'.join(lines)+'\n')
    print(json.dumps({'closed_report':str(ROOT/'report.md'),'native_generation':0,'quality_or_raw_score_changes':False}))


if __name__ == '__main__':
    main()
