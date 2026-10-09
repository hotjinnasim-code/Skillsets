"""Metadata/opaque-byte checks only; does not execute closure, seal or actors."""
import ast
import datetime
import hashlib
import json
import re
import shlex
import subprocess
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORY = ROOT/'checks/closure-helper-history'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pin(path):
    return {'path':str(path), 'sha256':sha(path), 'bytes':path.stat().st_size}

def functions(path, names, namespace):
    source = path.read_bytes()
    compile(source, str(path), 'exec')
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)

ns = {'ROOT':ROOT, 'Path':Path, 'hashlib':hashlib, 're':re, 'json':json}
functions(ROOT/'seal_single_five.py', {'read','pin','returned_source'}, ns)
ns.update(PROFILES=('editorial','craft','portfolio'), datetime=datetime, shlex=shlex, subprocess=subprocess)
functions(ROOT/'close_production.py', {'no_critic_start_proof'}, ns)
parse = ns['returned_source']
proof = ns['no_critic_start_proof']
pre = json.loads((HISTORY/'r11-return-source-closure-pre-edit.json').read_bytes())

def unchanged():
    for name, row in pre['protected_evidence_before'].items():
        assert pin(ROOT/name) == row
    for row in pre['frozen_pins_verified']:
        assert pin(Path(row['path'])) == row

unchanged()
indices = {
    1:[(21,22,23,24),(32,33,34,35),(43,44,45,46)],
    2:[(25,26,27,28),(36,37,38,39),(47,48,49,50)],
    3:[(24,25,26,27),(36,37,38,39),(47,48,49,50)],
    4:[(28,29,30,31),(37,38,39,40),(46,47,48,49)],
    5:[(23,24,25,26),(35,36,37,38),(46,47,48,49)]
}

def inner_args(command):
    outer = shlex.split(command)
    assert outer[:2] == ['/bin/zsh','-lc']
    return shlex.split(outer[2])

def records(argv):
    candidates = []
    for value in argv:
        try:
            data = json.loads(value)
        except (ValueError,TypeError):
            continue
        if isinstance(data,dict):
            candidates.append(data)
    if '-c' in argv:
        for node in ast.walk(ast.parse(argv[argv.index('-c')+1])):
            if (isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute)
                and isinstance(node.func.value,ast.Name) and node.func.value.id == 'json'
                and node.func.attr == 'loads' and node.args and isinstance(node.args[0],ast.Constant)
                and isinstance(node.args[0].value,str)):
                try:
                    data = json.loads(node.args[0].value)
                except ValueError:
                    continue
                if isinstance(data,dict):
                    candidates.append(data)
    return [r for data in candidates for r in (data,data.get('record'))
            if isinstance(r,dict) and r.get('outcome') == 'returned'
            and r.get('native_tool') == 'tools.image_gen__imagegen']

inventory, caches = [], []
for maker in range(1,6):
    directory = ROOT/'production'/f'R11-C1-M{maker}'
    completion = json.loads((directory/'completion.json').read_bytes())
    launch = json.loads((directory/'launch.json').read_bytes())
    trace = directory/'trace.jsonl'
    lines = trace.read_bytes().splitlines()
    events = [json.loads(line) for line in lines]
    assert sha(trace) == completion['trace']['sha256']
    session = completion['session_ids'][0]
    assert [e['thread_id'] for e in events if e.get('type') == 'thread.started'] == [session]
    assert '--ephemeral' in launch['argv'] and completion['argv'] == launch['argv']
    assert completion['exit_code'] == 0 and completion['input_pins_unchanged'] is True
    assert not any(e.get('item',{}).get('type') in ('mcp_tool_call','tool_call') for e in events)
    expected = {}
    for stage, (cs,cc,ss,sc) in zip(('initial','repair-1','repair-2'),indices[maker]):
        path = directory/'stages'/stage/'native-call.json'
        caller = json.loads(path.read_bytes())
        literal = parse(caller)
        manifest_path = path.parent/'manifest.json'
        manifest = json.loads(manifest_path.read_bytes())
        source = Path(literal)
        assert literal == manifest['source_argument'] == manifest['source']['path']
        assert source.parent == Path('/Users/nahyeonbin/.codex/generated_images')/session
        assert sha(source) == manifest['source']['sha256'] == sha(Path(manifest['files']['original']['path']))
        linked = []
        for start,end in ((cs,cc),(ss,sc)):
            a,b = events[start-1],events[end-1]
            assert a['type'] == 'item.started' and b['type'] == 'item.completed'
            assert a['item']['id'] == b['item']['id'] and b['item']['type'] == 'command_execution'
            assert b['item']['exit_code'] == 0
            linked.append({'id':b['item']['id'], 'started_line':start, 'completed_line':end,
                           'started_line_sha256':hashlib.sha256(lines[start-1]).hexdigest(),
                           'completed_line_sha256':hashlib.sha256(lines[end-1]).hexdigest(),
                           'event_type':'command_execution', 'exit_code':0})
        assert caller in records(inner_args(events[cc-1]['item']['command']))
        save = inner_args(events[sc-1]['item']['command'])
        assert 'save-native' in save and save[save.index('--source')+1] == literal
        output = json.loads(events[sc-1]['item']['aggregated_output'])
        assert output['manifest']['path'] == str(manifest_path) and output['manifest']['sha256'] == sha(manifest_path)
        assert output['source_sha256'] == manifest['source']['sha256']
        fields = [key for key in ('returned_source_path','exact_source_path_from_return','explicit_returned_source_path',
                  'returned_source_paths','explicit_returned_source_paths','explicit_returned_png_paths') if key in caller]
        for key in ('result_metadata','tool_return_metadata','returned_metadata','returned_result_metadata'):
            if isinstance(caller.get(key),dict):
                if 'output_hint' in caller[key]:
                    fields.append(key+'.output_hint')
                if 'hints' in caller[key]:
                    fields.append(key+'.hints[field=result.output_hint].value')
        inventory.append({'role':caller['role'], 'stage':stage, 'caller':pin(path), 'literal_source_fields':fields,
                          'literal_source_path':literal, 'manifest':pin(manifest_path), 'source':pin(source),
                          'caller_record_persistence':linked[0], 'save_native':linked[1], 'trace':pin(trace),
                          'session_id':session, 'direct_native_mcp_event_in_preserved_trace':False,
                          'checks':'literal/caller-serialization/save-native/manifest/source-hash/session-cache all agree'})
        expected[literal] = sha(source)
    actual = {str(path):sha(path) for path in source.parent.glob('*.png')}
    assert expected == actual
    caches.append({'role':directory.name, 'session':session, 'matches':True, 'exact_source_count':len(actual), 'sources':expected})

