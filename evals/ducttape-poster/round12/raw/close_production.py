"""Check actual whole-five production before critic sessions; no quality verdict."""
import datetime
import hashlib
import json
import shlex
import subprocess
from pathlib import Path
from seal_single_five import ROOT, PROFILES, read, pin, checked, returned_source, maker_provenance, validate_terminal


def no_critic_start_proof(case_id):
    """Allow untouched prepared jobs, but reject any runner-start evidence."""
    directory = ROOT/'reviews'
    existed = directory.exists()
    assert not directory.is_symlink(), 'Symlink in review evidence'
    prepared_files, jobs = [], []
    if existed:
        prefix = case_id+'/initial/'
        allowed = {'initial-stage-readiness.json'} | {
            prefix+name for name in ('case.json', 'packet.json', 'readiness.json')
        } | {prefix+'jobs/'+profile+'.json' for profile in PROFILES} | {
            prefix+'prompts/'+profile+'.txt' for profile in PROFILES
        }
        allowed_dirs = {str(parent) for name in allowed for parent in Path(name).parents if str(parent) != '.'}
        actual = set()
        for path in directory.rglob('*'):
            assert not path.is_symlink(), 'Symlink in review evidence'
            relative = str(path.relative_to(directory))
            if path.is_dir():
                assert relative in allowed_dirs, 'Critic output/unknown review directory already exists: '+relative
            else:
                assert path.is_file() and relative in allowed, 'Critic output/unknown review file already exists: '+relative
                actual.add(relative)
        assert actual == allowed, 'Incomplete or unexpected prepared review inventory'
        readiness = read(directory/'initial-stage-readiness.json')
        local = read(directory/prefix/'readiness.json')
        assert readiness['wave'] == 'initial' and set(readiness['cases']) == {case_id}
        assert readiness['all_makers_closed'] is True and readiness['closed_role_count'] == readiness['planned_role_count'] == 5
        assert readiness['cases'][case_id] == local and local['status'] == 'READY'
        assert local['mode'] == 'THREE_FRESH_COMPLETE_CRITICS'
        for profile in PROFILES:
            path = directory/prefix/'jobs'/(profile+'.json')
            job = read(path)
            assert job['case_id'] == case_id and job['wave'] == 'initial' and job['profile'] == profile
            assert job['prompt_file'] == str(directory/prefix/'prompts'/(profile+'.txt'))
            output = directory/prefix/'cli'/profile
            assert job['output_dir'] == str(output) and not output.exists()
            assert job['expected_outputs'] == [profile+'.observations.json', profile+'.json', profile+'.md']
            jobs.append({'profile':profile, 'job':pin(path), 'expected_output_dir':str(output), 'output_dir_absent':True})
        prepared_files = [pin(directory/name) for name in sorted(actual)]
    # The frozen runner creates its output directory and launch.json before
    # starting codex. No such artifacts exist above; also reject a current exec
    # or runner that could be starting before its launch record is visible.
    snapshot = subprocess.check_output(['ps', '-axo', 'pid=,ppid=,command='], text=True)
    live = []
    for line in snapshot.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) != 3:
            continue
        try:
            argv = shlex.split(parts[2])
        except ValueError:
            assert str(directory) not in parts[2], 'Unparseable process with review path'
            continue
        if not argv:
            continue
        executable = Path(argv[0]).name
        runner = executable.startswith('python') and any(Path(arg).name in ('run_agent.py', 'run_pool.py') for arg in argv[1:])
        review_exec = executable == 'codex' and 'exec' in argv and any(
            arg == str(directory) or arg.startswith(str(directory)+'/') or arg == 'reviews' or arg.startswith('reviews/')
            for arg in argv
        )
        if runner or review_exec:
            live.append({'pid':int(parts[0]), 'ppid':int(parts[1]), 'argv':argv})
    assert not live, 'A critic/runner process is already active; production closure remains unsealable'
    return {
        'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'reviews_directory_existed':existed,
        'production_closure_before_review_preparation':not existed,
        'prepared_jobs_exist':bool(jobs),
        'prepared_jobs':jobs,
        'prepared_files':prepared_files,
        'critic_runner_output_directories':0,
        'critic_launch_trace_completion_or_report_files':0,
        'actual_critic_sessions_observed':0,
        'live_critic_or_runner_processes':live,
        'process_snapshot_sha256':hashlib.sha256(snapshot.encode()).hexdigest(),
        'criterion':'Before actual critic starts, proven by complete preparation-only inventory and absence of frozen-runner start artifacts/current exec processes.',
        'limits':'Prepared jobs are retained. This is a protocol/file/process check; arbitrary unrecorded activity is not authenticated.'
    }


def main():
    freeze = read(ROOT/'planning/candidate-l-pre-generation-freeze.json')
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
    assert active == 0 and peak <= 3
    assert not (ROOT/'reviews').exists(), 'Prospective R12 requires closure BEFORE packet preparation'
    critic_proof = no_critic_start_proof(case['case_id'])
    result = {'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'roles':roles,
              'all5_before_critics':critic_proof['actual_critic_sessions_observed'] == 0,
              'all5_before_critics_semantics':'Production validation completed before actual critic starts; review preparation is also absent.',
              'critic_start_proof':critic_proof, 'native_attempts':attempts,
              'native_attempt_cap':15,'failures':failures,'actual_peak_maker_workers':peak,
              'native_source_cache_checks':cache_checks,
              'limits':'Actual byte/terminal/caller-literal/cache coverage only. Preserved ephemeral CLI traces expose caller-record persistence and save-native commands, not direct native MCP invocation/result events; independent quality and semantic viewing remain separate.'}
    assert result['all5_before_critics']
    with (ROOT/'planning/single-five-production-closure.json').open('x',encoding='utf-8') as handle:
        json.dump(result,handle,ensure_ascii=False,indent=2);handle.write('\n')
    print(json.dumps({'closed_roles':5,'native_attempts':attempts,'failures':failures,'peak_maker_workers':peak}))


if __name__ == '__main__':
    main()
