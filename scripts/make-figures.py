#!/usr/bin/env python3
"""Draws the README's figures from docs/marks.csv, as SVG, each for GitHub's light and dark theme.

    scripts/make-figures.py        # writes docs/figures/*-light.svg and *-dark.svg

The three grades of flicker are an ordered scale, so they share one hue in three steps: darker
means more on the light surface, lighter means more on the dark one. Both ramps pass the dataviz
palette validator's ordinal checks. Text never wears a data colour.
"""
import csv
import math
import pathlib
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "figures"
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'
W = 880

MODES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781", grid="#e1e0d9", axis="#c3c2b7",
                  border="#0b0b0b", ramp={"none": "#86b6ef", "some": "#2a78d6", "strong": "#104281"}, accent="#2a78d6",
                  rest="#898781"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781", grid="#2c2c2a", axis="#383835",
                 border="#ffffff", ramp={"none": "#184f95", "some": "#3987e5", "strong": "#9ec5f4"}, accent="#3987e5",
                 rest="#898781"),
}
GRADES = ["none", "some", "strong"]
PULSE_HZ = 240


def marks():
    with open(ROOT / "docs" / "marks.csv", newline="") as file:
        return list(csv.DictReader(file))


def shutter_seconds(text):
    top, bottom = text.split("/")
    return float(top) / float(bottom)


class Figure:
    """One card: a rounded surface with a title, a subtitle and whatever is drawn on it."""

    def __init__(self, mode, height, title, subtitle=""):
        self.c = MODES[mode]
        self.height = height
        self.parts = []
        self.rect(0.5, 0.5, W - 1, height - 1, self.c["surface"], rx=12, stroke=self.c["border"], stroke_opacity=0.10)
        if title:
            self.text(28, 40, title, size=16, weight=600)
        if subtitle:
            self.text(28, 62, subtitle, size=13, color=self.c["ink2"])

    def rect(self, x, y, w, h, fill, rx=0, stroke=None, stroke_opacity=1.0):
        extra = f' stroke="{stroke}" stroke-opacity="{stroke_opacity}"' if stroke else ""
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, color):
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1"/>')

    def text(self, x, y, value, size=13, weight=400, color=None, anchor="start", halo=False):
        """`halo` puts a ring of surface round the letters, so a line behind them doesn't run through.
        It's a second copy drawn underneath, since not every renderer knows `paint-order`."""
        common = f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"'
        if halo:
            surface = self.c["surface"]
            self.parts.append(f'<text {common} fill="{surface}" stroke="{surface}" stroke-width="5" '
                              f'stroke-linejoin="round">{escape(value)}</text>')
        self.parts.append(f'<text {common} fill="{color or self.c["ink"]}">{escape(value)}</text>')

    def cell(self, x, y, w, h, grades):
        """A grid cell with a 2px gap of surface around it; two grades split it down the middle."""
        grades = sorted(set(grades), key=GRADES.index)
        if not grades:
            self.text(x + w / 2, y + h / 2 + 4, "–", color=self.c["muted"], anchor="middle")
            return
        part = (w - 2) / len(grades)
        for place, grade in enumerate(grades):
            self.rect(x + 1 + place * part + (1 if place else 0), y + 1, part - (1 if len(grades) > 1 else 0), h - 2,
                      self.c["ramp"][grade], rx=3)

    def legend(self, x, y, note=""):
        self.text(x, y + 10, "Flicker", size=12, color=self.c["ink2"])
        x += 52
        for grade in GRADES:
            self.rect(x, y, 12, 12, self.c["ramp"][grade], rx=2)
            self.text(x + 18, y + 10, grade, size=12, color=self.c["ink2"])
            x += 30 + 7 * len(grade) + 14
        if note:
            self.text(x + 6, y + 10, note, size=12, color=self.c["muted"])

    def save(self, name, mode):
        body = "\n".join(self.parts)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {self.height}" width="{W}" height="{self.height}" '
               f'font-family=\'{FONT}\'>\n{body}\n</svg>\n')
        (OUT / f"{name}-{mode}.svg").write_text(svg)


