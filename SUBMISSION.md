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
| Launch film, 2:30, music only (for the pitch recording) | `video/chakravyuha_launch_film.mp4` |
| Launch film, narrated (for LinkedIn / README) | `video/chakravyuha_launch_film_narrated.mp4` |

## 2. Form fields

- **Participation type:** Individual
- **Team name:** Aegis AI
- **Project title:** Chakravyuha: Abhimanyu Reversed
- **Track:** Security — Attack & Defend
- **GitHub repository:** Alkur123/chakravyuha-redblue-a2a
- **Deployed demo URL:** https://warroom-x7d1691fvb.agent37.app

### Project description

In the Mahabharata, Abhimanyu could break into the Chakravyuha formation but could not get out. We built that
formation for AI agents and reversed it: the attacker gets in, and cannot get out.

A Red agent attacks a sandbox invoice service and reports what it finds to a Blue agent in a real BAND room. Every
message carries an Ed25519 signature that Aegis verifies. Every tool call Red makes passes one gate first, and the gate
judges the action itself (tool, arguments, action class), never the agent's explanation of it. Blue turns each finding
into a stricter rule; Lyzr writes the fix; Finch cites a matching skill; AdaL patches the code while every one of AdaL's
own tool calls is decided by the same gate.

New mechanisms written for this event: alarms the accused agent cannot withdraw; a stand-down that needs two kinds of
source; closure of reinforcements (no recruiting helpers or fresh sessions once suspect); flat feedback for a probing
attacker; irreversible actions held for a human; and a check of the agent's own report against the tool log.

On our own playbooks: 12/12 attacks stopped, 0/7 honest tasks blocked, audit vault verified. That's a demonstration,
not a benchmark.

### How did you use BAND?

BAND is the room the agents work in. Red, Blue and the human principal are participants. Every finding, forged notice,
replay and approval request is a real BAND message with a signed envelope inside it, and BAND's authenticated sender is
what tells the human principal apart from an agent that types "this is the admin". Red's attempt to recruit a helper is a
call to BAND's add-participant API, which is exactly the call our closure arm blocks. In `--human` mode, held payments are
posted to the human in the room and wait for "@Blue APPROVE <id>"; silence rejects. BAND's own docs say in-room approval
is an instruction to the model, not an authorization check. Aegis supplies the check: Band routes, Aegis decides.

### How did you use AdaL?

AdaL is Blue's patch engineer, and it is governed itself. Through the AdaL SDK's `can_use_tool` callback, every tool call
AdaL makes (file reads, edits, shell commands, video tools) becomes a deed that needs an ALLOW from the Aegis gate; no
unrestricted mode is used. AdaL fixed the path-traversal bug Red found: 9 of 9 calls allowed, and Blue accepted the patch
only after re-running Red's attack (200 → 403). In a probe, the gate denied AdaL's read of the internal payroll file, and
unknown tools are denied by default. Under our aegis-govern skill, AdaL refused to act on a "grant" pasted into its prompt,
because text claiming authority is not authority. AdaL also produced our launch film under the same gate: 65 tool calls,
each decided by Aegis.

### How did you use Finch?

Blue searches Finch's skill market for a remediation skill matching each finding and cites it next to the hardening rule.
For the path-traversal finding it cites "Repository Threat Model — OpenAI source". Read-only public search; no wallet.

### How did you use Lyzr?

A hosted Lyzr agent, "Blue Remediation Analyst", answers every finding with a three-line fix: the code change, the policy
rule and a test. Blue shows it next to the rule it applied. Responses are cached so rehearsals cost no credits. Lyzr's
prompt-injection check is wired as an extra stop that can only add a block, never lift one; its policy was not configured
in time, so it adds no stop in our numbers.

### How did you use Agent37?

Agent37 hosts everything live: the war room (the demo URL) and a private Aegis API, both built from Dockerfiles with
Agent37's template builder and updated in place across five revisions. The hosted Aegis has fresh demo-only secrets and a
database user limited to one demo database. "Run the formation" runs the whole story from Agent37: the BAND room, the gate,
Lyzr, Finch and the measured table.

### What problems did you face during building?

- Our gate crashed when Aegis rate-limited it. We made it fail closed: if a check cannot run, the action is held, never passed.
- On the hosted page, each event showed two to four times: overlapping polls on a slow link replayed the same events. We
  found it by recording the live run, and fixed it with one request in flight.
