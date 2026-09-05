# Thread / Matter commissioning: RF plan, VLAN constraint, Matter Thread dataset

Status: two of three blockers cleared (2026-09-01). Remaining: RF interference.
Trigger: commissioning a Tarken window actuator (Matter-over-Thread, no Wi-Fi fallback) failed from the HA companion app.

## Infrastructure facts

- OTBR add-on 3.1.2 on **ZBT-1 / SkyConnect** (`usb-Nabu_Casa_SkyConnect_v1.0_3c5974b15541ed11a7ba7ea7ccf2b06c-if00-port0`), 460800 baud, hardware flow control.
- Zigbee2MQTT 2.13.0 on **ZBT-2** (`usb-Nabu_Casa_ZBT-2_DCB4D90B9168-if00`), adapter `ember`, Zigbee **channel 25**. Separate USB ports.
- Thread network `ha-thread-30a2`, extPanId `935dad539f109af8`, panId 12450 (0x30a2), **channel 15**, created 2024-10-31, `preferred: true`.
- Matter Server add-on 9.2.0 (`matter-server/1.4.0`, matter.js 0.17.9), fabric_id 2. **10 Matter nodes**, which surface as 32 HA devices / 102 entities because node `@1:5` is a bridge that fans out into many devices. All 10 are **Wi-Fi** (SSID SMM); none are Thread.
- HA host `192.168.10.20/25`. IOT VLAN `192.168.20.0/24` (SSID "SMM IOT").

## Blocker 1 — RF collision (Thread ch 15 vs Wi-Fi ch 6) — OPEN

OTBR log is a continuous wall of `P-RadioSpinel-: Handle transmit done failed: ChannelAccessFailure`, roughly one every 10 s, with no other content. CCA sees the channel permanently busy, so the border router cannot transmit and no joiner can be answered.

| Radio | Channel | Band / centre |
|---|---|---|
| Wi-Fi 2.4 GHz | 6 | 2426–2448 MHz |
| Thread (802.15.4) | 15 | 2425 MHz |
| Zigbee (802.15.4) | 25 | 2475 MHz |

Thread sits 1 MHz below the AP's band edge, inside its spectral leakage. Zigbee on 25 is unaffected — which is why Zigbee works and Thread does not.

**Decision:** move the 2.4 GHz AP from channel 6 to **channel 1** (2401–2423), keeping Thread on 15 and Zigbee on 25 — the textbook-clean layout. Alternative if that is not enough (e.g. neighbouring APs on ch 1): re-form Thread on **channel 11** (2405 MHz), which is free today because the mesh is empty.

**Verification:** the `ChannelAccessFailure` lines in the OTBR add-on log must stop.

**If they do not stop after the channel move**, interference is eliminated and the next suspect is the ZBT-1's RCP firmware or the serial link — re-flash the dongle.

## Blocker 2 — Matter Server had no Thread dataset — RESOLVED

`data.server.info` reported `thread_credentials_set: false`. A controller with no operational dataset cannot send `AddOrUpdateThreadNetwork` during commissioning, so it can never onboard a Thread device — regardless of phone, VLAN or radio. An earlier attempt on 2026-08-30 03:40 failed with:

```
set_thread_dataset → Invalid Thread operational dataset:
must be a non-empty hex string with even length
```

HA had handed the server an empty string. The OTBR's own dataset was fine all along.

**Fix applied 2026-09-01.** Pull the active dataset TLV from the OTBR REST API and push it into the Matter Server:

1. `GET http://<otbr>:8081/node/dataset/active` with `Accept: text/plain` → returns the hex TLV.
2. HA websocket command **`matter/set_thread`** with `{"thread_operation_dataset": "<hex TLV>"}`.

Note the command is `matter/set_thread`, **not** `matter/set_thread_dataset` (that name is the matter-server-side handler and is rejected by HA as "Unknown command").

Confirmed afterwards: `thread_credentials_set: true`. No reload or restart was needed, so the 32 existing Matter devices were never interrupted.

**This must be re-done whenever the Thread dataset changes** (channel change, network re-form).

## Blocker 3 — VLAN split blocks mDNS — ruled out as primary, still relevant

Matter commissioning is mDNS-driven (UDP 5353, link-local multicast, TTL 1 — does not route between VLANs):

- `_meshcop._udp` — the OTBR border agent. Google's "checking connectivity with ha-thread-30a2" step is this lookup.
- `_matterc._udp` — the commissionable device.

Commissioning was tested from both the IOT VLAN and the main VLAN with the same failure, so this was not the deciding factor. Keep in mind for the future:

- **Thread** devices need cross-VLAN mDNS only during commissioning; afterwards HA reaches them over the Thread mesh via the border router.
- **Wi-Fi** Matter devices need it permanently.

Options if it ever bites: commission from HA's VLAN (no infrastructure change), or run an mDNS reflector between VLAN 10 and 20 with rules for UDP 5353 both ways, UDP 5540 (Matter operational) and the border agent port — at the cost of weakening the IOT isolation.

## Blocker 4 — Android companion app does not sync Thread credentials — RESOLVED

On Android the HA companion app does not push Thread credentials to Google Play Services automatically (open upstream bug, home-assistant/android#5805). Without it, commissioning fails with "Your device requires a Thread border router" even though OTBR is running and preferred.

Fix: **HA app → Settings → Companion app → Troubleshooting → Sync Thread credentials**. Re-run this whenever the Thread dataset changes.

## Remaining sequence

1. Move the 2.4 GHz AP to channel 1; confirm `ChannelAccessFailure` stops in the OTBR log.
2. Re-run "Sync Thread credentials" in the HA app.
3. Pair the Tarken within a couple of metres of the ZBT-1.
