# M3 geometry amendment only

The parent preserves the failed M3 coded-guide render and all prior planning files. This amendment performs no rendering, bitmap reading/editing, native generation, font change, score change or child-agent execution.

## Exact failure

In M3 `guide_spec.shapes[8]` (zero-based; the ninth shape), the rightmost narrow planted blade had vertices:

```json
[[1500, 602], [1598, 269], [1575, 205], [1520, 602]]
```

Nonadjacent edge 0 (`[1500,602]` to `[1598,269]`) and edge 2 (`[1575,205]` to `[1520,602]`) cross at approximately `[1537.789325, 473.593415]`. This is the sole nonadjacent crossing/touch found in the failed M3 polygon array. It is an invalid bow-tie vertex order, not a font or helper defect.

## Minimal prospective correction

The second and third vertices are exchanged, retaining all four exact coordinate pairs and the same bounds, fill, planted base and blade direction:

```json
[[1500, 602], [1575, 205], [1598, 269], [1520, 602]]
```

This follows the contour around the left base, upper-left tip edge, upper-right tip edge and right base. The blade remains rooted in the existing right pot and leans upward-right; its actual silhouette meaning and every other plant geometry are retained. Both duplicated planning representations (`guide_spec.shapes[8].points` and `guide_geometry_concept.shapes[8].points`) receive the identical order correction.

## Scope and checks

The new `plan-hierarchy-v3.json` differs from v2 only in those two duplicated point arrays. Directions M1/M2/M4/M5 are deep-equal to v2. All text, copy, line arrays, coordinates, fonts, hierarchy, conditions, assets, scores/method and all other geometry are unchanged. The original v2 metadata remains its historical creation record; parent-rendered coded guides are separate records.

A pure integer segment-intersection check finds no nonadjacent crossings/touches in any polygon in the new five `guide_spec` arrays. Replacing the two corrected arrays with their old order reconstructs the complete v2 object exactly. This is geometry preparation only, not a render confirmation or poster-quality check. The helper and its simple-polygon rule were not modified.

- v2 SHA-256: `a1b981b98d77e5eda45108c87cf4f05d6296b17a2e6476a81d2829343395fdba`
- v3 SHA-256: `fd07024789ae6919b9a695a949b1376572dd0e01de9cb52c67cb6c878caa75c8`
- Preserved failed spec SHA-256: `6df04bfa231344dd03765004795a72e146fd89f33a1942c50f05c370357de80a`
- Preserved render-status SHA-256: `5aed7898b056cf465a6cfafbe4c6c61d92ffdb6be7cd7c2b58224d06c05a7479`

The parent can extract M3 `directions[2].guide_spec` from v3 to a new coded-spec path for its next render attempt. No existing spec or result is overwritten.
