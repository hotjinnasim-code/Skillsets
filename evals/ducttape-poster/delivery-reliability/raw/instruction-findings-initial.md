# Independent instruction review

Scope: actual working-tree changes to the skill opening and section 5, invocation prompt, parallel production handoff, new delivery reference, and helper. No code/repository edits, artwork generation, network calls, or old evaluation changes. Read pins record the working-tree file bytes.

## Findings sent to root

1. Pixel-size placement differs between required final shape and generated block. SKILL.md:92 and delivery.md:48 require image followed by original link and size; prepare_delivery.py:263-265 puts size in the title above the image. Move size to the download line or align the stated required shape. Small presentation inconsistency.
2. Raw delivery diagnostics can reach the final reply. prepare_delivery.py:257 joins raw errors into unresolved cards, including filesystem exception paths from inspect_image. delivery.md:46 permits reporting an unrecoverable role, while delivery.md:52 and SKILL.md:92 require verbatim block transmission; SKILL.md:92 also says not to attach diagnostics. Keep detailed errors in delivery.json, and render a short user-facing unresolved statement in response.md. This affects failure paths only.
3. Native fallback should cover an actual valid attachment reference that the string helper cannot represent, as well as tools that support only native media blocks. prepare_delivery.py:250 accepts dialog references only with a parsed scheme; a valid opaque native reference must not be turned into a made-up URI to satisfy the helper. delivery.md:48 already prohibits opaque object serialization and says helper usage must not block delivery. Widen the fallback trigger wording to remove ambiguity.

## Resolved during review / accepted scope

- Initial SKILL section 5 claimed the helper catches a thumbnail download without qualification. Root scoped this to local download byte mismatches and explicitly states that dialog/native identity is not certified. Current SKILL.md:90 no longer overstates the check.
- Prompt shortening was deliberate, consistent with a concise skill invocation. It retains the skill trigger, default five distinct styles, user-count priority, preserved copy/constraints, inline images, original links, and actual dimensions. The skill's substantive design body and two-correction limit are unchanged. No restoration of the duplicated long prompt is needed.
- delivery.md explicitly separates unavailable delivery refs from selection NONE, requires all requested role records, directs central transfer from maker-only caches/cards into the current user conversation, and forbids regenerating to fix delivery.
- The native path preserves actual media blocks and original attachments, and the local path is conditioned on current-conversation absolute-path support. No new approval, network research, package-install, or design-review gate was added.
- READY is explicitly answer prepared only, with local container/header/SHA checks distinguished from full decode, dialog accessibility, and actual user-conversation rendering.

## Small wording ambiguity

parallel-production.md says the maker must not automatically convert an original path into a download reference; delivery.md:25 lets the central helper use an omitted ref's original path in a confirmed local mode. This is coherent by role/environment, but qualifying the maker sentence as requiring central confirmation of local path support would make the distinction explicit. Not a blocker.

Validation: read-only inspection plus git diff --check (passed at read time). No user-conversation display/download success was observed or claimed.
