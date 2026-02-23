# Meater Bluetooth Protocol

## Overview

Meater probes use Bluetooth Low Energy (BLE) for wireless communication. This document describes the protocol for reading temperature data.

## Device Identification

Meater probes advertise with these name patterns:
- `MEATER` - Original Meater
- `MEATER+` - Meater Plus
- `MEATER Block` - Meater Block
- `MEATER Pro` - Meater Pro

## BLE Service UUID

```
Service UUID: a75cc7fc-c956-488f-ac2c-6b92f1f60e64
```

## Characteristics

### Temperature Data

```
Characteristic UUID: 7edda774-045e-4bbf-909b-45d1991a9226
Properties: Read, Notify
```

**Data Format (4 bytes, little endian):**

| Bytes | Content |
|-------|---------|
| 0-1   | Tip temperature (raw) |
| 2-3   | Ambient temperature (raw) |

**Temperature Decoding:**

The raw temperature values use a proprietary encoding. The decoding formula:

```python
def decode_temperature(raw_value):
    return (raw_value / 16.0) - 20.0
```

This returns the temperature in Celsius.

**Example:**
- Raw value: 752
- Calculation: (752 / 16) - 20 = 47 - 20 = 27°C

### Battery Level

```
Characteristic UUID: 00002a19-0000-1000-8000-00805f9b34fb (standard BLE battery service)
Properties: Read
```

**Data Format:** 1 byte (0-100)

## Connection Process

1. **Scan** for devices advertising Meater service or name
2. **Connect** to the device
3. **Read** temperature characteristic
4. **Parse** the 4-byte response
5. **Decode** temperatures using the formula above

## Temperature Zones

### Internal (Tip) Temperature
- Sensor location: Inside the meat
- Range: -40°C to 100°C (-40°F to 212°F) for Original
- Range: -40°C to 100°C (-40°F to 212°F) for Plus
- Range: Up to 100°C+ for Block/Pro

### Ambient Temperature  
- Sensor location: Oven/grill end of probe
- Range: Up to 300°C+ (572°F+)
- Used to estimate cook time and detect oven temperature

## Battery Life

| Model | Battery Life |
|-------|-------------|
| Meater Original | 24+ hours |
| Meater Plus | 24+ hours |
| Meater Block | 24+ hours per probe |
| Meater Pro | 24+ hours |

Battery level is reported as percentage (0-100%).

## Range

| Model | Bluetooth Range |
|-------|----------------|
| Meater Original | ~10 ft (3m) |
| Meater Plus | ~165 ft (50m) |
| Meater Block | ~165 ft (50m) via Block |
| Meater Pro | ~165 ft (50m) |

## Notes

- Probes must be removed from the charger/base to be discoverable
- The probe enters sleep mode when inserted back into the charger
- Ambient temperature readings may be inaccurate at very low temperatures
- Metal enclosures (grills, smokers) can reduce Bluetooth range

## Official Resources

- Meater App: iOS and Android
- Website: https://www.meater.com
- Support: https://help.meater.com
