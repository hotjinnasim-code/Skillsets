from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import re
import subprocess

ROOT = Path('/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster')
HISTORY = ROOT / 'history/style-first-draft'
SOURCE = ROOT / 'Skillsets/skills/ducttape-poster'
DRAFT = ROOT / 'drafts/candidate-style-first'
record = json.loads((HISTORY / 'pins.json').read_text())

def pins(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob('*')) if p.is_file()}

assert pins(SOURCE) == record['source_12_file_sha256']
assert pins(DRAFT) == record['draft_12_file_sha256']
assert len(pins(DRAFT)) == 12
links = []
link_issues = []

def slug(heading):
    heading = re.sub(r'[`*]', '', heading).lower()
    heading = ''.join(c for c in heading if c.isalnum() or c in ' -_')
    return heading.replace(' ', '-')

for p in sorted(DRAFT.rglob('*.md')):
    for m in re.finditer(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', p.read_text()):
        target = m.group(1).strip().strip('<>')
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        dest, sep, anchor = target.partition('#')
        resolved = (p.parent / unquote(dest)).resolve() if dest else p
        item = {'from': str(p.relative_to(DRAFT)), 'target': target, 'exists': resolved.exists()}
        if not resolved.exists():
            link_issues.append(item)
        elif sep:
            headings = re.findall(r'^#{1,6}\s+(.+?)\s*#*$', resolved.read_text(), re.M)
            item['anchor_exists'] = unquote(anchor) in [slug(h) for h in headings]
            if not item['anchor_exists']:
                link_issues.append(item)
        links.append(item)

old = (SOURCE / 'references/evaluation-loop.md').read_text()
new = (DRAFT / 'references/evaluation-loop.md').read_text()
table = lambda t: '\n'.join(line for line in t.splitlines() if line.startswith('|'))
gate = lambda t: next(line for line in t.splitlines() if line.startswith('이 평가 루프의 **개별 이미지 PASS**'))
assert table(old) == table(new)
assert gate(old) == gate(new)
old_paras = old.split('\n\n')
new_paras = new.split('\n\n')
assert len(old_paras) == len(new_paras)
eval_changes = [a.split('\n')[0][:70] for a,b in zip(old_paras,new_paras) if a != b]
assert len(eval_changes) == 3, eval_changes
art_old = (SOURCE / 'references/art-direction.md').read_text().split('\n\n')
art_new = (DRAFT / 'references/art-direction.md').read_text().split('\n\n')
exclusion = lambda ps: [p for p in ps if p.startswith('제외하는 구성은') or p.startswith('이미지가 화면을 가득 채워도')]
assert exclusion(art_old) == exclusion(art_new)
source_grammar = (SOURCE / 'references/design-grammar.md').read_text()
draft_grammar = (DRAFT / 'references/design-grammar.md').read_text()
assert table(source_grammar) == table(draft_grammar)
idea_rows = len([line for line in draft_grammar.splitlines() if line.startswith('|')]) - 2
validation_command = [str(ROOT / 'evaluation/base/.venv/bin/python'), '-B',
                      '/Users/nahyeonbin/.codex/skills/.system/skill-creator/scripts/quick_validate.py',
                      str(DRAFT)]
validation = subprocess.run(validation_command, cwd=ROOT, text=True, capture_output=True)
assert validation.returncode == 0, validation.stderr
assert not link_issues, link_issues

checks = {
    'source_12_file_pins_unchanged': True,
    'draft_exact_12_files_and_pins': True,
    'helper_contract_catalog_byte_unchanged': all(record['source_12_file_sha256'][p] == record['draft_12_file_sha256'][p]
        for p in ['scripts/make_layout_guide.py', 'references/layout-guide-contract.md', 'references/reference-catalog.json']),
    'seven_criterion_table_byte_unchanged': True,
    'numeric_pass_threshold_paragraph_byte_unchanged': True,
    'evaluation_prose_changed_paragraphs': eval_changes,
    'evaluation_other_paragraphs_byte_unchanged': True,
    'exclusion_definition_first_two_paragraphs_byte_unchanged': True,
    'reference_relation_table_byte_unchanged': True,
    'optional_relation_idea_rows': idea_rows,
    'relative_link_count': len(links),
    'relative_anchor_link_count': len([x for x in links if '#' in x['target']]),
    'relative_link_issues': link_issues,
    'quick_validate': {'command': validation_command, 'exit_code': validation.returncode,
                       'stdout': validation.stdout, 'stderr': validation.stderr,
                       'scope': 'frontmatter/naming/scaffold validation only; not quality or runtime behavior'},
    'images_generated': 0, 'critics_run': 0, 'child_actors_created': 0,
    'live_runtime_frozen_raw_git_mutations': 0,
    'unresolved_scope_issues': []
}
(HISTORY / 'checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: checks[k] for k in ['source_12_file_pins_unchanged', 'helper_contract_catalog_byte_unchanged',
                  'relative_link_count', 'relative_anchor_link_count', 'relative_link_issues', 'optional_relation_idea_rows',
                  'unresolved_scope_issues']}, ensure_ascii=False, indent=2))
print(validation.stdout.strip())
