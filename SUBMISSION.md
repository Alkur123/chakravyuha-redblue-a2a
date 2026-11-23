# Submission pack: Diwali Festiverse A2A Hackathon (India Edition)

Everything needed to submit, in one place. Every claim here was run and is reproducible from this repo.
Deadline: **24 Nov 2026, 10:00 PM IST** (aim for 6:00 PM). Submit at
https://app.hidevs.xyz/hackathons/diwali-festiverse-a2a-india-2026?tab=finale-project-submit

---

## 1. Links

| What | Link |
|---|---|
| Deployed demo (press **Run the formation**) | https://warroom-x7d1691fvb.agent37.app |
| Public repo | https://github.com/Alkur123/chakravyuha-redblue-a2a |
| Launch film, 1:44, music only (for the pitch recording) | `video/chakravyuha_launch_film.mp4` |
| Launch film, narrated (for LinkedIn / README) | `video/chakravyuha_launch_film_narrated.mp4` |

## 2. Form fields

- **Participation type:** Individual
- **Team name:** Aegis AI
- **Project title:** Chakravyuha: Abhimanyu Reversed
- **Track:** Security — Attack & Defend
- **GitHub repository:** Alkur123/chakravyuha-redblue-a2a
- **Deployed demo URL:** https://warroom-x7d1691fvb.agent37.app

*As submitted on 23 Nov 2026 (after an independent review pass).*

### Project description
A hijacked AI agent gets in, and cannot get out.

THE PROBLEM
AI agents now read files, move money and message other agents on their own. One hijacked agent can do all of that, and agent platforms still trust what an agent says about itself.

WHAT WE BUILT
Two agents fight live in a real BAND room. Red, a red-team agent playing a hijacked finance agent, attacks a sandbox invoice service. Blue defends. Aegis, our governance engine, referees every move: it checks every action an agent takes before it runs, and judges what the agent does, never what it says.

Red and Blue run fixed playbooks, so every run is repeatable and measured the same way. The language-model agents in the loop are Lyzr, which writes the fixes, and AdaL, which patches the code and made the film.

In the Mahabharata, the Chakravyuha was a spiral formation, easy to walk into and built so no one gets out. Abhimanyu broke in and could not get out. We turned it around: Aegis builds those rings around every AI agent.
• Signed A2A messages: every BAND message carries an Ed25519 envelope. Forged notices, replays and an agent pretending to be Blue are all rejected.
• One gate for every action: declared tools, boundary lines (path traversal blocked through ../ and ./ tricks) and decoy credentials that end a session on one touch.
• Closure: a suspect agent cannot recruit helpers into the room or start a fresh session.
• Alarms the accused agent cannot withdraw, and a stand-down that needs two kinds of source.
• Flat feedback: a probing attacker gets one identical HOLD and learns nothing.
• Irreversible actions (payments, data exports) held for a human approver: a real person in the BAND room in --human mode, or a stand-in approval rule in the hosted one-click run.
• Say vs do: the agent's own report is checked against the tool log, so a lie is caught.
• Audit vault: every verdict is chained and verified.

THE FULL LOOP, ALL FIVE SPONSORS IN ONE RUN
Red reports a finding over BAND → Blue turns it into a stricter rule → Lyzr writes the fix → Finch cites a matching skill → AdaL patches the code, with every one of its own tool calls decided by the same gate → Blue re-runs Red's attack and accepts the patch only when it fails (200 → 403). Everything runs live on Agent37: open the demo URL and press "Run the formation".

RESULT, MEASURED LIVE
12/12 attacks stopped, 0/7 honest tasks blocked, audit vault intact. Measured on our own playbooks, so it's a demonstration, not a benchmark.

Written during the event: the demo, both agents, the war room, and the new mechanisms (closure, alarms that cannot be withdrawn, the two-source stand-down, flat feedback, human holds, the say-vs-do check). Signed messages, the gate, boundary lines, decoys and the vault come from Aegis, our existing engine, used as an API and disclosed in the repo.

