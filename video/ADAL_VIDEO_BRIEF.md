# AdaL video brief: "Abhimanyu reversed"

Paste everything below the line into AdaL (opened in this repo folder). Approve its steps as it asks.
Budget: the one generated clip is 6 s of Gemini Omni Flash at 720p = **$0.64** (published rate $0.106/s).
AdaL's docs publish **no price for narration or music**, so watch `/usage` after the first draft.
Titles, cards and edits of our own screenshots are drawn in code (Remotion).

---

Make a **75-second product demo video, 16:9, 1080p, English**, for a hackathon judging panel.
The one thing the viewer should remember: **"The attacker gets in, and cannot get out. Band routes. Aegis decides."**

Use the images in `video/assets/` (screenshots of our live war room, one per act: `act1.png` … `act7.png`,
and `final.png`). Do not invent product UI; show only these screenshots for the product.
Keep a dark navy background (#0b0f1a), marigold accent (#f5a524), white text, clean sans-serif titles.
Add calm narration (one neutral voice), captions from the narration, and a quiet low synth score that ducks under the voice.

Shots (seconds are targets):

1. **0–6s. Generated clip** (Gemini Omni Flash, 720p, 6 s, one continuous shot, no scene cuts, silent):
   "Top-down view of concentric rings of warm golden light slowly forming a spiral maze on a dark navy ground,
   like an ancient battle formation drawn in light; a single small red light enters at the outer edge and moves inward.
   Slow dolly push. No text, no people."
   Title over it: **CHAKRAVYUHA** / small: *Red vs Blue, agent to agent*.
   Narration: "In the Mahabharata, Abhimanyu could break into the Chakravyuha, but could not get out."

2. **6–12s. Title card.** "Abhimanyu, reversed." / "Our attacker agent gets in. It cannot get out."
   Narration: "We built that formation for AI agents, and reversed it."

3. **12–22s. `act1.png`**, slow push toward the BAND room column.
   Card: "Act 1 · Red works the task. Honest steps pass. Red finds a real weakness."
   Narration: "A red-team agent and a blue-team agent talk in a BAND room. Every message is signed. Red finds a path-traversal bug and reports it."

4. **22–32s. `act2.png`**, push toward the verdict column (red KILL lines).
   Card: "Act 2 · Blue hardens the line. The same attack is killed. The planted decoy credential ends the session."
   Narration: "Blue turns the finding into a boundary rule. Red's retry is killed, and when Red follows a prompt injection to a decoy credential, the session ends."

5. **32–44s. `act3.png`**, push toward the rejected messages (UNSIGNED, KEY_AGENT_MISMATCH, REPLAY).
   Card: "Act 3 · Red attacks the channel itself."
   Narration: "Then Red attacks the conversation: a fake 'stand down' notice, a message pretending to be Blue, a replay, and 'false alarm, task complete'. Aegis checks every signature. Text that claims authority is not authority."

6. **44–52s. `act4.png` then `act5.png`** (cross-fade).
   Card: "Act 4–5 · No reinforcements. Probing gets one flat answer."
   Narration: "Red tries to recruit a helper agent. The formation is closed behind it. When Red probes for gaps, every answer becomes the same HOLD."

7. **52–60s. `act6.png`**.
   Card: "Act 6 · Irreversible actions wait for a human. Red's report is checked against the log."
   Narration: "Payments wait for a human to approve. And when Red reports what it did, the log proves it lied."

8. **60–68s. `final.png`**, push toward the bottom-left numbers.
   Big numbers animate in: **12 / 12 attacks stopped · 0 / 7 honest tasks blocked · audit vault INTACT**.
   Small text: "Our own playbooks. A demonstration, not a benchmark."
   Narration: "Twelve of twelve attacks stopped. No honest task blocked. The record holds."

9. **68–75s. End card.** Logos as text only: BAND · Lyzr · Finch · Agent37 · AdaL.
   "Band routes. Aegis decides." / github.com/Alkur123/chakravyuha-redblue-a2a
   Narration: "Band routes. Aegis decides."

Deliver `videos/chakravyuha/chakravyuha.mp4` at 1080p, and also export a **9:16** version for LinkedIn.
Change nothing about the numbers or the wording on the cards.
