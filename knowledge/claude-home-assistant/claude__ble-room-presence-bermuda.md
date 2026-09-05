# BLE Room-Level Presence (Bermuda + Shelly BLE proxies)

Goal: know *which room* a phone is in, not just home/away. Built on the existing Shelly
Gen3/Gen4 fleet acting as Bluetooth proxies, with Bermuda BLE Trilateration consuming their
RSSI reports. No new hardware.

Status 2026-09-02: **live for Matos's Pixel.** Remaining work is the three iPhones and the
four blind rooms.

---

## 1. Bluetooth proxy layer (DONE)

`ble_scanner_mode: active` was set via the Shelly integration options flow on one well-placed
device per room. HA registers each as its own `bluetooth` config entry automatically — no
restart needed for these.

| Area | Device | MAC | Shelly config entry |
|---|---|---|---|
| Kitchen | Int_Button_Kitchen Lights | CC:8D:A2:5E:DD:BA | *(pre-existing)* |
| Living Room | Int_LivingTV2 | CC:8D:A2:64:BC:70 | 01K8SFFNRZ5TAJ0Y32A81RFZW7 |
| Living Room | Int_LivingDining2Down1 | CC:8D:A2:64:0D:00 | 01K8SFX2EZSM0PNQ6FAMTRE1JN |
| Hall entrance | Int_Hallway_2 | CC:8D:A2:46:E8:CC | 01KBNXCNBAYD4R32SVCBSXXRZZ |
| Stairs | Int_HallwayUP Light control | CC:8D:A2:47:43:B0 | 01K0M45B9P7N3R9W837ESHN8WH |
| BathroomUp | Shelly Bathroom extractor | CC:8D:A2:46:E8:B0 | 01JRGH5J41DRG8DZ3S46W8G00W |
| Office | Int_Office_Heating (1PM Mini Gen4) | 7C:2C:67:7B:CA:40 | 01KBJ0ZC8741EJ38CA8PXCTX0W |
| kids Bedroom | Shelly Display kid's Bedroom | 00:A9:0B:13:C5:61 | 01JQMETY3SA8MQS2V5K6B1B0V6 |
| Main Bedroom | Shelly Display Main Bedroom | 00:A9:0B:13:CA:07 | 01JSFET6GZCRSAZX55G5N7NN91 |
| Utility Room | Shelly Display Utility Room | 00:08:22:23:AA:7F | 01JEQ5NMQNPX1GB76YWHB1XG68 |
| Garage | Int_Garage_Door_5 | B0:81:84:A2:2C:B4 | 01KBP08VYZ5M8Q4WH4T83RQV0K |
| Patio | Int_Patio | CC:8D:A2:47:0D:78 | 01K8VHVT4W0B5873A65QSBRZH1 |
| Garage Ext | Int_BackHouse1 | B0:81:84:A2:38:B0 | 01K8SEVR8R9B9GTZPRS7PQ6GYE |

13 proxies total. Verify with `sensor.bermuda_global_total_proxy_count` (13) and
`sensor.bermuda_global_active_proxy_count` (typically 10 — outdoor units with nothing in
range are legitimately silent).

**Rooms with no proxy:** Eva Bedroom, PlayRoom, BathroomDown, Study — no Gen2+ Shelly there.
Shelly Plug S (Gen1) does NOT support BLE gateway, so Main Bedroom / kids Bedroom rely on
their Wall Displays. A Shelly 1PM Mini Gen4 behind any switch closes each gap.

**Why `active` and not `passive`:** active also captures scan-response data, which keeps
device naming and iBeacon resolution reliable. These are all mains-powered Gen3/Gen4 units,
so the extra CPU cost is acceptable. Drop a room to `passive` if that Shelly starts rebooting.

**Side benefit:** the four `xiaomi_ble` LYWSD03MMC temp sensors that were stuck `not_loaded`
now have coverage again.

## 2. Bermuda (DONE)

- Installed via HACS: `agittins/bermuda`, HACS id `676091897`.
- HA restart performed (required — new custom integration).
- Config entry `01M1FKRER0QBV6YJ0P0Y5F77W4`, state `loaded`, global options at defaults.

Options flow, for scripted changes: menu step `selectdevices` takes `configured_devices`
(multi-select of device addresses); menu step `globalopts` takes the seven tuning floats in
§6.