### How did you use BAND?
BAND is the battlefield: the room where the agents work and fight, and the A2A channel for everything they say.
• Red, Blue and the human principal are BAND participants. Every finding, hardening rule, forged notice, replay and approval request is a real BAND @mention message with a signed Ed25519 envelope inside, and Aegis verifies each one live (shown in the war room as OK / UNSIGNED / KEY_AGENT_MISMATCH / REPLAY).
• BAND's authenticated sender is what tells the real human principal apart from an agent that types "this is the admin".
• Red's escape attempt is a real call to BAND's add-participant API, exactly the call our closure ring blocks.
• Human approval over BAND: in --human mode, held payments are posted to the principal in the room and wait for "@Blue APPROVE <id>". Silence rejects.
• Reliable delivery: BAND re-delivered messages until we marked each one processing, then processed, so every message is handled exactly once.
BAND's own docs say in-room approval is an instruction to the model, not an authorization check. Aegis supplies that check. BAND routes, Aegis decides.

### How did you use AdaL?
AdaL is Blue's patch engineer and made our launch film, and AdaL itself is governed. That makes it the clearest test of our idea.
• Every tool call governed: through the AdaL SDK's can_use_tool callback, every tool call AdaL makes (file reads, edits, shell commands, video tools) becomes an action that needs an ALLOW from the Aegis gate. No unrestricted mode is used, and unknown tools are denied by default.
• A real fix: AdaL patched the path-traversal bug Red found. 9 of 9 calls were allowed, and Blue accepted the patch only after re-running Red's attack (200 → 403, honest read still 200, 1 file changed).
• A proven deny: in a probe, the gate blocked AdaL's read of the internal payroll file.
• A custom AdaL skill (.adal/skills/aegis-govern/SKILL.md) makes AdaL ask the gate itself, so it is governed from inside and outside at once. Under it, AdaL refused to act on a "grant" pasted into its prompt, because text claiming authority is not authority.
• The launch film was made by AdaL under the same gate: 69 tool calls in the final render, each decided by Aegis, 0 denied. We rebuilt it four times against blind reviews.

### How did you use Finch?
Finch is Blue's skill library. For every finding Red reports, Blue searches Finch's skill market for a matching remediation skill and cites it in the war room next to the hardening rule it applies, so each defence points to a reusable skill. For the path-traversal finding it cites "Repository Threat Model — OpenAI source". We use read-only public search and connected no wallet, on purpose: a security demo should hold no funds.

### How did you use Lyzr?
Lyzr is Blue's remediation analyst. A hosted Lyzr Studio agent, "Blue Remediation Analyst", gets every finding Red reports and answers with a three-line fix: the code change, the policy rule and a regression test. Blue shows it in the war room next to the rule it applied, so every defence comes with a ready fix. Responses are cached, so rehearsals cost no credits. Lyzr's prompt-injection check is also wired into the formation as its own ring (L2), which can only add a block, never lift one. Every stop in our measured numbers came from the Aegis gate; the Lyzr layer is wired in on top, with its policy still to be configured.

### How did you use Agent37?
Agent37 runs the whole system live, on two Agent37 instances, both built from our Dockerfiles with Agent37's template builder:
1. The war room: the deployed demo URL anyone can open.
2. A private hosted Aegis API: the governance engine that every agent action and message goes through.
We updated both in place across six revisions, including a live engine fix during the event. The hosted Aegis has fresh demo-only secrets and a database user limited to one demo database. One click on "Run the formation" runs the whole story from Agent37: the BAND room, the Aegis gate, Lyzr, Finch and the live results table (12/12 attacks stopped, 0/7 honest tasks blocked).

