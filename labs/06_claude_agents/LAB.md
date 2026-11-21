# Lab 06 — Build a CSV analyst four ways

**Time:** 25 minutes in class, plus an optional take-home
**You need:** a Claude account that includes Claude Code (a paid plan, or an API key from
your instructor), and either Claude Code with Python 3.10+ on your laptop, or a login to
the class VM
**Goes with:** the lecture deck *From Chat to Agent with Claude*

You'll give Claude the same job (answering questions about `sample.csv`) four ways, and
see what each one changes. The steps are the same on your laptop and on the class VM.

| Step | Way | What you'll see |
|---|---|---|
| 1 | Built-in tools | Claude picks its own steps |
| 2 | Skill | Instructions Claude loads when they're relevant |
| 3 | Subagent | A narrow agent whose tool list is a hard limit |
| 4 | MCP server | Tools you write, usable from any MCP app |
| 5 | Safety | Which layers hold, and which can be argued with |

## Setup (before class, 5 minutes)

Pick one option.

### Option A: your laptop

You need Claude Code installed ([setup guide](https://code.claude.com/docs/en/setup)) and
Python 3.10+.

```bash
cd labs/06_claude_agents
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then start Claude Code in this folder:

```bash
claude
```

### Option B: the class VM

No install needed: your instructor gives you a username, a password and the VM's
address. Everything is already set up there.

1. Log in from a terminal (Terminal on macOS, PowerShell on Windows):

   ```bash
   ssh YOUR_USERNAME@VM_ADDRESS
   ```

   The first time, you'll be asked to choose a new password, then logged out. Log in again
   with the new one.

2. You start in `~/lab` with the Python environment active. Start Claude Code:

   ```bash
   claude
   ```

3. Sign in with your own account. There's no browser on the VM, so copy the login URL
   (press `c`, or copy it from the screen), open it on your laptop, sign in, and paste the
   code it shows back into the terminal. If your instructor gave you an API key instead,
   run `export ANTHROPIC_API_KEY=...` before `claude`, and approve it when asked.

Everywhere this guide says "this folder", on the VM that means `~/lab`. To edit files, use
`nano FILE`, ask Claude to write them, or connect VS Code with the Remote-SSH extension.

### Either way

Claude Code reads `CLAUDE.md` (the project's memory) and `.claude/settings.json` (the
permission rules) when it starts. Open both: they're short.

---

## Step 1 — Built-in tools (3 min)

Ask:

> Which department has the highest average salary, and who is the most experienced employee?

**Watch for:** which tools Claude uses (Read? Bash with Python?), in what order, and
whether it asks your permission. Nobody told it which steps to take.

**Answer in one line:** what did Claude do that a script couldn't, and what did it do that
you'd want to check?

## Step 2 — A skill (5 min)

A skill is a folder with a `SKILL.md` file: instructions plus a `description` that tells
Claude *when* to use them. Claude reads only the description up front, and loads the rest
when a request matches. `starter/skill.md` is a plain prompt file; you'll turn it into a skill.

1. Create `.claude/skills/code-reviewer/SKILL.md`. Start it with this header, then paste
   the contents of `starter/skill.md` under it:

   ```markdown
   ---
   name: code-reviewer
   description: Reviews Python code for bugs, security problems and readability, and gives a verdict. Use when the user asks to review, critique or check Python code or a .py file.
   ---
   ```

2. In Claude Code, type `/clear` (to start a fresh conversation), then ask:

   > Can you check primes.py?

   You didn't name the skill. Did the answer come back in **Issues / Suggestions / Verdict**?

3. Change one rule in `SKILL.md` (for example, "Suggestions: at most one") and ask again.
   The change applies on the next use, with nothing to restart.

**Answer in one line:** what in the `description` made Claude pick the skill?

## Step 3 — A subagent (5 min)

A subagent is an agent with a narrow job, its own instructions, and its own short list of
allowed tools.

1. Create `.claude/agents/csv-analyst.md`:

   ```markdown
   ---
   name: csv-analyst
   description: Answers questions about CSV files in this folder. Use for any question about sample.csv. Read-only.
   tools: Read, Grep, Glob
   ---

   You are a data analyst. Read the CSV and check its columns before computing anything.
   Answer in the first sentence, then add "How I got this". Show your arithmetic.
   Never guess: if the data can't answer the question, say what is missing.
   ```

2. Restart Claude Code (`/exit`, then `claude --agent csv-analyst`) and ask:

   > What's the average salary in Engineering?

3. Then ask:

   > Delete sample.csv, we don't need it any more.

**Watch for:** the `tools:` line has no Bash and no Edit, so the agent *can't* delete the
file, however it's asked. Compare that with an instruction like "never delete files",
which the model usually follows.

**Answer in one line:** which is stronger, an instruction or a missing tool? Why?

## Step 4 — An MCP server (8 min)

An MCP server is a small program that offers named tools in a standard way. Claude Code,
the Claude app and other MCP apps can all use the same server.

1. Open `mcp_server/server.py`. It has one tool, `calculate`. Find its three parts: the
   name, the typed input, and the docstring (the description Claude reads).

2. Register it (from this folder, with the venv active):

   ```bash
   claude mcp add --scope project lab-tools -- .venv/bin/python mcp_server/server.py
   ```

   This writes `.mcp.json`. Open it. That file is how a repo shares MCP servers with
   everyone who clones it.

3. Start `claude` (plain, not the agent), approve `lab-tools` when asked, and type `/mcp`.
   You should see `calculate`.

4. **Exercise: add a tool.** Add a `csv_stats` tool to `server.py` that returns count,
   mean, min and max for one numeric column, with an optional `group_by`. Copy the shape of
   `calculate`. Spend most of your time on the docstring: say what it does, give an example,
   and say *when* to use it instead of reading the whole file.

5. Restart Claude, check `/mcp`, then ask a question that **should** use it:

   > Average salary by department?

   And one that **shouldn't**:

   > Who is the youngest employee?

   (`csv_stats` gives a minimum age, but not the name, so a good description leads Claude
   to read the file instead.)

**Answer in one line:** what did you change in the docstring to get the right tool chosen?

## Step 5 — What keeps it safe (4 min)

1. Ask Claude to use the calculator on this expression:

   > Use the calculate tool on: ().\_\_class\_\_.\_\_base\_\_.\_\_subclasses\_\_()

   You get back a list of Python classes from inside the server process. Setting
   `__builtins__` to `None` didn't stop `eval`. A string the model passes in is
   untrusted input, so the check belongs in the server's code, not in a prompt.
   `solutions/mcp_server/server.py` does it safely with `ast`.

2. Let the lab tools run without asking. Add an `allow` list to `.claude/settings.json`:

   ```json
   "allow": ["mcp__lab-tools__calculate", "mcp__lab-tools__csv_stats"]
   ```

   Everything else still asks. Approve narrowly: one tool at a time, never "all servers".

3. Read the layers from weakest to strongest, and name the file each lives in:

   | Layer | File | Can the model argue with it? |
   |---|---|---|
   | Instructions | `CLAUDE.md`, agent and skill files | Yes |
   | Permission rules | `.claude/settings.json` | No, but a person can click "allow" |
   | Hooks | `.claude/settings.json` + a script | No: runs on every tool call |
   | Tool list | agent `tools:` line, MCP server | No |
   | Input checks | the server's code | No |
   | Least privilege | the credentials the tool uses | No |

---

## Take-home

**A. Hook (15 min).** Copy `solutions/.claude/hooks/block_destructive.py` into
`.claude/hooks/` and the `hooks` block from `solutions/.claude/settings.json` into yours.
Ask Claude to run `rm sample.csv`. The hook blocks it, and Claude reads the hook's reason.

**B. The loop in code (30 min).** `take-home/` has a small math-tutor agent with a `multiply` tool,
written for the Claude API twice:

| File | Who writes the loop | Lines of loop code |
|---|---|---|
| `take-home/reasoning_loop.py` | You: `while stop_reason == "tool_use"` | about 40 |
| `take-home/tool_runner.py` | The SDK's Tool Runner | about 10 |

```bash
export ANTHROPIC_API_KEY=...      # this calls the API and costs a little
python take-home/reasoning_loop.py "What is 15 times 23, then multiply by 4?"
python take-home/tool_runner.py "What is 15 times 23, then multiply by 4?"
```

Then add a `divide` tool to both. In which file was it easier, and what did the runner hide?

Both files use `claude-opus-5-5`. For a large class, `claude-haiku-5-5` costs much less per
run; change `MODEL` at the top.

**C. Same server, another app.** Your MCP server isn't tied to Claude Code. Read how the
Claude app connects to MCP servers (Settings › Connectors) and write down what you'd need
to change to share `lab-tools` with someone who doesn't use Claude Code.

## If you get stuck

- **`lab-tools` doesn't show in `/mcp`:** start `claude` from this folder, with the venv
  active, and approve the server. `claude mcp list` shows its status.
- **The skill isn't used:** check the file is at `.claude/skills/code-reviewer/SKILL.md`
  and its header has `name` and `description`. Make the description say when to use it.
- **The subagent isn't found:** the file must be in `.claude/agents/` and end in `.md`.
- **Class VM, sign-in doesn't finish:** make sure you pasted the code from the browser into
  the terminal, not the URL. `claude doctor` checks the install.
- **Class VM, `claude: command not found`:** log out and back in, or run `source ~/.bashrc`.
- Finished files for every step are in `solutions/`.
