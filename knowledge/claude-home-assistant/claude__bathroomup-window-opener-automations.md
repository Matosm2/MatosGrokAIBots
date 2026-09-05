# BathroomUP Window opener — entities, automations, and design decisions

Built 2026-09-03. Device: **Tetnet Tarken WM**, hw Rev4, sw 3.0.1+0, Matter over Thread, battery-powered
sleepy end device (ICD idle poll 120 s). Area: BathroomUp. Device id `d7018721eaf6cf487435e9033d030d8e`.

## Three hard findings, discovered while building

### 1. The `script:` domain is not loaded on this install
There are **zero `script.*` entities** in the whole system. `ha_config_set_script` writes to
`scripts.yaml` successfully (watchman can see the entries in the file), but no entity is ever
registered, and `script.reload` changes nothing — `configuration.yaml` has no
`script: !include scripts.yaml` line.

Consequence: reusable open/close scripts are impossible, so **all window logic is inlined into the
automations**. If the include is ever added, the shared logic should be refactored back into
`script.bathroomup_window_open` / `_close` with `position` / `reason` variables.

### 2. `current_position` is effectively binary; `target_opening_position` is the honest readback
`cover.bathroomup_bathroomup_window` advertises `supported_features: 15`
(OPEN + CLOSE + SET_POSITION + STOP), and `cover.set_cover_position` **is** accepted —
`sensor.bathroomup_bathroomup_window_target_opening_position` correctly showed `45` after a 45 %
command. But `current_position` reported `100` and stayed there through several poll cycles.

So HA cannot confirm a partial opening. Partial positions are commanded but unverifiable.
This is one more reason the winter strategy below uses **full-open bursts** rather than a long
partial crack: full open is the one position we can actually verify.

### 3. The air-quality enum is not severity-ordered
`sensor.bathroomup_bathroomup_window_air_quality` options are
`['extremely_poor','very_poor','poor','fair','good','moderate']`. Never sort or compare against it.
All logic uses the numeric CO2 sensor instead.

## Winter heat-loss strategy: burst ventilation, not a long crack

Air carries almost no heat compared with the tiles, screed and walls. A **6-minute full-open
exchange** swaps essentially all the moist air while the thermal mass stays warm, so the room
re-heats mostly for free. A 45-minute crack instead chills the wall surfaces — expensive to reheat,
and cold surfaces are exactly where condensation and mould form.

Layered so the cheapest measure always goes first:

1. **Extractor leads.** The fan is turned on before any window action in every humidity path.
   Moving air with a fan costs far less than dumping heated air.
2. **Grace delay** (`input_number.bathroomup_window_leave_delay`, default 15 min) — the fan gets
   ~17 minutes to solve it alone before the window is considered at all.
3. **Re-check after the grace.** If humidity fell below 76 %, or the weather turned, nothing opens.
4. **Physics gate.** `binary_sensor.bathroomup_window_drying_ok` requires outdoor dew point to be at
   least 1.5 °C below indoor dew point. Relative humidity alone lies — on a muggy night, opening
   makes the room wetter.
5. **Mode split** on `input_number.bathroomup_window_winter_below` (default 12 °C outdoor):
   - **Cold** → up to 3 × (full open for `burst_minutes`, close, 8-minute recovery pause), stopping
     early once humidity < 74 %. The pause lets the surfaces give their moisture back so the next
     burst carries it out.
   - **Mild** → open to `vent_position` until humidity < 72 % for 5 min, hard capped at 45 min.
6. **Heating is off the whole time**, owned by the interlock below.

## No time gating, and no sleep-mode gate

Both removed at Matos's request (sleep mode 2026-09-03, clock cut-offs 2026-09-04). The window is on
the **first floor**, so an open sash is not a security concern, and overnight ventilation is wanted.
What was taken out:

- `input_boolean.sleepmode` — gone from every window automation, trigger and condition alike, and
  from the dashboard's decision-gate section.
- The **22:30 `condition: time` cut-off** on the humidity vent, CO2 vent and cooling automations.
- The **23:30 curfew trigger** on Safety Close, and its entry in the notification reason map.
- The **18:00 start** on evening cooling (it now runs on physics alone; the 20:30 time trigger
  remains as the usual entry point, so the alias still says "Evening").

**What still bounds an open window** — this is now the complete list, so do not weaken any of it
without adding a replacement:

| Bound | Where |
|---|---|
| 45-minute cap on a mild-weather humidity vent | `wait_for_trigger` timeout |
| 3 bursts max in cold weather | `repeat: count: 3` |
| 40-minute cap on a CO2 vent | `wait_for_trigger` timeout |
| 55-minute cap on a cooling run | `wait_for_trigger` timeout |
| 30-minute cap on a post-bath purge | `wait_for_trigger` timeout |
| **60-minute maximum-open watchdog** | Safety Close, `to: open for: 60 min` |
| Rain, wind > 35 km/h, outdoor < 2 °C, everyone away, HA restart | Safety Close triggers |

The 60-minute watchdog is the only unconditional one. It is now load-bearing.

## Live status readout — "why is it open, and for how long"

Added 2026-09-04. With the clock gates gone, finding the window open at an odd hour raises two
questions the dashboard could not previously answer. Three template sensors answer them:

| Entity | What it does |
|---|---|
| `sensor.bathroomup_window_driver` | Which automation is holding it open — Shower vent / CO2 vent / Cooling / Post-bath purge / **Manual - no automation running** / Closed / Unavailable |
| `sensor.bathroomup_window_open_for` | Minutes since the cover last opened |
| `sensor.bathroomup_window_closes_in` | Minutes until the governing cap fires |

The driver is read from each automation's `current` attribute (running-instance count), **not** from
`last_triggered` — a stale `last_triggered` would keep naming an automation that finished hours ago.

`closes_in` re-encodes the bounds table above: it picks the cap belonging to whichever automation is
running, substitutes `burst_minutes` when the outdoor temperature is below `winter_below`, takes the
smaller of that and the 60-minute watchdog, and subtracts the elapsed open time. **This duplicates
the timeouts that live inside the automations** — if a `wait_for_trigger` timeout is ever changed,
this sensor must be changed to match, or the dashboard will confidently display the wrong number.

The **Manual** case is the valuable one: cover open with no automation running means nothing will
close it early, and only the 60-minute watchdog applies. That is exactly the state worth spotting.

All three contain `now()`, so Home Assistant re-renders them every minute.

The Window view opens with a **Right now** section: a markdown card that states what is holding the
window open, how long it has been open, the latest closing time, and — per driver — the specific
condition that would close it early, with that condition's live value alongside it. So a shower vent
shows the humidity it is waiting to fall, a cooling run shows the room temperature and the gain.

## Helpers created

| Entity | Purpose |
|---|---|
| `input_boolean.bathroomup_window_auto` | Master enable for all automatic opening |
| `input_boolean.bathroomup_heating_suspended` | Records that *we* turned the heating off |
| `input_number.bathroomup_window_leave_delay` | Grace before opening, default **15 min** |
| `input_number.bathroomup_window_vent_position` | Mild-weather position, default 45 % |
| `input_number.bathroomup_window_burst_minutes` | Winter burst length, default 6 min |
| `input_number.bathroomup_window_winter_below` | Outdoor °C below which bursts are used, default 12 |
| `input_text.bathroomup_window_reason` | Last action + why, surfaced on the dashboard |
| `sensor.bathroomup_dew_point` | Indoor dew point (Magnus) from the Tarken's temp + RH |
| `sensor.bathroomup_cooling_gain` | Indoor − outdoor °C, so the 3 °C margin is a native condition |
| `sensor.bathroomup_window_driver` | Which automation is holding the window open |
| `sensor.bathroomup_window_open_for` | Minutes the cover has been open |
| `sensor.bathroomup_window_closes_in` | Minutes until the governing cap fires |
| `binary_sensor.bathroomup_window_is_open` | Cover position > 0 **OR** UniFi reed contact on |
| `binary_sensor.bathroomup_window_weather_ok` | No rain, wind < 35 km/h, outdoor > 2 °C, device online |
| `binary_sensor.bathroomup_window_drying_ok` | Outdoor dew point ≥ 1.5 °C below indoor |

All template helpers were created through the config flow (UI-editable), not `template:` YAML.

## Automations

| Automation | Mode | What it does |
|---|---|---|
| `bathroomup_window_open_close_heating` (rewritten) | queued | Sole owner of the heating interlock |
| `bathroomup_window_safety_close` | queued | Rain, wind, freeze, away, HA restart, 60-min watchdog |
| `bathroomup_window_humidity_vent_shower` | restart | The shower vent, with the 15-min grace and winter bursts |
| `bathroomup_window_co2_vent` | restart | Above 1200 ppm for 10 min, closes below 900 |
| `bathroomup_window_evening_cooling` | restart | Free cooling when indoor > 25 °C and gain > 3 °C |
| `bathroomup_window_bath_time_hook` | restart | Closes on bath start, purges after bath end |
| `bathroomup_window_actuator_verification` | queued | Tarken's report vs the independent UniFi reed |
| `bathroomup_window_device_health` | queued | Offline, recovered, battery, device problem flag |