def shutters(mode, rows):
    """The panel's own dimming on a white field: brightness down, shutters across."""
    levels = [(100, "600–720 nits"), (60, "176–211 nits"), (50, "140 nits"), (40, "45 nits"), (25, "8 nits")]
    plain = [row for row in rows if row["method"] == "panel"]
    speeds = sorted({row["shutter"] for row in plain if row["plan"] == "levels"} | {"1/200"}, key=shutter_seconds, reverse=True)
    figure = Figure(mode, 432, "Flicker on a white field, by shutter and brightness",
                    "The panel's own dimming, filmed at 100 frames a second. Each cell is what the camera showed.")
    c = figure.c
    x0, y0, cw, rh = 214, 124, 104, 46
    for column, speed in enumerate(speeds):
        middle = x0 + column * cw + cw / 2
        cycles = shutter_seconds(speed) * PULSE_HZ
        figure.text(middle, y0 - 26, f"{speed} s", weight=600, anchor="middle")
        figure.text(middle, y0 - 9, f"{cycles:.2g} cycles", size=11.5, color=c["muted"], anchor="middle")
        if abs(cycles - round(cycles)) < 0.06:
            figure.text(middle, y0 + len(levels) * rh + 20, "whole cycles: hidden", size=11.5, color=c["ink2"], anchor="middle")
    for line, (percent, nits) in enumerate(levels):
        y = y0 + line * rh
        figure.text(28, y + rh / 2 + 4, f"{percent}%", weight=600)
        figure.text(72, y + rh / 2 + 4, nits, size=12.5, color=c["ink2"])
        for column, speed in enumerate(speeds):
            grades = [row["verdict"] for row in plain if row["shutter"] == speed and int(row["panel_percent"]) == percent]
            figure.cell(x0 + column * cw, y, cw, rh, grades)
    figure.legend(28, figure.height - 36, "A split cell was marked differently in two runs.")
    figure.save("shutters", mode)


def cycles(mode):
    """How long each shutter's exposure is, against the pulse's cycle."""
    figure = Figure(mode, 394, "An exposure that spans whole cycles hides the pulse",
                    "The length of each shutter's exposure against a 240 Hz cycle of 4.2 ms. Flicker as filmed at 45 nits.")
    c = figure.c
    speeds = [("1/100", "some"), ("1/120", "none"), ("1/200", "strong"), ("1/250", "none"), ("1/500", "strong"), ("1/2000", "strong")]
    x0, y0, per_ms, rh, thick = 112, 122, 50, 32, 14
    bottom = y0 + len(speeds) * rh
    for count in (1, 2):
        x = x0 + count * 1000 / PULSE_HZ * per_ms
        figure.line(x, y0 - 6, x, bottom, c["axis"])
        figure.text(x, y0 - 14, f"{count} cycle{'s' if count > 1 else ''}", size=11.5, color=c["ink2"], anchor="middle")
    for tick in range(0, 11, 2):
        figure.text(x0 + tick * per_ms, bottom + 18, f"{tick} ms" if tick else "0", size=11.5, color=c["muted"], anchor="middle")
    for line, (speed, grade) in enumerate(speeds):
        y = y0 + line * rh + (rh - thick) / 2
        length = shutter_seconds(speed) * 1000 * per_ms
        hides = grade == "none"
        figure.text(x0 - 12, y + thick / 2 + 4, f"{speed} s", weight=600, anchor="end")
        figure.parts.append(f'<path d="M{x0},{y:.1f} h{length - 4:.1f} a4,4 0 0 1 4,4 v{thick - 8} a4,4 0 0 1 -4,4 h-{length - 4:.1f} z" '
                            f'fill="{c["accent"] if hides else c["rest"]}"/>')
        note = f"{shutter_seconds(speed) * PULSE_HZ:.2g} cycles · {'hides it' if hides else grade + ' flicker'}"
        figure.text(x0 + length + 10, y + thick / 2 + 4, note, size=12, color=c["ink2"], halo=True)
    figure.line(x0, y0 - 6, x0, bottom, c["axis"])
    y = figure.height - 36
    figure.rect(28, y, 12, 12, c["accent"], rx=2)
    figure.text(46, y + 10, "hides the flicker", size=12, color=c["ink2"])
    figure.rect(168, y, 12, 12, c["rest"], rx=2)
    figure.text(186, y + 10, "shows it", size=12, color=c["ink2"])
    figure.save("cycles", mode)


