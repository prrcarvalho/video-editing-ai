# Gemini Omni Flash: Flow UI → Pydoll Capture → FlowKit Implementation Plan

**Status:** Engineering execution plan  
**Research baseline:** 2026-06-18  
**Target FlowKit repository:** `crisng95/flowkit` and your private fork  
**Primary goal:** Make Gemini Omni Flash usable as a reliable, agent-callable stage in an automated video-editing and social-media content pipeline.

---

## 1. Desired end state

An AI agent such as Codex should be able to issue typed requests such as:

```text
Create a 9:16, 10-second Omni Flash clip from this product image and location reference.
Use the saved voice "Campaign Narrator".
Then edit the generated clip to replace the background, preserve the product, and make one follow-up refinement.
Download the final media and hand it to the local editing pipeline.
```

The production flow should become:

```text
Content brief
  → shot plan
  → reference assets
  → Omni generation or edit
  → polling and media persistence
  → automated quality review
  → optional follow-up edit
  → 1080p export/download
  → local timeline, captions, music, branding
  → social-platform publishing
```

This plan deliberately separates:

1. **UI discovery**
2. **Passive network mapping**
3. **Sanitized contract extraction**
4. **FlowKit gap analysis**
5. **Implementation**
6. **Agent/MCP integration**
7. **Production hardening**

Do not begin by adding a guessed model key to `models.json`. Omni Flash may use different request bodies, endpoints, workflow state, media input roles, edit-session identifiers, or response schemas.

---

## 2. Boundaries for the investigation

Use only:

- Your own Google account.
- Your own Flow projects.
- Assets you own or created for testing.
- Features available to your subscription and region.
- Normal Flow UI actions.

During discovery:

- Start with **passive CDP Network monitoring**, not active Fetch interception.
- Do not modify Flow requests.
- Do not export, persist, share, or commit bearer tokens, cookies, OAuth material, reCAPTCHA tokens, signed download-query strings, or account identifiers.
- Do not replay a captured reCAPTCHA token.
- Do not attempt to bypass plan, quota, safety, age, geographic, or account restrictions.
- Do not commit raw HAR files.
- Keep the browser bridge and FlowKit API bound to localhost.
- Keep a human confirmation step before any credit-consuming batch.

Pydoll distinguishes passive Network monitoring from active Fetch interception. Use the Network domain for the mapping phase. Only consider an execution transport after the request contracts are understood and reviewed.

---

## 3. Current official Omni Flash capability baseline

The current Flow documentation describes this Omni Flash surface:

| Capability | Officially documented state |
|---|---|
| Text-to-video | Both orientations; 4, 6, 8, and 10 seconds |
| First-frame-to-video | Both orientations; 4, 6, 8, and 10 seconds |
| First-and-last-frame video | Coming soon for Omni Flash |
| Ingredients/references-to-video | Both orientations; 4, 6, 8, and 10 seconds |
| Advanced references | Character/avatar and audio references |
| Video-to-video editing | Both orientations; output up to 10 seconds |
| Uploaded-video editing | Supported only in eligible regions |
| Generated-video editing | Supported |
| Follow-up editing | Up to three conversational turns |
| Preset voice references | Ingredients mode only |
| Custom voices | Preset base voice + performance prompt + optional sample |
| Extend | Not currently an Omni Flash feature |
| Output count | Selectable in the Flow UI |
| Orientation | Selectable in the Flow UI |
| Generation duration | Selectable in the Flow UI |

### Portugal / EEA limitation

Portugal is in the EEA. Google currently states that **uploaded-video edits are unavailable in the EEA**. Do not try to work around that restriction. In Portugal, capture the region-gating behavior and continue with:

- Generated-video editing.
- Text-to-video.
- First-frame-to-video.
- Image/video ingredients where exposed.
- Characters.
- Voice references.
- Custom voices.
- Multi-turn refinement of eligible generated clips.

Leave imported-video editing behind a runtime capability flag until it can be lawfully tested in an eligible account and location.

---

## 4. Current FlowKit baseline to compare against

The public FlowKit baseline currently has:

- Veo-oriented model mappings in `agent/models.json`.
- No Omni model mapping.
- No Omni-specific request type in `agent/models/enums.py`.
- Image generation and image editing.
- Image upload.
- Image-to-video.
- Start-and-end-frame Veo generation.
- Reference-image-to-video.
- Video upscaling.
- A local job queue, retries, polling, SQLite persistence, FFmpeg post-processing, and agent skills.

The current request enum is centered on:

```text
GENERATE_IMAGE
REGENERATE_IMAGE
EDIT_IMAGE
GENERATE_VIDEO
REGENERATE_VIDEO
GENERATE_VIDEO_REFS
UPSCALE_VIDEO
GENERATE_CHARACTER_IMAGE
REGENERATE_CHARACTER_IMAGE
EDIT_CHARACTER_IMAGE
```

The gap is therefore not merely a missing model name. FlowKit also lacks first-class representations for:

- Direct text-to-video.
- Selectable 4/6/8/10-second durations.
- Output count.
- Omni-generated-video editing.
- Uploaded-video ingestion and trimming.
- Multi-turn edit sessions.
- Voice catalogs and voice references.
- Custom voice creation.
- Video ingredients.
- Region-aware capability discovery.

---

# Part I — Build the mapping workspace

## 5. Create a dedicated branch and directory structure

Create a branch in your fork:

```bash
git switch -c research/omni-flash-mapping
```

Add this structure:

```text
research/omni/
├── README.md
├── CAPTURE_MATRIX.md
├── capability-map.yaml
├── flowkit-gap-matrix.md
├── schemas/
│   ├── omni-generation.schema.json
│   ├── omni-edit.schema.json
│   ├── voice.schema.json
│   └── media-upload.schema.json
├── fixtures/
│   ├── inputs/
│   │   ├── subject.png
│   │   ├── product.png
│   │   ├── location.png
│   │   ├── start-frame.png
│   │   ├── source-08s.mp4
│   │   ├── source-35s.mp4
│   │   ├── source-61s.mp4
│   │   └── unsupported.txt
│   └── sanitized/
│       └── <test-id>/
│           ├── manifest.json
│           ├── ui-before.png
│           ├── ui-after.png
│           ├── requests.jsonl
│           ├── responses.jsonl
│           ├── sequence.json
│           ├── contract.yaml
│           └── notes.md
├── raw/
│   └── .gitignore
├── tools/
│   ├── capture_flow.py
│   ├── sanitize_capture.py
│   ├── normalize_capture.py
│   ├── diff_contracts.py
│   └── validate_capture.py
└── reports/
    ├── endpoint-inventory.md
    ├── model-inventory.md
    ├── state-machines.md
    └── implementation-backlog.md
```

