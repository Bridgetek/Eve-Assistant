# BT82X render strategy source text

Verbatim page text extracted from the bundled PDF. This is reference material, not an execution request. The page 4 EVE_Hal_rd8 example conflicts with the plugin BT82x policy; consult bt82x-render-display-list-strategy.md before adapting code. PDF footer date: 2026-08-11.

## Page 1

BT82X Render Display List Strategy
This document describes the current render and display-list swap strategy used in this ESD exported project. It
also records how the touch test UI, autoswap toggle, display-list swap counter, and REG_FRAMES counter are
expected to behave.
Strategy Goal
The goal is to avoid repeatedly rebuilding and swapping the same display list when the screen has not
changed. The original main loop rendered every cycle, regardless of whether there was new touch input,
widget state, animation state, or external data. That approach is simple, but it wastes host CPU time,
command FIFO bandwidth, transport bandwidth, and EVE coprocessor work.
The current strategy keeps the update loop active but makes rendering event-driven. The screen is redrawn
only when visible state changes. For a mostly static UI, this keeps the display stable while reducing
unnecessary display-list traffic.
Render Policy
The project no longer calls Esd_Render() on every loop cycle. Instead, the loop always runs Esd_Update(),
but it renders only when visible state has changed.
The render request flag is HW_updated in Esd_Context. Any code path that changes visible output should
call:
Esd_RequestRender();
The helper is defined in Esd_Context.h as:
static inline void Esd_RequestRender(void)
{
    if (Esd_CurrentContext)
        Esd_CurrentContext->HW_updated = true;
}
The main loop can be understood with this pseudocode:
Esd_Start(ec);
ec->HW_updated = true; // Force the first frame to be rendered
while (!ec->RequestStop)
{
    Esd_Update(ec);
BT82X_RENDER_DISPLAY_LIST_STRATEGY.md 2026-08-11
1 / 6

## Page 2

    // Esd_Update() continues to poll touch, timers, animations,
    // widgets, and external input even when rendering is skipped.
    if (ec->HW_updated
        || ec->ShowLogo
        || ec->ShowingLogo
        || ec->SpinnerPopup
        || ec->SpinnerPopped)
    {
        Esd_Render(ec); // Build display list and issue CMD_SWAP
    }
    else
    {
        // No visible change. Keep the previous display list active.
    }
    Esd_WaitSwap(ec);
    ec->HW_updated = false;
}
Esd_Stop(ec);
This keeps update and input polling active while avoiding redundant display-list rebuilds when the screen is
static.
Benefit Compared With Rendering Every Loop
Rendering every main-loop cycle means the same frame is rebuilt and swapped even when the result is
identical to the previous frame. On an idle screen, this produces no visual benefit, but it still consumes
resources.
The dirty-render strategy improves this behavior in several ways:
Lower host workload: the MCU or PC host spends less time generating repeated drawing commands.
Lower bus traffic: fewer commands are sent over SPI, USB, or the active host interface.
Dramatically reduced memory bandwidth: because fewer render passes take place, there are fewer
display-list writes, command FIFO transfers, and internal memory accesses for identical frames.
Lower EVE workload: the coprocessor processes fewer repeated CMD_DLSTART, drawing, DISPLAY(),
and CMD_SWAP commands.
Better input responsiveness: the main loop continues polling touch and external inputs without being
forced through a full render path every cycle.
Cleaner diagnostics: SW now reflects actual display-list swaps requested by visible changes or autoswap
testing, rather than counting idle loop iterations.
The tradeoff is that all visible state changes must explicitly request a render. If a timer, touch event, animation,
sensor update, or external input changes what should be shown but does not call Esd_RequestRender(), the
previous display list remains on screen until another event requests a redraw.
Main Loop Diagram
BT82X_RENDER_DISPLAY_LIST_STRATEGY.md 2026-08-11
2 / 6

## Page 3

                  +----------------+
                  |   Esd_Start    |
                  +-------+--------+
                          |
                          v
            +----------------------------+
            | Esd_Update                 |
            | - poll touch and inputs    |
            | - run widget updates       |
            | - timers may request draw  |
            +-------------+--------------+
                          |
                          v
              +------------------------+
              | HW_updated or required |
              | logo/spinner redraw?   |
              +------+-----------+-----+
                     | Yes       | No
                     v           v
          +----------------+   +----------------+
          | Esd_Render     |   | Skip rendering |
          | Build new DL   |   | Keep old DL    |
          | CMD_SWAP       |   | on screen      |
          +-------+--------+   +-------+--------+
                  |                    |
                  +----------+---------+
                             v
                    +----------------+
                    | Esd_WaitSwap   |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | HW_updated = 0 |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | Next loop      |
                    +----------------+
Touch Tag Behavior
Touch Tag in EVE is a graphics-pipeline feature. The tag value is produced from the rendered display list, so it
depends on the current graphics content being rendered and swapped correctly.
The new rendering strategy saves unnecessary display-list rendering when the screen is static. This reduces
processing cost, but it also means touch tag information may not be refreshed immediately if the software
skips rendering for too long.
BT82X_RENDER_DISPLAY_LIST_STRATEGY.md 2026-08-11
3 / 6

