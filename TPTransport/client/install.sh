#!/usr/bin/env bash
# install.sh — deploy the bus-client on a Raspberry Pi (run as root)
#
# Usage:
#   sudo bash client/install.sh
#
# What it does:
#   1. Creates a dedicated system user (bus-client).
#   2. Copies the client package to /opt/bus-client/.
#   3. Creates a Python venv and installs dependencies.
#   4. Installs the systemd unit.
#   5. Creates required directories with correct ownership.
#   6. Prompts for BUS_API_TOKEN and BUS_SERVER_URL.
#
# After running: edit /etc/bus-client/env, then:
#   systemctl enable --now bus-client

set -euo pipefail

INSTALL_DIR="/opt/bus-client"
ENV_FILE="/etc/bus-client/env"
LOG_DIR="/var/log/bus-client"
LIB_DIR="/var/lib/bus-client"
SERVICE_USER="bus-client"

echo "=== bus-client installer ==="

# 1. System user
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --shell /sbin/nologin --create-home --home-dir "$INSTALL_DIR" "$SERVICE_USER"
    echo "Created user: $SERVICE_USER"
fi

# 2. Copy package
mkdir -p "$INSTALL_DIR"
cp -r "$(dirname "$0")"/../client "$INSTALL_DIR/client"
echo "Installed client package to $INSTALL_DIR"

# 3. Python venv
if [ ! -d "$INSTALL_DIR/venv" ]; then
    python3 -m venv "$INSTALL_DIR/venv"
fi
"$INSTALL_DIR/venv/bin/pip" install --quiet --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install --quiet -r "$INSTALL_DIR/client/requirements.txt"
echo "Python venv ready"

# 4. systemd unit
cp "$(dirname "$0")/bus-client.service" /etc/systemd/system/
systemctl daemon-reload
echo "Systemd unit installed"

# 5. Directories
mkdir -p "$LOG_DIR" "$LIB_DIR" "$(dirname "$ENV_FILE")"
chown "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR" "$LIB_DIR" "$INSTALL_DIR"
echo "Directories created"

# 6. Environment file
if [ ! -f "$ENV_FILE" ]; then
    cp "$(dirname "$0")/.env.example" "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    echo ""
    echo "Created $ENV_FILE from template."
    echo "Please edit it and set BUS_API_TOKEN and BUS_SERVER_URL, then run:"
    echo "  systemctl enable --now bus-client"
else
    echo "$ENV_FILE already exists — not overwritten."
fi

echo ""
echo "=== Installation complete ==="
echo "Next steps:"
echo "  1. nano $ENV_FILE"
echo "  2. systemctl enable --now bus-client"
echo "  3. journalctl -u bus-client -f"
