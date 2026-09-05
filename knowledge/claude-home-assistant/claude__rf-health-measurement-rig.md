# RF health measurement rig — dashboard, helpers, and method

Built 2026-09-04, to support moving the Zigbee coordinator, the 2.4 GHz AP and a third USB device
off a shared hub extension **one at a time**, with a way to tell whether each move actually helped.
Companion to `thread-matter-commissioning-rf-and-vlan.md` and
`incident-2026-09-02-tarken-thread-partition-split.md`.

Dashboard: **📡 RF Health** at `/rf-health/radios`.

## Why instantaneous readings are useless here

Within about fifteen minutes of observation the weather station's LQI was seen at **80, 196 and 184**,
with a one-hour mean of 130 and a one-hour minimum of 68. Any single glance at the LQI tile would have
"proved" whatever you wanted. Every judgement has to come from a windowed statistic.

## The measurement chain

### Devices being watched

| Radio | Device | Why it is here |
|---|---|---|
| Zigbee | `Home Weather Station` — Shelly *Weather station*, but paired via **Zigbee2MQTT**, IEEE `0xfc4d6afffe23cd9a`, on the Z2M bridge `0xe456acfffe4caa65` (v2.14.1) | The device that was hard to pair; the only Z2M device on this install exposing a `linkquality` entity |
| Thread | `BathroomUP Window` (Tetnet Tarken WM) | Moving the AP changes Thread too; this node already went dark for a day on 09-02 |
| WiFi | Bathroom wall display, Marstek Venus D and E, Ecowater | RSSI as an interference proxy — catches a move that helps Zigbee but hurts WiFi |

### Helpers created

Template sensors (config flow, UI-editable):

- `sensor.weather_station_report_age` — minutes since the station last reported
- `sensor.tarken_report_age` — same for the Thread node

Both use `last_reported`, **not** `last_changed`, so a repeated identical value still counts as a
received packet. Both contain `now()`, which makes Home Assistant re-render them every minute.

Statistics helpers:

| Entity | Source | Characteristic | Window |
|---|---|---|---|
| `sensor.home_weather_station_wx_lqi_avg_15m` | LQI | mean | 15 min |
| `sensor.home_weather_station_wx_lqi_avg_1h` | LQI | mean | 1 h |
| `sensor.home_weather_station_wx_lqi_min_1h` | LQI | value_min | 1 h |
| `sensor.wx_worst_report_gap_1h` | WX report age | value_max | 1 h |
| `sensor.tarken_worst_report_gap_1h` | Tarken report age | value_max | 1 h |
| `sensor.bathroomup_shellywalldisplay_bathroom_wifi_walldisplay_avg_15m` | wall display RSSI | mean | 15 min |
| `sensor.utility_room_marstek_venus_d_wifi_venus_d_avg_15m` | Venus D RSSI | mean | 15 min |

Annotation helpers: `input_select.rf_test_stage` (baseline → coordinator moved → AP moved → third
device moved → final layout → settling) and `input_text.rf_test_note`. The select's own state history
renders as a timeline on the LQI graph, so each segment of the trend is labelled with what was moved.

### Why "worst report gap" is the important metric

LQI describes only the packets that **arrived** — it is silent about the ones that did not. A link can
show a healthy LQI while losing a third of its transmissions. `value_max` of the report-age sensor
over a rolling hour is the largest observed silence, which is the closest thing available to a packet
loss figure without instrumenting the coordinator.

The `count` characteristic was considered for a reports-per-hour metric and **rejected**: the
statistics helper samples on state *changes*, so a run of identical LQI values would be counted once,
not once per report.

## Method

1. Set Stage to *Settling*, move **one** thing.
2. Wait **20 minutes** untouched — the 15-minute window must refill entirely with post-move samples,
   or the reading still contains the old position.
3. Set Stage to the step just performed, and record what moved in the note field.
4. Record LQI avg 15m, LQI min 1h, and worst report gap.

Rules: one change per reading, never compare readings taken less than 20 minutes apart, and check the
WiFi RSSI column before accepting a Zigbee improvement.

Rough scale for LQI (0–255): below ~60 marginal, above ~150 healthy. The **minimum** decides it — a
good mean with a poor minimum is an intermittently dropping link, which is what makes pairing fail.

## Observations at build time

- Zigbee LQI: 15 min mean **143**, 1 h mean **130**, 1 h minimum **68**. The spread is the finding.
- `sensor.tarken_report_age` read **13.8 min**, against an ICD idle poll of 2 min. Worth watching —
  it may be normal subscription behaviour for an unchanged temperature, or it may be early evidence
  the Thread link is still weak. The one-hour worst-gap statistic will settle this.
- `sensor.home_weather_station_voltage` and `_capacitor_voltage` were `unknown` at build time; the
  station had not yet published them. Relevant later, because a solar/capacitor-powered node can drop
  out for power reasons that look exactly like RF problems.
- WiFi baseline: wall display −60 dBm, Venus D −60, Venus E −58, Ecowater −67.

## Physical layout target

Carried onto the dashboard so it is visible while working:

- Each dongle on its **own USB 2.0 extension**, ~1 m from the host, **≥1 m apart** from each other,
  **2–3 m from the AP**, away from USB 3.0 ports/cables and NVMe enclosures.
- Channel plan: WiFi 2.4 GHz **1**, Thread **15**, Zigbee **25**.
- Isolation test: stop the Zigbee2MQTT app for 2–3 minutes and watch the OTBR log. A sharp drop in
  `ChannelAccessFailure` implicates the Zigbee dongle; no change implicates the AP or USB noise.
