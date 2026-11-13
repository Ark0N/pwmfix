# The MacBook Pro display's flicker: a review of the testing

This is the full account of one day of testing (2026-11-12) on one MacBook Pro: what was filmed,
what it showed, what was tried to remove the flicker, and where the first reading of the results
went wrong. The raw marks are in [`marks.csv`](marks.csv), and the working notes, in the order
things were found, are in [`findings.md`](findings.md).

## Summary

- **The display pulses at every brightness**, a plain white field at full brightness included,
  **at about 240 Hz**. The rate is inferred from which camera shutters hide the flicker, not
  measured with an instrument. It's the simplest rate that fits; 720 Hz would fit too.
- **The dimmer the picture, the stronger the flicker** on camera. That would fit a pulse whose
  dark part gets longer as the brightness goes down, which wasn't measured.
- **Nothing in software removed it.** Dimming the picture instead of the panel, lighting fewer
  pixels, two driver switches, other refresh rates and the display's presets all left it as it was
  at the same brightness.
- **The one thing that changed it is a brighter picture.** At 1/200 s a shell window in Light mode
  was clean where the same window in Dark mode flickered at every brightness. At 1/1000 s both
  flickered strongly.
- **Whether it matters to the eye is not known.** Every result here is what a camera shows.

## Setup

| | |
| --- | --- |
| Machine | MacBook Pro with PROLED XDR Display (Mac17,13, M5 Pro), macOS 27.2.1 |
| Display | built-in, 3024 × 1986, 120 Hz |
| Camera | An iPhone 18 Pro, at 100 frames a second in every recorded run; shutter from 1/100 to 1/2000 s. The camera app, the lens and the exposure (ISO, aperture) weren't recorded |
| Judge | the owner, looking at the camera's picture of the screen |
| Marks | 113, each "none", "some" or "strong" flicker |

Software can't see a display's flicker, so every test worked the same way. A small tool,
written for this and not published here, fills the screen with a test picture, sets the display
up for one step, and waits. The owner films the screen, marks what the camera shows,
and the tool moves to the next step. Each mark is saved with the camera's frame rate and shutter,
the panel's brightness and what was on the screen. At the end the tool puts the display back.

Brightness is given in nits as the display's driver reports it (`IOMFBBrightnessLevel`). No light
meter was used. The brightness slider's places and their nits on this machine:

| Slider | 100% | 75% | 60% | 55% | 50% | 45% | 40% | 30% | 25% | 10% |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nits | 600 | 265 | 176 | 156 | 140 | 80 | 45 | 15 | 8 | 1.5 |

Auto-brightness was on and sometimes lifted these (720 nits at 100%, 211 at 60%). The tables below
give the nits each step really had.

## 1. The panel's own dimming, at six shutters

A plain white field, dimmed with the brightness slider, filmed at 100 frames a second.

| Panel | 1/100 s | 1/120 s | 1/200 s | 1/250 s | 1/500 s | 1/2000 s |
| --- | --- | --- | --- | --- | --- | --- |
| 100% (600–720 nits) | none | none | none | none | none | strong |
| 60% (176–211 nits) | none | none | none | none | some | strong |
| 50% (140 nits) | none | none | some to strong | none | strong | strong |
| 40% (45 nits) | some | none | strong | none | strong | strong |
| 25% (8 nits) | strong | none | strong | some | strong | strong |

At 1/200 s the 50% step was marked "some" in one run and "strong" in another, which shows how
rough the three grades are.

Three things follow.

**The panel pulses at every brightness.** At 1/2000 s even white at 100% flickers strongly. A
brightness "where the flicker starts" is a property of the camera's shutter: between 176 and 156
nits at 1/200 s, above 211 nits at 1/500 s, nowhere at 1/120 s.

**The pulse is about 240 Hz.** An exposure that spans a whole number of cycles collects the same
light wherever it starts, so the flicker disappears at any brightness. The two shutters that hide
it are the two that fit a 240 Hz pulse:

| Shutter | Cycles of 240 Hz in one exposure | Flicker at 45 nits |
| --- | --- | --- |
| 1/100 s | 2.4 | some |
| 1/120 s | 2.0 | none |
| 1/200 s | 1.2 | strong |
| 1/250 s | 0.96 | none |
| 1/500 s | 0.48 | strong |
| 1/2000 s | 0.12 | strong |

- It isn't a slow shutter that hides it: 1/100 s is slower than 1/120 s and shows strong flicker
  at 8 nits, where 1/120 s shows none.
- It isn't 480 Hz: 1/500 s would then span about one cycle, and it's among the strongest.
- It isn't 120 Hz: 1/250 s would then be half a cycle and couldn't hide it.
- The small flicker left at 8 nits at 1/250 s fits too: 1/250 s is 4% short of a full cycle, which
  matters most when the lit part of the cycle is short.

The idea came from the run of grey fields in section 4, which happened to be filmed at 1/250 s and
came out clean. It was then put as a prediction before two more runs, that a dimmed white field
would be clean at 1/250 s and at 1/120 s, and both held. It is still an inference from marks, not
a measurement, and it has two limits:

- **A multiple of 240 Hz fits the same two shutters.** 480 and 960 Hz are out, since 1/500 s would
  then span nearly whole cycles, and 1200 Hz, since 1/200 s would. 720 Hz isn't ruled out by these
  marks. A shutter near 1/720 s would tell: it would hide a 720 Hz pulse and show a 240 Hz one.
  240 Hz is the simplest rate that fits.
- **The marks pin the rate only at 140 nits and below.** Above that the slower shutters all show
  a steady picture, and the pulse shows only at 1/500 s and faster, which can't tell its rate.

**The pulse is tied to the screen's refresh.** With the display switched from 120 Hz to 50 Hz, the
flicker vanished for the 100-frames-a-second camera, which is then in step with it; at 60 and
48 Hz it stayed. 240 Hz is two pulses for each of the screen's 120 frames a second.

## 2. Can the picture be dimmed instead of the panel?

This was the idea the work started with: hold the panel at 100%, where the camera at 1/200 s
shows no flicker, and make the picture darker instead.

The test that answers it shows each brightness twice in one run, at one camera setting (100
frames a second, 1/200 s): first the panel dimmed with a white field, then the panel at 100% with a
grey field of the same nits. The grey is made from pixel values, so it doesn't depend on any
assumption about the display's gamma table.

| Brightness | The panel dimmed, white | The panel at 100%, grey |
| --- | --- | --- |
| 600 nits | none | |
| 140 nits | strong | strong |
| 80 nits | strong | strong |
| 45 nits | strong | strong |
| 15 nits | strong | strong |

At the same brightness, a dark picture on a bright panel flickers like the panel's own dimming.

Two limits: all eight were marked "strong", so a difference of degree, if there is one, wouldn't
show; and nobody confirmed by eye that each pair was equally bright.

## 3. Everything else that was tried

All at 100 frames a second and 1/200 s unless it says otherwise.

| What | How | Result |
| --- | --- | --- |
| The gamma table | `CGSetDisplayTransferByFormula`, scaling the signal sent to the panel, with the panel at 100, 85, 75 and 60% | Looked like a fix at first, and wasn't: see the next section |
| Fewer, brighter pixels | White dots on black, one device pixel each, 1 of 2, 4, 9 and 16 lit, panel at 100, 75 and 60% | None at 1 of 2 with the panel at 100% (360 nits on average), some in every other pattern. At about 40 nits on average the dots were "some" where a dimmed field was "strong" |
| Pulse width maximization | The driver's `enablePulseWidthMaximization`, which by its name is what iPhones offer as Display Pulse Smoothing | The driver takes the value. Strong flicker at 45 nits either way |
| Dithering off | The driver's `enableDither`, as the Stillcolor app sets it | Strong at 45 nits either way, and no better combined with the gamma table |
| Other refresh rates | 60, 50 and 48 Hz | Strong at 60 and 48 Hz. None at 50 Hz, which only means the camera was in step |
| The display's presets | System Settings, Displays, Presets, switched by the owner | "nothing changed". Which presets and which camera setting weren't recorded |

The dot patterns are the only method that made any difference at equal brightness, and a small
one, at the price of most of the picture's detail. How the dots looked on the screen was never
checked, and a camera shows moiré on them, so that result is the weakest in this review.

## 4. What real use looks like

A made-up desktop with a shell window, the same picture in Dark and in Light mode. The Dark
version gives about 2% of the light a white screen would, the Light version about 83%.

At 100 frames a second and 1/200 s:

| Panel | Dark mode | Light mode |
| --- | --- | --- |
| as the owner had it (about 360 and 270 nits) | strong | none |
| 100% (600 nits) | some | none |
| 60% (176 nits) | some | none |
| 40% (45 nits) | some | some |

At 1/1000 s all eight were strong, in two separate runs. The second of those was started just
after the owner said they'd carry on at 1/200 s, and they picked 1/1000 s on the tool's screen.
It's kept as picked, since its marks match the first 1/1000 s run and not the 1/200 s run made
two minutes later; the owner didn't say which it was.

So at 1/200 s the screen flickers in Dark mode at every brightness, also at 100%, and in Light
mode it's clean down to the panel at 60%. That matches section 2: what counts is how much light the
picture gives, however the brightness is set. The owner had first seen it on their own screen, a
shell in Dark mode with the panel at 365 nits: strong flicker at 1/500 s.

One more run fits here. With the brightness left alone at about 300 nits, grey fields at 152, 76
and 30 nits showed no flicker and one at 9 nits a little. That run was filmed at 1/250 s, so it
says what section 1 says: that shutter hides the pulse.

## 5. How the first reading went wrong

For the first two hours of testing the conclusion was the opposite: that dimming the picture
worked. It's worth saying how, because the same mistakes are easy to make again.

1. **Every mark was at one shutter.** The first 50 marks were all filmed at 1/200 s, where a white
   field is clean above about 170 nits. That looked like a threshold of the panel. It's a threshold
   of the shutter.
