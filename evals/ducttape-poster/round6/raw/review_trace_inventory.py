"""Describe completed CLI trace observability without certifying visual reading."""
import collections, datetime, hashlib, json
from pathlib import Path

r=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
plan=read(r/'cli-reviews/dispatch-plan.json')
completed=read(r/'cli-reviews/all-completed.json')
assert completed['assignments']==len(plan['jobs'])
rows=[];intervals=[]
for job in plan['jobs']:
    wave,profile=job['wave'],job['profile']
    b=r/'cli-reviews'/wave/profile;c=read(b/'completion.json')
    events=[json.loads(x) for x in (b/'trace.jsonl').read_text().splitlines() if x.strip()]
    items=[x['item'] for x in events if x.get('type')=='item.completed']
    commands=[x['command'] for x in items if x.get('type')=='command_execution']
    first_packet=next((i for i,x in enumerate(commands) if 'packet.json' in x),None)
    action_reads=[i for i,x in enumerate(commands) if f'{profile}-action-first.json' in x and ('cat ' in x or 'read_text' in x or 'json.load' in x)]
    # This only identifies visible command strings, not all possible tool reads.
    touched=[z for x in items if x.get('type')=='file_change' for z in x.get('changes',[])]
    known_image_items=[x for x in items if 'view_image' in str(x.get('tool','')) or x.get('type') in ('image_view','view_image')]
    raw=r/f'blind-{wave}'/'reviews'/f'{profile}.json'
    record=read(raw) if raw.is_file() else {}
    rows.append({'wave':wave,'profile':profile,'session_id':c.get('cli_session_id'),
      'trace':{'path':str(b/'trace.jsonl'),'sha256':sha(b/'trace.jsonl')},
      'completed_item_types':dict(collections.Counter(x.get('type') for x in items)),
      'visible_command_count':len(commands),'first_packet_command_index':first_packet,
      'visible_action_record_read_command_indices':action_reads,
      'visible_action_read_before_first_packet_command':first_packet is not None and any(i<first_packet for i in action_reads),
      'serialized_image_view_item_count':len(known_image_items),
      'reported_main_view_record_count':len(record.get('viewed',[])),
      'visible_file_change_paths':[x.get('path') for x in touched],
      'scope':'Command ordering is partial trace evidence. Reported view records and visual transcription remain reviewer observations; absent serialized image-tool items do not establish that images were not viewed.'})
    parse=lambda s:datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
    intervals += [(parse(c['started_utc']),1),(parse(c['completed_utc']),-1)]
active=peak=0
for _,delta in sorted(intervals):active+=delta;peak=max(peak,active)
out={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assignments':len(rows),
 'actual_recorded_cli_interval_peak':peak,'rows':rows,
 'scope':'Runtime and partial command-trace inventory only, no rescoring, authorship or semantic viewing certificate.'}
with (r/'planning/review-trace-inventory.json').open('x') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({'assignments':len(rows),'recorded_cli_peak':peak,'serialized_image_view_item_counts':sorted({x['serialized_image_view_item_count'] for x in rows})}))
