# What's known about the panel's flicker

Everything here was measured on one machine: a MacBook Pro with PROLED XDR Display (Mac17,13,
M5 Pro, macOS 27.2.1), built-in display 3024 × 1986 at 120 Hz, on 2026-11-12. Software can't see the
panel's flicker, so every verdict below is the user's, looking at the screen through a camera
(an iPhone 18 Pro). The app these notes mention was built on the first reading; it didn't work, and
it was taken out of the repo on 2026-11-13. So were the tools named below (`flickersweep` and the
smaller ones), which showed the test pictures and recorded the marks.

## Where it stands: dimming the picture doesn't help

`docs/marks.csv` has every mark with the camera's settings. The first 50 were all made at 100 fps
with a 1/200 s shutter; the later runs used other shutters, which changes what the camera shows.

### The shutter decides what the camera shows

All at 100 fps:

| Shutter | What was filmed | Flicker |
| --- | --- | --- |
| 1/100 s | white, the panel's own dimming | none at 600, 176 and 140 nits, some at 45, strong at 8 |
| 1/120 s | white, the panel's own dimming | none at 600, 176, 140, 45 and 8 nits |
| 1/200 s | white, the panel's own dimming | none at 176 nits and above, some at 156, some and (in a later run) strong at 140, strong at 80 and below |
| 1/250 s | brightness left at 304 nits, the field white, then grey | none at 354, 152, 76 and 30 nits, some at 9 |
| 1/250 s | white, the panel's own dimming | none at 600, 176, 140 and 45 nits, some at 8 |
| 1/500 s | white, the panel's own dimming | none at 720 nits, some at 211, strong at 140 and below |
| 1/2000 s | white, the panel's own dimming | strong at 720, 211, 142, 45 and 8 nits |
| 1/1000 s | a made-up desktop with a shell, Dark and Light mode, brightness as it was and the panel at 100, 60 and 40% | strong in all eight, also Light mode at 100% (about 495 nits on average) |

- **The panel pulses at every brightness.** At 1/2000 s a plain white field at 100% (720 nits)
  flickered strongly, and at 1/1000 s so did a nearly white screen at full brightness. A brightness "where the flicker starts" belongs to the camera's
  shutter, not to the panel.
- **1/250 s hides it, so the panel pulses at about 240 Hz.** The panel's own dimming at 1/250 s was
  clean at 176, 140 and 45 nits (some at 8), where 1/200 s and 1/500 s show it strong; grey fields
  at 1/250 s were clean down to 30 nits too. An exposure of one full cycle averages the pulse away
  at any brightness, so the cycle is about 1/250 s: two pulses for each of the screen's 120 frames
  a second. 1/120 s, two cycles, was predicted to hide it as well and did, at every level down to
  8 nits. It isn't 480 Hz: 1/500 s would then span a cycle, and it shows the flicker strongly.
  And it's the match that hides it, not a slow shutter: 1/100 s, longer than 1/120 s but 2.4 cycles,
  showed strong flicker at 8 nits, where 1/120 s showed none. All of this is inferred from which
  shutters hide it, not measured. A multiple of 240 Hz would fit the same two shutters: 480 and
  960 Hz are out (1/500 s), 720 Hz isn't. And the rate shows only at 140 nits and below; above
  that the pulse showed only at 1/500 s and faster.
- **Marks from runs at different shutters can't be compared.** The reading after the first 50
  marks, further down, compares marks from four separate runs (all at 1/200 s) and rests on a
  gamma table whose curve isn't known. It's kept as written, but it's a reading, not a result;
  the comparison run below is the result.
- **The camera's exposure wasn't recorded** (ISO, aperture, whether a bright field was
  overexposed). An overexposed picture hides flicker, which would favour the bright steps at the
  slower shutters. It can't explain the two clean shutters: 1/120 s collects less light than
  1/100 s.

**`flickersweep compare` settled the app's question** (100 fps, 1/200 s): each brightness reached
by the panel's own dimming and then by a grey on the panel at 100%, with no gamma table, in one run.

