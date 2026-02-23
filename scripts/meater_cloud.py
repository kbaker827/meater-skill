#!/usr/bin/env python3
"""
Meater Cloud CLI - Monitor Meater probes via the Meater Cloud API (WiFi/Remote).

Usage:
    export MEATER_EMAIL="your@email.com"
    export MEATER_PASSWORD="your_password"
    python3 meater_cloud.py devices
    python3 meater_cloud.py monitor --device-id DEVICE_ID

Requirements:
    pip3 install requests
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' library required.", file=sys.stderr)
    print("Install: pip3 install requests", file=sys.stderr)
    sys.exit(1)


# Meater Cloud API
MEATER_CLOUD_BASE = "https://public-api.cloud.meater.com/v1"
MEATER_AUTH_URL = "https://fusion.googleapis.com/v1/projects/meater-768a7/databases/(default)/documents/users"


class MeaterCloudClient:
    """Client for Meater Cloud API."""
    
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.token = None
        self.user_id = None
        
    def login(self) -> bool:
        """Authenticate with Meater Cloud."""
        # Note: The actual Meater Cloud API uses Firebase Authentication
        # This is a simplified implementation
        
        try:
            # Firebase Auth REST API
            firebase_api_key = "AIzaSyBQ_2Z..."  # This would need the actual key
            
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
            
            payload = {
                "email": self.email,
                "password": self.password,
                "returnSecureToken": True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('idToken')
                self.user_id = data.get('localId')
                return True
            else:
                print(f"Login failed: {response.status_code}", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return False
                
        except Exception as e:
            print(f"Login error: {e}", file=sys.stderr)
            return False
    
    def get_devices(self) -> list:
        """Get list of registered devices/probes."""
        if not self.token:
            print("Not authenticated. Please login first.", file=sys.stderr)
            return []
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{MEATER_CLOUD_BASE}/devices",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('data', [])
            else:
                print(f"Error fetching devices: {response.status_code}", file=sys.stderr)
                return []
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return []
    
    def get_cooks(self, status: Optional[str] = None) -> list:
        """Get list of cooks."""
        if not self.token:
            print("Not authenticated.", file=sys.stderr)
            return []
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{MEATER_CLOUD_BASE}/cooks"
            
            if status:
                url += f"?status={status}"
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('data', [])
            else:
                print(f"Error fetching cooks: {response.status_code}", file=sys.stderr)
                return []
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return []
    
    def get_device_status(self, device_id: str) -> Optional[dict]:
        """Get current status of a specific device."""
        if not self.token:
            print("Not authenticated.", file=sys.stderr)
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{MEATER_CLOUD_BASE}/devices/{device_id}/status",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('data')
            else:
                print(f"Error fetching device status: {response.status_code}", file=sys.stderr)
                return None
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return None


def format_temperature(celsius: Optional[float]) -> str:
    """Format temperature in both C and F."""
    if celsius is None:
        return "N/A"
    fahrenheit = (celsius * 9/5) + 32
    return f"{celsius:.1f}°C / {fahrenheit:.1f}°F"


def cmd_login(email: str, password: str):
    """Test login credentials."""
    client = MeaterCloudClient(email, password)
    
    print("Authenticating with Meater Cloud...")
    if client.login():
        print("✓ Login successful!")
        print(f"User ID: {client.user_id}")
    else:
        print("✗ Login failed")
        sys.exit(1)


def cmd_devices(email: str, password: str):
    """List registered devices."""
    client = MeaterCloudClient(email, password)
    
    if not client.login():
        sys.exit(1)
    
    devices = client.get_devices()
    
    if not devices:
        print("No devices found.")
        return
    
    print(f"Found {len(devices)} device(s):\n")
    for device in devices:
        print(f"Device: {device.get('name', 'Unknown')}")
        print(f"  ID: {device.get('id', 'N/A')}")
        print(f"  Type: {device.get('type', 'N/A')}")
        print(f"  Model: {device.get('model', 'N/A')}")
        print(f"  Connected: {device.get('online', False)}")
        print()


def cmd_cooks(email: str, password: str, status: Optional[str] = None):
    """List cooks."""
    client = MeaterCloudClient(email, password)
    
    if not client.login():
        sys.exit(1)
    
    cooks = client.get_cooks(status=status)
    
    if not cooks:
        print("No cooks found.")
        return
    
    print(f"Found {len(cooks)} cook(s):\n")
    for cook in cooks:
        print(f"Cook: {cook.get('name', 'Unknown')}")
        print(f"  ID: {cook.get('id', 'N/A')}")
        print(f"  Status: {cook.get('status', 'N/A')}")
        print(f"  Device: {cook.get('device_id', 'N/A')}")
        
        tip_temp = cook.get('temperature', {}).get('tip')
        ambient_temp = cook.get('temperature', {}).get('ambient')
        target_temp = cook.get('target_temperature')
        
        print(f"  Meat Temp: {format_temperature(tip_temp)}")
        print(f"  Oven Temp: {format_temperature(ambient_temp)}")
        if target_temp:
            print(f"  Target: {format_temperature(target_temp)}")
        print()


def cmd_monitor(email: str, password: str, device_id: str, interval: int = 10):
    """Monitor a cook via cloud."""
    client = MeaterCloudClient(email, password)
    
    if not client.login():
        sys.exit(1)
    
    print(f"Monitoring device {device_id} (Ctrl+C to stop)\n")
    
    try:
        while True:
            status = client.get_device_status(device_id)
            
            if status:
                tip_temp = status.get('temperature', {}).get('tip')
                ambient_temp = status.get('temperature', {}).get('ambient')
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Meat: {format_temperature(tip_temp)} | "
                      f"Oven: {format_temperature(ambient_temp)}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No data available")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


def main():
    parser = argparse.ArgumentParser(description='Meater Cloud CLI')
    parser.add_argument('--email', '-e', help='Meater account email (or set MEATER_EMAIL)')
    parser.add_argument('--password', '-p', help='Meater account password (or set MEATER_PASSWORD)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Login
    subparsers.add_parser('login', help='Test login credentials')
    
    # Devices
    subparsers.add_parser('devices', help='List registered devices')
    
    # Cooks
    cooks_parser = subparsers.add_parser('cooks', help='List cooks')
    cooks_parser.add_argument('--status', '-s', choices=['active', 'completed', 'aborted'],
                             help='Filter by status')
    
    # Monitor
    monitor_parser = subparsers.add_parser('monitor', help='Monitor cook via cloud')
    monitor_parser.add_argument('--device-id', '-d', required=True, help='Device ID to monitor')
    monitor_parser.add_argument('--interval', '-i', type=int, default=10,
                               help='Update interval in seconds (default: 10)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Get credentials
    email = args.email or os.environ.get('MEATER_EMAIL')
    password = args.password or os.environ.get('MEATER_PASSWORD')
    
    if not email or not password:
        print("Error: Email and password required.", file=sys.stderr)
        print("Set MEATER_EMAIL and MEATER_PASSWORD environment variables", file=sys.stderr)
        print("Or use --email and --password arguments", file=sys.stderr)
        sys.exit(1)
    
    # Execute command
    if args.command == 'login':
        cmd_login(email, password)
    elif args.command == 'devices':
        cmd_devices(email, password)
    elif args.command == 'cooks':
        cmd_cooks(email, password, args.status)
    elif args.command == 'monitor':
        cmd_monitor(email, password, args.device_id, args.interval)


if __name__ == '__main__':
    main()