Set `research/omni/raw/` to ignore everything:

```gitignore
*
!.gitignore
```

Raw browser captures must never enter Git history.

---

## 6. Prepare deterministic test assets

Use simple, non-sensitive, original fixtures:

### `subject.png`

A fictional person or mascot generated for testing:

- One subject only.
- Plain background.
- No real celebrity.
- No personal face.
- Clear wardrobe and silhouette.

### `product.png`

A fictional product:

- Plain background.
- No real trademark.
- Clear front-facing design.
- Include one stable identifying feature, such as a geometric label.

### `location.png`

A clean environment reference:

- No people.
- Clear spatial layout.
- Distinctive lighting.
- No text or branding.

### `start-frame.png`

A single composed scene containing the fictional subject and product.

### Video fixtures

Create original videos with FFmpeg or a camera:

- `source-08s.mp4`: eight seconds, 1080p or lower, simple motion.
- `source-35s.mp4`: 35 seconds, to exercise the >30-second trimming workflow.
- `source-61s.mp4`: 61 seconds, to verify the documented 60-second rejection if imported editing is available.
- `unsupported.txt`: renamed or invalid media for client-side validation tests.

Do not test the 1 GB boundary unless there is a specific engineering need. It adds cost and risk without improving payload discovery.

---

## 7. Create one isolated Flow project

Create a project named:

```text
OMNI-MAP-2026-06-18
```

Inside it, keep collections or clear asset names:

```text
00 Baseline
01 Inputs
02 Text to Video
03 Frames
04 Ingredients
05 Voices
06 Generated Edits
07 Uploaded Edits
08 History
09 Downloads
```

Create one standard fictional Flow Character, for example:

```text
@MaraTest
```

Use a stable description and one or two clean reference images.

Use a dedicated browser profile that contains no unrelated Google work, email, client material, or personal uploads.

---

# Part II — Pydoll capture protocol

## 8. Pin and record the Pydoll environment

Record:

```text
Python version
Pydoll version
Chrome version
Operating system
Flow account tier
Country/region
Flow UI language
Flow project ID placeholder
FlowKit commit SHA
Capture date
```

At the research date, Pydoll’s public repository lists release `2.23.0`. Pin the exact version you validate rather than automatically upgrading during the study.

Run Chrome visibly, not headlessly, for the first mapping pass.

---

## 9. Use passive Network monitoring first

The capture harness should:

1. Start Chrome with the dedicated profile.
2. Open Flow.
3. Let the operator sign in normally.
4. Enable Pydoll Network events.
5. Register callbacks for:
   - `Network.requestWillBeSent`
   - `Network.responseReceived`
   - `Network.loadingFinished`
   - `Network.loadingFailed`
6. Filter to relevant resource types:
   - `XHR`
   - `Fetch`
   - `Media`
   - optionally `WebSocket`
7. Filter primarily to:
   - `labs.google`
   - `aisandbox-pa.googleapis.com`
   - relevant Google media-storage hosts
8. Capture request metadata and JSON request bodies.
9. Retrieve response bodies only after requests finish.
10. Do not retrieve large video/image binary bodies through the event log.
11. Disable network events immediately after the test action is complete.

Do **not** enable the Fetch interception domain for the initial mapping. Passive observation is sufficient to discover the request sequence.

---

## 10. Canonical procedure for every capture

Use this exact sequence for every test ID:

1. Open the dedicated Flow project.
2. Wait until the asset grid and prompt box are fully loaded.
3. Wait until background traffic becomes idle.
4. Record the visible credit balance.
5. Set the prompt box back to a known neutral state.
6. Clear prior Pydoll network logs.
7. Take `ui-before.png`.
8. Write the intended test configuration into `manifest.json`.
9. Start passive capture.
10. Perform exactly one test action or one generation.
11. Wait for:
    - UI success,
    - UI validation failure,
    - server failure, or
    - terminal generation status.
12. Collect request/response bodies for relevant JSON calls.
13. Take `ui-after.png`.
14. Record the new credit balance.
15. Stop network monitoring.
16. Sanitize immediately.
17. Normalize dynamic values.
18. Generate `sequence.json` in chronological order.
19. Derive `contract.yaml`.
20. Repeat the test once if it consumed no or minimal credits, to distinguish stable fields from random fields.
21. Mark the test `MAPPED`, `BLOCKED_BY_REGION`, `NOT_EXPOSED`, `UNSTABLE`, or `FAILED`.

Change only one variable per test. For example, do not change duration and orientation in the same comparison.

---

## 11. Required capture manifest

Each capture should contain:

```json
{
  "test_id": "B01",
  "feature": "omni_text_to_video",
  "captured_at": "2026-06-18T00:00:00Z",
  "region": "PT",
  "account_tier": "GOOGLE_AI_PRO",
  "flow_ui_language": "en",
  "flowkit_commit": "<SHA>",
  "pydoll_version": "<VERSION>",
  "chrome_version": "<VERSION>",
  "ui_path": [
    "Project",
    "Generation settings",
    "Video",
    "Omni Flash"
  ],
  "settings": {
    "orientation": "LANDSCAPE",
    "duration_seconds": 4,
    "output_count": 1
  },
  "inputs": [],
  "prompt_hash": "<SHA256>",
  "credit_before": null,
  "credit_after": null,
  "expected_result": "one 4-second landscape video",
  "observed_result": null,
  "status": "PLANNED"
}
```

Store the test prompt in `notes.md`, not in fields that could accidentally contain sensitive content.

---

## 12. Sanitization rules

Before saving a sanitized fixture, replace or remove:

### Headers

```text
Authorization
Cookie
Set-Cookie
Proxy-Authorization
X-Goog-AuthUser
X-Goog-Visitor-Id
X-Client-Data
X-Origin
SAPISIDHASH
```

Also redact any header containing:

```text
auth
token
cookie
session
captcha
secret
credential
```

### JSON fields