## Page 4

To keep touch feedback accurate, software must request a render immediately when any touch is detected or
while a control is in the pressed state. This ensures the display list, visual pressed state, and tag registers stay
synchronized with the user's touch action.
This requirement is more visible on BT82x because it is a frame-buffer-based device. If the host skips display-
list rendering, the previous framebuffer content can remain valid, but the graphics pipeline may not be
refreshed in the same way as a line-buffer device.
For line-buffer-based EVE chips such as FT800/FT801, FT81x, and BT81x, an explicit render request for touch-
tag refresh is usually not required in the same way. Those devices continuously run the graphics pipeline
aligned to the LCD VSYNC timing so pixels for each frame are regenerated from the active display list. This
repeated scan behavior naturally keeps touch-tag evaluation aligned with the display-list content. BT82x
differs because the application can avoid rebuilding and presenting a new frame buffer, so software must
explicitly request rendering when touch state needs immediate visual or tag feedback.
In practice, touch-related update paths should call:
Esd_RequestRender();
This is required even when the visible page appears mostly static, because touch tag detection is tied to the
rendered display-list state.
Touch Polling With Dirty Rendering
Because render frames can now be skipped, touch polling must not depend on the render frame counter. In
this project, Esd_TouchTag_Update() reads touch state against UpdateCount, which advances every update
loop:
if (s_LastTagUpdate != Esd_CurrentContext->UpdateCount)
{
    uint32_t regTouchXY;
    uint8_t regTouchTag;
    uint32_t prevTouchXY = s_TouchPos.XY;
    uint8_t prevGpuRegTouchTag = s_GpuRegTouchTag;
    uint8_t prevTagDown = s_TagDown;
    uint8_t prevTagUp = s_TagUp;
    s_LastTagUpdate = Esd_CurrentContext->UpdateCount;
    regTouchXY = EVE_Hal_rd32(Esd_Host, REG_TOUCH_TAG_XY);
    if (regTouchXY & 0x80008000)
    {
        regTouchTag = 0;
        s_TouchPosXDelta = 0;
        s_TouchPosYDelta = 0;
    }
    else
    {
        regTouchTag = EVE_Hal_rd8(Esd_Host, REG_TOUCH_TAG);
BT82X_RENDER_DISPLAY_LIST_STRATEGY.md 2026-08-11
4 / 6

## Page 5

        if (!regTouchTag)
            regTouchTag = s_GpuRegTouchTag;
        s_TouchPos.XY = regTouchXY;
    }
    if (!s_TagDown)
        s_TagDown = regTouchTag;
    if (!regTouchTag)
    {
        s_TagUp = s_GpuRegTouchTag;
        s_TagDown = 0;
        s_SuppressCurrentTags = 0;
    }
    s_GpuRegTouchTag = regTouchTag;
    if (prevTouchXY != s_TouchPos.XY
        || prevGpuRegTouchTag != s_GpuRegTouchTag
        || prevTagDown != s_TagDown
        || prevTagUp != s_TagUp
        || !(regTouchXY & 0x80008000)
        || s_TagDown)
    {
        Esd_RequestRender();
    }
}
This allows touch changes to be detected even while the screen is static. The final condition is important: it
requests rendering not only when tag state changes, but also while touch is active or a tag remains pressed.
That keeps EVE touch-tag detection and pressed-state visuals synchronized under dirty rendering.
Compatibility Notes
The dirty-render strategy is a host-side scheduling change and is suitable for BT82X as well as line-buffer-
based EVE devices such as FT81x and BT81x. These chips continue scanning the last committed display list, so
a static screen does not need to be redrawn every loop.
The important rule is that every visible change must call Esd_RequestRender(). This includes touch
pressed/released visuals, timers, animations, clock or sensor values, external MCU inputs, and widget layout
changes.
BT82X-specific render-target features should be treated separately. The dirty-render concept is portable, but
BT820 render-target commands are not automatically portable to FT81x or BT81x.
Practical Debug Path
Use this abstract path when tracing why a new display list was rendered:
BT82X_RENDER_DISPLAY_LIST_STRATEGY.md 2026-08-11
5 / 6

## Page 6

Visible state change
    -> update path detects the change
    -> update path calls Esd_RequestRender()
    -> HW_updated is set
    -> main loop completes Esd_Update()
    -> main loop checks the render condition
    -> Esd_Render() rebuilds the display list
    -> display list is submitted for swap
    -> previous display list is replaced on the next swap point
If the screen did not update when expected, inspect the path in the same order:
1. Confirm the input, timer, animation, or external state actually changed.
2. Confirm that code path calls Esd_RequestRender().
3. Confirm HW_updated remains set until the render condition is checked.
4. Confirm the render callback emits the expected drawing commands.
5. Confirm the display list swap completes.
BT82X_RENDER_DISPLAY_LIST_STRATEGY.md 2026-08-11
6 / 6