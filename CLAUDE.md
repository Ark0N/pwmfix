# PWMFix: notes for picking up work

The record of one day of testing (2026-11-12) whether software can dim the MacBook Pro's display
(PROLED XDR) without the flicker of the panel's own dimming. It can't, among the things tried. The
repo has the write-up, the data and the figures, and no other code than the script that draws the
figures. Start with `README.md` (the illustrated review), then `docs/review.md` (the full text)
and `docs/findings.md` (the working notes in the order things were found).

It grew out of LogoLight (`~/macostrayappapple`, github.com/Ark0N/LogoLight), where the user asked
"can we remove the pwm flickering at lower brightness?" (2026-11-12).

## The figures

```sh
scripts/make-figures.py    # draws docs/figures (a light and a dark SVG of each) from docs/marks.csv
```

The README shows them with `<picture>`, so GitHub picks the one for its theme. Run the script
again after new marks. `sips -s format png` renders an SVG for a look, without bold; an offscreen
`WKWebView` snapshot renders it properly. A headless Brave hung when tried.

## The tools aren't here

Every mark was made with `flickersweep`, a Swift tool that showed a test picture, set the display
up for a step, waited for the user's mark and saved it to `docs/marks.csv`; there were smaller
ones for the slider, the gamma table, the pulse width switch and dithering, and a menu bar app
built on the first reading. All of it was taken out of the repo (Decisions). The last source is in
the old history, which is kept in two places: the private repo `Ark0N/pwmfix-archive` and a local
bundle, `~/pwmfix-backup/pwmfix-history-2026-11-13.bundle` (`git clone` either: the tools are in
`tools/probes` at commit df230ba, the app at 14a0f2a).

## Rules, if filming is taken up again

- **Never let a failed build reach the screen.** Chain build-and-run with `&&`, not `;`, and don't
  pipe the build. Send its output to a file instead. A stale binary ran in LogoLight twice.
- The tools change the real screen. Say what's about to happen before running one while the user
  is at the Mac, and check afterwards that the slider and the gamma table are back. The gamma
  table goes back by itself when the process that set it exits; the brightness slider doesn't.
- Setting the slider drops auto-brightness's adjustment for a few minutes, so the panel comes back
  at other nits than it had. That's not a failed restore.
- Software can't see the flicker. Anything that claims to change it needs the user and a camera.
  Say so explicitly if it wasn't filmed.
- **Every filmed run starts on the tool's camera screen, where the user picks the frame rate and
  the shutter.** The user, 2026-11-12: "that was with 1/200 shutter and 100fps I can also test with
  other shutter speeds! always ask first which shutter setting I have before I do the testing so we
  can build some data!", then: "but always let me select that before the run starts", and later:
  "let me now at the start with setting I should use to makes sense to test". So don't pass the
  camera's settings for them, and say which setting makes sense and why, in the chat and on the
  picker. Every mark is saved with the camera's settings. The first 50 marks, all at 100 fps and
  1/200 s, were put in afterwards from the runs' output.
- A claim about flicker names the camera setting it was seen at. What a camera shows of a pulsing
  screen depends on its exposure time and frame rate, so "no flicker" at one setting isn't "no
  pulses".
- **Compare only marks from one run, or at least one shutter, and check by eye that two things
  called equally bright are.** Two wrong conclusions came from skipping that (Status).

## Git

- Remote: `https://github.com/Ark0N/pwmfix`, **public** since 2026-11-13, MIT. The user approved
  it after seeing the graphics at the top of the README. That repo was made new the same day, with
  one commit of the files as they were; the repo it replaced is the private `pwmfix-archive`. Ask
  before releasing anything, changing its visibility or touching the archive.
- **Fetch before pushing.** The user edits on GitHub too: on 2026-11-13 they added a note to the
  README there, and a push from here was rejected until it was rebased onto it.
- Work on `main`, commit in small logical steps, and push when a piece of work is done. Commit
  messages: a short imperative subject, then a body that explains *why*.

## Decisions (the user's call)

