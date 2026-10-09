"""Check actual whole-five production before critic jobs; no visual quality verdict."""
import datetime
import json
from pathlib import Path
from seal_single_five import ROOT, read, pin, checked, returned_source, maker_provenance, validate_terminal


def main():
    freeze = read(ROOT/'planning/candidate-i-pre-generation-freeze.json')
    for row in freeze['runtime_files']+freeze['helpers']+freeze['references']:
        checked(row)
    for key in ('case','central_plan','ratio'):
        checked(freeze[key])
    case = read(freeze['case']['path'])['cases'][0]
    assert case['count'] == len(case['roles']) == 5
    roles, cache_checks, intervals, sessions = [], [], [], []
    attempts = failures = 0
    for role in case['roles']:
        rid = role['role_id']; directory = ROOT/'production'/rid
        validated = validate_terminal(ROOT/'production', role, case['case_id'])
        assert validated['closed'] and not validated['errors'], validated['errors']
        paths = [p for p in (directory/'selection.json',directory/'unavailable.json') if p.is_file()]
        assert len(paths) == 1
        completion, session = maker_provenance(directory,rid,paths[0])
        sessions.append(session)
        result = read(paths[0])
        expected = {}
        for stage in validated['stages']:
            stage_dir = directory/'stages'/stage['stage']
            caller = read(stage_dir/'native-call.json')
            assert caller['role'] == rid and caller['stage'] == stage['stage'] and caller['outcome'] == stage['outcome']
            if stage['outcome'] == 'returned':
                manifest = read(stage_dir/'manifest.json')
                assert returned_source(caller) == manifest['source']['path']
                assert checked(manifest['source'])['sha256'] == checked(manifest['files']['original'])['sha256']
                expected[str(Path(manifest['source']['path']).resolve())] = manifest['source']['sha256']
        expected_callers = {str((directory/'stages'/s['stage']/'native-call.json').resolve()) for s in validated['stages']}
        assert expected_callers == {str(p.resolve()) for p in directory.rglob('native-call.json')}
        cache = Path('/Users/nahyeonbin/.codex/generated_images')/session
        actual = {str(p.resolve()):pin(p)['sha256'] for p in cache.glob('*.png')}
        assert actual == expected
        cache_checks.append({'role':rid,'session':session,'matches':True,'sources':expected})
        attempts += result['counts']['native_calls']; failures += result['counts']['failed']
        intervals += [(completion['started_utc'],1),(completion['completed_utc'],-1)]
        roles.append({'role':rid,'session':session,'counts':result['counts'],'selected_stage':result.get('selected_stage'),
                      'started_utc':completion['started_utc'],'completed_utc':completion['completed_utc'],
                      'completion':pin(directory/'completion.json'),'terminal':pin(paths[0])})
    assert len(set(sessions)) == 5 and attempts <= 15
    active = peak = 0
    for _,delta in sorted(intervals,key=lambda x:(x[0],x[1])):
        active += delta; peak = max(peak,active)
        assert active >= 0
    assert active == 0 and peak <= 2
    result = {'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'roles':roles,
              'all5_before_critics':not (ROOT/'reviews').exists(), 'native_attempts':attempts,
              'native_attempt_cap':15,'failures':failures,'actual_peak_maker_workers':peak,
              'native_source_cache_checks':cache_checks,
              'limits':'Actual byte/terminal/caller/cache coverage only; independent quality and semantic viewing remain separate.'}
    assert result['all5_before_critics']
    with (ROOT/'planning/single-five-production-closure.json').open('x',encoding='utf-8') as handle:
        json.dump(result,handle,ensure_ascii=False,indent=2);handle.write('\n')
    print(json.dumps({'closed_roles':5,'native_attempts':attempts,'failures':failures,'peak_maker_workers':peak}))


if __name__ == '__main__':
    main()