Redact values under keys containing:

```text
accessToken
idToken
oauth
authorization
cookie
recaptcha
captchaToken
sessionToken
bearer
email
gaia
accountId
userId
```

### URLs

Strip or replace:

- Signed storage query strings.
- OAuth query parameters.
- User-specific path fragments.
- Email addresses.
- Account IDs.
- Long opaque tokens.

Preserve:

- Host.
- Endpoint path.
- HTTP method.
- Status code.
- Content type.
- Request-body field names and value types.
- Model identifier.
- Duration.
- Aspect ratio.
- Output count.
- Input roles.
- Polling state names.
- Media type.
- Stable capability flags.

### Dynamic ID normalization

Build one capture-local mapping:

```text
actual project ID      → <PROJECT_ID>
actual media ID        → <MEDIA_001>
actual operation ID    → <OPERATION_001>
actual workflow ID     → <WORKFLOW_001>
actual edit session ID → <EDIT_SESSION_001>
actual voice ID        → <VOICE_001>
```

Use the same placeholder everywhere within that capture so relationships remain visible.

---

## 13. Capture contract format

For each feature, derive a contract without guessing values:

```yaml
capability: omni_text_to_video
status: mapped

ui:
  model_label: Omni Flash
  mode: text_to_video
  orientation: landscape
  duration_seconds: 4
  output_count: 1

submit:
  method: "<captured>"
  host: "<captured>"
  path: "<captured>"
  request_content_type: "<captured>"
  required_body_paths:
    - "<captured.path>"
  optional_body_paths: []
  model_field_path: "<captured or null>"
  duration_field_path: "<captured or null>"
  orientation_field_path: "<captured or null>"
  output_count_field_path: "<captured or null>"

poll:
  required: true
  method: "<captured>"
  path: "<captured>"
  operation_id_path: "<captured>"
  pending_states: []
  success_states: []
  failure_states: []

result:
  media_id_path: "<captured>"
  media_url_path: "<captured>"
  duration_path: "<captured or null>"
  mime_type_path: "<captured or null>"

security:
  recaptcha_action_name: "<name only; never token>"
  browser_session_required: true

flowkit:
  implementation_status: not_started
```

---

# Part III — Exact Flow UI capture matrix

## 14. Group A — Model and UI inventory

### A00 — Background baseline

1. Open the project.
2. Do not touch the prompt box.
3. Capture 30–60 seconds of idle traffic.
4. Save the recurring background endpoints.
5. Use this as a subtraction baseline for every later capture.

**Purpose:** Remove project refresh, media refresh, telemetry, credit refresh, and other unrelated traffic from feature-specific traces.

---

### A01 — Select Omni Flash

1. Click the model name at the bottom of the prompt box.
2. Click **Video**.
3. Open the video-model selector.
4. Select **Omni Flash**.
5. Do not generate.
6. Capture:
   - model-list/config requests,
   - UI labels,
   - any capability metadata,
   - any credit-cost metadata.

**Record:** Whether the model selector itself triggers a request or whether the model identifier appears only at generation time.

---

### A02 — Inventory Omni settings

With Omni Flash selected:

1. Open generation settings.
2. Record every orientation choice.
3. Record every output-count choice.
4. Record every duration choice.
5. Record available generation submodes:
   - plain Video,
   - Frames,
   - Ingredients,
   - any other visible mode.
6. Capture screenshots of each open menu.
7. Do not generate.

**Expected current values:** Both orientations and 4/6/8/10-second choices.

---

### A03 — Inventory the Add menu

1. Keep Omni Flash selected.
2. Click **Add** under the prompt.
3. Record every category:
   - upload media,
   - project media,
   - Characters,
   - Voices,
   - any audio/video-specific category.
4. Open each submenu without selecting anything.
5. Record visible file-type hints and limits.

**Purpose:** Discover inputs that may not be fully described in help documentation.

---

### A04 — Unsupported first + last frame

1. Select **Video → Frames**.
2. Add a start frame.
3. Attempt to add an end frame while Omni Flash remains selected.
4. Observe whether Flow:
   - disables the control,
   - reports “coming soon,”
   - switches to Veo,
   - or allows submission.
5. Do not override an automatic model change.
6. Capture the UI transition and any capability-validation request.

**FlowKit rule:** Do not expose Omni first+last-frame generation until an actual successful contract is captured.

---

### A05 — Extend an Omni clip

After creating a successful Omni clip:

1. Open the clip.
2. Look for **Extend**.
3. If the button is absent or disabled, record that state.
4. If Flow proposes switching to Veo, record the behavior but do not treat it as an Omni operation.

---

## 15. Group B — Text-to-video

Use this stable prompt:

```text
A small blue ceramic robot walks across a clean studio table toward a glowing orange cube. Locked camera, soft daylight, natural room ambience, no text.
```

### B01 — Landscape, 4 seconds, one output

1. Select Omni Flash.
2. Select **Video** with no Frames or Ingredients.
3. Set landscape.
4. Set one output.
5. Set four seconds.
6. Enter the prompt.
7. Start capture.
8. Click **Generate**.
9. Wait for the final clip.
10. Capture submission, polling, media retrieval, credits, and download metadata.

This is the canonical minimum Omni generation.

### B02 — Portrait, 4 seconds

Repeat B01, changing only orientation to portrait.

**Diff target:** The exact orientation field and any model-key change.

### B03 — Landscape, 6 seconds

Repeat B01, changing only duration to six seconds.

### B04 — Landscape, 8 seconds

Repeat B01, changing only duration to eight seconds.

### B05 — Landscape, 10 seconds

Repeat B01, changing only duration to ten seconds.

**Diff target for B03–B05:** Locate the duration field and determine whether different duration choices alter model identifiers, endpoint paths, or credit metadata.

### B06 — Two outputs

1. Use the same prompt and B01 settings.
2. Change only output count from one to two.
3. Generate.
4. Determine whether Flow:
   - sends one batch request with two items,
   - uses a sample-count field,
   - or submits two independent operations.

Do not test larger output counts until the cost behavior is understood.

---

## 16. Group C — First-frame-to-video

### C01 — Upload a local start frame

1. Select **Video → Frames**.
2. Drag `start-frame.png` into **Add start frame**.
3. Capture the upload separately until it receives a reusable media ID.
4. Clear logs.
5. Set Omni Flash, landscape, four seconds, one output.
6. Enter:

