# Acceptance gate = re-run Gemini analysis and diff against a frozen accepted-open list

A Recreation is accepted when re-running the Gemini formula analysis on the new render
produces a deviation diff (vs the viral Exemplar) containing **nothing outside a pre-frozen
*accepted-open list*** — the deviations we consciously chose not to fix. Every other deviation
must be closed.

For **reel-1-pedro** the accepted-open list is the ~12 VO-timing / VO-content-bound deviations
from `gemini_pipeline/outputs/reel-1-pedro/formula-gap-analysis_20260612.md`:
#1, #2, #8, #9, #11, #18, #33, #34, #45, #50, #56, the 24.0s → ~26.5s runtime miss, and the
**VO-content half of #14** (the four *spoken* stacked tips — its visual half, the 4-shot screencast
run, IS closed).
They are frozen because the user has ruled out **any** VO re-record, and ffmpeg cannot compress
the existing voice onto the viral grid without destroying naturalness (the hook alone needs ~1.92×).

Note: several "timing" deviations are *partially* closed — the cut/caption placement tracks
Pedro's actual sped VO (deterministic), but the spoken word still lands where it lands. Captions
are timed to the real voice, never to the viral grid, or they desync and read as broken.

## Why this shape

The pipeline needs a deterministic *termination condition* for its retry loop. "Zero deviations"
is unreachable the moment any deviation is accepted-open; "looks good to me" yields no reusable
gate. Partitioning the deviation set and re-running the *same* analysis that produced it makes the
gate self-consistent and reusable across future reels.

## Trade-off

The shipped reel knowingly misses the formula's most-emphasized dimension (front-half timing).
Accepted because the alternative (re-record) is declined by the user, and the **edit-grammar**
deviations — where most of the formula's transferable value lives — are all still closed.
