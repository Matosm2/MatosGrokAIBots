# Notification log & "Notifications Live" dashboard

Built 2026-09-01. Answers: *"what has the house been telling me while I didn't have my phone?"*

## The problem

Home Assistant does not persist push notifications. `notify.mobile_app_*` is
fire-and-forget — there is no entity, no history, no card. Any notification
dashboard has to build its own store first.

`notify.notify` is not used anywhere in this instance; all ~36 alerting
automations call a specific `notify.mobile_app_<device>` service directly. That
makes a `call_service` event trigger a complete interception point.

## Architecture

```
automation fires notify.mobile_app_pixel_10_pro_fold
        │
        ▼  (HA emits a `call_service` event on the bus)
automation.notification_logger_phones
        ├─► 12 rotating input_text slots   → "Now" feed (survives restarts)
        ├─► logbook.log vs input_boolean.notification_feed → "History" view
        ├─► counter.notifications_today
        └─► counter.notifications_critical_today (keyword match)
```

Firing a synthetic `call_service` event with `ha_call_event` exercises the whole
chain **without sending a real push** — that is how this was tested at 01:30.

## Objects created

| Object | Purpose |
|---|---|
| `input_text.notif_log_01` … `_12` | Rotating feed store, 255 chars each |
| `input_boolean.notification_feed` | Never toggled; exists only as the logbook anchor so `logbook.log` entries have an entity to attach to and the logbook card can filter on it |
| `counter.notifications_today` | All pushes since 00:00 |
| `counter.notifications_critical_today` | Alert-keyword pushes since 00:00 |
| `input_datetime.last_notification` | Freshness stamp |
| `automation.notification_logger_phones` | The interceptor, `mode: queued`, `max: 30` |
| `automation.notification_counters_nightly_reset` | Zeroes both counters at 00:00 |
| Dashboard `notifications-live` | Views: `now`, `history`, `house`, `stats` |

## Slot record format

Pipe-triple delimited, chosen because `~|~` will not appear in notification text
and does not collide with markdown table syntax:

```
2026-09-02T01:30:07+02:00~|~🧺~|~Lena~|~🧺 Washing machine finished~|~Cycle done at 22:03 — 1.24 kWh used.
      timestamp            cat   device        title (≤60)                    message (≤120)
```

Total stays under the 255-char `input_text` limit. `relative_time(as_datetime(p[0]))`
renders "12 minutes ago" from field 0.

## Scope

Logged: Matos (Pixel 10 Pro Fold), Lena, Rui, Cristiana, and the three duty
phones — one event trigger per service, `trigger.id` carries the display name.

Deliberately excluded: `mobile_app_kitchen_display`, `firetablet_new`,
`firetablet_old`, `tablet_samsung`, `pixel_tablet`, `screen_bathroom`. Wall
displays receive far more traffic than phones and would drown the 12-slot feed.

Filtered out by condition: empty messages, `clear_notification`, `delete_alert`,
`remove_channel`, `request_location_update`, anything starting `command_` or
`TTS`. Only pushes a human would actually have seen get logged.

## Category classification

Keyword match on `(title ~ ' ' ~ message) | lower`, first match wins:

🔴 critical (`alert fault offline unreachable problem leak fail error critical alarm shortfall deadlock stuck down`, plus the 🔴 and ⚠️ glyphs) →
🧺 laundry → 🚗 EV → 🔋 battery → ☀️ solar → 💧 water → 🧊 freezer →
🤖 vacuum/mower → 💶 price → 🔔 default.

The 🔴 category is what the *History → Alerts only* card filters on and what
increments the critical counter.

## Live-status panel wiring

The *Needs attention* card is a hand-rolled Jinja list rather than
`custom:auto-entities`, because the alert set mixes on-means-bad and
off-means-bad polarity and enum comparisons:

| Source | Bad when |
|---|---|
| `input_boolean.marstek_fleet_unreachable` | `on` |
| `input_boolean.marstek_delivery_fault` | `on` |
| `input_boolean.marstek_backup_alert_d` / `_e` | `on` |
| `input_boolean.freezer_alert_active` | `on` |
| `binary_sensor.ecowater_leak_alert` | `on` |
| `binary_sensor.utility_room_marstek_venus_d/e_modbus_connection` | `off` |
| `sensor.inverter_alarms` | not `None` |
| `sensor.inverter_device_status` | not `On-grid` |
| `sensor.utility_room_hw_p1meter_grid_import_daily` | `unknown`/`unavailable` |

Renders "✅ All clear" when the list is empty.

## Sign conventions used in the "At a glance" card

- `sensor.power_meter_active_power` — **negative = importing**, positive = exporting
- `sensor.batteries_charge_discharge_power` (Huawei) — positive = charging
- `sensor.marstek_battery_power_kw` — positive = charging (matches the Modbus
  integration mapping in `energy-battery-architecture.md`)

Verified against a live sample: PV 0 W, Tesla drawing 3.5 kW at 01:30 → power
meter read −4007 W.

## Gotchas hit while building

- **Do not escape `|` inside `{{ }}` for markdown tables.** Jinja renders before
  the markdown parser runs, so a filter pipe never reaches the table syntax. A
  `\|` inside an expression is a Jinja syntax error. This bit once and was fixed
  with a `python_transform`.
- Markdown card line breaks need **two trailing spaces**, not a bare newline.
- Markdown cards need an explicit `entity_id:` list when the template reads
  entities through a loop variable — auto-detection cannot see `states(s)`.
- The logbook card key is `target: {entity_id: [...]}`. `entities:` is not in
  the current schema.
- `ha_config_set_automation` flags the event-payload template condition as an
  anti-pattern. It is a false positive — no native condition can inspect
  `trigger.event.data.service_data`.
- The service-registry validation warnings on `event_data.service` are also false
  positives; those are bare service names inside event data, not `domain.service`.

## Extending

To add a device, add one more event trigger with a new `id` — nothing else
changes. To keep more than 12 entries in the feed, add slots and extend the
shift chain (the logbook already holds the full recorder-length history, so the
slot count only governs the pretty feed).
