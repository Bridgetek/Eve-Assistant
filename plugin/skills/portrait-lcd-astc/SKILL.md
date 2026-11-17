---
name: portrait-lcd-astc
description: Use for Bridgetek EVE portrait LCD support, native 800x1280 panels operated as 1280x800 landscape, BT819 ASTC cache locality, column-wise ASTC fetch, EAB offline asset rotation, portrait touch mapping, or related hardware/software architecture evaluations.
---

# Portrait LCD support: ASTC cache-friendly rendering (BT819 proposal)

## Status and scope

This is a **proposed engineering optimization**, not an implemented, documented, or silicon-validated BT819 feature. BT819 is a user-confirmed forthcoming target; device-specific cache details below are **user-supplied assumptions**, not independently verified official specifications. Do not conflate BT819 with BT818 or BT820. Review the plugin's general `instructions` guidance for other EVE-generation details and bitmap transformation. Verify RTL/datasheet behavior and exact EAB/ESD support before making implementation claims.

## Engineering problem

A native portrait 800x1280 LCD may be mounted/used with a landscape logical 1280x800 UI. A 90-degree texture sampling transform can make adjacent output pixels traverse vertically through an ASTC source, decreasing horizontal cache-line locality. This concerns **texture sampling rotation**, not necessarily final LCD scanout rotation. Before proposing a fix, determine where display orientation is applied in the pipeline and whether ASTC source fetches actually become column-wise. A screen rotation applied after texture decoding may leave normal row-major texture fetch intact, eliminating the alleged issue. LCD timing, logical orientation, rendering coordinates, and touch coordinates are separate problems.

## Quantitative illustrative model

Assume ASTC 4x4 blocks, a hypothetical 256-entry BT819 cache, and one cache entry comprising four **horizontally adjacent ASTC blocks** (equivalent to 16 source pixels across). A source-column traversal through 1280 image pixels intersects ceil(1280/4)=320 ASTC block rows. **If** each such row maps to a distinct entry, its working set is 320 entries, larger than 256. This can cause replacement thrashing across repeated scans depending on traversal schedule, associativity, replacement, prefetch, neighboring-pixel reuse, and cache residency. One traversal having 320 distinct entries **does not imply 320 misses per subsequent output column** or prove a frame-rate penalty.

For a 1280-pixel **horizontal** traversal, four horizontal blocks per entry yields ceil(1280/(4*4))=80 distinct entries in this simplified layout, a 75% reduction in distinct entries for that one traversal (320 to 80). **This is not a measured 75% reduction in misses, traffic, rendering time, or power.** Real traffic also depends on block width/height, metadata, cache-line mapping, image tiling, sampling schedule, clipping, multiple textures, flash access, and working-set reuse. Do not generalize the numeric model to other ASTC footprints or device generations.

## Recommended layered architecture

- **P0: functional portrait panel support** independent of asset optimization: physical LCD timing, orientation/scanout mapping, logical application coordinates, touch coordinate transform, resolution constraints, and correct clipping/rendering. An ordinary non-preprocessed asset must remain correctly drawable.
- **P1: optional EAB orientation-aware ASTC conversion** for suitable static assets: rotate source pixel images 90 or 270 degrees *before ASTC compression* to match a favorable sampling direction where RTL traces prove one exists. Do not merely reorder already compressed blocks: block-internal texel positions and ASTC encoding also need appropriate rotation. Package physical source/output dimensions, block footprint, asset orientation, bitmap layout/stride, and orientation-transform metadata. The exact EAB UI/CLI/MCP operation is a proposal, **not an existing verified command**.
- **P1: ESD/EveApps integration**: define independent `panel_native_orientation`, `logical_ui_orientation`, and `asset_orientation` (naming illustrative). Use metadata to select texture mapping and image placement without double rotating. Keep ordinary graphics, fonts, vector primitives, video, touch, and runtime transforms working; do not claim all can be handled through offline image rotation.
- **P2: automation**: profile assets and recommend per-asset pre-rotation only where measured benefit and visual correctness justify it; consider special cases such as atlases, glyphs, nine-patch assets, animations, and multiple orientations.
- **Conditional hardware follow-up**: consider prefetch, address swizzle, alternative cache line grouping/associativity/capacity only if instrumentation shows software optimization cannot address relevant workloads.

## Key technical distinctions

- Distinguish physical panel 800x1280, logical UI 1280x800, source image size, rotated encoded bitmap dimensions, and output bitmap rectangle. A pre-rotated bitmap drawn with the same transform as the unrotated one can become double-rotated or clipped.
- `BITMAP_TRANSFORM_A-F` defines **output-to-source sampling** (u=A*x+B*y+C, v=D*x+E*y+F); 90-degree sampling transforms often replace source-row traversal with source-column traversal. For BT815/BT817/BT818 see general bundled bitmap-transform guidance and official BRT_AN_033; BT819 command encoding and support remain to be confirmed.
- `REG_ROTATE`/`CMD_SETROTATE` cannot be assumed to move the ASTC sampling step or to imply cache thrashing. Map their actual pipeline position for the target revision before promising speedups.
- An 800x1280 panel is not automatically supported by a given EVE variant; verify maximum timing counts, physical output capability, required throughput, and panel interface. Do not assume ability to drive it solely because assets can be rotated.
- EAB pre-rotation may increase build variants, flash usage, or asset-management burden, and ASTC rotation can change compression artifacts. Test pixel correctness, quality and package sizing.

## Validation matrix and decision gates

Compare on identical content, brightness, refresh, bus configuration and ASTC footprint:

1. Baseline source ASTC with 90-degree bitmap sampling transform.
2. Source pixels pre-rotated before ASTC encoding, rendered through a correctly compensated or identity sampling transform.
3. Logical/UI/display rotation via device-supported screen-rotation path, separate from explicit texture rotation.
4. Mixed workload: fullscreen background, several ASTC textures, widgets, text, alpha, animation, touch, and dynamic redraw.
5. Capacity/organization sweep where RTL allows: 128/256/384/512 entries, cache replacement options and access grouping.

Capture per-frame ASTC source/block addresses, cache hits/misses and evictions, flash transactions/bytes and burst patterns, memory latency and stalls, render latency including worst case, output underrun, frame time/FPS, power where measured, memory consumption, and image/touch correctness. Prove where coordinate rotation occurs in the graphics/ASTC pipeline. Treat all modeled numbers as assumptions until RTL/hardware evidence. Use emulator evidence as functional Gate A and real hardware/RTL measurement as distinct performance Gate B; don't claim hardware validation from an emulator screen capture alone.

## Suggested EAB configuration — illustrative ONLY

```yaml
# Concept proposal, not released EAB syntax
panel_native_resolution: [800, 1280]
logical_ui_resolution: [1280, 800]
target: BT819
asset_optimization:
  mode: portrait_astc
  rotation: auto
  astc_footprint: 4x4
  optimize_cache_locality: true
```

## How to answer future user queries

When asked about Portrait LCD support, first explain the distinction between functional rotation and performance optimization; then show the conditional 320 vs 256 vs 80-entry model **with assumptions**, describe EAB's offline pixel rotation proposal and metadata needs, give implementation trade-offs and an RTL test plan. Never suggest this is an existing EAB flag or a proven BT819 performance fix. Don't ask the user to repeat the already-provided chip, native panel size, proposed cache size and entry grouping for this scenario. Explicitly separate proven legacy EVE documentation from BT819 roadmap assumptions. Prefer the main `instructions` skill for official reference links and generation-specific details.