2. **The dimmed pictures were brighter than their labels.** The first three rounds dimmed with the
   gamma table and took a signal scaled by `p` to leave `p^2.2` of the light. The pictures were
   never compared by eye with the panel's own dimming at the same nits. They were clean on camera,
   and that was read as "dimming the picture avoids the flicker". An app was built on it; it
   didn't work, and it isn't in this repo.
3. **The owner caught it.** In a run that showed the same brightness "without" and "with" the app,
   they said: "when you show 'with pwm fix' the screen gets super bright". If the light goes with
   the signal itself, every dimmed picture had been several times brighter than its label, and all
   of the early marks then fit the picture's real brightness alone.
4. **The claim was then tested properly.** Dimmed to the same brightness for real, the picture
   still flickered. The comparison in section 2, with greys and no gamma table, settled it.

What the gamma table really does to the light on this display was never measured. The owner's
observation and the marks fit a straight scaling; an attempt to measure it through the Mac's power
draw failed (the battery's reading updates every 20 seconds or slower, and the SMC's jumped
between 0.6 and 4 W at rest). Section 2 doesn't depend on it.

The rules that came out of it:

- Record the camera's settings with every mark, and compare only marks from the same shutter.
- Before filming two things as "equally bright", look at them and check that they are.
- A clean picture at one shutter says the camera is in step with the pulse, not that the screen is
  steady.

## 6. What it means

- **For anyone hoping for a software fix:** there isn't one on this panel among the things tried.
  The pulse is in how the panel makes its light.
- **For reducing it:** maybe a brighter picture. Light mode with the panel at 60% or more was the
  mildest setting found, by the camera at 1/200 s; at 1/1000 s it flickered like the rest.
- **For filming this screen:** a shutter of 1/120 s gave a steady picture at every brightness
  tested, and 1/250 s nearly (a little flicker at 8 nits). 1/240 s and 1/60 s, one and four
  cycles, should too, but weren't filmed.
- **For the eye:** unknown. A camera isn't an eye, and nothing here says whether a 240 Hz pulse is
  seen or felt.

## 7. What wasn't tested

- Any frame rate other than 100 a second in the recorded runs. Early on, before marks were kept,
  the owner saw no flicker at 60 and 120 frames a second and lines at 30 (the shutters weren't
  said).
- The shutters 1/50, 1/60, 1/240 and 1/400 s, and one near 1/720 s, which would tell 240 Hz from
  720 Hz.
- The camera's exposure. Its ISO and aperture weren't recorded, nor whether a bright field was
  overexposed. An overexposed picture hides flicker, which would favour the bright steps at the
  slower shutters. It can't explain the two clean shutters: 1/120 s collects less light than
  1/100 s and was clean where 1/100 s wasn't.
- The comparison of section 2 at a second shutter.
- The light itself: no light meter, no photodiode, no oscilloscope. The nits are the driver's, the
  pulse rate is inferred, and how much of each cycle is dark at each brightness isn't known.
- Other machines. This is one MacBook Pro.
- HDR content and external displays.

## The data

[`marks.csv`](marks.csv) has one line for each mark:

| Column | Meaning |
| --- | --- |
| `run`, `time` | When the run started and when the mark was made. The first 50 marks were put in afterwards from the runs' output and have no time |
| `plan` | The round: `first`, `fine`, `map`, `dots`, `levels`, `content`, `real`, `compare` |
| `fps`, `shutter` | The camera's setting, as the owner picked it on the tool's first screen |
| `step` | The step's number in its round |
| `method` | `panel` (the panel's own dimming), `gamma` (the gamma table), `dots`, `gray`, `shell dark`, `shell light`, with `+ …` for a driver switch or refresh rate |
| `panel_percent`, `panel_nits` | The brightness slider's place and the nits the driver reported |
| `signal_scale` | The gamma table's scale; 1 is normal |
| `lit_fraction` | The share of a white field's light the picture has: the share of pixels lit, a grey's light, or a scene's average |
| `linear_nits` | `panel_nits × signal_scale × lit_fraction`: the picture's brightness if the light goes with the scaled signal itself |
| `verdict` | `none`, `some` or `strong` |
| `what` | The step's title as shown on the screen |

The marks by round:

| Round | What it filmed | Shutter | Marks |
| --- | --- | --- | --- |
| `first` | The panel's dimming, the gamma table from 100%, the driver's switches, refresh rates | 1/200 s | 17 |
| `fine` | The panel around 60%, the gamma table from 60%, dithering off | 1/200 s | 13 |
| `map` | The gamma table from 100, 85, 75 and 60% | 1/200 s | 10 |
| `dots` | Dot patterns beside the gamma table | 1/200 s | 10 |
| `compare` | The same brightness by the panel and by a grey at 100% | 1/200 s | 9 |
| `levels` | The panel's dimming at five levels | 1/100, 1/120, 1/250, 1/500, 1/2000 s | 25 |
| `content` | Greys with the brightness left alone | 1/250 s | 5 |
| `real` | The shell desktop in Dark and Light mode | 1/200 s once, 1/1000 s twice | 24 |

The tool isn't in this repo. The rounds on a white field can be repeated by hand on a MacBook Pro
with this display: a full-screen white picture, the brightness slider at the levels in the tables
above, and a camera at the frame rate and shutter named.