### Why the heating interlock was rewritten

The original triggered on `binary_sensor.window_bathroomup_contact` and did
`scene.create` → `climate.set_hvac_mode: off` on every open, restoring on every close. Two latent bugs:

- **A partial motorised opening may not break the reed contact**, so the heating would keep running
  with the window open. Now driven by `binary_sensor.bathroomup_window_is_open`, which is contact
  **OR** cover position.
- **Double-snapshot could strand the heating off forever.** If a second open event fired while the
  thermostat was already off, `scene.create` would snapshot the *off* state, and the next close
  would faithfully restore "off" — permanently. `input_boolean.bathroomup_heating_suspended` now
  records that we were the ones who suspended it; the snapshot only happens when the thermostat is
  actually running, and the restore only happens when our flag is set.

### Why the actuator verification matters here
A motorised opener can report success while the sash is jammed, iced, or blocked by a towel, and
everything downstream then trusts a lie. The open check only fires above 40 % so a tilt-open that
keeps the reed magnets close cannot raise a false alarm. The close check is the important half: if
Safety Close believes it shut the window and it did not, the house is open to rain — that branch
retries once, then notifies.

### Sensor choice
Triggers use `sensor.sensor_temp_bathroom_humidity` (the same sensor as the existing extractor pair)
and `sensor.shellywalldisplay_bathroom_temperature` for room temperature. Both are mains-powered and
update promptly. The Tarken's own temp/RH sit on the sleepy Thread node behind a 2-minute poll and
lag; they are used for CO2, dew point and display only.

Note the three bathroom humidity sensors disagree materially (Tarken 76 %, sensor_temp 70 %, wall
display 50 % at the same moment). Thresholds are calibrated to `sensor_temp` and are not portable
to the others.

## Dashboard

`dashboard-bathroomup` gained a second view at `/dashboard-bathroomup/window` (the existing view
now has the stable path `room`). Sections: **Right now** (live status card + driver / open-for /
closes-in tiles), Window control, Vent now (25/45/100/close buttons), Air (with a 24 h
humidity-vs-position-vs-fan history graph), "Why it will or will not open" (every gate as a tile),
Tuning (the four sliders), Device health, and an automation toggle list.

## Verified live

**2026-09-03 — heating interlock, end to end on the real device:**

1. Close with flag off → no stale restore fired. Heating stayed `heat` @ 22 °C, preset `home`. ✅
2. Open → snapshot created, `climate` → `off`, `suspended` → `on`. ✅
3. Close → `climate` restored to `heat` @ 22 °C preset `home`, `suspended` → `off`. ✅

**2026-09-04 — status readout, against a live cooling run:** driver `Cooling`, open 33 min,
closes in 22 min, cap 55 min, matching the automation's `wait_for_trigger` timeout exactly.

All 8 automations load and are `on`; all traces finished cleanly with no errors.

## Open items

- Add `script: !include scripts.yaml` to `configuration.yaml` if reusable scripts are wanted anywhere.
- **The outdoor weather station is now live** (2026-09-04) — a Shelly *Weather station* paired over
  Zigbee2MQTT, not the Shelly WiFi integration. It exposes
  `binary_sensor.home_weather_station_rain_status` (device_class moisture) and
  `sensor.home_weather_station_rain_rate`: **real local rain detection**, which the window
  automations do not yet use. They still rely on `weather.forecast_home` (met.no) alone. With clock
  curfews removed, wiring the local rain sensor into `binary_sensor.bathroomup_window_weather_ok`
  and as a Safety Close trigger is the highest-value remaining improvement. Watch the units when
  doing it: the station reports wind in **m/s**, the forecast in **km/h**, and the existing guards
  use a 35 **km/h** threshold — 35 m/s is 126 km/h and would never fire.
- Cooling effectiveness looks poor: during the 2026-09-04 run the room sat at 27.1–27.2 °C against
  19.6 °C outside (gain 7.6 °C) and was not falling after 33 minutes. Either the commanded 50 %
  opening is not physically happening (see finding 2), or 50 % simply moves too little air. Worth a
  controlled comparison against a full-open run before trusting the cooling automation.
- Pre-existing unrelated error, seen while checking logs: `configuration.yaml` lines 54/62/70/78 —
  `'friendly_name' is an invalid option for 'template'`, four template sensors failing to load.