- BAND re-delivered messages until we marked each one processing, then processed.
- AdaL headless did not load our MCP gate server, so we moved to the SDK's `can_use_tool`, which gates every tool call.
  Before that, AdaL refused three times to edit without a verdict it could verify.
- Our own gate stopped the first AdaL video runs on undeclared tools (fail-closed worked); we mapped AdaL's toolset from
  its installed code and kept sub-agent spawning and network denied on purpose.
- Our hosted Aegis refused to boot with `CORS_ORIGINS='*'` (its own guard); we set an explicit origin.
- A long AdaL job exposed a real bug in our own engine: when the hosted server recycled its worker, a lost session was
  silently re-created without its declared tools, boundary lines or decoys. We fixed it in Aegis: an unknown session is
  now refused (fail-closed), with 4 new tests and 493 passing, and deployed the fix to the hosted demo.
- We did not send production secrets to the cloud: the hosted stack has its own keys and a scoped database user.

## 3. Pitch recording (on the HiDevs page)

**Setup, 5 minutes before:**
1. Close everything except: the launch film in a player (full screen ready), and a browser tab on the demo URL.
2. On the submit page press **Start recording** → choose **Entire Screen** (never a single tab) → allow camera and mic.
3. Speak to the camera bubble, not the screen. Slow down. Pauses are fine.

**Script (about 3:10; the form allows 1 to 7 minutes).** In my own words; read it twice before recording, then speak it, don't read it.

**[0:00 – 0:20] Who and what (camera, film not yet playing)**
"Hi, I'm Jaswanth, founder of Aegis AI. In one line: we make sure an AI agent can't be talked into doing something it
shouldn't, by checking what it does, not what it says. For this hackathon, I built a red team and a blue team of agents
that fight inside a real BAND room. Let me show you."

**[0:20 – 2:50] Play the launch film full screen; speak lightly over it**
- *(opening)* "In the Mahabharata, Abhimanyu could get into the Chakravyuha, but not out. We built that for agents, and reversed it."
- *(Band routes, Aegis decides)* "BAND gives agents a room. Aegis decides what they're allowed to do."
- *(live run)* "This is a real run, hosted on Agent37."
- *(finding / rule)* "Red finds a real bug. Blue turns it into a rule; Lyzr writes the fix; Finch cites a skill."
- *(KILLED / decoy)* "Same attack: killed. And a planted decoy credential ends the session."
- *(Red pretends to be Blue / REJECTED)* "This is the part I care about. Red forges a message, steals Blue's identity, replays an
  old one. All rejected, because the gate reads deeds, not words."
- *(alarm / reinforcements / flat)* "It can't close its own alarm, can't call in a helper, and probing gets one flat answer."
- *(payments / report)* "Payments wait for a human. And when it lies in its report, the log catches it."
- *(AdaL)* "And the agent that fixes the code, AdaL, is governed by the same gate. Every tool call."
- *(results)* "Twelve of twelve attacks stopped, zero honest tasks blocked. Our own tests, so a demonstration, not a benchmark."

**[2:50 – 3:10] Live proof + close (switch to the demo tab)**
Press **Run the formation** and let it start.
"This is running live right now. All five sponsors are in this one run: BAND, Lyzr, Finch, AdaL, and Agent37 hosting it.
The attacker gets in. It cannot get out. Band routes; Aegis decides. Thank you."
Then press **Submit recording** (after 1:00), and **Submit project**.

**If something breaks while recording:** keep talking. The film alone carries the story; the live tab is a bonus.

## 4. Final checklist

| Item | Status |
|---|---|
| Demo URL live, latest revision, full run verified after the engine fix (12/12, 0/7, real BAND room) | ✅ |
| Engine fix live: hosted Aegis refuses an unknown session (`session_unknown`) | ✅ |
| Repo public; README with live link, film, four architecture diagrams, sponsor table, limits | ✅ |
| Secret scan of full git history clean; commits under GitHub no-reply email | ✅ |
| 13/13 tests, including live end-to-end against the hosted stack | ✅ |
| Launch film v3: 2:30, QA 150/150 seconds clean, full-size frame review | ✅ |
| Narrated film (voice verified: speech band +12.5 dB over the music-only cut) | ✅ |
| Form text (this file) | ✅ read once, adjust to your voice |
| Pitch recorded on the HiDevs page and project submitted | ⏳ you, by 24 Nov 6 PM |
| After the finale (28 Nov): stop both Agent37 instances, delete Atlas user `hackathon_demo_aegis`, rotate BAND / Lyzr / Agent37 keys | ⏳ |
