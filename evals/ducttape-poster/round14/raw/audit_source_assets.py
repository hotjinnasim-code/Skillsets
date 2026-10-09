"""Check source-view attestations already required by the frozen critic prompt."""
import argparse,hashlib,json
from pathlib import Path
PROFILES=('editorial','craft','portfolio')

def pin(p):
    p=Path(p).resolve(strict=True)
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def audit(packet_path,report_dir):
    packet=json.loads(Path(packet_path).read_bytes()); assets=packet.get('source_assets',[]); layouts=packet.get('protected_layouts',[])
    expected={a['asset_id']:(a['actual_path'],a['sha256']) for a in assets}
    expected_layout={(x['manifest']['path'],x['manifest']['sha256']) for x in layouts}
    results={}
    for profile in PROFILES:
        rp=Path(report_dir)/profile/(profile+'.json'); errors=[]
        try:
            raw=json.loads(rp.read_bytes()); proc=raw.get('procedure',{})
            seen=proc.get('source_assets_viewed',[])
            if not isinstance(seen,list): errors.append('source_assets_viewed must be an array');seen=[]
            actual={}
            for item in seen:
                if not isinstance(item,dict) or item.get('asset_id') in actual or item.get('viewed') is not True:
                    errors.append('Every actual source must have one truthful asset_id/path/sha256/viewed:true entry');continue
                actual[item.get('asset_id')]=(item.get('path'),item.get('sha256'))
            if actual!=expected:errors.append('Source view identities/pins do not match all actual packet assets')
            reads=proc.get('protected_layouts_read',[])
            if not isinstance(reads,list):errors.append('protected_layouts_read must be an array');reads=[]
            actual_layout=set()
            for item in reads:
                if not isinstance(item,dict):errors.append('Protected-layout read must name its exact manifest pin');continue
                manifest=item.get('manifest',item)
                if item.get('read') is False or not isinstance(manifest,dict):errors.append('Protected-layout read denied or malformed');continue
                pair=(manifest.get('path'),manifest.get('sha256'))
                if pair in actual_layout:errors.append('Duplicate protected-layout read entry')
                actual_layout.add(pair)
            if actual_layout!=expected_layout:errors.append('Protected-layout read pins do not match all prescribed packet manifests')
            results[profile]={'gate':'NA' if errors else 'PASS','errors':errors,'raw_report':pin(rp),'observed_source_assets_viewed':seen,'observed_protected_layouts_read':reads}
        except (OSError,ValueError,TypeError,AttributeError) as exc:
            results[profile]={'gate':'NA','errors':[str(exc)],'raw_report':pin(rp) if rp.is_file() else None}
    return {'kind':'prescribed_source_attestation_audit','packet':pin(packet_path),'case_id':packet['case_id'],'wave':packet['wave'],'gate':'NA' if any(r['gate']=='NA' for r in results.values()) else 'PASS','expected_source_assets':len(expected),'expected_protected_layout_manifests':len(expected_layout),'profiles':results,'limits':['Checks existing frozen prompt requirements; no new aesthetic gate, raw rewrite or critic replacement.','Source viewing/read and order are semantic attestations, not serialized native-tool events.','The original frozen v4 summary remains separately preserved.']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--report-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.packet,a.report_dir)
    with a.output.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2)
    print(json.dumps({'case_id':r['case_id'],'wave':r['wave'],'source_attestation_gate':r['gate'],'expected_assets':r['expected_source_assets']}))