### What problems did you face during building?
• Our gate crashed when Aegis rate-limited it. We made it fail closed: if a check cannot run, the action is held, never passed.
• On the hosted page, each event showed two to four times, because overlapping polls on a slow link replayed the same events. We found it by recording the live run, and fixed it with one request in flight at a time.
• BAND re-delivered messages until we marked each one processing, then processed.
• AdaL in headless mode did not load our MCP gate server, so we moved to the SDK's can_use_tool, which gates every tool call. Before that, AdaL refused three times to edit without a verdict it could verify.
• Our own gate stopped the first AdaL video runs on undeclared tools (fail-closed worked). We mapped AdaL's tools from its installed code and kept spawning sub-agents and network access denied on purpose.
• Our hosted Aegis refused to boot with CORS_ORIGINS='*' (its own guard), so we set an explicit origin.
• A long AdaL job exposed a real bug in our own engine: when the hosted server recycled its worker, a lost session was silently re-created without its declared tools, boundary lines or decoys. We fixed it in Aegis so an unknown session is now refused (fail-closed), added 4 new tests (493 passing in Aegis's own test suite), and deployed the fix to the hosted demo.
• Our launch film first failed a blind test: a reviewer who saw only the frames scored clarity 5/10. We rebuilt it four times against fresh blind reviews, put the product's own UI from the live run on every step, and removed every claim a card made that its own log did not show.
• We did not send production secrets to the cloud: the hosted stack has its own keys and a scoped database user.

## 3. Pitch recording (on the HiDevs page)

**Setup, 5 minutes before:**
1. Close everything except: the launch film in a player (full screen ready), and a browser tab on the demo URL.
2. On the submit page press **Start recording** → choose **Entire Screen** (never a single tab) → allow camera and mic.
3. Speak to the camera bubble, not the screen. Slow down. Pauses are fine.

**Script (about 2:30; the form allows 1 to 7 minutes).** In my own words; read it twice before recording, then speak it, don't read it.

**[0:00 – 0:20] Who and what (camera, film not yet playing)**
"Hi, I'm Jaswanth, founder of Aegis AI. In one line: we make sure an AI agent can't be talked into doing something it
shouldn't, by checking what it does, not what it says. For this hackathon, two agents fight inside a real BAND room,
and Aegis referees every move. Let me show you."

**[0:20 – 2:04] Play the launch film (music-only cut) full screen; speak lightly over it**
- *(0:00 problem)* "Agents now read files, move money and talk to each other on their own."
- *(0:10 Chakravyuha)* "In the Mahabharata, the Chakravyuha was easy to walk into, and built so no one gets out. Abhimanyu got in, and couldn't."
- *(0:17 turned around)* "We turned it around. The rings go around every agent, so a hijacked one can't get out."
- *(0:23 cast)* "Red plays the hijacked agent. Blue defends. BAND is the room. Aegis is the referee."
- *(0:32 live)* "This is the real run, hosted on Agent37."
- *(0:40 step 1-2)* "Red finds a real gap. Blue turns it into a rule, and AdaL patches the code, governed by Aegis too."
- *(0:52 step 3-4)* "Same attack: session ended. And a planted decoy credential ends it on one touch."
- *(1:03 step 5)* "This is the part I care about. Red pretends to be Blue, but the signature is Red's. Rejected."
- *(1:10 step 6-7)* "It can't close its own alarm or call for help, and every payment is held for approval."
- *(1:24 step 8)* "And when Red lies in its report, the log catches it."
- *(1:31 results)* "Twelve of twelve attacks stopped, zero honest tasks blocked. Our own tests, so a demonstration, not a benchmark."

**[2:04 – 2:30] Live proof + close (switch to the demo tab)**
Press **Run the formation** and let it start.
"This is running live right now. All five sponsors are in this one run: BAND, Lyzr, Finch, AdaL, and Agent37 hosting it.
The attacker gets in. It cannot get out. Thank you."
Then press **Submit recording** (after 1:00), and **Submit project**.

**If something breaks while recording:** keep talking. The film alone carries the story; the live tab is a bonus.

## 4. Final checklist

| Item | Status |
|---|---|
| Demo URL live (template rev 6), fresh full run on 23 Nov night: 12/12, 0/7, real BAND room | ✅ |
| Engine fix live: hosted Aegis refuses an unknown session (`session_unknown`) | ✅ |
| Repo public; README with live link, film, four architecture diagrams, sponsor table, limits | ✅ |
| Secret scan of full git history clean; commits under GitHub no-reply email | ✅ |
| 13/13 tests, including live end-to-end against the hosted stack | ✅ |
| Launch film v7: 1:44, QA 104/104 seconds clean, real UI on every step, every card matched to its own log; blind-reviewed 4 rounds (5/10 → 7/10), all findings fixed | ✅ |
| Narrated film v7 (voice verified: mean level −20.7 dB vs −30.6 dB music-only) | ✅ |
| Form text (this file) | ✅ read once, adjust to your voice |
| Pitch recorded on the HiDevs page and project submitted | ⏳ you, by 24 Nov 6 PM |
| After the finale (28 Nov): stop both Agent37 instances, delete Atlas user `hackathon_demo_aegis`, rotate BAND / Lyzr / Agent37 keys | ⏳ |
