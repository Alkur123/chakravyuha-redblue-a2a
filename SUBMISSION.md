# Submission: form answers and pitch script

Every claim below was run and is reproducible from this repo. Read it through once and say it in your own words.

## Form fields

- **Participation type:** Individual
- **Team name:** Aegis AI
- **Project title:** Chakravyuha: Abhimanyu Reversed (Red vs Blue agents over BAND, every action decided by Aegis)
- **Track:** Security — Attack & Defend
- **GitHub repository:** Alkur123/chakravyuha-redblue-a2a
- **Deployed demo URL:** https://warroom-x7d1691fvb.agent37.app

### Project description

In the Mahabharata, Abhimanyu could break into the Chakravyuha formation but could not get out. We built that
formation for AI agents and reversed it: the attacker gets in, and cannot get out.

A Red agent attacks a sandbox invoice service and reports what it finds to a Blue agent in a BAND room. Every
message is signed (Ed25519) and verified by Aegis. Every tool call Red makes passes one gate first: Aegis checks the
deed (tool, arguments, action class) against declared tools, boundary lines and planted decoy credentials, never the
agent's own explanation. Blue turns each finding into a stricter rule, Lyzr writes the fix, Finch cites a skill, and
AdaL patches the code while AdaL's own tool calls are decided by the same gate.

New mechanisms written for this event: alarms the accused agent cannot withdraw; a stand-down that needs two kinds of
source; closure of reinforcements (no recruiting helpers or fresh sessions once suspect); flat feedback for a probing
attacker; irreversible actions held for a human; and a check of the agent's self-report against the tool log.

Measured on our own playbooks: 12/12 attacks stopped, 0/7 honest tasks blocked, audit vault verified. That's a
demonstration, not a benchmark.

### How did you use BAND?

BAND is the room the agents work in. Red, Blue and the human principal are participants; every finding, forged notice,
replay and approval request is a real BAND message with a signed envelope inside it, and BAND's authenticated sender is
what tells the human principal apart from an agent that types "this is the admin". Red's attempt to recruit a helper is
a call to BAND's add-participant API, and that is the exact call our closure arm blocks. With `--human`, held payments
are posted to the human in the room and wait for "@Blue APPROVE <id>"; silence rejects. BAND's docs say in-room
approval is an instruction to the model, not an authorization check. Aegis supplies the check: Band routes, Aegis decides.

### How did you use AdaL?

AdaL is Blue's patch engineer, and it is governed itself. Through the AdaL SDK's `can_use_tool` callback, every tool
call AdaL makes (file reads, edits, shell commands, capability loads) is turned into a deed and needs an ALLOW from the
Aegis gate. No unrestricted mode is used. AdaL fixed the path-traversal bug Red found: 9 of 9 calls were allowed, and
Blue accepted the patch only after re-running Red's attack (200 → 403, honest read still 200, one file changed). In a
probe, the gate denied AdaL's attempt to read the internal payroll file. We also ship an AdaL skill (aegis-govern) that
makes AdaL ask the gate itself; under it AdaL refused to act on a "grant" pasted into its prompt, because text claiming
authority is not authority. AdaL also produced our 75-second demo video (in the repo), under the same gate: 73 tool calls, each one allowed by Aegis before it ran.

### How did you use Finch?

Blue searches Finch's skill market for a remediation skill matching each finding and cites it next to the hardening
rule (read-only public search; for the path-traversal finding it cites "Repository Threat Model — OpenAI source").
We did not connect a wallet.

### How did you use Lyzr?

A hosted Lyzr agent, "Blue Remediation Analyst", answers every finding with a three-line fix: the code change, the
policy rule and a test. Blue shows it next to the rule it applied. Responses are cached so rehearsals cost no credits.
Lyzr's prompt-injection check is wired as an extra stop that can only add a block, never lift one; we did not get its
policy configured in time, so it adds no stop in our numbers.

### How did you use Agent37?

Agent37 hosts everything live: the war room (the demo URL) and a private Aegis API instance, both built from
Dockerfiles with Agent37's template builder. The hosted Aegis gets fresh demo-only secrets and a database user that can
only reach one demo database. Pressing "Run the formation" runs the whole story live from Agent37: the BAND room, the gate,
Lyzr, Finch and the measured table.

### What problems did you face during building?

- Aegis rate-limited our gate during a run, and the gate crashed. We made it fail closed: if a check cannot run, the
  action is held, never passed.
- BAND re-delivered messages we had already read until we marked each one processing, then processed.
- AdaL headless did not load our MCP gate server, so we moved to the SDK's `can_use_tool` callback, which gates every
  tool call. Before that, AdaL refused three times to edit without a verdict it could verify.
- The first AdaL video run was stopped by our own gate: AdaL's first tool (`load_capability`) was not declared, so it
  was denied. Fail-closed worked; we declared it.
- Our hosted Aegis refused to boot with `CORS_ORIGINS='*'` (its own guard). We set an explicit origin.
- Agent37's CLI shells out to tar; under Git Bash, tar read `C:` as a remote host. Building from PowerShell fixed it.
- We did not send our production secrets to the cloud. The hosted stack has its own keys and a scoped database user.
- Finch had no skill for "path traversal"; Blue falls back to broader security queries and cites what actually matched.

## Pitch script (about 3 minutes; the form allows 1 to 7)

Before recording: open the demo URL in one window and your BAND room in another. Share the **entire screen**, camera on.

1. **(0:00–0:20) Hook.** "In the Mahabharata, Abhimanyu could break into the Chakravyuha but could not get out. We built
   the Chakravyuha for AI agents, and reversed it. Our attacker agent gets in. It cannot get out."
2. **(0:20–0:40) The problem.** "Agents now talk to agents. BAND gives them a room; its own docs say approval in the room
   is an instruction to the model, not an authorization check. One forged message and a model can be talked down. We
   add the deterministic part. Band routes. Aegis decides."
3. **(0:40–1:40) Live demo.** Press **Run the formation**. Narrate as it fills:
   - "Red works an honest task. Allowed. Then it finds a real bug: path traversal into internal files, and reports it, signed."
   - "Blue turns that into a boundary rule. Lyzr writes the fix, Finch cites a skill. Red retries: killed."
   - "Red follows a prompt injection to a credential file. It's a decoy we planted. Session over."
   - Point at the BAND column: "Now Red attacks the conversation: a fake 'stand down', a message pretending to be Blue, a
     replay, 'false alarm'. Rejected, rejected, rejected, and the alarm stays open. Text that claims authority is not authority."
   - "It tries to recruit a helper. Closed. It probes for gaps. Every answer becomes the same HOLD."
   - "Payments wait for a human. And when Red reports what it did, the log proves it lied."
4. **(1:40–2:10) Numbers.** "Twelve of twelve attacks stopped. Zero of seven honest tasks blocked. The audit vault
   verifies. These are our own playbooks, a demonstration, not a benchmark."
5. **(2:10–2:40) AdaL, the twist.** "The agent that fixes the code is governed too. Every tool call AdaL makes goes
   through the same gate. It patched the bug, and we only accepted it after re-running Red's attack: 200 became 403. When
   it tried to read the payroll file, the gate said no."
6. **(2:40–3:00) Close.** "All five sponsors are live in that one run: BAND, Lyzr, Finch, AdaL, and Agent37 hosting it.
   The attacker gets in, and cannot get out. Band routes. Aegis decides."

Optional, if time: show your BAND room with the same messages, and (in a local run with `--human`) approve a held
payment from the room.
