# Incident 2026-09-04 — House shutters stayed open after dark

**Window:** 16:47 → 21:05 local (Europe/Brussels)
**Impact:** All Somfy/Overkiz shutters (fireplace, living room W, living room S, kitchen, garage) stayed fully open (position 100) through dusk and ~40 min past full dark. Hall entrance window and main bedroom curtains closed normally (different integration).

## Timeline

- **16:47:33** — All Overkiz cover entities go `unavailable`. `pyoverkiz.client` starts logging `ClientConnectorDNSError: Cannot connect to host gateway-2072-8303-5497.local:8443 [MDNS lookup failed]` — 224 occurrences up to 20:57:18.
- **20:29:00** — `automation.close_windows_sunset` triggers (illuminance dusk / night watchdog), takes the **normal** branch (sunset + <2h).
- **20:20–20:35** — Every `cover.set_cover_position` / `cover.close_cover` in the sequence fails silently: `homeassistant.helpers.service: Referenced entities cover.shutter_* are missing or not currently available` (11x fireplace, 11x LR W, 11x LR S, 3x kitchen). No automation error, no notification — the run continued as if it had worked.
- **20:36** — Hall entrance window and main bedroom curtains close (not Overkiz, so unaffected).
- **20:36 →** — Run enters the parallel garage branch: `wait_for_trigger` on `binary_sensor.door_garage_contact → off`, timeout 30 min. The contact has read `on` (open) since the 15:36 restart, so the run **holds `mode: single` until ~21:06**.
- **20:57:34** — Overkiz recovers (DNS/gateway reachable again). All five shutters reappear reporting `open` / position 100.
- **20:58 → 21:02** — The 1-minute night watchdog fires every minute and is rejected: 5 consecutive traces with `execution: failed_single`. The recovery path is blocked by the still-running 20:29 execution.
- **~21:03** — Manual `cover.close_cover` on fireplace, LR W, LR S, kitchen. Garage left open (door contact still reads open).

## Root cause

Two independent faults compounding:

1. **Overkiz gateway unreachable via mDNS for ~4h10m.** `gateway-2072-8303-5497.local` did not resolve, so the local API was unreachable and every cover went `unavailable`. Service calls against unavailable entities are a **warning, not an error** in HA — the closing automation therefore reported success.
2. **The watchdog cannot self-heal while the garage branch is waiting.** `mode: single` + a 30-minute `wait_for_trigger` on the garage door contact means one failed run suppresses up to 30 minutes of 1-minute retries. Recovery at 20:57 could not be acted on until ~21:06.

Contributing: `binary_sensor.door_garage_contact` has read `on` since 15:36:25, which is what arms the 30-minute wait every single run.

## Fix candidates

- **Verify the close actually happened.** After the closing block, re-check the covers and re-issue / notify if any is not `closed`. Cheapest version: a `repeat until` around the close actions, or a post-close verification step like the one in `ev-charge-control-and-actuator-verification`.
- **Guard on availability.** Add a condition that at least one Overkiz cover is not `unavailable` before running the sequence, and notify (rather than silently no-op) when they are.
- **Stop the garage wait from blocking the watchdog.** Move the 30-minute `wait_for_trigger` out of `close_windows_sunset` into its own `mode: single` automation triggered on `door_garage_contact → off`. The closing automation then finishes in ~7 min instead of up to 37, and the 1-min watchdog stays live.
- **Check the garage door contact.** 5.5 h of continuous `on` is either a genuinely open door or a stuck/dead sensor; it silently changes the automation's runtime profile.
- **Watch the mDNS dependency.** If `.local` resolution is flaky on this network, pin the Overkiz gateway to a static IP / hostname instead of mDNS discovery. Relates to `thread-matter-commissioning-rf-and-vlan` and `config-drift-watchdogs`.
