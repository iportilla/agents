#!/usr/bin/env bash
# Prepare an Ubuntu VM (24.04 LTS recommended) to host the Claude agents lab.
#
# Run once, as root, on a fresh instance:
#   sudo bash setup-vm.sh
#
# It installs Python and git, puts a read-only copy of the lab in /opt/lab,
# and builds one shared Python environment in /opt/lab-venv that every
# student account uses. Claude Code itself is installed per student by
# add-students.sh, because its installer and sign-in are per user.
#
# Optional environment variables:
#   REPO_URL     git repo that holds the lab (default: this course's repo)
#   REPO_BRANCH  branch to check out (default: main)

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/iportilla/agents.git}"
REPO_BRANCH="${REPO_BRANCH:-main}"
LAB_SUBDIR="labs/06_claude_agents"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root: sudo bash $0" >&2
  exit 1
fi

echo "==> Installing system packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q python3 python3-venv python3-pip git curl ca-certificates nano fail2ban

echo "==> Fetching the lab from $REPO_URL ($REPO_BRANCH)"
rm -rf /opt/agents-src
git clone --depth 1 --branch "$REPO_BRANCH" "$REPO_URL" /opt/agents-src
rm -rf /opt/lab
cp -r "/opt/agents-src/$LAB_SUBDIR" /opt/lab
rm -rf /opt/agents-src /opt/lab/cloud   # students don't need the instructor scripts
chmod -R a+rX /opt/lab

echo "==> Building the shared Python environment in /opt/lab-venv"
python3 -m venv /opt/lab-venv
/opt/lab-venv/bin/pip install -q --upgrade pip
/opt/lab-venv/bin/pip install -q -r /opt/lab/requirements.txt
chmod -R a+rX /opt/lab-venv

echo "==> Turning on fail2ban (blocks repeated failed SSH logins)"
systemctl enable --now fail2ban >/dev/null 2>&1 || echo "    (fail2ban not started: no systemd here)"

echo
echo "Done. Next: sudo bash add-students.sh students.txt"
