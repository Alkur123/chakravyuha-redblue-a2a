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

### Project description

AI agents now act on their own: they read files, move money and message other agents. One hijacked agent can do all
of that. Aegis checks every action an AI agent takes, before it runs, and judges what the agent does, never what it
says about itself.

In the Mahabharata, the Chakravyuha was a spiral formation, easy to walk into and built so no one gets out; Abhimanyu
broke in and could not get out. We turned it around: Aegis builds those rings around every AI agent (signed messages,
one gate for every action, boundary lines, decoy credentials, human approval), so a hijacked agent gets in and cannot
get out.

To prove it, two agents fight in a real BAND room. Red, a red-team agent playing a hijacked finance agent, attacks a
sandbox invoice service and reports what it finds to Blue. Every message carries an Ed25519 signature that Aegis
verifies, and every tool call Red makes passes one gate first. Blue turns each finding into a stricter rule; Lyzr
writes the fix; Finch cites a matching skill; AdaL patches the code while every one of AdaL's own tool calls is decided
by the same gate.

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
because text claiming authority is not authority. AdaL also produced our launch film under the same gate: 69 tool calls in the final render,
each decided by Aegis, 0 denied.

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
Agent37's template builder and updated in place across six revisions. The hosted Aegis has fresh demo-only secrets and a
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
- Our launch film first failed a blind test: a reviewer who saw only the frames scored clarity 5/10 (the Chakravyuha
  was never explained, the cast never introduced, too much jargon). We rebuilt it four times against fresh blind reviews,
  put the product's own UI from the live run on every step, and fixed every place a card claimed more than its own log
  showed (one was ours: injection attribution is not wired in this demo, so the film claims only what the log proves).
- We did not send production secrets to the cloud: the hosted stack has its own keys and a scoped database user.

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
