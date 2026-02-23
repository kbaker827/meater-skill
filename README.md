# Meater Skill for OpenClaw

Monitor Meater wireless meat thermometers (Original, Plus, Block, Pro) via Bluetooth Low Energy.

## What is OpenClaw?

[OpenClaw](https://github.com/openclaw/openclaw) is an open-source agent framework. This skill extends OpenClaw with Meater probe monitoring capabilities.

## Requirements

- Meater wireless meat thermometer (Original, Plus, Block, or Pro)
- Bluetooth enabled on your computer/device
- Python 3.7+
- bleak library: `pip3 install bleak`

## Installation

```bash
pip3 install bleak
```

## Usage

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

Get a single temperature reading:

```bash
python3 scripts/meater.py read --address "AA:BB:CC:DD:EE:FF"
```

Output:
```
Connected to AA:BB:CC:DD:EE:FF

Meater Probe (AA:BB:CC:DD:EE:FF)
  Internal (Meat): 68.0°C / 154.4°F
  Ambient (Oven):  180.5°C / 356.9°F
  Battery: 85%
```

### 3. Monitor Continuously

Watch temperatures while cooking:

```bash
python3 scripts/meater.py monitor --address "AA:BB:CC:DD:EE:FF" --interval 5
```

Output:
```
Monitoring AA:BB:CC:DD:EE:FF (Ctrl+C to stop)

Connected to AA:BB:CC:DD:EE:FF

[14:32:10] Meat: 154.4°F | Oven: 356.9°F
[14:32:15] Meat: 155.2°F | Oven: 357.1°F
[14:32:20] Meat: 156.1°F | Oven: 357.5°F
...
```

### 4. Get Probe Info

```bash
python3 scripts/meater.py info --address "AA:BB:CC:DD:EE:FF"
```

## Commands

| Command | Description |
|---------|-------------|
| `scan` | Find nearby Meater probes |
| `read` | Read temperatures once |
| `monitor` | Continuous monitoring |
| `info` | Get probe details |

## Temperature Readings

- **Internal (Tip)** - Temperature inside the meat
- **Ambient** - Oven/grill temperature
- Both displayed in Celsius and Fahrenheit

## Tips

- Remove probe from charger/base to make it discoverable
- Keep within Bluetooth range (varies by model: 10-165 ft)
- Metal enclosures (grills, smokers) can reduce range
- Probes enter sleep mode when returned to charger

## Supported Models

| Model | Range | Features |
|-------|-------|----------|
| Meater Original | ~10 ft | 2 sensors |
| Meater Plus | ~165 ft | 2 sensors |
| Meater Block | ~165 ft | 4 probes, WiFi base |
| Meater Pro | ~165 ft | 2 sensors, longer probe |

## Protocol Reference

See [`references/ble-protocol.md`](references/ble-protocol.md) for detailed Bluetooth protocol documentation.

## Troubleshooting

**"No Meater probes found"**
- Make sure probe is removed from charger
- Check Bluetooth is enabled
- Move closer to the probe

**"Could not parse temperature data"**
- Try reconnecting
- Check probe battery level

**Connection errors**
- Ensure no other device (phone app) is connected to the probe
- Try scanning again to confirm address

## License

MIT