- **The repo is kept as a record of the findings** (2026-11-12: "keep the repo as a record of the
  findings"). Don't delete or archive anything unless they ask.
- **The README is the review, with graphics**: "make the read in the readme with nice graphics and
  stuff", "and link to all results" (2026-11-12). `docs/review.md` is the longer text behind it.
  Keep the two in step.
- **No Swift code in the repo** (2026-11-13). First: "remove the whole swift program from the repo
  anyway", which took out the app; then, asked what should go public of the test tools that were
  kept, they chose to remove all Swift code. Don't bring any of it back unless they ask.
- **MIT license** (chosen 2026-11-13), as LogoLight has.
- **The public history started fresh** (chosen 2026-11-13): one clean commit, in a new repo, so
  that nothing removed can be reached from it. Don't push the old history to it.
- **The README's note under the summary is the user's own**, added on GitHub (2026-11-13): "I hope
  someone can prove me wrong about this data. And maybe there is a fix for this! I am open to
  inputs. I think scientifically." They wrote "proof me wrong" and had that one word fixed. Leave
  the rest of its wording alone unless they ask.
- **The two graphics at the top** (2026-11-13; `hero` and `funny` in `scripts/make-figures.py`).
  The first was asked for as "one cool graphic for the top", to be shown and approved before the
  repo went public. A draft with a pulse train, three shutters and meters was "too unclear make it
  simpler"; one with only the headline and a row of pulses: "the graphic should show all the
  shutter speeds tested, simple!". The one kept has a bar for each of the seven shutters under the
  pulses. The second was asked for as "a funny graphic that showcases IF the software would
  exist!": the app as an advertisement, with "0 % less flicker". Shown both, they chose the first
  on top and the joke below it.
- **The name**: the user floated "pwmfix" and then asked for the folder and the repo under that
  name.

## Status

Nothing is being built. What the testing found (113 marks, all by the user's iPhone 18 Pro at 100
frames a second; which app and lens wasn't said):

- **The panel pulses at every brightness**, white at 100% too (strong at 1/2000 s at every level).
- **The rate is about 240 Hz by the simplest reading**: 1/120 s (two cycles) hides the flicker at
  every level and 1/250 s (0.96 of one) nearly; 1/100 s, a slower shutter that doesn't fit, shows
  it. Any multiple of 240 Hz hides at the same two shutters: 480 and 960 Hz are out (1/500 s),
  1200 Hz (1/200 s); 720 Hz isn't, and a shutter near 1/720 s would tell. The rate shows only at
  140 nits and below; above that the pulse showed only at 1/500 s and faster.
- **Dimming the picture instead of the panel doesn't help** (the `compare` round, 1/200 s, one
  run): strong flicker both ways at 140, 80, 45 and 15 nits.
- **Nothing else in software changed it**: dot patterns, the driver's pulse width switch,
  dithering off, 60, 50 and 48 Hz, the display's presets (the user's own try; which presets and
  camera setting wasn't said).
- **A brighter picture showed less of it at 1/200 s**: a shell in Light mode was clean down to the
  panel at 60%, in Dark mode never. At 1/1000 s both were strong.

How the first reading went wrong, for about two hours: every mark was at one shutter (1/200 s),
and the pictures dimmed with the gamma table were brighter than their labels (the tools took a
signal scaled by `p` to leave `p^2.2` of the light; it leaves about `p`). The user caught it
during a WITHOUT and WITH demo: "the Problem is when you show 'with pwm fix' the screen gets super
bright!", and after a run dimmed linearly: "now I still get flickering at the low nits?". The gamma
table's real curve was never measured.

What a correctness sweep changed on 2026-11-13, because the text claimed more than the marks carry:

- 240 Hz became "the simplest rate that fits" (above).
- 1/250 s wasn't predicted before it was first filmed. The `content` greys happened to be filmed
  at it and were clean; that gave the idea, which then predicted the two `levels` runs.
- The camera's exposure was never recorded (ISO, aperture, whether white was overexposed). An
  overexposed picture hides flicker.
- The second 1/1000 s `real` run was started just after the user said "I will continue with
  1/200". They picked 1/1000 themselves (the picker had nothing picked then), and the marks match
  the first 1/1000 s run, so it's kept; they never said which it was.

Not filmed: other frame rates; 1/50, 1/60, 1/240, 1/400 and about 1/720 s; the comparison at a
second shutter. Not tried: the apps that already dim with the gamma table (Dimit's "PWM-Safe
mode", Gamma Dimmer, Gamma Control, BetterDisplay, Lunar). Whether any of it matters to the eye
hasn't been asked.
