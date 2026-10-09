"""Write only the two owned planning directions and their factual status."""
from pathlib import Path
from collections import Counter
import json

ROOT = Path.cwd().resolve()
OUT = ROOT / "out"
PINNED = [
    "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/work/round18/planning/single-five-case.json",
    "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-u/SKILL.md",
    "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-u/references/production-brief.md",
    "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-u/references/design-grammar.md",
    "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/candidate-u/references/layout-guide.md",
    "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/layout-guide-helper/revision-v2/make_layout_guide.py",
    "/Users/nahyeonbin/Desktop/_Codex/Ducttape Poster/drafts/layout-guide-helper/revision-v2/README.md",
]
COPY = [x["text"] for x in json.loads(Path(PINNED[0]).read_text())["cases"][0]["copy"]]


def read_guide(role, attempt):
    stem = role.lower() + f"-guide-attempt-{attempt:02d}"
    paths = {k: str(OUT / (stem + suffix)) for k, suffix in [
        ("spec", ".spec.json"), ("png", ".png"), ("svg", ".svg"),
        ("manifest", ".manifest.json"), ("render_log", ".render.log")
    ]}
    spec = json.loads(Path(paths["spec"]).read_text())
    manifest = json.loads(Path(paths["manifest"]).read_text())
    assert all(Path(p).is_file() for p in paths.values())
    assert Counter(b["copy"] for b in spec["text_blocks"]) == Counter(COPY)
    assert len(spec["text_blocks"]) == 12
    assert all(" ".join(b["lines"]) == b["copy"] for b in spec["text_blocks"])
    assert all(not any(b["planned_area_overflow_px"].values()) for b in manifest["text_blocks"])
    return paths, spec, manifest


def copy_plan(spec, manifest, meanings):
    result = []
    for n, (b, m, meaning) in enumerate(zip(spec["text_blocks"], manifest["text_blocks"], meanings), 1):
        result.append({
            "entry_id": f"entry_{n:02d}",
            "exact_copy": b["copy"],
            "function": meaning[0],
            "image_and_next_entry_relationship": meaning[1],
            "actual_guide_lines": b["lines"],
            "guide_area": {"x": b["x"], "y": b["y"], **b["area"]},
            "alignment": b["align"],
            "baseline_spacing_px": b["line_spacing"],
            "guide_font": {"path": b["font"]["path"], "index": b["font"]["index"],
                           "size_px": b["font"]["size"], "family": m["font"]["family"],
                           "style": m["font"]["style"]},
            "actual_line_advances_px": [l["advance_px"] for l in m["line_measurements"]],
        })
    return result


def attempts(role, count, selected):
    result = []
    for n in range(1, count + 1):
        stem = role.lower() + f"-guide-attempt-{n:02d}"
        rec = json.loads((OUT / f"guide-render-record-{n:02d}.json").read_text())
        item = next(a for a in rec["attempts"] if a["role_id"] == role)
        rendered = item["exit_code"] == 0
        result.append({
            "attempt": n, "renderer_exit_code": item["exit_code"],
            "spec_path": str(OUT / (stem + ".spec.json")),
            "log_path": str(OUT / (stem + ".render.log")),
            "outputs_created": rendered, "selected_as_planning_reference": n == selected,
            "reason": (
                "Renderer stopped before outputs: AppleMyungjo lacks required Unicode cmap/OS/2 metadata combination. Original spec and failure log retained."
                if n == 1 else
                "Supported explicit font faces selected; M2 chair/brace endpoints moved clear of invitation. Both rendered."
                if n == 2 else
                "M1 paragraph placed wholly within the table plane, table outlines shortened outside its glyph area, and final action run aligned beyond the chair leg."
            ),
            "output_paths": {k: str(OUT / (stem + suffix)) for k, suffix in [
                ("svg", ".svg"), ("png", ".png"), ("manifest", ".manifest.json")
            ]} if rendered else {},
        })
    return result


