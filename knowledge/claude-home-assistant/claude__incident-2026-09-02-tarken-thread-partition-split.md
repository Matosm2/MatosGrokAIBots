# Incident 2026-09-02 — Tarken window actuator offline: Thread mesh partition split

Status: OPEN. Device commissioned successfully but unreachable since 2026-09-02 03:32 local.

## Device

- `BathroomUP Window` — Tetnet **Tarken WM**, hw Rev4, sw 3.0.1+0, serial 10281, device_id `d7018721eaf6cf487435e9033d030d8e`.
- Matter node **`@1:4b`** (node id 0x4B), `network_type: thread`, `node_type: sleepy_end_device`, `available: false`.
- ICD profile from the Matter Server: `isIntermittentlyConnected: true`, `idleModeDuration: 120000` (2 min poll), `isBatteryPowered: true`, `threadChannel: 15`.
- 17 entities, all `unavailable` since **2026-09-02 03:32:14**.

## Timeline

| Local time | Event |
|---|---|
| 09-02 03:14:36 | First states appear — commissioning succeeded (boot reason `power_on_reboot`) |
| 09-02 03:15:58, 03:16:56 | Two brief unavailable/available flaps |
| 09-02 03:16:56 | Last good report: battery 100 %, Thread channel 15, routing role `sleepy_end_device` |
| 09-02 03:32:14 | Went `unavailable` and never returned |
| ~09-02 04:26 | OTBR restarted (inferred from add-on uptime clock) |
| 09-03 03:21 | Matter Server + OTBR restarted; OTBR came up as **leader of a brand-new partition `0xcfc16b7` with no children**; `@1:4b` did not return |

## Root cause — two border routers on the same Thread network, split across VLANs

Thread integration diagnostics for network `935dad539f109af8` (`ha-thread-30a2`) list **two** routers:

| Router | Address | VLAN | Neighbour state |
|---|---|---|---|
| `homeassistant-otbr.local.` (ZBT-1) | 192.168.10.20 | 10 (main) | state 64, probes 0 |
| `gw2-fbeebbe594ba.local.` (**IKEA DIRIGERA**) | 192.168.20.120 | 20 (IOT) | **state 1, probes 6** — unreachable |

The DIRIGERA has joined the same Thread network but sits on the IOT VLAN, so the two border routers have no IPv6/backbone connectivity to each other. The mesh split into two partitions — 85 log lines of:

```
[N] Mle-----------: Different partition (peer:1311993566, local:2102372517)
```

After the 09-03 restart the OTBR logged `Attach attempt 1, AnyPartition reattaching with Active Dataset` and then went straight to **leader** of a fresh partition — i.e. it found no reachable partition to merge with, confirming the isolation.

## Reconnect evidence — all attempts are HA → device, none from the device

- **227** `PeerConnection … [network-unreachable] send ENETUNREACH` lines. The Matter Server retries `@1:4b` on a **2-minute cadence**, indefinitely.
- It cycles the two cached OMR addresses: `fdde:f379:1470:1:bf51:5339:7035:e8ea` (used through 09-02) and `fda7:2c72:3976:1:4210:9729:61ab:bdb5` (after the 09-03 restart). Neither is in HA's partition, whose advertised on-mesh prefix is `fdf7:f6d1:8c85:2352::/64` — so the failure is `ENETUNREACH` at the host kernel: no route at all, the packet never leaves the box.
- `IpServiceStatus @1:4b Resolving (no address known)` — the mDNS `_matter._tcp` lookup returns nothing, because the SRV record would be published by the DIRIGERA on VLAN 20.
- **Nothing from the device side.** The OTBR log contains no parent request, no child add, no joiner activity for it — only `ChannelAccessFailure` and `Different partition`. The Tarken is attached to a parent in the other partition and has no reason to look for HA.

Side observation: node `@1:a` fails the same way on `fdbd:6564:912b:af5c::…`, matching the third extended PAN ID `BD6564912BD3AF5C` seen in `ThreadDiagnosticsService … partial(no_credentials)` — the DIRIGERA also runs its own separate Thread network.

## Contributing factor — RF collision still not fixed

The OTBR log is still a wall of `P-RadioSpinel-: Handle transmit done failed: ChannelAccessFailure`, roughly one every 5–10 s (see `thread-matter-commissioning-rf-and-vlan.md`, Blocker 1). The 2.4 GHz AP is evidently still on channel 6 against Thread channel 15. HA's border router can barely transmit, which makes its partition weak and biases a sleepy end device toward the DIRIGERA's partition.

### Proximity also matters, not just the channel plan

Channel separation is only half the story — at short range you leave the far field and hit receiver desensitisation:

- Free-space loss at 2.4 GHz over 5 cm is only ~14 dB, so a 0 dBm Zigbee burst from the ZBT-2 arrives at the ZBT-1 antenna at roughly **−14 dBm**, against a −100 dBm sensitivity floor and a front end that compresses near −20 dBm. The RF filter cannot reject that 50 MHz away, so CCA reads the channel busy → `ChannelAccessFailure`, even though channel 15 vs 25 is nominally clean.
- An AP at +20 dBm one metre away lands at about **−20 dBm** on the dongle, continuously.
- USB 3.0 ports/cables and NVMe enclosures emit broadband noise across 2.4 GHz.

Mitigation: each dongle on its own **USB 2.0 extension cable**, ~1 m from the host, **≥1 m apart from each other**, **2–3 m from the AP**, away from USB3 and storage. Keep the 1 / 15 / 25 channel layout.

**Isolation test:** stop the Zigbee2MQTT add-on for 2–3 minutes and watch the OTBR log. If `ChannelAccessFailure` drops sharply, the ZBT-2 is a real contributor; if unchanged, it is the AP and/or USB noise.

## Fix sequence

1. **Move the 2.4 GHz AP from channel 6 to channel 1.** Verify `ChannelAccessFailure` stops in the OTBR add-on log.
2. **Resolve the two-border-router split.** Pick one:
   - Remove the DIRIGERA from the `ha-thread-30a2` network (IKEA Home smart app → Hub → Thread → leave/reset network), leaving the ZBT-1 as the only border router; or
   - Move the DIRIGERA onto VLAN 10 (or bridge IPv6 + mDNS between VLAN 10 and 20) so the two routers form one partition over the backbone.
   Option A preserves IOT isolation and is the smaller change.
3. **Re-attach the Tarken.** Power-cycle it within a couple of metres of the ZBT-1; it should pick a parent in HA's partition and come back. If it does not, remove the Matter node and re-commission (re-run "Sync Thread credentials" in the companion app first).

## Verification

- OTBR log free of `ChannelAccessFailure` and of `Different partition`.
- Thread diagnostics show a single router for `935dad539f109af8`, or both with neighbour state 64.
- `ENETUNREACH` retries for `@1:4b` stop; `sensor.bathroomup_bathroomup_window_thread_channel` reports 15 and the device's IPv6 addresses fall under the OMR prefix advertised by HA's OTBR.
