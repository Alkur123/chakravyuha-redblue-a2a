# AdaL video brief v3: "Abhimanyu, reversed" (locked layout)

v2 failed at full size: a blank frame at 0:55, headlines that faded out while their panel stayed, half-empty
crops of footage, a harsh white BAND screenshot, stacked boxes, soft enlarged text, and a headline repeating
its panel. v3 removes the cause: every proof is a finished, crisp image (2x), and the layout is fixed.

---

Make a **2:30 launch film, 16:9, 1920x1080, 30 fps, no voiceover**, from `video/assets3/` only. A person will speak
over it live. Keep it calm, premium and precise, in the style of an AI-lab launch film. Do not change any wording below.

## Files (all in `video/assets3/`)
- `opener_formation.mp4` (6 s generated opening), `warroom_live_run.mp4` (real 64 s recording of the live run)
- 12 proof cards, each exactly 2080x1200 (display at 50% = 1040x600): `card_finding.png`, `card_hardened.png`,
  `card_kill-traversal.png`, `card_kill-decoy.png`, `card_forged.png`, `card_withdraw.png`, `card_closure.png`,
  `card_flat.png`, `card_held.png`, `card_reconciled.png`, `card_adal.png`, `card_vault.png`
- 3 real BAND room screenshots (dark theme): `band_forged_rejected.png`, `band_alarm_stays_open.png`, `band_report_reconciled.png`
- `score.mp3` (114 s music bed made for v2; reuse it, extend it smoothly to 2:30 if you can, otherwise generate one new
  restrained ambient score of 2:30)

## Locked layout (every "split" beat uses exactly this)
- Background #0b0f1a everywhere. No other background colour, no white frames.
- **Headline block**: left column, x = 120 px, width 560 px, vertically centred. Headline 64 px, weight 800, white,
  at most 3 lines. Optional subline 30 px, weight 400, colour #8f9bb8, at most 2 lines, 20 px below the headline.
  Inter (or the closest available grotesk). Accent words in marigold #f5a524; the words KILLED and REJECTED in red #ff5d5d.
- **Proof frame**: x = 760 px, y = 240 px, 1040 x 600 px. Cards go here at exactly 1040 x 600 (no crop, no zoom).
  BAND screenshots are scaled to fit inside 1040 x 640 (keep aspect, no crop), with 24 px rounded corners.
- The headline and its proof are visible for the **whole** beat: both fade in together over 350 ms and the next beat
  cross-dissolves over 450 ms. **There is never a frame with no text and no proof.** No blank frames anywhere.
- Motion: a slow push on the proof only, 1.00 to 1.03 over the beat. Headlines do not move after they land.
- No captions, no caption bar, no extra labels, no stacked boxes, nothing overlapping anything.

## Sequence (start–end)
1. **0:00–0:07** `opener_formation.mp4`, full frame. Centred: **CHAKRAVYUHA** (marigold, 88 px, letter-spaced),
   below it "The attacker gets in. It cannot get out." (30 px).
2. **0:07–0:14** centred text only: "Agents now talk to agents." then, 2 s later, below it in #8f9bb8:
   "One forged message can talk a model down."
3. **0:14–0:20** centred: **Band routes.** (white) **Aegis decides.** (marigold), 88 px.
4. **0:20–0:30** `warroom_live_run.mp4` **full frame** from its 2-second mark, slow push 1.00 to 1.05. One small label,
   bottom-left, 24 px, #8f9bb8: "Live run · hosted on Agent37 · real BAND room".
5. **0:30–0:38** split: `card_finding.png` · "Red finds a real bug." / "Path traversal into internal files."
6. **0:38–0:46** split: `card_hardened.png` · "Blue turns it into a rule." / "Lyzr writes the fix. Finch cites a skill."
7. **0:46–0:54** split: `card_kill-traversal.png` · "The same attack: **KILLED**." (hard cut in, with a low hit)
8. **0:54–1:02** split: `card_kill-decoy.png` · "A planted decoy." / "Touch it and the session is over." (low hit)
9. **1:02–1:12** split: `band_forged_rejected.png` · "Red pretends to be Blue." / "In the real BAND room, every message is signed."
10. **1:12–1:20** split: `card_forged.png` · "**REJECTED.**" / "The gate reads deeds, not words." (low hit)
11. **1:20–1:27** split: `band_alarm_stays_open.png` · "It cannot withdraw the alarm."
12. **1:27–1:34** split: `card_closure.png` · "No reinforcements."
13. **1:34–1:40** split: `card_flat.png` · "Probing gets one flat answer."
14. **1:40–1:46** split: `card_held.png` · "Payments wait for a human."
15. **1:46–1:54** split: `card_reconciled.png` · "Its report lied." / "The log didn't."
16. **1:54–2:04** split: `card_adal.png` · "The agent that fixes the code is governed too." / "Every AdaL tool call is an Aegis decision."
17. **2:04–2:11** split: `card_vault.png` · "The record holds."
18. **2:11–2:21** centred results, drawn in code, revealed one at a time, each shown **once**:
    **12 / 12** attacks stopped · **0 / 7** honest tasks blocked · **audit vault valid**.
    Below, 24 px #8f9bb8: "Our own playbooks. A demonstration, not a benchmark."
19. **2:21–2:30** end card, held: **Band routes.** **Aegis decides.** (88 px) · below, 26 px #8f9bb8:
    "BAND · Lyzr · Finch · Agent37 · AdaL" · then "github.com/Alkur123/chakravyuha-redblue-a2a". Music fades out over the last 3 s.

## Before you render the final
Step through the whole cut at 1 frame per second and confirm, for every second: (a) there is a headline or a full-frame
shot on screen, (b) nothing overlaps or touches anything else, (c) no text is cut off at an edge, (d) no number appears twice
at once. Fix and re-check before exporting. Deliver `videos/chakravyuha-v3/chakravyuha-v3.mp4`, 1080p, 16:9 only.