def compare(mode, rows):
    """The same brightness by the panel's own dimming and by a grey on the panel at 100%."""
    run = [row for row in rows if row["plan"] == "compare"]
    reference = [row for row in run if row["method"] == "panel" and row["panel_percent"] == "100"]
    dimmed = [row for row in run if row["method"] == "panel" and row["panel_percent"] != "100"]
    grey = [row for row in run if row["method"] == "gray"]
    figure = Figure(mode, 250, "The same brightness, reached two ways",
                    "One run at 100 frames a second and 1/200 s. Dimming the picture instead of the panel changes nothing.")
    c = figure.c
    x0, y0, cw, rh = 262, 112, 116, 46
    columns = [("600 nits", reference, [])] + [(f"{float(row['panel_nits']):.0f} nits", [row], [other])
                                                 for row, other in zip(dimmed, grey)]
    for column, (label, top, low) in enumerate(columns):
        x = x0 + column * cw
        figure.text(x + cw / 2, y0 - 10, label, weight=600, anchor="middle")
        figure.cell(x, y0, cw, rh, [row["verdict"] for row in top])
        figure.cell(x, y0 + rh, cw, rh, [row["verdict"] for row in low])
    for line, (name, detail) in enumerate([("The panel dimmed", "a white field"), ("The panel at 100%", "a grey of the same nits")]):
        y = y0 + line * rh
        figure.text(28, y + 21, name, weight=600)
        figure.text(28, y + 38, detail, size=12, color=c["ink2"])
    figure.legend(28, figure.height - 36)
    figure.save("compare", mode)


def modes(mode, rows):
    """A shell window in Dark and in Light mode, at four brightness levels."""
    run = [row for row in rows if row["plan"] == "real" and row["shutter"] == "1/200"]
    figure = Figure(mode, 262, "A shell window in Dark mode and in Light mode",
                    "The same made-up desktop, filmed at 100 frames a second and 1/200 s.")
    c = figure.c
    x0, y0, cw, rh = 262, 120, 145, 46
    percents = []
    for row in run:
        if row["panel_percent"] not in percents:
            percents.append(row["panel_percent"])
    for column, percent in enumerate(percents):
        x = x0 + column * cw
        nits = [float(row["panel_nits"]) for row in run if row["panel_percent"] == percent]
        usual = column == 0
        figure.text(x + cw / 2, y0 - 26, "as it was set" if usual else f"panel at {percent}%", weight=600, anchor="middle")
        spread = f"{min(nits):.0f}–{max(nits):.0f} nits" if max(nits) - min(nits) > 5 else f"{nits[0]:.0f} nits"
        figure.text(x + cw / 2, y0 - 9, spread, size=11.5, color=c["muted"], anchor="middle")
        for line, look in enumerate(["shell dark", "shell light"]):
            grades = [row["verdict"] for row in run if row["panel_percent"] == percent and row["method"] == look]
            figure.cell(x, y0 + line * rh, cw, rh, grades)
    for line, (name, look, window, bar, ink) in enumerate([("Dark mode", "shell dark", "#121212", "#383838", "#dbdbdb"),
                                                           ("Light mode", "shell light", "#ffffff", "#e6e6e6", "#1f1f1f")]):
        y = y0 + line * rh
        share = float(next(row["lit_fraction"] for row in run if row["method"] == look))
        figure.rect(28, y + 9, 40, 28, window, rx=4, stroke=c["border"], stroke_opacity=0.25)
        figure.rect(28.5, y + 9.5, 39, 6, bar, rx=3)
        for place, width in enumerate([22, 30, 16]):
            figure.rect(33, y + 19.5 + place * 5, width, 1.6, ink)
        figure.text(82, y + 21, name, weight=600)
        figure.text(82, y + 38, f"{share * 100:.0f}% of a white screen's light", size=12, color=c["ink2"])
    figure.legend(28, figure.height - 36)
    figure.save("modes", mode)


