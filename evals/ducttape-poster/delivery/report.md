# Poster delivery correction

Generated images could remain in maker/tool outputs while the parent’s answer only described completion. Section 5 now requires the parent’s final user-facing answer to display each suitable selected poster individually, followed by its actual original-resolution download link and pixel dimensions. The maker handoff preserves available display/download references alongside the selected original file. Local desktop paths and current-dialog file/media references are distinguished; no fixed GPT Work URL scheme is assumed.

Two independent agents produced actual final-answer drafts from existing local delivery fixtures:

| Request | Visible image embeds | Selected original links | Unresolved roles |
| --- | ---: | ---: | --- |
| [Five selected](raw/forward/five-answer.md) | 5 | 5 | 0 |
| [One edited selection](raw/forward/one-edit-answer.md) | 1 | 1 | 0 |
| [Four selected plus NONE](raw/forward/partial-answer.md) | 4 | 4 | 1, disclosed |

Root verified each original link against the selected file path/hash and reported dimensions, distinguished display previews from originals, and checked that the NONE attempt was not delivered as a final selection. [Inputs and observations](inventory.json) retain the exact text records. Frontmatter validation and diff checks passed; 56 local document links resolved. No new images were generated and no historical visual verdict was changed. Fixture SELECTED/NONE values are delivery-test inputs, not re-approval of the old pictures’ design quality.

This tests answer construction and local file identity, not live rendering/downloading in GPT Work. Official [image review documentation](https://learn.chatgpt.com/docs/image-generation) and [file delivery documentation](https://learn.chatgpt.com/docs/artifacts-viewer?surface=app) describe general supported review/download workflows; they do not establish a universal file URL scheme. Actual available user-dialog media/file references must be used.
