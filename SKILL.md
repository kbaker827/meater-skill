---
name: meater
description: Monitor Meater wireless meat thermometers (Original, Plus, Block, Pro) via Bluetooth or WiFi/Cloud API. Use when the user wants to check cooking temperatures, monitor probe status, or track meat doneness.
---

# Meater

Monitor Meater wireless meat thermometers via Bluetooth Low Energy (BLE) or the Meater Cloud API (for remote/WiFi access).

## Connection Methods

### Method 1: Bluetooth (Direct)
Best for: Local monitoring, real-time updates

**Requirements:**
- Meater probe (Original, Plus, Block, or Pro)
- Bluetooth enabled on your device
- Python 3 with `bleak` library: `pip3 install bleak`

### Method 2: Cloud API (WiFi/Remote)
Best for: Remote monitoring, historical data, Meater Block users

**Requirements:**
- Meater account with cloud sync enabled
- Meater Block (recommended) OR app syncing to cloud
- Meater API credentials (email/password)

## Quick Start

### Bluetooth Mode

```bash
# Scan for probes
python3 scripts/meater.py scan

# Read temperatures
python3 scripts/meater.py read --address "AA:BB:CC:DD:EE:FF"
```

### Cloud Mode

```bash
# Login and list cooks
export MEATER_EMAIL="your@email.com"
export MEATER_PASSWORD="your_password"
python3 scripts/meater_cloud.py devices

# Monitor current cook
python3 scripts/meater_cloud.py monitor --device-id "PROBE_ID"
```

## Bluetooth Commands

| Command | Description |
|---------|-------------|
| `scan` | Scan for nearby Meater probes |
| `read` | Read current temperatures once |
| `monitor` | Continuously monitor temperatures |
| `info` | Get probe info (battery, firmware) |

## Cloud Commands

| Command | Description |
|---------|-------------|
| `login` | Authenticate with Meater Cloud |
| `devices` | List registered probes/devices |
| `cooks` | List active and recent cooks |
| `monitor` | Monitor cook via cloud |
| `history` | Get cook history |

## Temperature Readings

Meater probes provide:
- **Tip Temperature** - Internal meat temperature
- **Ambient Temperature** - Oven/grill temperature  
- **Target Temperature** - Set target (if configured in app)

## Resources

### scripts/
- `meater.py` - Bluetooth CLI tool
- `meater_cloud.py` - Cloud API CLI tool

### references/
- `ble-protocol.md` - Bluetooth protocol documentation
- `cloud-api.md` - Meater Cloud API documentation

## Examples

### Bluetooth: Find and read
```bash
python3 scripts/meater.py scan
python3 scripts/meater.py read --address "AA:BB:CC:DD:EE:FF"
```

### Cloud: Remote monitoring
```bash
export MEATER_EMAIL="user@example.com"
export MEATER_PASSWORD="password"
python3 scripts/meater_cloud.py devices
python3 scripts/meater_cloud.py monitor --device-id "ABC123"
```

### Bluetooth: Continuous monitoring
```bash
python3 scripts/meater.py monitor --address "AA:BB:CC:DD:EE:FF" --interval 5
```

### Cloud: Check cook history
```bash
python3 scripts/meater_cloud.py history --limit 10
```