def hero(mode, rows):
    """The banner at the top of the README: every shutter that was filmed, as a bar the length of
    its exposure, under the pulses it has to fit.

    The pulses are a drawing (the pulse's shape wasn't measured). Each verdict is the mark made with
    the panel at 40% (45 nits): on a white field, or on the shell desktop for the one shutter that
    was only filmed there."""
    c = MODES[mode]
    dark = mode == "dark"
    figure = Figure(mode, 496, "")
    add = figure.parts.append
    core = c["ramp"]["strong"] if dark else c["accent"]
    add('<defs><filter id="hero-glow" x="-80%" y="-80%" width="260%" height="260%">'
        '<feGaussianBlur stdDeviation="10"/></filter></defs>')

    add(f'<text x="28" y="42" font-size="11" letter-spacing="0.8" fill="{c["muted"]}">'
        f'MACBOOK PRO  ·  PROLED XDR DISPLAY  ·  FILMED WITH AN IPHONE 18 PRO AT 100 FRAMES A SECOND</text>')
    figure.text(26, 114, "≈ 240 Hz", size=64, weight=700)
    figure.text(30, 139, "the simplest rate that fits the marks", size=12, color=c["muted"])
    figure.text(344, 94, "The display's light pulses at every brightness.", size=18, weight=600)
    figure.text(344, 119, "Nothing tried in software removes it.", size=18, color=c["ink2"])

    # Time runs to the right from x0: the pulses on top, one bar for each shutter under them.
    period = 1000 / PULSE_HZ
    x0, per_ms, top, tall = 104, 54, 184, 52
    first, pitch, thick = top + tall + 22, 26, 14
    speeds = sorted({row["shutter"] for row in rows}, key=shutter_seconds, reverse=True)
    bottom = first + (len(speeds) - 1) * pitch + thick
    for count in (1, 2):
        x = x0 + count * period * per_ms
        add(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{bottom + 4}" stroke="{c["axis"]}" stroke-width="1" stroke-dasharray="2 3"/>')
        figure.text(x + 6, top - 10, f"{count} pulse{'s' if count > 1 else ''}", size=11, color=c["muted"])
    lit = 0.2 * period * per_ms
    pulses = "".join(f'<path d="M{x0 + place * period * per_ms:.1f},{top + tall} v-{tall - 6} a6,6 0 0 1 6,-6 h{lit - 12:.1f} '
                     f'a6,6 0 0 1 6,6 v{tall - 6} z"/>' for place in range(4))
    add(f'<g fill="{c["accent"]}" opacity="{0.9 if dark else 0.32}" filter="url(#hero-glow)">{pulses}</g>')
    add(f'<g fill="{core}">{pulses}</g>')
    figure.line(x0, top + tall, W - 28, top + tall, c["axis"])
    figure.text(28, top + 24, "The light", weight=600)
    figure.text(28, top + 41, "of the display", size=11.5, color=c["ink2"])

    for line, speed in enumerate(speeds):
        y = first + line * pitch
        marks_here = [row["verdict"] for row in rows if row["shutter"] == speed and row["panel_percent"] == "40"
                      and row["method"] in ("panel", "shell dark", "shell light")]
        clean = set(marks_here) == {"none"}
        length = shutter_seconds(speed) * 1000 * per_ms
        figure.text(28, y + 12, f"{speed} s", weight=600)
        add(f'<path d="M{x0},{y} h{length - 4:.1f} a4,4 0 0 1 4,4 v{thick - 8} a4,4 0 0 1 -4,4 h-{length - 4:.1f} z" '
            f'fill="{core if clean else c["rest"]}"/>')
        if clean:
            figure.text(x0 + length + 10, y + 12, "no flicker", size=12.5, weight=600, halo=True)
        else:
            figure.text(x0 + length + 10, y + 12, "flicker", size=12.5, color=c["ink2"], halo=True)
    figure.line(x0, top + tall, x0, bottom + 4, c["axis"])

    figure.text(28, bottom + 30, "Each bar is how long the shutter stays open. The two that fit whole pulses showed no flicker "
                "(filmed with the screen dimmed to 45 nits).", size=11.5, color=c["muted"])
    figure.text(28, bottom + 47, "A drawing: the pulse's shape wasn't measured. 1/1000 s was filmed on a desktop picture, the rest on "
                "a white field.", size=11.5, color=c["muted"])
    figure.save("hero", mode)


def funny(mode):
    """A joke under the banner: PWMFix as an advertisement, if it existed. Nothing in it is data."""
    c = MODES[mode]
    dark = mode == "dark"
    panel, rule = ("#262624", "#383835") if dark else ("#ffffff", c["grid"])
    figure = Figure(mode, 452, "")
    add = figure.parts.append
    add('<defs><filter id="funny-glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7"/></filter>'
        '<filter id="funny-shadow" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur stdDeviation="9"/></filter></defs>')

    def spaced(x, y, value):
        add(f'<text x="{x}" y="{y}" font-size="11" letter-spacing="0.8" fill="{c["muted"]}">{escape(value)}</text>')

    spaced(28, 42, "COMING NEVER  ·  FOR THE MACBOOK PRO WITH PROLED XDR DISPLAY")
    figure.text(26, 108, "PWMFix", size=60, weight=700)
    figure.text(290, 86, "The software fix for display flicker.*", size=19, weight=600)
    figure.text(290, 111, "If it existed.", size=19, color=c["ink2"])

    # The app: a little menu with one switch and one slider.
    x, y, w, h = 28, 170, 300, 160
    add(f'<rect x="{x}" y="{y + 6}" width="{w}" height="{h}" rx="14" fill="#000000" opacity="{0.45 if dark else 0.14}" '
        f'filter="url(#funny-shadow)"/>')
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{panel}" stroke="{c["border"]}" stroke-opacity="0.14"/>')
    figure.text(x + 20, y + 38, "Dim Without Flicker", size=14, weight=600)
    add(f'<rect x="{x + w - 64}" y="{y + 21}" width="44" height="24" rx="12" fill="{c["accent"]}"/>')
    add(f'<circle cx="{x + w - 32}" cy="{y + 33}" r="10" fill="#ffffff"/>')
    figure.line(x + 20, y + 60, x + w - 20, y + 60, rule)
    middle, track = y + 86, w - 96
    add(f'<circle cx="{x + 28}" cy="{middle}" r="3.5" fill="{c["muted"]}"/>')
    figure.rect(x + 46, middle - 2, track, 4, rule, rx=2)
    figure.rect(x + 46, middle - 2, track * 0.36, 4, c["accent"], rx=2)
    add(f'<circle cx="{x + 46 + track * 0.36:.1f}" cy="{middle}" r="8" fill="#ffffff" stroke="{c["axis"]}"/>')
    sun = x + w - 26
    add(f'<circle cx="{sun}" cy="{middle}" r="4.5" fill="{c["muted"]}"/>')
    for ray in range(8):
        dx, dy = math.cos(ray * math.pi / 4), math.sin(ray * math.pi / 4)
        add(f'<line x1="{sun + 7 * dx:.1f}" y1="{middle + 7 * dy:.1f}" x2="{sun + 9.5 * dx:.1f}" y2="{middle + 9.5 * dy:.1f}" '
            f'stroke="{c["muted"]}" stroke-width="1.4" stroke-linecap="round"/>')
    figure.line(x + 20, y + 112, x + w - 20, y + 112, rule)
    figure.text(x + 20, y + 139, "Flicker removed", color=c["ink2"])
    figure.text(x + w - 20, y + 139, "0 %", weight=700, anchor="end")

    # Without and with: the same pulses twice, on a screen that's dark in both themes.
    for left, title in ((372, "WITHOUT PWMFIX"), (624, "WITH PWMFIX")):
        spaced(left, 186, title)
        add(f'<rect x="{left}" y="196" width="228" height="112" rx="10" fill="#111110" stroke="{c["border"]}" stroke-opacity="0.16"/>')
        bars = "".join(f'<path d="M{left + 30 + place * 38},284 v-52 a5,5 0 0 1 5,-5 h6 a5,5 0 0 1 5,5 v52 z"/>' for place in range(5))
        add(f'<g fill="#3987e5" opacity="0.9" filter="url(#funny-glow)">{bars}</g><g fill="#9ec5f4">{bars}</g>')
        add(f'<line x1="{left + 18}" y1="284" x2="{left + 210}" y2="284" stroke="#4a4a46"/>')
    figure.text(612, 262, "=", size=30, weight=600, color=c["ink2"], anchor="middle")
    add(f'<g transform="rotate(-7 782 200)"><rect x="700" y="184" width="164" height="30" rx="15" fill="{c["accent"]}"/>'
        f'<text x="782" y="204" font-size="12.5" font-weight="700" text-anchor="middle" fill="#ffffff" letter-spacing="0.6">'
        f'0 % LESS FLICKER!</text></g>')
    figure.text(612, 336, "Same panel. Same pulses. Same flicker.", size=14, weight=600, anchor="middle")

    add(f'<text x="28" y="384" font-size="15"><tspan fill="{c["accent"]}" letter-spacing="2">★★★★★</tspan>'
        f'<tspan dx="10" font-weight="600" fill="{c["ink"]}">“I can’t see any difference.”</tspan>'
        f'<tspan dx="8" font-size="12.5" fill="{c["ink2"]}">my iPhone 18 Pro, at 1/200 s</tspan></text>')
    figure.text(28, 424, "* It doesn't exist: the one I built and filmed at seven shutter speeds left the flicker where it was. "
                "The data: github.com/Ark0N/pwmfix", size=11.5, color=c["muted"])
    figure.save("funny", mode)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = marks()
    for mode in MODES:
        hero(mode, rows)
        funny(mode)
        shutters(mode, rows)
        cycles(mode)
        compare(mode, rows)
        modes(mode, rows)
    print(f"{len(list(OUT.glob('*.svg')))} figures in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
