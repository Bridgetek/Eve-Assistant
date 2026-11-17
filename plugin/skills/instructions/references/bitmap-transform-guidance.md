# Bitmap transform matrix and coefficient C

## Provenance and applicability

This reference incorporates the user-requested bilingual programmer guide, `BT815_Bitmap_Transform_C_OpenGL_EN_ZH_Programmer_Guide.docx`, prepared on 2026-11-03. The document is a teaching and implementation reference, not an independent silicon specification. Its examples were checked against official EveApps interfaces and a source-level EVE checker; they were not compiled for the user's board or verified on hardware.

- BT815 and BT816: BT81x mathematical and command guidance applies, subject to exact SDK and asset configuration.
- BT817 and BT818: the same bitmap-transform concepts and BT81x command model apply. BRT_AN_033 v2.8 explicitly covers BT815/6 and BT817/8. Confirm SDK helper availability, target configuration and generation-specific differences before building.
- BT819: the user explicitly confirmed on 2026-11-03 that BT819 is the correct model, is coming in 2027, and that this bitmap-transform knowledge applies to it. Record these as user-provided roadmap/applicability statements, not an independently verified public release announcement. Apply the conceptual matrix guidance to BT819; do not rename it BT818 or repeatedly ask if the model is a typo. Its device-specific programming guide was not available in this session: verify coefficient encoding, commands, SDK helpers, memory map, target selection and hardware behavior before emitting BT819-specific implementation claims. Do not invent chip IDs, build targets or hardware validation.
- BT820/BT82x: the affine mathematics is useful, but this document does not establish byte-for-byte command, helper, FIFO, precision or host-access compatibility. Use the BT82x guide and applicable repository; retain the skill's strict aligned 32-bit access policy.

When answering a bitmap transformation question, use the concepts and programmer workflow below. Identify the exact EVE model. Keep confirmed hardware behavior, mathematical derivations, coding recommendations and untested examples distinct.

## Direct bitmap coefficients are sampling coordinates

Use the column-vector convention. With local output position $(x,y)$ relative to the bitmap drawing origin, and source sampling position $(u,v)$:

$$
\begin{bmatrix}u\\v\\1\end{bmatrix}
=\begin{bmatrix}A&B&C\\D&E&F\\0&0&1\end{bmatrix}
\begin{bmatrix}x\\y\\1\end{bmatrix}
$$

$$
u=Ax+By+C,\qquad v=Dx+Ey+F
$$

C adds an X offset in **source pixels**. F adds a Y offset. These are not byte addresses, normalized UV offsets, or absolute screen positions. A/B/D/E form the linear sampling map. Use this continuous-coordinate model for teaching; do not promise pixel-identical output without matching pixel centers, quantization, filtering and wrap behavior.

For $A=E=1$ and $B=D=F=0$, $u=x+C$. A feature at source $u=40$ appears at output $x=40$ for C=0, x=30 for C=+10, and x=50 for C=-10. Thus positive C moves the visible pattern left within the fixed output region; negative C moves it right. With rotation/shear this direction rule is insufficient.

To translate the whole bitmap on screen, change its vertex/drawing origin. Use C/F when changing sampling within an output window. The transform does not automatically move or enlarge BITMAP_SIZE's rectangle.

## BT81x encoding

C/F use signed 15.8 fixed point in a 24-bit field: one sign bit, 15 integer bits, eight fractional bits. Initial C/F are zero.

$$
C_{raw}=\operatorname{round}(256C),\qquad C=C_{raw}/256
$$

Range: -32768 through 32767.99609375; resolution: 1/256 source pixel. Examples: +1 → 256 → 0x000100; +10 → 2560 → 0x000A00; -10 → -2560 → low 24 bits 0xFFF600; +0.5 → 128.

For a verified EveApps helper:

```c
int32_t c_raw = -20 * 256;
EVE_CoDl_bitmapTransformC(phost,
    ((uint32_t)c_raw) & 0x00FFFFFFu);
```

Use multiplication, not a negative signed left shift. Check range before converting arbitrary user values; masking is packing, not overflow validation. A/B/D/E have separate precision controls; do not apply C/F encoding indiscriminately. In the verified SDK, `_ex` helpers explicitly select precision. Inspect the actual header when packing negative linear coefficients; do not assume a uint16_t helper preserves every sign bit needed by the hardware encoding.

## OpenGL comparison and inverse transforms

Compare direct EVE bitmap coefficients to texture-coordinate sampling transformations, not solely to an OpenGL model/vertex matrix. Legacy GL_TEXTURE transforms texture coordinates; modern GLSL can compute:

```glsl
vec2 sourcePx;
sourcePx.x = A * localPx.x + B * localPx.y + C;
sourcePx.y = D * localPx.x + E * localPx.y + F;
vec2 uv = sourcePx / vec2(textureSize(image, 0));
vec4 color = texture(image, uv);
```

For ordinary sampler2D and source width W, a C offset corresponds to normalized horizontal offset C/W. Convert normalized output coordinates to local pixels first. GLSL mat3 constructors take columns. Match origin and Y direction; do not assume an OpenGL setup necessarily uses the same axes as EVE.

With matching coordinate conventions, a desired forward geometry transform M has sampling map inverse(M). Forward translation x= u+20 gives sampling u=x-20, so direct C=-20. For a nonzero A and no rotation/shear:

$$
\Delta x=-\Delta C/A
$$

A=0.5 visually doubles width. Increasing C by 10 then moves content left by 20 output pixels. Forward x=2u+20 gives A=0.5 and C=-10, not -20. For an invertible 2x2 linear sampling block L, displacement obeys delta_p = -inverse(L) * delta_t, where delta_t=(delta_C, delta_F).