```text
The robot slowly reaches for the orange cube while the camera gently pushes in. Preserve the opening composition and the robot design.
```

7. Generate and capture the complete sequence.

**Separate contracts:**

- Image upload.
- Start-frame Omni generation.

### C02 — Use an existing project image

1. Save or generate an image in Flow.
2. Select it from project assets rather than uploading.
3. Use it as the start frame.
4. Repeat C01 generation settings.

**Diff target:** Confirm that uploaded and project-native media resolve to the same input role and media identifier shape.

### C03 — Start frame, portrait

Repeat C01 and change only orientation.

### C04 — Start frame, 10 seconds

Repeat C01 and change only duration.

---

## 17. Group D — Ingredients and references

### D01 — One image ingredient

1. Select Omni Flash.
2. Select **Video → Ingredients**.
3. Upload or select `product.png`.
4. Use:

```text
The blue robot presents the exact product from the ingredient on a clean studio table. Preserve the product geometry and label design.
```

5. Generate at four seconds, one output.
6. Map:
   - input media role,
   - ingredient order,
   - prompt/reference linkage,
   - media upload behavior.

### D02 — Multiple image ingredients

1. Add `subject.png`, `product.png`, and `location.png`.
2. Mention every ingredient explicitly in the prompt.
3. Generate.
4. Determine:
   - maximum observed reference count,
   - ordering,
   - role/type per ingredient,
   - whether reference labels are transmitted.

### D03 — Use `@` project-asset selection

1. Type `@`.
2. Select an already uploaded project asset.
3. Add it as an ingredient.
4. Generate with the same D01 prompt.

**Diff target:** Confirm whether UI selection and drag/upload produce identical generation payloads after media creation.

### D04 — Native Flow Character

1. Type `@MaraTest`.
2. Select the Character.
3. Enter:

```text
@MaraTest walks into the test location and picks up the exact product reference.
```

4. Generate once with only the Character.
5. Generate once with Character + product ingredient.
6. Capture how a Character differs from a generic image reference:
   - character ID,
   - media references,
   - voice linkage,
   - metadata.

### D05 — Video ingredient

1. Select **Video → Ingredients**.
2. Add a short original video if the UI allows video ingredients in your region.
3. Add one image ingredient.
4. Generate.
5. Map:
   - video-upload sequence,
   - media type,
   - input role,
   - trimming or preprocessing,
   - whether audio is retained as a reference.

Do not confuse a video ingredient with video-to-video editing. Record the UI mode and request contract separately.

### D06 — Avatar / `@me` availability

1. Type `@me`.
2. Record whether the avatar option is available.
3. If unavailable because of region, mark `BLOCKED_BY_REGION`.
4. Do not attempt to bypass the restriction.

### D07 — Preset voice ingredient

1. Select Omni Flash.
2. Select **Video → Ingredients**.
3. Click **Add → Voices**.
4. Choose one preset voice.
5. Reference it in the prompt as shown by Flow, for example `@Voice: <name>`.
6. Generate a clip with a single short spoken sentence.
7. Capture:
   - voice ID,
   - voice reference role,
   - ingredient representation,
   - prompt linkage,
   - audio settings.

### D08 — Voice outside Ingredients negative test

1. Select Omni Flash.
2. Select plain Video rather than Ingredients.
3. Attempt to add or reference the same voice.
4. Record the UI error or server validation error.
5. Do not retry repeatedly.

**Purpose:** Capture a clean capability-validation contract.

---

## 18. Group E — Voice catalog and custom voices

### E01 — Voice catalog and preview

1. Select **Add → Voices**.
2. Start capture before opening the list.
3. Record the voice catalog request.
4. Hover over one preset voice.
5. Click **Play** for its sample.
6. Capture the preview-media request separately.

**Record:** Stable voice IDs, display-name fields, preview metadata, locale, gender/style fields if present, and whether catalog results are paginated.

### E02 — Open custom voice creation

1. Click **Add → Voices → Create New Voice**.
2. Record every field and default.
3. Select a preset Base Voice.
4. Use a test name:

```text
Omni Test Voice 01
```

5. Enter a performance prompt:

```text
Warm, confident documentary delivery with restrained energy and clear articulation.
```

6. Enter sample dialogue:

```text
The campaign begins with one clear idea.
```

7. Start capture.
8. Click **Sync**.
9. Wait for the preview.

**Map:** Whether Sync creates a temporary voice, a preview operation, or both.

### E03 — Save the custom voice

1. Continue from E02.
2. Clear capture logs after preview completion.
3. Click **Save New Voice**.
4. Capture the save operation.
5. Record the permanent voice ID and project/account scope.

### E04 — Generate with the saved custom voice

1. Start a new Ingredients generation.
2. Select the saved custom voice.
3. Generate a four-second clip containing one short spoken line.
4. Confirm the saved voice ID is reused.

### E05 — Voice lifecycle inventory

Inspect the saved voice UI for:

- Rename.
- Edit performance prompt.
- Re-sync.
- Duplicate.
- Delete.
- Project scope versus account scope.

Capture only operations that are visibly supported. Do not invent routes for absent controls.

---

## 19. Group F — Generated-video editing

### F01 — Edit an Omni-generated clip

1. Open the B01 result.
2. Set generation settings to **Video → Omni Flash**.
3. Add this edit prompt:

```text
Change the daylight to a warm cinematic sunset while preserving the robot, cube, camera position, and timing.
```

4. Generate.
5. Map:
   - source video media ID,
   - edit mode indicator,
   - source segment representation,
   - parent/child relationship,
   - output duration,
   - output media,
   - edit session/context ID.

### F02 — Edit a Veo-generated clip through Omni

1. Create or select a Veo clip.
2. Switch the active model to Omni Flash.
3. Apply the same lighting edit.
4. Compare with F01.

**Purpose:** Determine whether source-model provenance affects the edit contract.

### F03 — Edit with an image ingredient

1. Open an editable generated clip.
2. Add `product.png` as an ingredient.
3. Enter:

```text
Replace the orange cube with the exact product ingredient. Preserve the robot and camera movement.
```

4. Generate.
5. Determine how edit inputs and ingredient inputs coexist.

### F04 — Follow-up turn 2

From the F03 result, enter:

```text
Make the product 15 percent smaller and move it slightly left. Preserve every other change.
```

Capture the second-turn request.

### F05 — Follow-up turn 3

Enter:

```text
Add a soft reflection beneath the product without changing its shape.
```

Capture the third-turn request.

### F06 — Attempt turn 4

Enter a fourth refinement.

Record whether Flow:

- rejects it,
- starts a new edit context,
- drops earlier context,
- or requires the result to be saved as a new source.

This determines the FlowKit session state machine.

### F07 — Edit preferences

Using the same source clip, run separate captures changing only:

- orientation,
- output count,
- output duration.

Do not combine these changes in one test.

### F08 — History and Save to Project

1. Open the edited clip.
2. Open the **History** panel.
3. Hover over an earlier version.
4. Click **Save to Project**.
5. Capture the project-save operation.
6. Determine whether a new media ID is created or an existing version is promoted.

### F09 — Save frame and reuse it

1. Pause an edited video.
2. Hover over the chosen frame.
3. Click **Save frame**.
4. Capture the frame-extraction/save operation.
5. Use the resulting image:
   - once as a start frame,
   - once as an ingredient.

This reveals the conversion path from video frame to reusable image media.

---

## 20. Group G — Uploaded-video editing

### G00 — Region gate check in Portugal

1. Select **Video → Omni Flash**.
2. Try to upload `source-08s.mp4` as an edit source.
3. Record whether:
   - the feature is absent,
   - upload is accepted but edit is blocked,
   - or Flow displays a regional message.
4. Mark the feature `BLOCKED_BY_REGION`.
5. Stop. Do not use a VPN or another technique to circumvent the restriction.

### G01–G06 — Only in a lawfully eligible environment

Run these only when the account and physical region are eligible.

#### G01 — Short MP4

1. Upload `source-08s.mp4`.
2. Let Flow process and run checks.
3. Select the full segment.
4. Enter a simple lighting edit.
5. Generate.

#### G02 — 35-second source and trimming

1. Upload `source-35s.mp4`.
2. Capture the initial upload and processing.
3. Observe the required reduction to 30 seconds.
4. Choose a 30-second source range.
5. In the edit trimming window, select a 10-second segment.
6. Generate.

Map both trim representations separately.

#### G03 — Supported format validation

Test `.mov`, `.avi`, and `.wmv` with very small original clips.

The goal is to map client/server validation and MIME handling, not to generate from every format.

#### G04 — Rejection tests

Test separately:

- `source-61s.mp4`.
- `unsupported.txt`.
- A zero-byte `.mp4`.
- A corrupted video.

Capture clean validation errors.

#### G05 — Uploaded edit with ingredient

Add `product.png` during the video edit and generate.

#### G06 — Uploaded edit follow-up turns

Repeat the F04–F06 multi-turn sequence and determine whether uploaded sources use the same edit-session contract as generated sources.

---

## 21. Group H — Retrieval, download, and upscale integration

These are not exclusive to Omni, but they are required by the production pipeline.

### H01 — Download original result

1. Hover over an Omni output.
2. Click **More → Download**.
3. Record:
   - download metadata request,
   - chosen format/resolution,
   - media URL host/path without signed query data,
   - file MIME type,
   - actual duration and dimensions.

### H02 — 1080p upscale

1. Select an approved Omni result.
2. Choose 1080p upscale/export if the UI exposes it.
3. Capture the upscale submission and result.
4. Confirm that the FlowKit fork never defaults a Pro account to 4K.

### H03 — Watermark and metadata observation

Record, without trying to remove it:

- visible watermark presence,
- SynthID/content-credential metadata where observable,
- resolution,
- duration,
- codec,
- frame rate,
- audio stream details.

Use `ffprobe` after download.

---

## 22. Group I — Agent-mediated Omni behavior

Treat Flow Agent as a separate orchestration layer. Implement direct Omni first.

### I01 — Agent creates Omni variations

1. Turn on Agent.
2. Ask for two Omni video variations.
3. Observe:
   - Agent/chat request,
   - model planning,
   - generation submissions,
   - whether the model is explicitly Omni,
   - output grouping.

### I02 — Agent edits multiple clips

1. Select or drag two generated clips into Agent.
2. Request the same edit on both.
3. Determine whether:
   - one batch request is sent,
   - multiple Omni requests are created,
   - a shared instruction/context ID is used.

Do not couple FlowKit’s initial Omni provider to Agent internals. Agent support should be a later optional adapter.

---

# Part IV — Analyze the captures

## 23. Build an endpoint and sequence inventory

For each test, classify calls as:

### Control plane

- Project operations.
- Model/capability configuration.
- Credits.
- Asset listing.
- Voice catalog.
- Character lookup.
- History/version management.

### Media plane

- Image upload.
- Video upload.
- Media preprocessing.
- Generation submit.
- Edit submit.
- Voice preview/sync.
- Polling.
- Media retrieval.
- Download/upscale.

### Telemetry/background

- Analytics.
- Logging.
- Refreshes.
- Unrelated UI data.

Do not implement telemetry endpoints.

---

## 24. Determine stable versus dynamic fields

Run structural diffs across repeated captures.

### Stable candidates

- Endpoint path.
- Model identifier.
- Capability or generation type.
- Duration enum.
- Aspect-ratio enum.
- Output-count field.
- Input role.
- Media type.
- Voice role.
- Edit turn field.
- Status enum.

### Dynamic candidates

- Project ID.
- Session ID.
- Batch ID.
- Operation/workflow ID.
- Media ID.
- Timestamps.
- Seeds.
- Signed URLs.
- reCAPTCHA token.
- Browser/session identifiers.

Never hardcode a dynamic capture value.

---

## 25. Derive state machines

Create state diagrams for:

### Generation

```text
prepared
  → submitted
  → pending
  → processing
  → succeeded
  → media_ready
```

Include all observed failure states.

### Upload

```text
selected
  → uploaded
  → processing
  → safety_check
  → ready
```

### Edit session

```text
source_selected
  → turn_1_submitted
  → turn_1_ready
  → turn_2_submitted
  → turn_2_ready
  → turn_3_submitted
  → turn_3_ready
  → closed_or_reset
```

### Custom voice

```text
base_selected
  → preview_sync_submitted
  → preview_ready
  → saved
  → referenced_in_generation
```

---

