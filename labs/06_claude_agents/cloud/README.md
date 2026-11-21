# Optional: run the lab on an AWS VM

For students who can't install Claude Code on their own laptop. You run one Ubuntu VM
on AWS; each student gets their own Linux account on it, with Claude Code and the lab
already set up. All they need is a terminal with SSH (built into macOS, Linux and
Windows 10+) and a browser.

```
student laptop ──SSH──▶ EC2 VM (Ubuntu)
                         ├─ /home/student01/lab   own copy of the lab + own Claude Code
                         ├─ /home/student02/lab
                         └─ /opt/lab-venv         one shared Python environment
```

## What students still need

**Each student signs in to Claude Code with their own account.** The VM doesn't
change that. Claude Code needs one of:

- a paid Claude plan (Pro, Max, Team or Enterprise), or
- a Claude Console API key.

The free claude.ai plan doesn't include Claude Code. If your institution has a Team or
Enterprise plan, give students seats; otherwise, create Console API keys with a spend
limit. Never share one key across the class: you lose track of use, and one leak exposes
everyone.

## 1. Launch the VM (about 10 minutes)

In the AWS console, EC2 › Launch instance:

| Setting | Value |
|---|---|
| AMI | Ubuntu Server 24.04 LTS (x86_64 or Arm) |
| Instance type | Depends on class size; see below |
| Key pair | Create or pick one. This is your admin login, not the students’ |
| Security group | Inbound SSH (port 22) **only from your campus or classroom IP range**, never `0.0.0.0/0` |
| Storage | 30 GB gp3 for up to about 30 students (each Claude Code install is a few hundred MB) |

**Sizing.** Claude Code's documentation asks for 4 GB+ of RAM on the machine it runs on.
Each logged-in student runs their own Claude Code process plus a small Python MCP server.
As a starting point, plan on about 0.5 GB per active student on top of 4 GB, for example a
16 GB instance for about 20–25 students. Before class, sign in a few test accounts at once
and watch `free -h` to check.

**Alternative: one small VM per student.** You get better isolation and no shared limits,
but more instances to manage. Use the same two scripts with a one-line roster.

## 2. Set it up (about 10 minutes)

From your laptop, copy the scripts up and run them:

```bash
scp -i your-key.pem cloud/*.sh ubuntu@VM_ADDRESS:~
ssh -i your-key.pem ubuntu@VM_ADDRESS
```

On the VM:

```bash
sudo bash setup-vm.sh
nano students.txt                     # one username per line, see students.example.txt
sudo ENABLE_PASSWORD_SSH=1 bash add-students.sh students.txt
```

`setup-vm.sh` installs Python, copies the lab to `/opt/lab` (from this repo's `main`
branch) and builds the shared environment. `add-students.sh` creates the accounts and
installs Claude Code for each one. It writes the first-login passwords to
`credentials.csv`, readable only by root.

`ENABLE_PASSWORD_SSH=1` lets students log in with a password, so they don't need to
manage SSH keys. That's why the security group must be limited to your IP range.
`fail2ban` is installed to block repeated failed logins, and each student must choose a
new password the first time they log in.

## 3. Hand out logins

Give each student only their own line from `credentials.csv`, then delete the file:

```bash
sudo shred -u credentials.csv
```

Students follow "Option B: the class VM" in `LAB.md`.

## 4. Before class: test one account end to end

1. SSH in as a test student, set the new password, and check you land in `~/lab` with the
   environment active.
2. Run `claude` and complete the sign-in (see below).
3. Run steps 1 and 4 of the lab: ask the CSV question, then register `lab-tools` and check `/mcp`.

**Signing in over SSH.** On first launch Claude Code tries to open a browser. On a VM there
isn't one, so press `c` to copy the login URL, or copy it from the screen. Open it in the
laptop's browser, sign in, and paste the code it shows back into the terminal at the
`Paste code here if prompted` prompt. With a Console API key instead:
`export ANTHROPIC_API_KEY=...` before running `claude`, and approve the key when asked.

## 5. After the course

Terminate the instance in the EC2 console. It deletes every account and its sign-in
credentials with it. To remove one student before then: `sudo userdel -r USERNAME`.

## Notes

- **Where data goes.** Work done on the VM goes to Anthropic's API exactly as on a laptop.
  The lab only uses the made-up `sample.csv`.
- **Updates.** Each student's Claude Code updates itself. To rebuild the lab copy after
  changing the repo, rerun `setup-vm.sh`. Existing students keep their `~/lab`.
- **Editing files.** Students can edit with `nano`, ask Claude to create the files, or
  connect VS Code with the Remote-SSH extension.
