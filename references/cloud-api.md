# Meater Cloud API Reference

## Overview

The Meater Cloud API allows remote access to your Meater probes via WiFi (when using Meater Block) or through the Meater app's cloud sync feature.

## Authentication

Meater Cloud uses **Firebase Authentication**.

### Login Endpoint

```
POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}
```

**Request Body:**
```json
{
  "email": "your@email.com",
  "password": "your_password",
  "returnSecureToken": true
}
```

**Response:**
```json
{
  "idToken": "eyJhbGciOiJSUzI1...",
  "email": "your@email.com",
  "refreshToken": "AEu4IL2...",
  "expiresIn": "3600",
  "localId": "user_id_here"
}
```

The `idToken` is used as a Bearer token for subsequent API calls.

## Base URL

```
https://public-api.cloud.meater.com/v1
```

## Endpoints

### List Devices

```
GET /devices
Authorization: Bearer {idToken}
```

**Response:**
```json
{
  "data": [
    {
      "id": "probe_id_here",
      "name": "My Meater Probe",
      "type": "meater_plus",
      "model": "MEATER+",
      "online": true,
      "last_seen": "2024-01-15T14:30:00Z"
    }
  ]
}
```

### Get Device Status

```
GET /devices/{device_id}/status
Authorization: Bearer {idToken}
```

**Response:**
```json
{
  "data": {
    "id": "probe_id",
    "online": true,
    "battery": 85,
    "temperature": {
      "tip": 68.5,
      "ambient": 180.2,
      "target": 71.0
    },
    "cook": {
      "id": "cook_id",
      "name": "Steak",
      "status": "active"
    }
  }
}
```

### List Cooks

```
GET /cooks?status={active|completed|aborted}
Authorization: Bearer {idToken}
```

**Response:**
```json
{
  "data": [
    {
      "id": "cook_id",
      "name": "Ribeye Steak",
      "status": "active",
      "device_id": "probe_id",
      "created_at": "2024-01-15T14:00:00Z",
      "temperature": {
        "tip": 68.5,
        "ambient": 180.2,
        "target": 71.0
      }
    }
  ]
}
```

### Get Cook Details

```
GET /cooks/{cook_id}
Authorization: Bearer {idToken}
```

### Get Cook History

```
GET /cooks/history?limit={n}
Authorization: Bearer {idToken}
```

## Temperature Data

All temperatures are returned in **Celsius**.

| Field | Description |
|-------|-------------|
| `tip` | Internal meat temperature |
| `ambient` | Oven/grill temperature |
| `target` | Target temperature (if set) |

## Device Status Values

| Status | Description |
|--------|-------------|
| `online` | Device connected and reporting |
| `offline` | Device not connected |
| `cooking` | Active cook in progress |
| `idle` | Device on but not cooking |

## Cook Status Values

| Status | Description |
|--------|-------------|
| `active` | Cook in progress |
| `completed` | Target temperature reached |
| `aborted` | Cook cancelled |
| `paused` | Cook paused |

## Rate Limits

- 100 requests per minute per user
- WebSocket connections: 1 per device

## Notes

### WiFi vs Bluetooth

| Method | Range | Updates | Best For |
|--------|-------|---------|----------|
| Bluetooth | 10-165 ft | Real-time | Local monitoring |
| Cloud/WiFi | Unlimited | ~10 sec delay | Remote monitoring |

### Meater Block

Meater Block acts as a WiFi bridge:
1. Block connects to probes via Bluetooth
2. Block connects to your WiFi network
3. Data syncs to Meater Cloud
4. Access from anywhere via Cloud API

### App Requirement

For cloud access without a Meater Block:
- Meater app must be running and syncing
- Phone must have internet connectivity
- Probe must be in Bluetooth range of phone

## Official Resources

- Meater Website: https://www.meater.com
- Meater App: iOS and Android (required for cloud sync)
- Support: https://help.meater.com