## 26. Produce the FlowKit gap matrix

Use this format:

| Capability | Flow UI capture | Current FlowKit | Required work | Priority |
|---|---|---|---|---|
| Omni text-to-video | B01–B06 | Missing | Provider, request model, parser | P0 |
| Omni first frame | C01–C04 | Partial Veo analogue | Omni-specific adapter | P0 |
| Image ingredients | D01–D04 | Partial | Generalized media-role inputs | P0 |
| Video ingredient | D05 | Missing | Video upload/input role | P1 |
| Preset voices | D07/E01 | Missing | Voice catalog/reference | P1 |
| Custom voices | E02–E05 | Missing | Voice service and persistence | P1 |
| Generated-video edit | F01–F09 | Missing | Edit sessions and history | P0 |
| Imported-video edit | G00–G06 | Region-blocked in PT | Capability-gated adapter | P2 |
| Output duration | B03–B05 | Missing | Schema and API propagation | P0 |
| Output count | B06 | Missing | Batch/output schema | P0 |
| 1080p upscale | H02 | Partially present | Correct Pro-safe default | P0 |

---

# Part V — Implement Omni in the FlowKit fork

## 27. Recommended architecture

Do not fold Omni into the existing Veo method with many conditionals.

Add a provider layer:

```text
agent/providers/
├── base.py
├── veo.py
└── omni.py

agent/contracts/
├── generation.py
├── edit.py
├── media.py
└── voice.py

agent/services/
├── media_upload.py
├── edit_sessions.py
├── voice_service.py
└── capability_service.py
```

Suggested interface:

```python
class VideoProvider(Protocol):
    async def generate(self, request: VideoGenerationRequest) -> GenerationSubmission: ...
    async def edit(self, request: VideoEditRequest) -> GenerationSubmission: ...
    async def poll(self, operation: RemoteOperation) -> GenerationResult: ...
```

Use:

```text
VeoProvider
OmniProvider
```

The existing extension or a Pydoll browser transport should sit below the providers.

---

## 28. Add a transport abstraction

```python
class FlowTransport(Protocol):
    async def request(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        json_body: dict | None,
        captcha_action: str | None,
        timeout_seconds: float,
    ) -> dict: ...
```

Implement adapters:

```text
ExtensionFlowTransport   # recommended initial production transport
PydollFlowTransport      # optional later transport
FixtureFlowTransport     # tests using sanitized captures
```

### Recommended decision

Use Pydoll for mapping first, but retain the existing FlowKit Chrome extension for the first production Omni implementation. The extension already integrates with FlowKit’s queue and browser session.

Consider replacing it with a Pydoll transport only after:

- Omni contracts are stable.
- Browser-session behavior is reliable.
- Security review is complete.
- No token export is required.
- The Pydoll transport can execute entirely inside the authenticated browser context.

---

## 29. Add capability discovery

Create:

```text
GET /api/capabilities
```

Return account- and region-aware capabilities:

```json
{
  "models": {
    "veo": true,
    "omni_flash": true
  },
  "omni": {
    "text_to_video": true,
    "first_frame_to_video": true,
    "first_last_frame_to_video": false,
    "image_ingredients": true,
    "video_ingredients": true,
    "preset_voices": true,
    "custom_voices": true,
    "generated_video_edit": true,
    "uploaded_video_edit": false,
    "max_edit_turns": 3,
    "durations": [4, 6, 8, 10],
    "orientations": ["LANDSCAPE", "PORTRAIT"]
  },
  "region": "PT"
}
```

Populate this from captured capability/config responses where possible. Otherwise combine documented rules with live UI availability, and label the source.

The agent must consult this endpoint before planning work.

---

## 30. Add first-class request models

### Generation

```python
class OmniGenerationCreate(BaseModel):
    project_id: str
    prompt: str
    orientation: Literal["LANDSCAPE", "PORTRAIT"]
    duration_seconds: Literal[4, 6, 8, 10]
    output_count: int = Field(default=1, ge=1)
    start_frame_media_id: str | None = None
    ingredient_media_ids: list[str] = []
    character_ids: list[str] = []
    voice_id: str | None = None
    dry_run: bool = False
    confirm_credit_spend: bool = False
```

### Edit

```python
class OmniEditCreate(BaseModel):
    project_id: str
    source_video_media_id: str
    prompt: str
    orientation: Literal["LANDSCAPE", "PORTRAIT"]
    duration_seconds: Literal[4, 6, 8, 10]
    output_count: int = Field(default=1, ge=1)
    ingredient_media_ids: list[str] = []
    source_trim_start_ms: int | None = None
    source_trim_end_ms: int | None = None
    parent_edit_session_id: str | None = None
    dry_run: bool = False
    confirm_credit_spend: bool = False
```

### Follow-up edit

```python
class OmniEditTurnCreate(BaseModel):
    prompt: str
    ingredient_media_ids: list[str] = []
    confirm_credit_spend: bool = False
```

### Voice

```python
class CustomVoiceCreate(BaseModel):
    name: str
    base_voice_id: str
    performance_prompt: str
    sample_dialogue: str | None = None
```

Adjust the field names to the captured contracts. Do not copy these conceptual names into remote payloads without a mapping layer.

---

## 31. Expand persistence

The current scene-centric schema is too narrow for arbitrary Omni editing.

Add migrations for:

### `media_asset`

```text
id
remote_media_id
project_id
kind                  # image, video, audio, frame
source                # uploaded, generated, extracted_frame
mime_type
width
height
duration_ms
local_path
remote_url
parent_asset_id
metadata_json
created_at
```

### `generation_job`

```text
id
provider              # veo, omni
capability            # text_to_video, first_frame, ingredients, edit
project_id
prompt
orientation
duration_seconds
output_count
status
remote_operation_id
remote_workflow_id
credit_before
credit_after
error_code
error_message
request_hash
created_at
updated_at
```

### `generation_input`

```text
job_id
asset_id
role                  # start_frame, ingredient, source_video, character, voice
position
remote_role
metadata_json
```

### `edit_session`

```text
id
project_id
root_source_asset_id
current_asset_id
remote_session_id
turn_count
max_turns
status
created_at
updated_at
```

### `voice_profile`

```text
id
remote_voice_id
name
base_voice_id
performance_prompt
preview_asset_id
scope
status
created_at
updated_at
```

---

