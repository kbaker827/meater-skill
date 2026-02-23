---
name: meater
description: Monitor Meater wireless meat thermometers (Original, Plus, Block, Pro) via Bluetooth. Use when the user wants to check cooking temperatures, monitor probe status, or track meat doneness.
---

# Meater

Monitor Meater wireless meat thermometers via Bluetooth Low Energy (BLE).

## Quick Start

### Requirements

- Meater probe (Original, Plus, Block, or Pro)
- Bluetooth enabled on your device
- Python 3 with `bleak` library: `pip3 install bleak`

### Scan for Probes

```bash
python3 scripts/meater.py scan
```

### Read Temperatures

```bash
# Read from a specific probe
python3 scripts/meater.py read --address "AA:BB:CC:DD:EE:FF"

# Read and monitor continuously
python3 scripts/meater.py monitor --address "AA:BB:CC:DD:EE:FF"
```

## Temperature Readings

Meater probes provide:
- **Tip Temperature** - Internal meat temperature
- **Ambient Temperature** - Oven/grill temperature  
- **Target Temperature** - Set target (if configured in app)

## Common Commands

| Command | Description |
|---------|-------------|
| `scan` | Scan for nearby Meater probes |
| `read` | Read current temperatures once |
| `monitor` | Continuously monitor temperatures |
| `info` | Get probe info (battery, firmware) |

## Resources

### scripts/
- `meater.py` - CLI tool for Meater probe communication

### references/
- `ble-protocol.md` - Meater Bluetooth protocol documentation

## Examples

### Find your probe
```bash
python3 scripts/meater.py scan
```

### Check temperature quickly
```bash
python3 scripts/meater.py read --address "AA:BB:CC:DD:EE:FF"
```

### Monitor while cooking
```bash
python3 scripts/meater.py monitor --address "AA:BB:CC:DD:EE:FF" --interval 5
```

### Get probe information
```bash
python3 scripts/meater.py info --address "AA:BB:CC:DD:EE:FF"
```
