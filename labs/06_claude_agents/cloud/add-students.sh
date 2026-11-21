#!/usr/bin/env bash
# Create one Linux account per student on the lab VM, each with its own copy
# of the lab and its own Claude Code install.
#
# Run as root after setup-vm.sh:
#   sudo bash add-students.sh students.txt
#
# students.txt has one username per line (lowercase letters, digits, - or _;
# lines starting with # are skipped). For each student this script:
#   - creates the account with a random password they must change at first login
#   - copies the lab to ~/lab and links ~/lab/.venv to the shared /opt/lab-venv
#   - installs Claude Code for that user (in ~/.local/bin)
# and writes the usernames and passwords to credentials.csv (readable by root only).
#
# Optional environment variables:
#   ENABLE_PASSWORD_SSH=1  allow SSH logins with a password (off by default
#                          on Ubuntu cloud images). Only do this with the
#                          security group limited to your campus IP range.

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Run as root: sudo bash $0 students.txt" >&2
  exit 1
fi
if [[ $# -ne 1 || ! -f "$1" ]]; then
  echo "Usage: sudo bash $0 students.txt" >&2
  exit 1
fi
if [[ ! -d /opt/lab || ! -x /opt/lab-venv/bin/python ]]; then
  echo "Run setup-vm.sh first." >&2
  exit 1
fi

ROSTER="$1"
OUT="credentials.csv"
touch "$OUT"
chmod 600 "$OUT"
[[ -s "$OUT" ]] || echo "username,password" > "$OUT"

while IFS= read -r raw || [[ -n "$raw" ]]; do
  user="$(echo "$raw" | tr -d '[:space:]')"
  [[ -z "$user" || "$user" == \#* ]] && continue
  if [[ ! "$user" =~ ^[a-z_][a-z0-9_-]{0,31}$ ]]; then
    echo "!! Skipping '$user': not a valid username" >&2
    continue
  fi
  if id "$user" >/dev/null 2>&1; then
    echo "-- $user already exists, skipping"
    continue
  fi

  echo "==> $user"
  password="$(head -c 18 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 14)"
  useradd --create-home --shell /bin/bash "$user"
  echo "$user:$password" | chpasswd
  chage -d 0 "$user"            # must choose a new password at first login
  chmod 750 "/home/$user"       # students can't read each other's work

  cp -r /opt/lab "/home/$user/lab"
  ln -s /opt/lab-venv "/home/$user/lab/.venv"
  chown -R "$user:$user" "/home/$user/lab"

  # Claude Code's native installer works per user, into ~/.local/bin.
  sudo -u "$user" -H bash -c 'curl -fsSL https://claude.ai/install.sh | bash' >/dev/null
  if ! grep -q '.local/bin' "/home/$user/.bashrc"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "/home/$user/.bashrc"
  fi
  echo 'cd ~/lab 2>/dev/null && source .venv/bin/activate' >> "/home/$user/.bashrc"

  echo "$user,$password" >> "$OUT"
done < "$ROSTER"

if [[ "${ENABLE_PASSWORD_SSH:-0}" == "1" ]]; then
  echo "==> Allowing SSH password logins"
  printf 'PasswordAuthentication yes\nKbdInteractiveAuthentication yes\n' \
    > /etc/ssh/sshd_config.d/60-lab-passwords.conf
  systemctl restart ssh 2>/dev/null || systemctl restart sshd 2>/dev/null || true
fi

echo
echo "Done. Usernames and first-login passwords are in $(realpath "$OUT")."
echo "Hand each student their own line, then delete the file."