## 32. Add API routes

Suggested routes:

```text
POST /api/media/upload-image
POST /api/media/upload-video
GET  /api/media/{id}

POST /api/omni/generations
GET  /api/omni/generations/{job_id}

POST /api/omni/edits
POST /api/omni/edits/{session_id}/turns
GET  /api/omni/edits/{session_id}

GET  /api/omni/voices
POST /api/omni/voices/preview
POST /api/omni/voices
DELETE /api/omni/voices/{voice_id}

GET  /api/capabilities
```

Only add routes confirmed by UI behavior. For unsupported lifecycle actions, omit the API rather than guessing.

---

## 33. Add queue request types

Either migrate from a closed Literal to a capability-based job model, or add:

```text
GENERATE_VIDEO_OMNI
EDIT_VIDEO_OMNI
CONTINUE_VIDEO_EDIT_OMNI
UPLOAD_VIDEO
CREATE_CUSTOM_VOICE
PREVIEW_CUSTOM_VOICE
```

A generalized job model is preferable because Omni will likely expand.

The worker must:

- Enforce prerequisites.
- Persist operation IDs before polling.
- Avoid duplicate submissions on retries.
- Understand all observed Omni response schemas.
- Apply backoff.
- Store terminal failure details.
- Preserve edit-session turn count.
- Stop before turn four unless the captured contract shows a valid reset path.

---

## 34. Implement upload handling

### Image upload

Reuse the current upload path where the captured contract matches.

### Video upload

Implement:

- MIME validation.
- Extension validation.
- Duration inspection with `ffprobe`.
- File-size validation.
- Region capability check.
- Upload progress.
- Remote processing state.
- Safety-check state.
- Media ID persistence.
- Optional trim metadata.

For Portugal, `POST /api/media/upload-video` may still be useful for video ingredients if Flow exposes them, but `POST /api/omni/edits` must reject imported-video edit sources when the live capability says false.

---

## 35. Implement edit sessions

The FlowKit service should own a local edit-session record even if Flow’s remote contract uses another name.

Rules:

1. Turn 1 creates the session.
2. Turn 2 references turn 1’s context and output.
3. Turn 3 references the same continuing context.
4. Turn 4 is rejected locally unless the captured UI contract demonstrates a supported reset/new-session workflow.
5. Each output remains an immutable `media_asset`.
6. The session’s `current_asset_id` advances after success.
7. A failed turn does not advance the session.
8. The user can fork an earlier version into a new session.

This models Flow’s History behavior without overwriting assets.

---

## 36. Implement voices as real assets, not prompt text

Do not map FlowKit’s existing `voice_description` field to Omni voice references.

Keep separate concepts:

```text
voice_description
  = natural-language guidance appended to a Veo prompt

remote voice profile
  = a Flow voice entity identified by a captured remote ID
```

The Omni provider should send the remote voice reference using the exact role and field discovered in D07/E04.

---

## 37. Add dry-run and credit confirmation

Every generation/edit endpoint should support:

```json
{
  "dry_run": true
}
```

Dry run returns:

- selected provider,
- capability,
- model,
- number of outputs,
- duration,
- references,
- predicted operation count,
- live credit balance,
- known current cost if exposed,
- unsupported settings,
- sanitized request preview.

A real request requires:

```json
{
  "confirm_credit_spend": true
}
```

For agent use, require confirmation when:

- output count > 1,
- a batch contains multiple scenes,
- Quality/expensive models are selected,
- retries would create a new paid submission.

---

# Part VI — Tests and validation

## 38. Fixture-based contract tests

Every sanitized capture becomes a test fixture.

Tests should verify:

- Payload builder produces the captured stable structure.
- Dynamic IDs are inserted in the correct paths.
- Parser extracts operation/workflow/media IDs.
- Poller recognizes pending, success, and failure.
- Media result is persisted.
- Voice result is persisted.
- Edit turn increments correctly.
- Secret fields never appear in logs or snapshots.

Use `FixtureFlowTransport` in CI. Never use a live Google account in CI.

---

## 39. Live smoke tests

Run manually against your own test project:

1. Omni text-to-video, 4 seconds, one output.
2. Omni first-frame-to-video.
3. Omni image ingredient.
4. Omni preset voice ingredient.
5. Omni custom voice generation.
6. Generated-video edit turn 1.
7. Edit turn 2.
8. Edit turn 3.
9. 1080p export/download.
10. Veo regression generation.

Each smoke test must check:

- Correct Flow project.
- Correct media appears in the Flow UI.
- Correct local database record.
- Correct downloaded file.
- Correct duration and orientation.
- No duplicate paid submissions.
- No secret logging.

---

## 40. UI round-trip verification

After every new implementation:

1. Generate through FlowKit.
2. Refresh the Flow UI.
3. Confirm the asset appears in the intended project.
4. Open it manually.
5. Confirm History/source relationships where relevant.
6. Confirm it can be selected as a later ingredient or edit source.
7. Download manually and compare metadata with the programmatic download.

A backend call that creates an inaccessible or orphaned asset is not complete.

---

## 41. Regional and account tests

Test capability behavior for:

- Portugal / EEA.
- Google AI Pro.
- Insufficient credits.
- Feature rollout absent.
- Voice feature absent.
- Imported-edit feature absent.
- Model temporarily unavailable.

Return clear errors such as:

```text
OMNI_NOT_AVAILABLE
UPLOADED_VIDEO_EDIT_BLOCKED_BY_REGION
CUSTOM_VOICE_NOT_AVAILABLE
UNSUPPORTED_DURATION
MAX_EDIT_TURNS_REACHED
INSUFFICIENT_CREDITS
MODEL_ACCESS_DENIED
```

Do not silently fall back to another model unless the caller explicitly permits fallback.

---

## 42. Security tests

Verify:

- API binds to `127.0.0.1`.
- CORS is not wildcard in production.
- Local API requires a secret or authenticated IPC.
- Callback secret is actually validated.
- Raw auth headers are never logged.
- Raw cookies are never logged.
- Raw HAR directory is gitignored.
- Signed media URLs are stripped before logs.
- Pydoll profile directory has restrictive filesystem permissions.
- The browser-session transport cannot call arbitrary domains.
- Endpoint allowlists are narrow.
- Request bodies are size-limited.
- Uploaded paths cannot escape approved directories.

---