Keeping a pivot $(c_x,c_y)$ fixed gives:

$$
C=c_x-Ac_x-Bc_y,\qquad F=c_y-Dc_x-Ec_y
$$

Nonzero C/F may therefore compensate a pivot rather than represent explicit user translation. For 2x enlargement around (50,50), A=E=0.5 and C=F=25.

## Programmer workflow

1. Start from the applicable official Bitmap sample; verify board initialization, display setup, model, SDK and helper signatures. Use the connected engineering assistant first when available.
2. Load/convert the source once. Reserve RAM_G, verify format, source width/height, byte stride and byte count. A PNG/JPEG file is not raw RGB565 until decoded. Addresses in the document are examples, not an approved resource map.
3. Select the bitmap handle and cell. Describe source data with setBitmap or the matching source/layout helpers. Set output size, filter and wrap separately.
4. Choose either direct A-F sampling coefficients, or coprocessor `loadIdentity → translate/scale/rotate → setMatrix`. Do not accidentally overwrite direct coefficients with a subsequent setMatrix.
5. Emit BEGIN(BITMAPS), a vertex in the declared VERTEX_FORMAT, and END. When vertexFormat=4, vertex2f arguments are pixel coordinates multiplied by 16. Check supported range and screen clipping.
6. Reset matrix/state as needed, emit DISPLAY, issue SWAP, and use the HAL FIFO helpers to submit/wait and handle faults. Command completion is not a measurement of LCD frame rate or proof that a vertical-blank swap has completed.

The documented 64x64 raw RGB565 example uses 8192 bytes, a 128-byte stride, source address 0x10000 and handle 0. All are explicit example assumptions. A 2x result requires a 128x128 output rectangle but still describes the source as 64x64. Setting bitmapSize alone does not scale.

### Coprocessor visual scaling

```c
EVE_CoCmd_loadIdentity(phost);
EVE_CoCmd_scale(phost, 2 * 65536, 2 * 65536);
EVE_CoCmd_setMatrix(phost);
```

This is visual scale 2; direct sampling A/E would be 0.5. Coprocessor scale/translate parameters are signed 16.16, not the direct C/F 15.8 values.

### Translate and scale

```c
EVE_CoCmd_loadIdentity(phost);
EVE_CoCmd_translate(phost, 20 * 65536, 0);
EVE_CoCmd_scale(phost, 2 * 65536, 2 * 65536);
EVE_CoCmd_setMatrix(phost);
```

Using the documented BT81x composition convention, this describes forward T*S: source points scale first, then translate. Sampling is u=0.5x-10. Reversing these calls changes the composition and scales the translation too. An internal +20 output shift of a 128-wide enlarged image needs a 148-wide rectangle. Moving the whole rectangle instead needs only a different vertex.

### Rotation with a safe output region

For a 64x64 source centered at local output (64,64):

```c
EVE_CoCmd_loadIdentity(phost);
EVE_CoCmd_translate(phost, 64 * 65536, 64 * 65536);
EVE_CoCmd_rotate(phost, 30 * 65536 / 360);
EVE_CoCmd_translate(phost, -32 * 65536, -32 * 65536);
EVE_CoCmd_setMatrix(phost);
```

Angle units are 65536 per full clockwise turn. Forward composition is T(64,64)*R(30 degrees)*T(-32,-32). For this example, a centered 128x128 output rectangle contains the rotated 64x64 source. Recompute bounds for other sizes/scales. A source square of side 64 can require a bounding square of about 90.51 pixels.

### State and animation

Load unchanged assets once. Keep angle/scale/position in application state and rebuild commands when visible content changes. Start fresh compositions with loadIdentity to avoid accumulation.

SAVE_CONTEXT/RESTORE_CONTEXT protects graphics state, including direct bitmap coefficients, but does not restore the coprocessor working matrix. Reset the latter explicitly. The programmer document's full-frame routine resets the coprocessor matrix, restores graphics context, then emits DISPLAY/SWAP and checks EVE_Cmd_waitFlush. This is a reusable drawing routine with assumed source loading; not a fully built MCU application.

Check source format/bytes/address, output rectangle and clipping, color/alpha/blend, wrap requirements, coefficient precision/sign/range, transform order, state leakage, FIFO space, faults, DISPLAY and SWAP. Validate with unit matrix and C=0,+10,-10 first, then add scale/rotation/pivot. Keep emulator evidence and hardware verification separate.

## Sources

- Bundled bilingual guide: [BT815_Bitmap_Transform_C_OpenGL_EN_ZH_Programmer_Guide.docx](BT815_Bitmap_Transform_C_OpenGL_EN_ZH_Programmer_Guide.docx).
- [BRT_AN_033 v2.8](https://brtchip.com/wp-content/uploads/2026/02/BRT_AN_033_BT81X-Series-Programming-Guide.pdf), covering BT815/6 and BT817/8; bitmap matrix, BITMAP_SIZE and coprocessor matrix chapters.
- [Official Bitmap example](https://github.com/Bridgetek/EveApps/blob/master/SampleApp/Bitmap/Src/Bitmap.c).
- [EVE_CoDl.h](https://github.com/Bridgetek/EveApps/blob/master/common/eve_hal/EVE_CoDl.h).
- [EVE_CoCmd.h](https://github.com/Bridgetek/EveApps/blob/master/common/eve_hal/EVE_CoCmd.h).
- [Khronos OpenGL 1.4 specification](https://registry.khronos.org/OpenGL/specs/gl/glspec14.pdf).

Official references and SDK source take precedence for implementation-critical device details. Do not treat this teaching document as proof of a successful compile, emulator run, physical test or unverified device compatibility.
