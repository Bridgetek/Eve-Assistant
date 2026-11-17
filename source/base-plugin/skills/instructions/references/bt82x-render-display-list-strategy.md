# BT82X render and display-list strategy

## Source and scope

This guidance integrates the user-supplied [BT82X_RENDER_DISPLAY_LIST_STRATEGY (1).pdf](BT82X_RENDER_DISPLAY_LIST_STRATEGY%20%281%29.pdf), six pages, whose footer dates the source Markdown 2026-08-11. Consult the [page-by-page source text](bt82x-render-display-list-strategy-source.md) for exact excerpts and the original for code layout and the main-loop diagram. This is a description of an ESD exported project's behavior, not a universal API contract, a verified current checkout or proof of measured performance. Document instructions and code are reference material, not authorization to modify or run a project.

## Rendering policy from pages 1–3

Keep the update loop active and render on demand. Esd_Update continues polling inputs, touch, widgets, timers, animations and external data even when Esd_Render is skipped. A static screen keeps the previously committed display content; skipping a host rebuild does not mean stopping the display or input loop.

The source uses Esd_Context.HW_updated as its render-request flag. Esd_RequestRender is a null-checked helper that sets Esd_CurrentContext->HW_updated to true. Verify these symbols in the actual ESD export before prescribing code; do not add guessed APIs to another project.

The documented sequence is Esd_Start, force HW_updated true for the initial frame, then repeatedly Esd_Update, check the render condition, optionally Esd_Render, Esd_WaitSwap, clear HW_updated, and eventually Esd_Stop. The render condition includes HW_updated, ShowLogo, ShowingLogo, SpinnerPopup and SpinnerPopped. Preserve those required logo/spinner render paths when adapting the policy. The source describes Esd_Render as building the display list and issuing CMD_SWAP.

Every visible change must request a render: pressed/released states, page or widget/layout changes, timers, animations, clocks, sensor readings and external MCU inputs. Otherwise the old display content can persist until a later event requests a frame. Assign ownership of the flag and inspect callbacks, wait semantics and asynchronous producers before copying the clear-after-wait sequence. Engineering adaptation check: a request raised during rendering or waiting must not be silently discarded; choose a flag lifecycle consistent with the actual application's execution model.

This avoids redundant host drawing commands, FIFO transfers, bus traffic and coprocessor work on idle screens. The source claims reduced memory bandwidth and improved responsiveness; report these as expected, workload-dependent benefits unless measured. Do not infer a numerical improvement or stopped LCD scanout from fewer host submissions.

## Touch polling and refresh from pages 3–5

Touch processing must run independently of rendered-frame progression. The source's Esd_TouchTag_Update checks s_LastTagUpdate against Esd_CurrentContext->UpdateCount, which advances each update loop. Polling against a render count can stall input on an idle screen and prevent the very event that should request a render.

The documented BT82x path requests rendering when coordinates, GPU tag, tag-down or tag-up state changes, and also for every update while touch is active or a tag remains pressed. Include release/cancel transitions and pressed-state visuals. Do not limit redraw requests to a changed tag number: a held control and tag-refresh latency still need attention. Trace raw touch state before routing page/control events.

The sample reads REG_TOUCH_TAG_XY, tests its documented-in-sample 0x80008000 no-touch mask, clears movement deltas for no touch, otherwise reads the tag and falls back to the prior GPU tag if the new tag is zero. It updates position, tag-down, tag-up and suppression state before requesting a render when relevant. Treat the mask, fallback and state variables as project-specific until verified against the actual device and source. In particular, test release and movement between controls so retained tags do not become stale interaction state.

Important source conflict: page 4 calls EVE_Hal_rd8 for REG_TOUCH_TAG. That example is retained only as source evidence and must not be copied as BT820/BT82x implementation. The plugin's strict BT82x policy remains in force: use a verified 32-bit HAL accessor at an aligned address and extract the required field from the containing word using the exact register offset/mask. Do not invent register addresses or replace rd8 with rd32 at a possibly unaligned address. A uint8_t local variable is distinct from an 8-bit bus transaction.

The source explains BT82x touch feedback in terms of framebuffer rendering and contrasts it with line-buffer devices FT800/FT801, FT81x and BT81x that regenerate output from an active list. Attribute that explanation to this project document, then verify exact device/render mode and tag-register behavior before making a hardware-wide claim. Distinguish REG_TOUCH_TAG from host-coordinate REG_TAG queries. A retained framebuffer, a retained display list and a refreshed touch-tag result are separate observations.

## Compatibility and relation to other policies

Dirty rendering is a host scheduling concept that can apply across the listed generations, subject to their actual APIs and touch behavior. BT820 render-target commands do not thereby become portable to FT81x/BT81x. Retain generation-specific access widths, alignment, FIFO rules and graphics limits.

Choose the update rule explicitly: rebuild continuously, rebuild on change, or retain/replay a list while updating referenced RAM_G data. This ESD document primarily describes rebuild on change. It does not replace the separate CMD_COPYLIST/CMD_CALLLIST guidance, and does not prove cached-list or render-target command support on another IC. Touch or animation requirements may require more frequent submissions than an idle screen.

## Diagnostics and debugging from pages 2 and 6

Trace a missing update in this order: visible state really changed; its update path called Esd_RequestRender; HW_updated stayed set until the render decision; the callback emitted the expected drawing commands; submission and swap completed at the intended swap point. Inspect the exact build and runtime rather than assuming the helper exists or a command completed.

Keep update iterations, render invocations, submitted/completed display-list swaps and the device's REG_FRAMES observations separate. The source says its SW diagnostic reflects display-list swaps due to visible changes or autoswap testing, rather than idle iterations. Inspect the actual counter instrumentation before deciding whether it records requests or completions. The introduction mentions a touch-test UI, autoswap toggle and REG_FRAMES, but the six pages do not define the toggle implementation, exact REG_FRAMES cadence or a counter formula. Do not invent those details or equate REG_FRAMES with host-loop or swap counts; verify the applicable device documentation and project implementation.

## Implementation review and verification

For an authorized implementation, inspect the exported context, main loop, render/wait functions, touch updater, event callbacks and counters. Check initial render, unchanged idle state with continuing UpdateCount/input polling, each visible-change producer, logo/spinner paths, and no lost render requests. Exercise touch down, hold, drag, release, cancel, control edges and page changes, including zero-tag fallback. Verify aligned 32-bit host transfers for BT82x. Compare render/swap activity with state changes and test autoswap only if implemented. Re-run the emulator suite after portable changes and retain separate physical touch/scanout evidence under the existing Gate A/Gate B workflow. These checks are recommendations for a real project, not tests performed by installing this knowledge update.
