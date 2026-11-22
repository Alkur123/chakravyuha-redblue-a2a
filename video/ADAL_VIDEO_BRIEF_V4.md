# AdaL video brief v4: teach the idea first, then prove it

Why v4: a blind reviewer scored v3 clarity 5/10. The first 20 seconds said nothing concrete, the Chakravyuha was
never explained, Red/Blue/BAND/Aegis were never introduced, the cards were full of internal jargon, and simple cards
sat too long while dense screens flashed by. v4 fixes all of that with finished frames that already say it plainly.

---

Make a **2:00 launch film, 16:9, 1920x1080, 30 fps, no voiceover**, from `video/assets5/` only. A person will speak
over it live. Calm, premium, precise. Do not add or change any words; every frame already contains its text.

## Layout rules (simple, so nothing can overlap)
- Background #0b0f1a everywhere.
- **Full frames** (`explain_*.png`, `v4_f-*.png`, 3840x2160): show full screen, scaled to 1920x1080.
- **Cards** (`v4_c-*.png`, 2080x1200): show **alone, centred**, scaled to **1456 x 840** (crisp; they are 2x). No headline
  next to them; each card already says what it shows.
- `band_spoof_rejected.png`: centred, scaled to 1500 px wide, with ONE line of text above it (centred, 52 px, weight 800,
  white): "Live in BAND: Red signs a message as Blue." and ONE line below it (34 px, #8f9bb8): "Aegis checks the key. Rejected."
- `warroom_live_run.mp4`: full frame, from its 2-second mark, with ONE label bottom-left (28 px, #8f9bb8):
  "This is a real run, live on Agent37."
- Transitions: 400 ms cross-dissolve between every beat. Motion: a slow push 1.00 to 1.03 on each image. **No blank
  frames, no captions, nothing on screen except the asset and the lines specified above.**
- Music: `score.mp3`, faded in over 1 s, faded out over the last 3 s, low under everything. If it is shorter than 2:00,
  extend it smoothly. A soft low hit on "Stopped.", "It was a trap.", the REJECTED beats and "Caught."

## Sequence (start–end), every second accounted for
1. **0:00–0:06** `explain_e3-problem.png` (AI agents now act on their own)
2. **0:06–0:12** `v4_f-product.png` (what Aegis is, in one sentence)
3. **0:12–0:18** `explain_e1-chakravyuha.png` (what the Chakravyuha is)
4. **0:18–0:22** `explain_e2-abhimanyu.png`
5. **0:22–0:30** `explain_e4-answer.png` (the rings mapped to real checks)
6. **0:30–0:37** `v4_f-cast.png` (Red, Blue, BAND, Aegis)
7. **0:37–0:42** `warroom_live_run.mp4` with its label
8. **0:42–0:48** `v4_c-bug.png`
9. **0:48–0:54** `v4_c-fix.png`
10. **0:54–1:00** `v4_c-adal.png`
11. **1:00–1:05** `v4_c-retry.png` (low hit)
12. **1:05–1:11** `v4_c-decoy.png` (low hit)
13. **1:11–1:17** `band_spoof_rejected.png` with its two lines (low hit)
14. **1:17–1:24** `v4_c-forged.png`
15. **1:24–1:31** `v4_c-trapped.png`
16. **1:31–1:37** `v4_c-money.png`
17. **1:37–1:43** `v4_c-lie.png` (low hit)
18. **1:43–1:47** `v4_c-record.png`
19. **1:47–1:54** `v4_f-results.png`
20. **1:54–2:00** `v4_f-end.png` (held; music fades out)

## Before rendering the final
Step through at 1 frame per second: every second shows one asset fully (or a 400 ms dissolve between two), nothing is
cropped, nothing overlaps, no blank frame. Deliver `videos/chakravyuha-v4/chakravyuha-v4.mp4`, 1080p, 16:9.
