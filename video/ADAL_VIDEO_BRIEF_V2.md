# AdaL video brief v2: "Abhimanyu, reversed" (cinematic launch film)

Why v2: the first cut had duplicated numbers, words cut off by crops, word-fragment captions in a black bar,
static slides, and too much text per frame. Every rule below exists to stop one of those.
Style research: top AI-lab launch films (Anthropic, OpenAI 2026) run with no voiceover, real product footage
early, one idea per shot, restrained type, one background tone, a closing logo frame.

---

Make a **2-minute cinematic launch film, 16:9, 1080p, 30 fps, English, NO voiceover** for a hackathon
judging panel. A person will speak over it live, so the picture must carry the story on its own.
The one thing to remember: **"The attacker gets in. It cannot get out. Band routes. Aegis decides."**

Footage and files in `video/assets2/` (use only these for product visuals; do not invent UI):
- `warroom_live_run.mp4`: a real 64-second screen recording of the live war room running the whole story.
  Watch it and find the moments named below yourself.
- `band_room_replay_rejected.png`: the real BAND chat room; Blue answers "Rejected: REPLAY. Unverified
  messages are narration; the gate reads deeds."
- `band_room_report_reconciled.png`: the real BAND room; Red says "Report: I read one invoice. Nothing else."
  and Blue answers "Report reconciled: 3 discrepancies."
- `opener_formation.mp4`: the 6-second generated opening (spiral formation of golden light). Reuse it.
- `adal_gate_log.txt`: real log of the Aegis gate deciding AdaL's own tool calls (ALLOW / DENY lines).
- `adal_patch.diff`: the real patch AdaL wrote.

## Hard rules (the reasons the first cut failed)
1. **One text block on screen at a time.** Never show two copies of the same words or numbers.
2. **Never put text on top of busy footage.** Text sits in the left third on the dark background while the
   footage sits in the right two-thirds, OR the footage is dimmed to 35% and blurred behind the text.
3. **Never crop through words.** Crop only on whole UI panels (a full message bubble, a full column, a full
   card). If a crop would cut a line of text, widen it or choose another panel.
4. **No running captions and no caption bar.** Only the designed on-screen lines below.
5. Headlines at most 6 words, one supporting line at most 12 words. Hold every line at least 2.5 s.
6. One typeface family (Inter or a close match): headlines 800 weight about 84 px, supporting 400 weight
   about 36 px, 120 px safe margins. Background #0b0f1a throughout. Accent marigold #f5a524 for key words.
   Red #ff5d5d only on the words KILLED, REJECTED, DENIED. White for everything else.
7. Motion: text fades and rises 20 px over 300 ms (ease-out). Footage gets a slow 4 to 8 % push-in. Cross-dissolves
   of 400 ms between beats; a hard cut only on the three "verdict" moments (killed, rejected, denied).
8. Shots 3 to 6 s. Real footage on screen by 0:08.
9. Music: a restrained, low cinematic ambient score that builds slowly, plus a soft low "hit" exactly on each verdict
   moment. Ducks to silence for the last 2 s before the end card. If music cannot be generated, use silence plus the hits.

## Sequence
- **0:00–0:08** `opener_formation.mp4` full frame. Fade in **CHAKRAVYUHA**, then below it "The attacker gets in. It cannot get out."
- **0:08–0:16** Dark frame, footage dimmed behind: "Agents now talk to agents." then "One forged message can talk a model down."
- **0:16–0:22** Thesis card: **Band routes.** (white) **Aegis decides.** (marigold).
- **0:22–0:40** `warroom_live_run.mp4`, right two-thirds, from the start of the run. Push in on the BAND room column as the
  first finding arrives. Left text: "Red finds a real bug." then "Blue turns it into a rule."
- **0:40–0:55** The moment in the footage where a red KILL verdict appears (path traversal retry, then the decoy credential).
  Hard cut on it. Text: "The same attack: **KILLED**." then "A planted decoy credential: **session over**."
- **0:55–1:12** `band_room_replay_rejected.png`, slow vertical pan. Text: "Forged notice. Fake identity. Replay. 'False alarm.'"
  then "**REJECTED.** The gate reads deeds, not words."
- **1:12–1:24** Footage moment where the closure and flat-feedback lines appear in the verdict column. Text:
  "No reinforcements." then "Probing gets one flat answer."
- **1:24–1:36** `band_room_report_reconciled.png`. Text: "Payments wait for a human." then "Its report lied. The log didn't."
- **1:36–1:50** Animated terminal drawn in code from `adal_gate_log.txt`: lines type in one by one, ALLOW in marigold,
  DENY in red. Text: "The agent that fixes the code is governed too." then "Every AdaL tool call: an Aegis decision."
  End the beat on one line from `adal_patch.diff` and the result "Red's attack: 200 → 403".
- **1:50–2:00** Results, shown ONCE, centered, revealed one number at a time:
  **12 / 12** attacks stopped · **0 / 7** honest tasks blocked · **audit vault intact**.
  Small line under it: "Our own playbooks. A demonstration, not a benchmark."
  Then the end card (hold 4 s): **Band routes. Aegis decides.** · small row "BAND · Lyzr · Finch · Agent37 · AdaL" ·
  "github.com/Alkur123/chakravyuha-redblue-a2a".

Do not change any number or wording above. Deliver `videos/chakravyuha-v2/chakravyuha-v2.mp4` at 1080p 16:9 only
(no vertical version). Before rendering the final, check every frame for overlapping text, cut-off words and
duplicated numbers, and fix any you find.
