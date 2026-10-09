"""Corroborate saved successful native stages with each fresh maker's own cache."""
import argparse, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def audit(require_all=True):
    corpus=json.loads((ROOT/'planning/corpus20.json').read_bytes()); rows=[]; errors=[]; open_roles=[]
    for case in corpus['cases']:
        for role in case['roles']:
            d=ROOT/'production'/role['role_id']; cp=d/'completion.json'
            if not cp.is_file(): open_roles.append(role['role_id']); continue
            completion=json.loads(cp.read_bytes()); sessions=completion['session_ids']
            if len(sessions)!=1: errors.append(role['role_id']+': exactly one actual session required'); continue
            folder=Path('/Users/nahyeonbin/.codex/generated_images')/sessions[0]
            actual={str(p.resolve()):digest(p) for p in folder.glob('*.png')}
            expected={}
            for mp in (d/'stages').glob('*/manifest.json'):
                m=json.loads(mp.read_bytes()); source=m['source']; expected[str(Path(source['path']).resolve())]=source['sha256']
                if digest(m['files']['original']['path'])!=source['sha256']:errors.append(role['role_id']+': original/source mismatch')
            if expected!=actual: errors.append(role['role_id']+': fresh session cache and complete successful-stage source inventory disagree')
            rows.append({'role':role['role_id'],'session':sessions[0],'completion_path':str(cp),'completion_sha256':digest(cp),'cache_folder':str(folder),'expected_sources':expected,'actual_sources':actual,'matches':expected==actual})
    if require_all and open_roles: errors.append('All twenty roles must be terminal before full source coverage can pass')
    return {'status':'FAIL' if errors else 'PASS','scope':'Complete H successful native source cache corroboration' if require_all else 'Partial terminal-role cache corroboration, not whole-phase closure','planned_roles':20,'audited_roles':len(rows),'open_roles':open_roles,'errors':errors,'records':rows,'limits':['This verifies exact files and coverage, not aesthetic quality or serialized tool events. Failed attempts remain counted by actual caller records even when no image file is created.']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args();result=audit(not a.partial)
    if a.output:
        with a.output.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}));raise SystemExit(0 if result['status']=='PASS' else 1)
