#!/usr/bin/env python3
"""Read-only accounting for closed D/E and separately predeclared F/G calls."""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--allow-incomplete', action='store_true', help='Report open F/G calls without claiming phase closure.')
a = ap.parse_args()
r = Path(__file__).resolve().parent
errors, results, events, incomplete = [], {}, [], []
phases = [('D', r), ('E', r / 'continuation-e'), ('F', r / 'continuation-f'), ('G', r / 'continuation-g')]
caps = {'D': 24, 'E': 6, 'F': 6, 'G': 9}
for phase, phase_root in phases:
    command = [sys.executable, str(phase_root / 'validate.py')]
    if phase in {'F', 'G'}:
        command.append('--allow-incomplete')
    v = subprocess.run(command, capture_output=True, text=True)
    try:
        out = json.loads(v.stdout)
    except (ValueError, TypeError):
        errors.append(phase + ' validator produced no valid JSON')
        results[phase] = {'status': 'FAIL', 'recorded_calls': 0, 'records': [], 'errors': [v.stderr]}
        continue
    results[phase] = out
    if v.returncode != 0 or out['status'] == 'FAIL':
        errors.append(phase + ' validator not PASS: ' + out['status'])
    elif out['status'] == 'INCOMPLETE':
        incomplete.append(phase)
    elif out['status'] != 'PASS':
        errors.append(phase + ' validator has unknown status: ' + out['status'])
    if out.get('phase_cap') != caps[phase] or out['recorded_calls'] > caps[phase]:
        errors.append(phase + ' original/separate cap changed or exceeded')
    for row in out['records']:
        events.extend([(row['start'], 1), (row['end'], -1)])

closure = json.loads((r / 'planning/DE-call-phase-closure.json').read_text())
f_plan = json.loads((r / 'continuation-f/planning/phase-plan.json').read_text())
g_plan_path = r / 'continuation-g/planning/phase-plan.json'
g_plan = json.loads(g_plan_path.read_text())
if hashlib.sha256(g_plan_path.read_bytes()).hexdigest() != '96160b13510366e678e1f7d2769374e22366e07baa9d3ebf1785bbd492f2a3a8':
    errors.append('Predeclared G plan changed')
for phase, expected_used in [('D', 16), ('E', 5)]:
    if results[phase]['recorded_calls'] != closure[phase]['used'] or closure[phase]['used'] != expected_used:
        errors.append('Closed ' + phase + ' count changed')
    if closure[phase]['unchanged_original_cap'] != caps[phase]:
        errors.append('Closed ' + phase + ' original cap changed')
    if closure[phase]['unused_retired'] != caps[phase] - closure[phase]['used']:
        errors.append('Closed ' + phase + ' retirement differs')
base = 95 + results['D']['recorded_calls'] + results['E']['recorded_calls']
total = base + results['F']['recorded_calls'] + results['G']['recorded_calls']
if base != 116 or base != closure['whole_completed'] or base != f_plan['accounting']['closed_history_before_F']:
    errors.append('Closed whole history base differs')
if (closure.get('historical_before_round5') != 95 or f_plan['scope']['phase_native_call_cap'] != 6
        or g_plan['scope']['phase_native_call_cap'] != 9
        or g_plan['accounting']['closed_DE_whole_history'] != 116
        or g_plan['accounting']['F_unchanged_cap'] != 6 or g_plan['accounting']['G_separate_cap'] != 9
        or g_plan['accounting']['maximum_active_whole_history'] != 131):
    errors.append('Historical/separate phase cap accounting changed')
if total > 131:
    errors.append('Whole recorded history exceeds predeclared maximum131')
active = peak = 0
for _, delta in sorted(events):
    active += delta
    peak = max(peak, active)
if peak > 3:
    errors.append('Actual cross-phase native interval peak exceeds environment3')
fg_closure_path = r / 'planning/FG-call-phase-closure.json'
fg_closure = None
if fg_closure_path.is_file():
    fg_closure = json.loads(fg_closure_path.read_text())
    for phase in ['F', 'G']:
        row = fg_closure[phase]
        if (row['used'] != results[phase]['recorded_calls'] or row['unchanged_original_cap'] != caps[phase]
                or row['unused_retired'] != caps[phase] - row['used']):
            errors.append('Closed ' + phase + ' used/cap/retirement differs')
        pin = row['source_plan']
        if hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest() != pin['sha256']:
            errors.append('Closed ' + phase + ' plan pin changed')
    if fg_closure['whole_completed'] != total or incomplete:
        errors.append('F/G closure differs from completed call metadata')
status = 'FAIL' if errors else ('INCOMPLETE' if incomplete else 'PASS')
out = {'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': status,
       'scope': 'Recorded manifests, all four original phase validators and exact-byte/source pins; not exhaustive tool history, visual quality, authorship, physical or print certification. D/E unused calls remain retired. F6 and G9 stay separate; earlier125/122 cap snapshots are immutable. INCOMPLETE never claims phase closure.',
       'historical_before_round5': 95, 'D_used': results['D']['recorded_calls'], 'D_unchanged_cap': 24,
       'D_unused_retired': closure['D']['unused_retired'], 'E_used': results['E']['recorded_calls'], 'E_unchanged_cap': 6,
       'E_unused_retired': closure['E']['unused_retired'], 'F_used': results['F']['recorded_calls'], 'F_separate_cap': 6,
       'G_used': results['G']['recorded_calls'], 'G_separate_cap': 9, 'whole_recorded': total,
       'predeclared_whole_maximum': 131, 'current_active_whole_maximum': total if fg_closure else 131,
       'call_phases': 'ALL_CLOSED' if fg_closure else 'F_G_OPEN',
       'FG_closure': {'path': str(fg_closure_path), 'sha256': hashlib.sha256(fg_closure_path.read_bytes()).hexdigest(), 'record': fg_closure} if fg_closure else None,
       'actual_cross_phase_interval_peak': peak,
       'incomplete_phases': incomplete, 'errors': errors, 'phase_checks': results}
print(json.dumps(out, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors or (incomplete and not a.allow_incomplete) else 0)
