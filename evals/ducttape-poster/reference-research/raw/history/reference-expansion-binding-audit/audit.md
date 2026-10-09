# Research count and binding audit

The record arithmetic supports **200 archive article observations, with 8 revisits inside that set**, and **37 studio rasters yielding 20 counted poster groups under the worker’s rule**. These are observer attestations and different counting units. They do not establish 220 independently distinct poster works.

This audit read only the eight pinned JSON/text inputs. It compared identifiers, metadata, declared hashes, dimensions, classifications, grouping flags, uncertainty text, and report declarations. It did not reopen source rasters, inspect contact sheets or traces, reconstruct visual tool events, use a browser, generate imagery, start agents, or access credentials. Source-raster hashes and dimensions below are recorded values; only the eight pinned input files were independently hashed. All eight remained unchanged.

## Recomputed archive totals

| Measure | Total | Basis |
|---|---:|---|
| Downloaded candidate records / distinct article URLs | 200 | 100 for 2024 and 100 for 2025; one selected image per article |
| Layout-scale observations attested by root | 200 | 200 observation rows with `actual_viewed=true` |
| Additional native-source revisits | 8 | Nested within those 200 rows; add zero works |
| Distinct declared raster hashes | 200 | Zero repeated hash values; raster bytes not reopened |
| Whole-positive / partial-only / excluded-template records | 100 / 86 / 14 | Exactly matches root and catalog count summaries |
| Non-poster / unresolved classification records | 0 / 0 | No such classifications assigned; no independent media determination here |
| Nonempty author credit labels | 148 | Exact strings, not independent studios |
| Records without an author label | 1 | `BP2025-012`; catalog preserves this as null |

Native revisits are `BP2025-035`, `BP2025-047`, `BP2025-082`, `BP2024-013`, `BP2024-038`, `BP2024-063`, `BP2024-077`, and `BP2024-078`. Each revisit’s declared path, hash, and decoded dimensions match its parent record. The root records reference 25 contact sheets; contained display sizes are 380–390 px wide and 488–570 px high. Those declarations support a layout-scale scope, not complete small-copy reading or an independently confirmed sequence of tool events.

There are **198 distinct author/title label pairs**, including the missing-author pair. Two labels recur: “Dario Argento, Filmpodium Zürich” (`BP2025-002`, `BP2025-018`) and “Scène Ella Fitzgerald” (`BP2025-064`, `BP2024-040`). Each pair has different article URLs, declared raster hashes, and observer descriptions of different compositions. Repeated labels alone do not justify collapsing them into duplicate posters. Conversely, the article rule does not independently settle cross-article series identity. The honest supported archive total is 200 observed article records under that rule.

## Recomputed studio totals

| Measure | Total |
|---|---:|
| Manifest candidates | 41 |
| Downloaded rasters / observation attestations | 37 / 37 |
| Unavailable candidates | 4 |
| Distinct declared raster hashes / byte-duplicate excess | 37 / 0 |
| All-media work keys / files reduced by grouping | 29 / 8 |
| Whole-positive / partial-only / excluded-template files | 14 / 8 / 1 |
| Non-poster / unresolved files | 11 / 3 |
| Eligible poster files before series grouping | 23 |
| Counted poster groups / poster file reduction | 20 / 3 |
| Counted whole-positive / partial-only / excluded-template groups | 12 / 7 / 1 |
| Whole-or-partial groups | 19 |
| Recorded confirmed poster-surface files / groups | 24 / 21 |
| Author labels / labels represented in the 20 counted groups | 9 / 8 |
| Nonnull author/title metadata pairs / null-title files | 24 / 3 |

The four unavailable candidates are `east-FNT-01`, `east-EP-01`, `east-EP-05`, and `west-U09`. They have no observation rows and add no observed posters.

The **21 versus 20** distinction is explicit in the worker data: `west-U10` has `is_poster=true` but unresolved detail/quality classification and is excluded from the effective poster count. Thus 20 is the worker’s eligible-group total, while 21 counts recorded confirmed poster surfaces after the same grouping. `east-EP-04`, classified excluded-template, still contributes one real poster group to 20; it does not contribute to the 19 whole-or-partial groups. These are counting-policy distinctions, not this audit’s quality judgments.

Unresolved files are `west-U10`, `west-U12`, and `west-U21`. Poster media are unknown for U12 and U21. The non-posters are `east-EP-02`, `west-U03`, U05, U06, U11, U13, U15, U19, U20, U22, and U23.