literal = '/literal/session/image.png'
hint = f'Generated images are saved to /literal/session as {literal} by default.'
positive = []
for key in ('returned_source_path','exact_source_path_from_return','explicit_returned_source_path'):
    assert parse({key:literal}) == literal
    positive.append(key)
for key in ('returned_source_paths','explicit_returned_source_paths','explicit_returned_png_paths'):
    assert parse({key:[literal]}) == literal
    positive.append(key)
for key in ('result_metadata','tool_return_metadata','returned_metadata','returned_result_metadata'):
    assert parse({key:{'output_hint':hint}}) == literal
    positive.append(key+'.output_hint')
    assert parse({key:{'hints':[{'field':'result.output_hint','value':hint}]}}) == literal
    positive.append(key+'.hints')
assert parse({'returned_result_hints':[{'field':'result.output_hint','value':hint}]}) == literal
positive.append('returned_result_hints')
negative = [
    ('missing',{}), ('directory-only',{'result_metadata':{'directory':'/literal/session'}}),
    ('wrong-scalar-type',{'explicit_returned_source_path':[literal]}),
    ('wrong-list-type',{'explicit_returned_png_paths':literal}), ('empty-list',{'explicit_returned_png_paths':[]}),
    ('two-list-paths',{'explicit_returned_png_paths':[literal,'/literal/session/other.png']}),
    ('conflicting-scalar-hint',{'explicit_returned_source_path':'/literal/session/other.png','result_metadata':{'hints':[{'field':'result.output_hint','value':hint}]}}),
    ('conflicting-M3-list-hint',{'explicit_returned_png_paths':['/literal/session/other.png'],'returned_metadata':{'output_hint':hint}}),
    ('conflicting-hints',{'result_metadata':{'output_hint':hint,'hints':[{'field':'result.output_hint','value':hint.replace('image.png','other.png')}]}}),
    ('metadata-not-dict',{'result_metadata':[hint]}), ('hints-not-list',{'result_metadata':{'hints':hint}}),
    ('hint-not-dict',{'result_metadata':{'hints':[hint]}}),
    ('wrong-hint-type',{'result_metadata':{'hints':[{'field':'result.output_hint','value':[hint]}]}}),
    ('freeform-hint',{'result_metadata':{'output_hint':'image saved /literal/session/image.png'}}),
    ('directory-mismatch',{'result_metadata':{'output_hint':hint.replace('to /literal/session as','to /other as')}}),
    ('relative',{'explicit_returned_source_path':'literal/image.png'}),
    ('traversal',{'explicit_returned_source_path':'/literal/../image.png'}),
    ('noncanonical-dot',{'explicit_returned_source_path':'/literal/./image.png'}),
    ('wrong-suffix',{'explicit_returned_source_path':'/literal/image.jpg'}),
    ('newline',{'explicit_returned_source_path':'/literal/im\nage.png'}),
    ('nul',{'explicit_returned_source_path':'/literal/im\x00age.png'})
]
for label,caller in negative:
    try:
        parse(caller)
    except AssertionError:
        pass
    else:
        raise AssertionError('Negative accepted: '+label)

