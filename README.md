# Meater Skill for OpenClaw

Monitor Meater wireless meat thermometers (Original, Plus, Block, Pro) via **Bluetooth** (direct) or **WiFi/Cloud** (remote).

## What is OpenClaw?

[OpenClaw](https://github.com/openclaw/openclaw) is an open-source agent framework. This skill extends OpenClaw with Meater probe monitoring capabilities.

## Two Connection Methods

### 🔷 Method 1: Bluetooth (Direct)
**Best for:** Local monitoring, real-time updates, lowest latency

**Requirements:**
- Meater probe (any model)
- Bluetooth on your computer/device
- Python 3.7+
- `bleak` library

### 🔷 Method 2: Cloud API (WiFi/Remote)
**Best for:** Remote monitoring, Meater Block users, historical data

**Requirements:**
- Meater account with cloud sync
- Meater Block (recommended) OR app syncing to cloud
- `requests` library

## Installation

```bash
# For Bluetooth mode
pip3 install bleak

# For Cloud mode
pip3 install requests

# For both
pip3 install bleak requests
```

## Bluetooth Usage

### 1. Scan for Probes

Find your Meater probe's Bluetooth address:

```bash
python3 scripts/meater.py scan
```

Output:
```
Found 1 Meater probe(s):

Name: MEATER+
  Address: AA:BB:CC:DD:EE:FF
  RSSI: -65 dBm
```

### 2. Read Temperatures

```bash
python3 scripts/meater.py read --address "AA:BB:CC:DD:EE:FF"
```

Output:
```
Meater Probe (AA:BB:CC:DD:EE:FF)
  Internal (Meat): 68.0°C / 154.4°F
  Ambient (Oven):  180.5°C / 356.9°F
  Battery: 85%
```

### 3. Monitor Continuously

```bash
python3 scripts/meater.py monitor --address "AA:BB:CC:DD:EE:FF" --interval 5
```

## Cloud (WiFi) Usage

### 1. Set Credentials

```bash
export MEATER_EMAIL="your@email.com"
export MEATER_PASSWORD="your_password"
```

### 2. List Devices

```bash
python3 scripts/meater_cloud.py devices
```

### 3. Monitor Remotely

```bash
python3 scripts/meater_cloud.py monitor --device-id "PROBE_ID"
```

### 4. List Active Cooks

```bash
python3 scripts/meater_cloud.py cooks --status active
```

## Commands

### Bluetooth Commands

| Command | Description |
|---------|-------------|
| `scan` | Find nearby probes |
| `read` | Read temperatures once |
| `monitor` | Continuous monitoring |
| `info` | Probe details & battery |

### Cloud Commands

| Command | Description |
|---------|-------------|
| `login` | Test credentials |
| `devices` | List registered probes |
| `cooks` | List active/recent cooks |
| `monitor` | Remote monitoring |

## Comparison: Bluetooth vs Cloud

| Feature | Bluetooth | Cloud/WiFi |
|---------|-----------|------------|
| **Range** | 10-165 ft | Unlimited |
| **Latency** | ~1 second | ~10 seconds |
| **Requires Block** | No | Recommended |
| **Remote Access** | No | Yes |
| **Historical Data** | No | Yes |
| **Battery Impact** | None | None |

## Supported Models

| Model | Bluetooth Range | Cloud Support |
|-------|----------------|---------------|
| Meater Original | ~10 ft | Via app sync |
| Meater Plus | ~165 ft | Via app sync |
| Meater Block | ~165 ft | ✓ Native WiFi |
| Meater Pro | ~165 ft | Via app sync |

## Temperature Readings

- **Internal (Tip)** - Temperature inside the meat
- **Ambient** - Oven/grill temperature
- Both displayed in Celsius and Fahrenheit

## Resources

- `references/ble-protocol.md` - Bluetooth protocol docs
- `references/cloud-api.md` - Cloud API docs

## Troubleshooting

**"No Meater probes found" (Bluetooth)**
- Remove probe from charger
- Check Bluetooth is enabled
- Move closer to probe

**"Login failed" (Cloud)**
- Verify email/password
- Check cloud sync is enabled in Meater app
- Ensure you have internet connectivity

**Cloud not updating**
- Meater app must be running (if no Block)
- Phone must have internet (if no Block)
- Check Meater Block WiFi connection

## License

MIT