| Repeated work key | Files | Counted poster groups | Grouping effect |
|---|---|---:|---|
| Gandules 2010 | U02, U03, U04, U20 | 1 | U02/U04 poster grouping removes one poster file; U03/U20 are support banners |
| Amsterdam Sinfonietta series | U01, U16, U17 | 1 | Removes two poster files; observer explicitly describes different compositions in one series |
| Barcelona Gallery Weekend inaugural series | U07, U22 | 1 | U22 is publication/collateral |
| Fi de Partida series | U14, U15 | 1 | U15 is folded-print collateral |
| Kosmopolis series | U06, U23 | 0 | Both are recorded non-posters |

All U identifiers in this table have the `west-` prefix. These five groups account for all eight reductions from 37 files to 29 all-media keys. Only three reductions affect the eligible poster count. They are series/media groupings, not byte-identical duplicates. Classification-scoped key counts are 12, 7, 1, 9, and 3, respectively; their sum is 32 because three work keys span poster and non-poster classes. The all-media total remains 29.

The nine credited author labels have raster/countable-group totals: studio fnt 3/3; Everyday Practice 3/2; Sulki and Min 5/5; Ordinary People 4/4; Studio Dumbar/DEPT 3/1; Hey 11/3; HORT 3/1; Studio Feixen 1/1; Bureau Borsche 4/0. All labels are metadata; the worker reports zero independently verified author or project values. Independent studio totals are unknown, not 148 or 9. “24 known pairs” means nonnull metadata pairs, not 24 independently established project identities.

## Bindings and optional catalog

There are no differences in archive manifest-to-observation bindings apart from the intentional observation flag change. All 37 studio observation IDs match exactly the available manifest IDs, and their author/title, page URL, image URL, declared path/hash, and metadata dimensions match. The completion’s studio-manifest hash matches the pinned manifest; its 37 raster pins match the observation records’ declared sources. This does not verify raster bytes independently.

The optional catalog has **200 archive rows and 37 studio rows**, with exact ID coverage and no changed retained field values. It preserves all eight native revisits, row classifications, counted poster flags, source URLs/hashes/dimensions, observation/fact text, and studio identity/unresolved-detail arrays. `BP2025-012` remains author-null. HORT titles for U05, U18, and U19 remain null and separate.

The catalog faithfully retains the observer’s unresolved bindings: `east-SM-01` keeps metadata title **Professionalism** alongside the reported visible **ON POSTERS**, without resolving the page/image identity; `west-U21` keeps **Gandules** and the reported filename-2012/visible-’14 conflict without treating either as an independently verified year. It also retains the limitations of the four very small Bureau Borsche rasters (U10 76×114, U11 76×114, U12 57×76, U13 76×43). The study records 25 partial small-copy cases and two unreadable-body cases; these are observer reading limits, not audit transcriptions.

The catalog is a source lookup. Its optional scope does not make source reopening or per-request source mappings mandatory. Source imagery remains research, never client assets or redistributed runtime imagery.

## Concrete documentation discrepancies

1. **Report registration is empty despite three actual reports.** The user identifies the worker’s actual `observations.json`, `study.md`, and `status.json` under `/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/research/reference-expansion/local-studio-study/output_dir/`. The pinned worker status declares those same three artifacts there. Nevertheless, `completion.json` has `reports: {}`. This audit read the two pinned JSON reports; `study.md` was not pinned and was not opened or filesystem-checked. The discrepancy is preserved, and completion was not rewritten.

2. **Root archive observation status conflicts with its observation flag.** All 200 root observation rows retain `status: "unviewed candidate"` while setting `actual_viewed: true` and adding observations. The raw manifest’s 200 false flags are a preserved candidate snapshot, not evidence of zero subsequent observations. The root’s inherited status should be understood as a field inconsistency; neither input was altered.

3. **The catalog weakens the studio attribution provenance caveat.** Its global limit says author/project labels “come from source-page metadata.” The study instead explicitly identifies the supplied labels as user-provided metadata and records zero independent attribution verification; the catalog omits that qualifier. This is a qualification omission, not a changed author/title value or proof that the metadata did not ultimately originate on source pages. The explicit row-level misbinding and unknown-title caveats remain intact.

The recomputed arithmetic has no count mismatch. The worker’s 74 image-read calls, 38 visual emissions, and 37 unique originals are internally consistent observer claims; they are not independently reconstructed tool events. No benchmark, universal quality, or AI authorship conclusion follows from this audit. Input SHA-256 pins and structured totals are recorded in `status.json`.