actual_proof = proof('R11-C1')
assert actual_proof['reviews_directory_existed'] and actual_proof['prepared_jobs_exist']
assert actual_proof['production_closure_before_review_preparation'] is False
assert actual_proof['actual_critic_sessions_observed'] == 0
critic_negative = []
with tempfile.TemporaryDirectory(prefix='r11-no-critic-proof-') as temp:
    temporary = Path(temp).resolve()
    review = temporary/'reviews'
    review.mkdir()
    ns['ROOT'] = temporary
    ns['subprocess'] = types.SimpleNamespace(check_output=lambda *a,**k:'')
    for path in (ROOT/'reviews').rglob('*'):
        target = review/path.relative_to(ROOT/'reviews')
        if path.is_dir():
            target.mkdir(exist_ok=True)
        else:
            data = path.read_bytes()
            if path.parent.name == 'jobs':
                job = json.loads(data)
                for field in ('output_dir','prompt_file'):
                    job[field] = str(temporary/Path(job[field]).relative_to(ROOT))
                data = json.dumps(job).encode()
            target.write_bytes(data)
    proof('R11-C1')
    def reject(label, operation, restore):
        operation()
        try:
            proof('R11-C1')
        except AssertionError:
            critic_negative.append(label)
        else:
            raise AssertionError('Critic negative accepted: '+label)
        finally:
            restore()
    path = review/'R11-C1/initial/cli'
    reject('empty-output-directory',lambda:path.mkdir(),lambda:path.rmdir())
    path = review/'R11-C1/initial/launch.json'
    reject('launch-artifact',lambda:path.write_text('{}'),lambda:path.unlink())
    path = review/'.unknown'
    reject('hidden-unknown-artifact',lambda:path.write_text('x'),lambda:path.unlink())
    path = review/'R11-C1/initial/packet.json'
    raw = path.read_bytes()
    reject('incomplete-preparation',lambda:path.unlink(),lambda:path.write_bytes(raw))
    path = review/'R11-C1/initial/jobs/editorial.json'
    raw = path.read_bytes()
    job = json.loads(raw);job['output_dir'] = str(review/'wrong-output')
    reject('wrong-job-output-binding',lambda:path.write_text(json.dumps(job)),lambda:path.write_bytes(raw))
    path = review/'R11-C1/initial/prompts/editorial.txt'
    raw = path.read_bytes();outside = temporary/'outside';outside.write_bytes(raw)
    reject('symlink-preparation',lambda:(path.unlink(),path.symlink_to(outside)),lambda:(path.unlink(),path.write_bytes(raw)))
    for label,command in (
        ('live-runner-process',f'11 1 python3 {temporary}/run_agent.py --job {review}/R11-C1/initial/jobs/editorial.json'),
        ('live-review-exec-process',f'12 1 codex exec --ephemeral --json -C {review}/R11-C1/initial/cli/editorial -')
    ):
        ns['subprocess'] = types.SimpleNamespace(check_output=lambda *a,command=command,**k:command+'\n')
        try:
            proof('R11-C1')
        except AssertionError:
            critic_negative.append(label)
        else:
            raise AssertionError('Live process accepted: '+label)
ns['ROOT'] = ROOT
ns['subprocess'] = subprocess
unchanged()
result = {
    'schema_version':1, 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'PASS_SAME_EXISTING_EVIDENCE_LEVEL', 'native_call_count':len(inventory),
    'all15_inventory':inventory, 'session_cache_checks':caches,
    'parser_positive_schema_cases':positive, 'parser_negative_cases':[label for label,_ in negative],
    'parser_all15_accepted':True, 'critic_start_proof_actual':actual_proof,
    'critic_start_negative_cases':critic_negative,
    'frozen_pin_rows_verified_unchanged':len(pre['frozen_pins_verified']),
    'production_and_prepared_review_files_verified_unchanged':len(pre['protected_evidence_before']),
    'closure_or_seal_or_native_or_critic_launched':False, 'visual_pixels_viewed':False,
    'quality_scores_evaluated':False,
    'verification_attempt_history':[
        {'status':'ENVIRONMENT_IMPORT_FAILED','reason':'System python lacks PIL; changed to AST extraction of only pure metadata functions without importing image helpers.'},
        {'status':'AUDIT_ASSERTION_SCHEMA_CORRECTED','reason':'Verifier initially expected nested source.sha256 in save-native output; actual output source_sha256 was inspected and the verifier corrected without changing any evidence or helper.'},
        {'status':'FIXTURE_PATH_CORRECTED','reason':'macOS /var temporary-root alias is a symlink; resolved the isolated fixture root to its canonical /private path so unchanged pin containment rules apply.'}
    ],
    'direct_native_tool_event_authentication':'Unavailable in preserved ephemeral CLI traces; caller serialization and save-native events do not authenticate direct native return.'
}
with (HISTORY/'r11-return-source-closure-validation.json').open('x',encoding='utf-8') as handle:
    json.dump(result,handle,ensure_ascii=False,indent=2);handle.write('\n')
print(json.dumps({'status':result['status'], 'all15':len(inventory), 'parser_positive_schemas':len(positive),
                  'parser_negative_cases':len(negative), 'no_critic_negative_cases':len(critic_negative),
                  'protected_files':len(pre['protected_evidence_before']), 'actual_critic_sessions_observed':0}))
