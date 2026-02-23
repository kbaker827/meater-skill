#!/usr/bin/env python3
"""
Meater CLI - Monitor Meater wireless meat thermometers via Bluetooth.

Usage:
    python3 meater.py scan
    python3 meater.py read --address "AA:BB:CC:DD:EE:FF"
    python3 meater.py monitor --address "AA:BB:CC:DD:EE:FF"

Requirements:
    pip3 install bleak
"""

import argparse
import asyncio
import sys
import time
from typing import Optional, Tuple

try:
    from bleak import BleakClient, BleakScanner
    from bleak.backends.characteristic import BleakGATTCharacteristic
except ImportError:
    print("Error: 'bleak' library required.", file=sys.stderr)
    print("Install: pip3 install bleak", file=sys.stderr)
    sys.exit(1)


# Meater BLE UUIDs
MEATER_SERVICE_UUID = "a75cc7fc-c956-488f-ac2c-6b92f1f60e64"
MEATER_DATA_UUID = "7edda774-045e-4bbf-909b-45d1991a9226"
MEATER_BATTERY_UUID = "2a19"

# Meater device names
MEATER_NAMES = ["MEATER", "MEATER+", "MEATER Block", "MEATER Pro"]


def decode_temperature(raw_value: int) -> float:
    """Decode Meater temperature from raw sensor value."""
    # Meater uses a proprietary encoding
    # Based on reverse engineering of the Meater protocol
    if raw_value == 0:
        return 0.0
    
    # Convert to temperature (Celsius)
    # This is an approximation based on documented algorithms
    temperature = (raw_value / 16.0) - 20.0
    return round(temperature, 1)


def parse_meater_data(data: bytes) -> dict:
    """Parse raw Meater BLE data."""
    if len(data) < 4:
        return {}
    
    # Meater data format (little endian)
    # Bytes 0-1: Tip temperature (internal meat temp)
    # Bytes 2-3: Ambient temperature (oven/grill temp)
    
    tip_raw = int.from_bytes(data[0:2], byteorder='little', signed=False)
    ambient_raw = int.from_bytes(data[2:4], byteorder='little', signed=False)
    
    tip_temp = decode_temperature(tip_raw)
    ambient_temp = decode_temperature(ambient_raw)
    
    return {
        "tip_temperature_c": tip_temp,
        "tip_temperature_f": round(tip_temp * 9/5 + 32, 1),
        "ambient_temperature_c": ambient_temp,
        "ambient_temperature_f": round(ambient_temp * 9/5 + 32, 1),
        "raw_data": data.hex()
    }


async def scan_for_probes(timeout: int = 10):
    """Scan for nearby Meater probes."""
    print(f"Scanning for Meater probes ({timeout}s)...\n")
    
    devices = await BleakScanner.discover(timeout=timeout)
    
    probes = []
    for device in devices:
        name = device.name or "Unknown"
        if any(meater_name in name for meater_name in MEATER_NAMES):
            probes.append(device)
    
    if not probes:
        print("No Meater probes found.")
        print("\nTips:")
        print("- Make sure your probe is out of the charger/base")
        print("- Ensure Bluetooth is enabled")
        print("- Try moving closer to the probe")
        return
    
    print(f"Found {len(probes)} Meater probe(s):\n")
    for probe in probes:
        print(f"Name: {probe.name}")
        print(f"  Address: {probe.address}")
        print(f"  RSSI: {probe.rssi} dBm")
        print()


async def read_temperatures(address: str):
    """Read temperatures from a Meater probe."""
    try:
        async with BleakClient(address, timeout=30.0) as client:
            print(f"Connected to {address}\n")
            
            # Read temperature data
            data = await client.read_gatt_char(MEATER_DATA_UUID)
            temps = parse_meater_data(data)
            
            if not temps:
                print("Error: Could not parse temperature data")
                return
            
            print(f"Meater Probe ({address})")
            print(f"  Internal (Meat): {temps['tip_temperature_c']}°C / {temps['tip_temperature_f']}°F")
            print(f"  Ambient (Oven):  {temps['ambient_temperature_c']}°C / {temps['ambient_temperature_f']}°F")
            
            # Try to read battery if available
            try:
                battery_data = await client.read_gatt_char(MEATER_BATTERY_UUID)
                battery_level = int.from_bytes(battery_data, byteorder='little')
                print(f"  Battery: {battery_level}%")
            except:
                pass
            
    except Exception as e:
        print(f"Error reading from probe: {e}", file=sys.stderr)
        print("\nMake sure:", file=sys.stderr)
        print("- The probe address is correct", file=sys.stderr)
        print("- The probe is powered on (out of charger)", file=sys.stderr)
        print("- You're within Bluetooth range", file=sys.stderr)


async def monitor_probe(address: str, interval: int = 5):
    """Continuously monitor a Meater probe."""
    print(f"Monitoring {address} (Ctrl+C to stop)\n")
    
    try:
        async with BleakClient(address, timeout=30.0) as client:
            print(f"Connected to {address}\n")
            
            while True:
                try:
                    # Read temperature data
                    data = await client.read_gatt_char(MEATER_DATA_UUID)
                    temps = parse_meater_data(data)
                    
                    if temps:
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{timestamp}] Meat: {temps['tip_temperature_f']}°F | "
                              f"Oven: {temps['ambient_temperature_f']}°F")
                    
                    await asyncio.sleep(interval)
                    
                except Exception as e:
                    print(f"[{time.strftime('%H:%M:%S')}] Error reading: {e}")
                    await asyncio.sleep(interval)
                    
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


async def get_probe_info(address: str):
    """Get probe information."""
    try:
        async with BleakClient(address, timeout=30.0) as client:
            print(f"Probe Information ({address})\n")
            
            # Get services
            services = await client.get_services()
            
            print(f"Services: {len(services.services)}")
            for service in services:
                print(f"  {service.uuid}: {service.description}")
                for char in service.characteristics:
                    print(f"    - {char.uuid}: {char.description}")
            
            # Try to read battery
            try:
                battery_data = await client.read_gatt_char(MEATER_BATTERY_UUID)
                battery_level = int.from_bytes(battery_data, byteorder='little')
                print(f"\nBattery Level: {battery_level}%")
            except Exception as e:
                print(f"\nBattery: Unable to read ({e})")
            
    except Exception as e:
        print(f"Error connecting to probe: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Meater Wireless Thermometer CLI')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for Meater probes')
    scan_parser.add_argument('--timeout', '-t', type=int, default=10,
                            help='Scan timeout in seconds (default: 10)')
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read temperatures once')
    read_parser.add_argument('--address', '-a', required=True,
                            help='Bluetooth address of the probe (e.g., AA:BB:CC:DD:EE:FF)')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Continuously monitor temperatures')
    monitor_parser.add_argument('--address', '-a', required=True,
                               help='Bluetooth address of the probe')
    monitor_parser.add_argument('--interval', '-i', type=int, default=5,
                               help='Read interval in seconds (default: 5)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get probe information')
    info_parser.add_argument('--address', '-a', required=True,
                            help='Bluetooth address of the probe')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Run the appropriate command
    if args.command == 'scan':
        asyncio.run(scan_for_probes(args.timeout))
    elif args.command == 'read':
        asyncio.run(read_temperatures(args.address))
    elif args.command == 'monitor':
        asyncio.run(monitor_probe(args.address, args.interval))
    elif args.command == 'info':
        asyncio.run(get_probe_info(args.address))


if __name__ == '__main__':
    main()