## 3. Phone beacons

Phones rotate their BLE MAC every ~15 min, so they cannot be tracked by MAC. The fix is the
Companion app's **BLE Transmitter**, which broadcasts a fixed iBeacon UUID/Major/Minor.

Companion app → Settings → Companion app → Manage sensors → **BLE Transmitter**:

1. Toggle **Enable Transmitter** on.
2. Keep the same UUID on every phone; give each a unique **Major/Minor**.
3. Advertise mode **Balanced**, transmit power **High**. (Low-latency mode sharpens room
   resolution but costs noticeably more battery.)

Bermuda then lists each phone as `<uuid>_<major>_<minor>`. Tick it in
Settings → Devices & Services → Bermuda → Configure → **Select Devices**.

| Person | Phone | Beacon | Status |
|---|---|---|---|
| Matos | Pixel 10 Pro Fold | `B7D3960CBFD64E74A5E01C3D5C6625FD_100_40004` | DONE 2026-09-02 |
| Lena | iPhone 15 Pro | — | pending |
| Rui | iPhone | — | pending |
| Cristiana | iPhone | — | pending |

**iOS quirk:** the transmitter stops if the Companion app is force-closed from the app
switcher. Tell the iPhone users not to swipe-kill it. If that proves flaky, the alternative
is IRK-based tracking (Bermuda accepts an IRK directly), but extracting an iPhone's IRK
requires a paired Mac.

## 4. Entities

Bermuda generates entity IDs from the raw beacon string, which are unusable. Rename them on
creation to the `<person>_phone_*` pattern:

| Bermuda default | Renamed to |
|---|---|
| `sensor.bermuda_<beacon>_area` | `sensor.matos_phone_room` |
| `sensor.bermuda_<beacon>_floor` | `sensor.matos_phone_floor` |
| `sensor.bermuda_<beacon>_distance` | `sensor.matos_phone_distance` |
| `device_tracker.bermuda_<beacon>_bermuda_tracker` | `device_tracker.matos_phone_ble` |

Device renamed to **Matos Pixel (BLE)** (device id `44a5dd6a0b84c82c49e98f1a4a131bc8`).

`sensor.matos_phone_room` carries `area_id`, `area_name`, `floor_id`, `floor_name` and
`current_mac` as attributes; `device_tracker.matos_phone_ble` carries `scanner` (the Shelly
that currently hears it loudest) and `area`.

## 5. Dashboard

`/ble-presence` — **Presence**, `mdi:map-marker-radius`, in the sidebar. Two views:

- **Where** (`/ble-presence/where`) — live room/floor/distance tiles, a templated floor map
  that pins the current room against the scanner covering it, 24 h room history, 12 h
  distance graph, and a logbook of room changes.
- **How it works** (`/ble-presence/how`) — the iBeacon → Shelly proxy → Bermuda chain
  explained, Bermuda's global health counters, known limits, how to add another phone, and
  the calibration procedure.

**Maintenance note:** the floor-map card's room list is hardcoded Jinja inside the markdown
card on the *Where* view. Adding a proxy to a new room means editing that list too.

## 6. Tuning reference

Bermuda global options (all at defaults):

| Field | Default | Note |
|---|---|---|
| `max_area_radius` | 20.0 m | Generous on purpose — avoids `unknown` in the four blind rooms, at the cost of room bleed |
| `max_velocity` | 3.0 m/s | Rejects impossible jumps |
| `devtracker_nothome_timeout` | 30 s | Silence before `not_home` |
| `update_interval` | 10.0 s | Re-evaluation cadence |
| `smoothing_samples` | 20 | Rolling window |
| `attenuation` | 3.0 | Path-loss exponent |
| `ref_power` | -55.0 dBm | Expected RSSI at 1 m |

Fix wrong-room errors with *Calibration 2: Scanner RSSI Offsets* (hold the phone 1 m from
each proxy in turn) before touching radii — back-box depth varies the per-Shelly offset by
~10 dB and that dominates the error.

## 7. Not done yet

- Three iPhones (§3).
- Proxies for PlayRoom, Eva Bedroom, BathroomDown, Study.
- RSSI offset calibration — untouched, so early room assignments will be rough.
- No automations built on this yet.