# Part VII — Codex/MCP integration

## 43. Expose typed MCP tools

After the REST API is stable, expose:

```text
flow.capabilities
flow.credits
flow.projects.create
flow.media.upload
flow.media.get
flow.omni.generate
flow.omni.edit
flow.omni.continue_edit
flow.omni.edit_session
flow.voices.list
flow.voices.preview
flow.voices.create
flow.jobs.get
flow.jobs.cancel
flow.assets.download
flow.video.upscale_1080p
```

Every credit-consuming MCP tool should accept:

```text
dry_run
confirm_credit_spend
idempotency_key
```

Tool responses should include:

```text
job_id
status
provider
model
duration
orientation
output_count
credit_before
credit_after
asset_ids
error
```

Do not expose remote bearer tokens, cookies, reCAPTCHA tokens, or signed URLs to the model.

---

## 44. Codex operating instructions

Add to `AGENTS.md`:

```text
Before using Omni:
1. Call flow.capabilities.
2. Call flow.credits.
3. Use dry_run for every generation plan.
4. Present expected operations and maximum known credit cost.
5. Require user approval before confirm_credit_spend=true.
6. Never request uploaded-video editing when capability=false.
7. Never exceed three edit turns in one Omni edit session.
8. Preserve original source assets.
9. Use one output during exploration.
10. Prefer 4-second tests until the final shot is approved.
11. Download only approved outputs.
12. Use 1080p, not 4K, for Google AI Pro.
```

---

## 45. Example agent workflow

```text
User brief
  ↓
flow.capabilities
  ↓
flow.credits
  ↓
Create shot plan
  ↓
Upload/generate references
  ↓
Dry-run each Omni request
  ↓
User approves
  ↓
Submit one-output drafts
  ↓
Automated visual/audio QC
  ↓
Edit failed shots, maximum three turns
  ↓
Select finals
  ↓
1080p export/download
  ↓
FFmpeg/Resolve/CapCut stage:
    trim
    captions
    music
    transitions
    branding
    loudness
  ↓
Platform-specific render
  ↓
Publish
```

Flow should generate and transform shots. A conventional local editor should still handle the final multi-track timeline, subtitles, music mixing, transitions, color finishing, and platform packaging.

---

# Part VIII — Execution order

## 46. Milestone sequence

### Milestone 0 — Capture safety

Complete:

- Dedicated profile.
- Raw-capture gitignore.
- Sanitizer.
- Baseline A00.
- Secret-leak unit tests.

### Milestone 1 — Core Omni generation

Capture and implement:

- A01–A04.
- B01–B06.
- C01–C04.

Deliver:

- Omni provider.
- Duration.
- Orientation.
- Output count.
- Text-to-video.
- First-frame-to-video.
- Polling/parser.
- Media persistence.

### Milestone 2 — References

Capture and implement:

- D01–D05.
- D03 project-asset reuse.
- D04 native Character mapping.

Deliver:

- Generalized media inputs.
- Image/video ingredient roles.
- Upload service.

### Milestone 3 — Generated-video editing

Capture and implement:

- F01–F09.

Deliver:

- Source-video editing.
- Multi-turn sessions.
- Immutable history.
- Save/fork behavior.
- Frame extraction integration where possible.

### Milestone 4 — Voices

Capture and implement:

- D07–D08.
- E01–E05.

Deliver:

- Voice catalog.
- Voice previews.
- Custom voice creation.
- Saved voice references.

### Milestone 5 — Regional imported editing

Capture G00 in Portugal.

Only implement G01–G06 after lawful eligible testing. Keep the capability disabled in Portugal.

### Milestone 6 — Agent and pipeline integration

Implement:

- MCP tools.
- Codex instructions.
- Credit confirmation.
- Quality-review loop.
- Download/upscale.
- Social-content pipeline integration.

### Milestone 7 — Optional Flow Agent mapping

Capture I01–I02 only after direct Omni support is stable.

---

## 47. Definition of done

Omni support is complete for a capability only when all are true:

- [ ] Exact Flow UI path documented.
- [ ] At least one sanitized successful capture exists.
- [ ] Error or unsupported behavior captured.
- [ ] Stable request fields identified.
- [ ] Dynamic fields identified.
- [ ] Submission contract implemented.
- [ ] Polling/result contract implemented.
- [ ] Media is persisted locally.
- [ ] Asset appears correctly in the Flow UI.
- [ ] Credit delta is recorded.
- [ ] Retry is idempotent.
- [ ] No secret appears in fixtures or logs.
- [ ] Fixture test passes.
- [ ] Live smoke test passes.
- [ ] Agent tool schema exists.
- [ ] Capability is region-gated where required.
- [ ] Existing Veo workflow remains passing.

---

## 48. First captures to run

Run only these three first:

### Capture 1 — A00

Idle project baseline.

### Capture 2 — A01/A02

Open the model and settings menus, select Omni Flash, and inventory all visible choices without generating.

### Capture 3 — B01

One output, landscape, four seconds, plain text-to-video.

Do not proceed to custom voices or editing until B01 produces:

- A sanitized submit request.
- A complete polling sequence.
- A terminal success response.
- A media identifier.
- A downloadable output.
- A known credit delta.
- A contract fixture that can be parsed by a unit test.

That first contract will reveal whether Omni can reuse the current FlowKit video transport or requires a distinct provider and parser.

---

## 49. Reference sources

Official Flow documentation:

- [Learn about Google Flow models and supported features](https://support.google.com/flow/answer/16352836?hl=en)
- [Create videos in Google Flow](https://support.google.com/flow/answer/16353334?hl=en)
- [Edit videos and build scenes in Google Flow](https://support.google.com/flow/answer/16935718?hl=en)
- [Where you can use Google Flow](https://support.google.com/flow/answer/16353544?hl=en)

Pydoll documentation:

- [Pydoll repository](https://github.com/autoscrape-labs/pydoll)
- [Network monitoring](https://pydoll.tech/docs/features/network/monitoring/)
- [Request interception](https://pydoll.tech/docs/features/network/interception/)
- [HAR network recording](https://pydoll.tech/docs/features/network/network-recording/)
- [Browser-context HTTP requests](https://pydoll.tech/docs/features/network/http-requests/)

FlowKit baseline:

- [crisng95/flowkit](https://github.com/crisng95/flowkit)