COMMON_LIMITATIONS = [
    "These are newly authored planning diagrams and direction briefs, not generated posters, benchmarks, aesthetic scores, or final approval.",
    "1672x941 is the requested guide rounding for 16:9. It is not a new client pixel requirement or a promise of native output geometry.",
    "Gray fills, simple polygons, schematic faces/hands and area boundaries only explain the large scene or relational arrangement. They are not the proposed final materials, palette, drawing finish or anatomy.",
    "The PNGs use the recorded Apple SD Gothic Neo font bytes and TTC indices. The SVGs request installed family and weight; viewers may substitute faces. No fonts were copied, embedded or downloaded.",
    "The Pillow runtime used BASIC layout. Cmap coverage and measured text bounds describe this guide, without guaranteeing future native shaping, font application, exact line breaks, geometry or reading comfort.",
    "The nominal 720px display sizes are planning calculations, not pixel thresholds or an empirical final-poster readability claim. Final native type and image/copy relationships remain for ROOT's later production.",
    "Default python3 lacked Pillow; an existing local Pillow dependency runtime was read only. Both first guide attempts then stopped on unsupported AppleMyungjo metadata. The preflight note, exclusive failed specs and renderer logs are retained.",
]


def main():
    p1, s1, m1 = read_guide("R18-C1-M1", 3)
    p2, s2, m2 = read_guide("R18-C1-M2", 2)

    meaning1 = [
        ("Identity / first verbal anchor: the shared Saturday promise", "The open light title sits between two close bent heads, at the opening of the common workbench view. Its left edge begins the gently leftward-descending spine; the cooperative English line follows without a separate title plate."),
        ("Identity / cooperative register", "A compact Latin line confirms that the two repair contacts are a shared activity. Its alignment belongs to the title's opening, then the meaning sentence begins slightly left where the upper neighbor's bent elbow opens the route."),
        ("Meaning / practical and emotional proposition", "The sentence bridges faces to actual repair hands and the lit bench. The following paragraph begins below and slightly left, at the table's calm working plane rather than a caption corner."),
        ("Meaning plus participation / one continuous explanatory paragraph", "Three left-aligned lines move from chair and clothing nouns, through the bring-your-object invitation and neighboring repairers, to the complete sharing-and-learning phrase. The final line drops directly to the workshop name on the same descending optical axis."),
        ("Identity / name of the actual event", "This is the next anchor after the learning phrase. It makes the experience an identifiable local workshop, then opens the date/time row immediately below on the same living bench plane."),
        ("Visit / date anchor", "The larger date begins the single schedule row just beyond the chair joint, paired with time to its right. It is a modest numeric emphasis inside the spine rather than a detached date panel."),
        ("Visit / matching day and time", "Time continues the date row horizontally; the route returns to the left edge immediately below for the venue. The chair/garment action remains large on either side of this row."),
        ("Visit / destination", "The venue begins the last nearly vertical portion of the spine. Fee follows at an adjacent baseline and shared left edge, making attendance practical rather than requiring a search across corners."),
        ("Participation / cost and provided tools", "This line shares the venue's area and the final x472 action axis, clear of the chair leg. Its tool provision is echoed by the two visible tools being jointly held and used."),
        ("Action / registration deadline", "The deadline is the first line of a continuous three-line action exit, adjacent to fee and using a medium weight. The invitation and URL follow on precisely the same guide axis."),
        ("Action / what the participant brings", "A full sentence stays on one line below deadline. It echoes the substantial chair and torn shirt already handled by neighbors, and leads immediately to the join URL."),
        ("Action / registration destination and final anchor", "The URL closes the same spine in medium weight. It sits alongside the continuing chair legs and shared garment hold, so the final action remains within the active scene."),
    ]
    meaning2 = [
        ("Identity / first strong verbal anchor on the cloth-side node", "The upper-right title shares the shirt-and-neighbor contact's horizontal extent. It names the whole graphic field, while the shirt's left-reaching sleeve/hand leads across to the invitation at the seam's left mouth."),
        ("Identity / relational bridge on the wood-side node", "The Latin phrase belongs above the chair contact and the hand-to-hand screwdriver transfer. It reads as the shared relation between wood and cloth, with its position complementary to the title at the opposite upper contact."),
        ("Meaning / consequence of the shared work", "The proposition sits immediately above the substantial lower-left chair contact. It closes the material relation after the main information run; it is attached to the experience rather than stacked below the headline."),
        ("Meaning / one continuous two-line explanation across the seam", "Each original sentence occupies one complete line. The object invitation and the neighboring sharing/learning experience retain a stable left start and natural word spaces across a broad quiet interval between repair contacts. Workshop identity begins below that same left edge."),
        ("Identity / first event anchor after the paragraph", "The event name starts the seam's first logistics row; date and time continue across the same baseline. It shifts the reading from complete narrative sentences to one connected event row."),
        ("Visit / numeric hinge in the event row", "The date is a compact semibold hinge near the seam's middle. Its row neighbors are event name to the left and time to the right; venue, fee and deadline follow immediately below."),
        ("Visit / event duration", "Time completes the first row toward the cloth-side contact. The adjacent registration column is on the lower row, so the reader can reach deadline and URL without returning to a distant footer."),
        ("Visit / place in the lower event row", "The venue starts the second connected row under the event name, keeping the place tied to the workshop instead of treating it as a separate graphic node."),
        ("Participation / cost and access to tools", "The fee/tools line is the middle of the second row beneath date, surrounded by the actual shared screwdriver and supported cloth. It bridges venue at left to deadline at right."),
        ("Action / endpoint of the lower event row", "The deadline sits on the right seam edge beneath time. The actual sewing-thread path continues outside this text area toward the lower-right spool and gives the adjacent URL a material exit direction."),
        ("Action / the seam's first explanatory-entry line", "The invitation lies at the left mouth below the large chair contact and above the paragraph. It leads immediately from a recognizable thing being fixed to the explanation, rather than waiting until the bottom as a second footer."),
        ("Action / registration exit from the seam", "The URL sits directly below deadline on the right edge. Thread and a receiving hand continue past it to the lower-right contact, coupling an action destination to the shared-tool relation."),
    ]

    d1 = {
        "role_id": "R18-C1-M1", "ordinal": 1, "ratio": "16:9",
        "internal_direction_name": "Four neighbors, one working-light spine",
        "whole_image_and_copy_plan": "A close oblique scene of four neighbors repairing a chair and a shirt surrounds one gently descending copy spine, which runs from the Saturday promise through a compact paragraph to workshop, visit and registration information on the common working plane.",
        "positive_direction_brief": {
            "content_idea": "Repair is a small shared accomplishment made through contact: a neighbor braces a loose chair rail while another turns a screwdriver, and a second pair tensions a torn shirt while one stitches. Both tasks belong to one current encounter at the same bench, with faces, upper bodies, worn sleeves, hands and full recognizable repair objects in one continuous view.",
            "whole_scene_execution": "Use a slightly elevated elbow-height view close enough that the near two bodies crop at the lower edges and the upper two faces and bent shoulders remain legible. The chair occupies the left near edge; its back slats, seat, splayed legs and loose rail stay recognizable. At right, a shirt's collar and sleeves remain whole enough to identify clothing, while the tear and a small repair stitch are held between two neighbors. Give the left pair distinct hands: one stabilizes the same rail the other's driver tip actually meets. At right, one hand holds cloth on either side of the tear and another grips the needle, with thread visibly under modest tension. Shared directional light, continuous tabletop grain and consistent contact shadows join all four people into one place.",
            "spatial_and_crop_decisions": "Budget the paragraph's 730x174 guide area first. The upper faces and bent arms open a gently narrowing light interval that becomes the bench plane; the paragraph remains a flat typographic overlay within this active interval. Large bodies and objects continue around it to the image edges. The table edge is visible outside the paragraph, with a softened tonal transition through the opening above it. The lower action axis begins beyond the chair's outer leg. Let image contours and gestures determine this interval and keep the gestures recognizably substantial.",
            "type_coupling": "Use an open, relatively light display title as the invitation into the scene, a compact medium Latin register, then a regular proposition leading to a precise, medium-optical-body explanation. The title follows the space between bent heads; the paragraph begins just inside the working-light plane; the last learning phrase leads by adjacency to workshop identity. A descending left optical edge links workshop, date/time, venue and cost. Deadline, object invitation and URL finish as one adjoining run. Keep every baseline flat, natural word spaces intact, and the three body lines together even as the scene's plane shifts around them.",
            "material_color_emotion": "A lucid, figurative painted scene with closely observed wood grain, worn cotton, knuckles, needle/thread and repair contact. Burnished amber on the common working plane, deep plum in surrounding shadows, coral and indigo clothing, and warm skin variations can make focused concentration feel generous and unhurried. Preserve crisp dark body text over the amber working light; light title/upper identity can sit in the plum interval. Painterly surface belongs to people, wood and cloth, with precise flat text. The guide's grays do not prescribe these colors or the final light.",
            "recognizable_visual_evidence": "Four human figures with visible heads and arms, one large chair, one large shirt, two paired repair contacts, a screwdriver tip meeting the chair joint and a held needle/thread meeting the shirt tear. The meaningful image is the joint work itself.",
        },
        "paragraph_shape": {
            "copy_entry": "entry_04", "single_continuous_block": True,
            "native_guide_area_px": {"x": 521, "y": 292, "width": 730, "height": 174},
            "font": {"path": "/System/Library/Fonts/AppleSDGothicNeo.ttc", "index": 0, "face": "Regular", "size_px": 44},
            "baseline_spacing_px": 59, "actual_line_advances_px": [492, 578, 590],
            "semantic_line_groups": ["The two repair-object noun groups remain together.", "The bring-it instruction joins the neighboring repairers and their tools.", "Sharing leads into the complete method-and-learning phrase, including its final verb."],
            "display_assumption": "At 720px wide, native guide size 44 scales nominally to about 18.95px, baseline spacing to about 25.41px. This is a per-case planning example.",
            "entry_to_first_line": "The title/English/proposition sequence descends along the open elbow-and-light interval into the paragraph's left start.",
            "last_line_to_next_anchor": "The complete learning phrase is followed below by entry_05 on the same gently descending axis, then the date/time pair.",
        },
        "reading_route": {
            "first_anchor": "entry_01 between the upper bent heads, supported by the two shared repair contacts",
            "main_entry_order": ["entry_01", "entry_02", "entry_03", "entry_04", "entry_05", ["entry_06", "entry_07"], "entry_08", "entry_09", "entry_10", "entry_11", "entry_12"],
            "route_geometry": "A gentle down-left opening from x579 to x521, then through x503/x484 to a nearly vertical final x470–472 run. The date/time row is the one short horizontal expansion. All other visit and registration entries belong to the same continuous spine.",
        },
        "actual_copy_roles": copy_plan(s1, m1, meaning1),
        "distinction_from_other_owned_direction": "M1 is a single inhabited scene with a compact three-line paragraph and a downward information sequence inside the bent bodies. M2 has separate shared-contact groups at multiple positions, complete sentences spanning a horizontal seam, event details continuing across it and registration exiting on its right edge.",
        "native_design_prompt_recommendation": "Create one flat 16:9 workshop poster as a close oblique painted scene of four neighbors at a shared workbench. At left, one braces a loose chair rail while another turns a screwdriver; at right, one tensions a torn shirt while another stitches it. Use deep plum shadows, burnished amber work light, coral/indigo sleeves and lucid human/tool contact. Follow the guide's gently descending copy spine: open light title, compact three-line body, then workshop, visit and registration in one connected run. Let elbows, chair rails and the shared working plane shape the reading interval. Keep text precise and flat. Use the supplied twelve copy entries exactly once.",
        "guide": {"kind": "new own text-and-shape planning diagram", "selected_attempt": 3, "canvas": s1["canvas"], "paths": p1, "final_own_png_viewed": True, "shape_count": len(s1["shapes"]), "text_entry_count": len(s1["text_blocks"]), "planned_area_overflow_note": "All selected text blocks have zero reported planned-area overflow in this guide; this is a layout measurement only."},
        "guide_attempt_history": attempts("R18-C1-M1", 3, 3),
    }
    d2 = {
        "role_id": "R18-C1-M2", "ordinal": 2, "ratio": "16:9",
        "internal_direction_name": "Shared contacts around an open information seam",
        "whole_image_and_copy_plan": "Large chair, garment and hand-to-hand tool contacts are distributed around a broad information seam; a title on the upper-right cloth relation leads toward the object invitation at the left seam mouth, two full sentence lines cross the opening, and adjoining event rows carry the reader rightward to deadline and join URL.",
        "positive_direction_brief": {
            "content_idea": "The act of sharing tools makes different repairs one neighborhood experience. Build a relational graphic from actual repair contacts: two neighbors hold and tighten a wooden chair rail, another pair holds a shirt's torn seam and stitches it, two hands exchange a screwdriver, and lower contacts support a cloth patch and receive a spool. Their material continuities make the relation legible before any extra explanation.",
            "distributed_graphic_execution": "Give the upper-left chair a broad tilted back, two visible slats, a seat and a clear tightened rail. Two cuffed forearms end in distinct hands on the wood and driver. The center-upper contact is a substantial hand-to-hand screwdriver exchange. Upper right is a recognizable shirt with collar, sleeves and a jagged tear held open by two people; a needle actually meets the tear. Lower left returns to a jointly held chair structure, lower center shows a supported cloth patch, and lower right receives the same thread on a spool. Use meaningful changes of scale and angle among these contacts, with no card grid. The forearms, fingers and material/tool contact should feel human and specific, even in simplified ink shapes.",
            "seam_and_crop_decisions": "Reserve a broad opening through the middle as the information seam before shaping the surrounding graphic contacts. In the selected guide, a 1240x130 explanation block begins at x89,y413, below the invitation and between the upper object contours and lower supported objects. The upper wood brace points toward the invitation without crossing it. A sewing-thread connection bends around the right edge of the logistics and extends into the lower spool contact. These are physical continuities of the pictured repairs. The seam is open negative space within the full graphic field, with contours of real objects at its edges; its text is flat and unaffected by their perspective.",
            "type_coupling": "Place the medium-weight Korean title as an identity anchor over the upper-right shirt relation and the compact Latin phrase over the upper-left chair relation. The invitation sits at the left mouth of the seam and immediately opens the explanatory paragraph. Keep the paragraph as two complete sentence lines with a shared left start, generous body and natural spacing. The event name starts directly below the paragraph and opens a continuous horizontal name/date/time row. Venue, fee and deadline make the adjacent lower row, with URL under deadline at the right seam edge. The proposition belongs to the lower-left shared chair contact as the meaning of the work. Thus identity is paired with upper material relations, explanation spans their common seam, and action exits beside the real thread receiver.",
            "material_color_emotion": "Use a saturated, crisp print graphic with cobalt chair structure, vermilion garment contours, lavender field and restrained bright lime accents on tool handles or cuffs. Flat ink masses, controlled grain inside larger objects and decisive human fingers give public energy and warmth. Material-based connections are wood rails, steel driver shaft and sewing thread. Maintain precise dark type on the quiet lavender seam and keep the clothing and wood contact edges strong enough to organize the whole image. Neutral guide colors are purely schematic.",
            "recognizable_visual_evidence": "Chair structure with actual shared driver contact; shirt collar/sleeves and tear held by two hands; screwdriver passed from one clothed arm to another; cloth patch supported by a pair; thread connected to the lower-right hand and spool. These are linked experiences rather than interchangeable ornamental nodes.",
        },
        "paragraph_shape": {
            "copy_entry": "entry_04", "single_continuous_block": True,
            "native_guide_area_px": {"x": 89, "y": 413, "width": 1240, "height": 130},
            "font": {"path": "/System/Library/Fonts/AppleSDGothicNeo.ttc", "index": 0, "face": "Regular", "size_px": 46},
            "baseline_spacing_px": 61, "actual_line_advances_px": [738, 1014],
            "semantic_line_groups": ["The complete first sentence invites the two recognizable repair objects.", "The complete second sentence explains neighbors, sharing tools, method and learning in one continuous line, including its final verb."],
            "display_assumption": "At 720px wide, native guide size 46 scales nominally to about 19.81px, baseline spacing to about 26.27px. The two full sentence advances scale to about 318px and 437px. This is a per-case planning example.",
            "entry_to_first_line": "The upper-right title/shirt contact reaches left toward entry_11 at the seam mouth; that invitation and the paragraph share x89 and are directly adjacent.",
            "last_line_to_next_anchor": "The full learning sentence stays within the seam. Entry_05 begins beneath its left start and opens the name/date/time row horizontally, then the venue/fee/deadline row and right-edge URL.",
        },
        "reading_route": {
            "first_anchor": "entry_01 together with the upper-right shirt's two-person stitch contact; entry_02 and the chair/tool transfer offer the complementary upper entry",
            "main_entry_order": ["entry_01", "entry_02", "entry_11", "entry_04", ["entry_05", "entry_06", "entry_07"], ["entry_08", "entry_09", "entry_10"], "entry_12"],
            "meaning_reprise": "entry_03 sits over the lower-left jointly handled chair and closes the relational reading after the information seam.",
            "route_geometry": "Upper-right identity to left seam mouth; stable two-line paragraph at x89; horizontal event row and immediately adjacent lower logistics row; down to URL at x1040. The lower-left proposition is attached to the lower chair contact, and the right thread carries the action exit to the spool.",
        },
        "actual_copy_roles": copy_plan(s2, m2, meaning2),
        "distinction_from_other_owned_direction": "M2 uses an open graphic relation with upper identities attached to different material contacts, a broad two-sentence explanation seam, invitation before explanation, horizontally adjoining event information and a right-edge registration exit. M1 carries identity, explanation and action in one downward spine inside a single human scene.",
        "native_design_prompt_recommendation": "Create one flat 16:9 poster as a saturated relational print graphic: large shared chair-rail repair, shirt stitching, a hand-to-hand screwdriver transfer, a jointly supported cloth patch and a receiving hand/spool distributed around an open information seam. Use cobalt wood forms, vermilion clothing and a quiet lavender text field. The title identifies the upper-right shirt relation; the invitation opens the seam at left, followed by two complete sentence lines. Continue directly into adjoining event rows, with deadline and URL exiting along the real thread at right. Attach the meaning sentence to the lower shared chair contact. Keep human fingers, collars, chair slats and tool contact specific. Use the supplied twelve copy entries exactly once.",
        "guide": {"kind": "new own text-and-shape planning diagram", "selected_attempt": 2, "canvas": s2["canvas"], "paths": p2, "final_own_png_viewed": True, "shape_count": len(s2["shapes"]), "text_entry_count": len(s2["text_blocks"]), "planned_area_overflow_note": "All selected text blocks have zero reported planned-area overflow in this guide; this is a layout measurement only."},
        "guide_attempt_history": attempts("R18-C1-M2", 2, 2),
    }

    directions = {
        "schema_version": 1, "case_id": "R18-C1", "purpose": "Two independent initial-design planning directions for ROOT comparison before any native generation",
        "owned_role_count": 2, "owned_roles": ["R18-C1-M1", "R18-C1-M2"],
        "pinned_design_inputs_read": PINNED,
        "scope": "Only these two planning guides. The five-poster case count and comparison of all five belong to ROOT.",
        "guide_canvas_rounding": {"width": 1672, "height": 941, "intended_ratio": "16:9", "client_pixel_requirement": False},
        "copy_contract": "Each role's diagram includes the twelve supplied entries once. Original words, spaces, punctuation and number forms are conserved; only deliberate word-space line boundaries differ. Only supplied copy is printed in the diagrams.",
        "current_composition_requirement": "Substantial, content-grounded shared repair organizes the whole image and the actual copy route. The current default exclusion of passive headline/date/information panels with subordinate imagery or empty-room dressing remains in effect. The proposals use living scene or material-contact continuities; neither proposes a white/cream torn-page center with surrounding props.",
        "directions": [d1, d2],
        "limitations": COMMON_LIMITATIONS,
    }

    status = {
        "schema_version": 1, "case_id": "R18-C1", "state": "two_planning_directions_written",
        "call0": 0, "call0_meaning": "Native image generation/edit calls made in this planning task",
        "native_image_calls": 0, "image_gen_calls": 0, "native_poster_outputs_created": 0,
        "agents_spawned": 0, "web_calls": 0, "credentials_accessed": False,
        "old_images_opened": 0, "old_scores_read": 0, "other_assistant_plans_read": 0,
        "source_artwork_read": 0, "bitmap_inputs_to_renderer": 0, "raster_input_edits": 0,
        "owned_roles": ["R18-C1-M1", "R18-C1-M2"], "owned_role_count": 2,
        "planning_direction_count": 2, "selected_planning_reference_count": 2,
        "new_successful_svg_count": 3, "new_successful_png_count": 3,
        "own_new_png_views": 3, "total_guide_renderer_attempts": 5,
        "successful_guide_renders": 3, "failed_guide_renderer_attempts": 2,
        "runtime_preflight_failures": 1,
        "native_case_poster_count_owned_by_root": 5,
        "role_records": [
            {"role_id": "R18-C1-M1", "direction_written": True, "actual_copy_entries": 12, "guide_renderer_attempts": 3, "failed_guide_attempts": 1, "successful_guide_renders": 2, "selected_guide_attempt": 3, "guide_paths": p1, "native_calls": 0, "native_poster_outputs": 0},
            {"role_id": "R18-C1-M2", "direction_written": True, "actual_copy_entries": 12, "guide_renderer_attempts": 2, "failed_guide_attempts": 1, "successful_guide_renders": 1, "selected_guide_attempt": 2, "guide_paths": p2, "native_calls": 0, "native_poster_outputs": 0},
        ],
        "attempt_preservation": {"outputs_overwritten": 0, "exclusive_specs_preserved": 5, "renderer_logs_preserved": 5, "runtime_preflight_note": str(OUT / "runtime-preflight-failure.txt"), "render_records": [str(OUT / f"guide-render-record-{n:02d}.json") for n in [1, 2, 3]]},
        "runtime": {"renderer_path": PINNED[5], "executed_from": str(ROOT), "python": "/Applications/Xcode.app/Contents/Developer/usr/bin/python3", "pillow_dependency_path": "/Users/nahyeonbin/.codex/worktrees/terrain-alignment/NAMOK-Bible-Maps/.cache/terrain-python/lib/python3.9/site-packages", "dependency_use": "Read-only runtime dependency; no project source, artwork or design material in that tree was read.", "shaping_engine": "BASIC", "font_binaries_copied": 0, "font_downloads": 0, "network_package_installs": 0},
        "recorded_checks": {"two_owned_role_ids": True, "selected_specs_match_all_twelve_pinned_copy_entries_once": True, "word_spaces_and_punctuation_conserved": True, "all_selected_paths_exist": True, "selected_text_blocks_report_no_planned_area_overflow": True, "final_own_new_guide_pngs_viewed": True, "meaning": "These checks record the concrete handoff and guide fit only; they are not poster quality or final approval."},
        "directions_path": str(ROOT / "directions.json"), "status_path": str(ROOT / "status.json"),
        "limitations": COMMON_LIMITATIONS,
        "next_owner": "ROOT compares these with the remaining three directions before any native generation.",
    }
    for name, payload in [("directions.json", directions), ("status.json", status)]:
        with (ROOT / name).open("x", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(ROOT / name)


if __name__ == "__main__":
    main()