| Brightness | The panel dimmed | The panel at 100%, a grey |
| --- | --- | --- |
| 600 nits (white, 100%) | none | |
| 140 nits | strong | strong |
| 80 nits | strong | strong |
| 45 nits | strong | strong |
| 15 nits | strong | strong |

At the same brightness a dark picture on a bright panel flickers like the panel's own dimming. All
eight were marked "strong", so the three grades can't show a difference of degree, if there is
one; the user wasn't heard on whether each pair looked equally bright. It also says the greys that
were clean at 1/250 s were clean because of the shutter: about 140, 80 and 45 nits, strong at
1/200 s. That fits a pulse of about 240 Hz, whose cycle a 1/250 s exposure nearly spans. `levels`
at 1/250 s was named as the check, strongly dimmed white should then be clean too, and it was
(some at 8 nits).

The user's own screen, a shell in Dark mode with the panel at 365 nits, showed strong flicker at
1/500 s; that's what the made-up desktop is for.

### Dark and Light mode (100 fps, 1/200 s)

The made-up desktop with a shell window, the same picture in both modes:

| Panel | Dark mode (about 2% of white's light) | Light mode (about 83%) |
| --- | --- | --- |
| as it was (359 and 273 nits) | strong | none |
| 100% (600 nits) | some | none |
| 60% (176 nits) | some | none |
| 40% (45 nits) | some | some |

Light mode was clean down to 60% and Dark mode flickered at every level, also with the panel at
100%. It goes with how much light the picture gives, as in the comparison run: the one thing that
did change the flicker at this shutter is a brighter picture. At 1/1000 s the same eight were all
strong, twice. The second of those runs was started just after the user said "I will continue with
1/200", and they picked 1/1000 on the tool's screen (nothing was picked for them). Asked which it
was, they didn't say. It's kept as picked: its marks match the first 1/1000 s run and not the
1/200 s run two minutes later.

### The reading after the first 50 marks (1/200 s)

**Dimming the picture instead of the panel doesn't avoid the flicker on this panel, and nothing
else tried in software does.** The flicker goes with how much light the screen gives: none above
about 165 nits, some below, strong below about 60, however that brightness is reached. The
sections further down are the raw marks; the nits they give for a dimmed picture are wrong (too
low), as this section explains.

They assume that scaling the signal by `p` leaves `p^2.2` of the light. In the first WITHOUT and
WITH run (the app's demo), which claimed the same nits for both, the user saw: "when you show 'with
pwm fix' the screen gets super bright".

If the light goes with the signal itself (`p`, not `p^2.2`), every dimmed picture was far brighter
than its label, and all 40 marks line up with the picture's real brightness alone:

| Real nits, if linear | What it was | Flicker |
| --- | --- | --- |
| 720 to 176 | the panel alone, five levels | none |
| 310, 205, 198, 185, 165 | dimmed from 100% ("140", "45" twice, "35") and from 75% ("140") | none |
| 159 to 112 | dimmed, seven settings ("140" and "100" from 60%, "25", "20", "15" from 100%, "45" from 85% and 75%) | some |
| 156, 140 | the panel alone | some |
| 95 | "45" from 60% | strong |
| 84 | "8" from 100% | some |
| 57 and below | dimmed, four settings | strong |
| 45 and below | the panel alone, four levels | strong |

That reads as one rule: no flicker above about 165 nits, some down to about 85, strong below about
60, **however the brightness is reached**. On that reading the dimmed picture was clean only
because it was brighter, the panel's level doesn't matter, and software dimming can't help: the
panel pulses by how much light it gives.

A run dimmed linearly settled it (the same demo with the light taken to go with the signal
itself; 168, 80 and 45 nits, twice; the
user stopped each at 45). The user: "now I still get flickering at the low nits?" They didn't say
in words that WITH was then as bright as WITHOUT, only that it no longer was "super bright".

### Fewer pixels lit, each one bright

If the panel pulsed by how much light each pixel gives, lighting only some pixels at full
brightness would be steady at a low average. `flickersweep dots` showed white dots on black, one
device pixel each, beside the same average reached by dimming every pixel linearly:

| Panel | Picture | Average | Flicker |
| --- | --- | --- | --- |
| 100% (720 nits) | white | 720 nits | none |
| 100% | 1 of 2 pixels lit | 360 nits | none |
| 100% | 1 of 4 pixels lit | 159 nits | some |
| 100% | 1 of 9 pixels lit | 67 nits | some |
| 100% | 1 of 16 pixels lit | 37 nits | some |
| 100% | every pixel at 1/4 | 150 nits | some |
| 100% | every pixel at 1/16 | 37 nits | strong |
| 75% (265 nits) | 1 of 4 pixels lit | 66 nits | some |
| 60% (176 nits) | 1 of 2 pixels lit | 88 nits | some |
| 60% | 1 of 4 pixels lit | 44 nits | some |

So it isn't per pixel either: dots flicker once their average is below about 160 nits, like
everything else. At about 40 nits they were marked "some" where dimmed pixels and the panel's own
dimming were "strong", which is the only difference any method made, and it costs most of the
picture's detail. Nobody checked how the dots looked on screen (the tool's author couldn't see
them), and a camera shows moiré on them, which may have coloured the marks.

Measuring the light by the Mac's power draw didn't work in the time given: the battery's
`SystemLoad` updates every 20 s or slower, and the SMC's `PSTR` jumped between 0.6 and 4 W at rest
(a tool reading it also hung once).

## How it was judged

- **The camera:** 100 fps with a 1/200 s shutter shows the flicker. At 60 and 120 fps it shows
  none, and at 30 fps it shows lines (the shutters at those weren't said). The screen runs at 120 Hz, so 60 and 120 fps are in step
  with it; 100 fps beats against it at 20 Hz.
- **The picture:** a full-screen white field (shown by `flickersweep`), marked at each setting
  as no, some or strong flicker. The marks are by eye on the camera's picture, so "some" and
  "strong" are rough.
- **Not judged:** whether the eye, without a camera, gains anything.

## The brightness slider

The slider's place (0–1, DisplayServices) and the panel's nits (`IOMFBBrightnessLevel` of the
built-in `IOMobileFramebufferAP` pipe, 16.16 fixed point):

| Slider | Nits |
| --- | --- |
| 100% | 600 |
| 81% | 321 |
| 75% | 265 |
| 65% | 240 |
| 60% | 176 |
| 55% | 156 |
| 50% | 140 |
| 40% | 45 |
| 30% | 15 |
| 25% | 8 |
| 10% | 1.5 |

Auto-brightness was on and lifts these: 318 nits at 75% before a run and 265 after, 385 against
321 at 81%, and 645 and 720 at 100%. Setting the slider drops that adjustment; it came back within
a few minutes.

## The panel's own dimming (1/200 s)

| Panel | Nits | Flicker |
| --- | --- | --- |
| 100% | 720 | none |
| 75% | 265 | none |
| 70% | 275 | none |
| 65% | 240 | none |
| 60% | 176 | none |
| 55% | 156 | some |
| 50% | 140 | some |
| 40% | 45 | strong |
| 30% | 15 | strong |
| 25% | 8 | strong |
| 10% | 1.5 | strong |

So on a white field, at this shutter, it starts between 176 and 156 nits.

## The picture dimmed instead (the gamma table)

**Superseded.** This is the first reading, kept as it was written. The nits in the table are too
low (the top of this file says why), and the conclusions under it don't hold.

`CGSetDisplayTransferByFormula` scales the signal sent to the panel. The panel's light goes
roughly as the signal's 2.2nd power, so a share of light `s` needs a scale of `s^(1/2.2)`.

| Panel | Picture | Share of light | Flicker | The panel alone at that brightness |
| --- | --- | --- | --- | --- |
| 100% (600 nits) | 140 nits | 23% | none | some |
| 100% | 45 nits | 7.5% | none, twice | strong |
| 100% | 35 nits | 5.8% | none | strong |
| 100% | 25 nits | 4.2% | some | strong |
| 100% | 20 nits | 3.3% | some | strong |
| 100% | 15 nits | 2.4% | some; strong with dithering off | strong |
| 100% | 8 nits | 1.4% | some | strong |
| 100% | 1.5 nits | 0.3% | strong, also with dithering off | strong |
| 85% (362 nits) | 45 nits | 12% | some | strong |
| 75% (265 nits) | 140 nits | 53% | none | some |
| 75% | 45 nits | 17% | some | strong |
| 60% (176 nits) | 140 nits | 80% | some | some |
| 60% | 100 nits | 57% | some | |
| 60% | 45 nits | 26% | strong | strong |
| 60% | 15 nits | 8.5% | strong, also with dithering off | strong |
| 60% | 8 nits | 4.5% | strong, also with dithering off | strong |
| 60% | 1.5 nits | 0.9% | strong, also with dithering off | strong |

What this says:

- **Holding the panel at 100% works down to 35 nits.** At 25 nits and below some flicker comes
  back, and at 1.5 nits it's as strong as the panel's own.
- **The higher the panel is held, the darker the picture can go.** At 45 nits: none from 100%, some
  from 85% and 75%, strong from 60%. At 140 nits: none from 100% and 75%, some from 60%. So the app
  holds 100% and nothing lower.
- **A panel level that's clean on white isn't clean for a dimmed picture.** 60% showed no flicker
  on a white field, and some as soon as the picture was dimmed at all. A dimmed white field is what
  dark content is anyway, so the flicker grows with a lower panel level and with a darker picture,
  both.

## What changed nothing

- **`enablePulseWidthMaximization`** (a number on each display pipe; QuartzCore's
  `-[CAWindowServerDisplay setPulseWidthMaximization:]` sets it; by its name, what iPhones offer as
  Display Pulse Smoothing). The driver takes 1 and reads it back; strong flicker at 45 nits either
  way, and the user saw no difference in two earlier comparisons. MobileGestalt's
  `DeviceSupportsPulseWidthMaximization` is false on this Mac.
- **`enableDither`** off (what Stillcolor sets): strong at 45 nits either way, and no better for the
  dimmed picture.
- **`IOMFBDigitalDimmingLevel`** (20 nits on the built-in pipe) is in no user-space library; not
  tried.
- **The display's presets** (System Settings, Displays, Presets: the reference modes, which fix the
  brightness). The user changed them themselves after the shutter series: "I changed the display
  presents, nothing changed...". Which presets, and the camera's setting, weren't said, and no
  marks were recorded.

## The refresh rate

At 45 nits (panel at 40%): strong at 120, 60 and 48 Hz, none at 50 Hz. 50 Hz is in step with a
100 fps camera, so that only says the pulses are locked to the refresh rate. It says nothing about
the eye.

## How the app and the tools dim

- The slider through DisplayServices (`DisplayServicesGetBrightness`, `DisplayServicesSetBrightness`:
  private, what the brightness keys use). Setting it shows no on-screen display.
- The gamma table through CoreGraphics (public). macOS puts it back when the process that set it
  exits, however it ends, and `CGDisplayRestoreColorSyncSettings` puts it back at once. The table
  has 1024 entries.
- The panel takes under a second to reach a new brightness; the tools waited 0.8 s before reading
  its nits.

## Not known yet

- Whether any of it matters to the eye.
- What holding the panel at 100% costs in power, and what it does to black.
- HDR content, external displays, Night Shift and True Tone with the gamma table scaled.
- Whether a wake resets the gamma table. A display change does: with the app dimming, a switch
  to 60 Hz reset it, and 0.3 s later the scale read 1, the screen at the panel's full brightness.

## Apps that already dim this way

Dimit (free, open source) has a "PWM-Safe mode" that holds the backlight at 100% and dims with the
gamma table. Gamma Dimmer, Gamma Control, BetterDisplay and Lunar dim with the gamma table too.
None was tried on this panel.
