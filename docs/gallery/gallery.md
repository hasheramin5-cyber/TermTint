# TermTint Gallery

Ye gallery dikhati hai ke TermTint ka output asal terminal mein kaisa nazar aata hai.
Har screenshot TermTint ke apne primitives (`colored()`, `styled()`, `Style`, `Theme`,
`visible_len()`) se banaya gaya hai. Tables, dashboards aur diff viewers library ke
built-in widgets nahi hain, ye sirf is baat ki misaal hain ke in primitives se kya kuch
banaya ja sakta hai.

Kul 27 pages hain.

## Contents

- [Overview](#overview)
- [Matrix: named foreground x background](#matrix-named-foreground-x-background)
- [Styles](#styles)
- [Readability](#readability)
- [Badges](#badges)
- [UI examples](#ui-examples)
- [256 colours](#256-colours)
- [True Color aur fallback](#true-color-aur-fallback)
- [Utilities](#utilities)
- [Palettes](#palettes)

---

## Overview

![Overview](termtint_pro_01_overview.png)

Gallery ka cover page: coverage badges (8 named fg/bg colours, 256-colour, True Color,
8 styles, 5 theme roles, chainable `Style()`, 3 fallback tiers, ANSI utils, `print_*`
helpers, WCAG contrast), saare 27 pages ka index aur environment ki maloomat.

---

## Matrix: named foreground x background

Saari 56 named fg/bg pairs, alag-alag text styles ke sath. Rows foreground hain aur
columns background.

### Normal, italic, underline

![Matrix: normal, italic, underline](termtint_pro_02_matrix-normal-italic-ul.png)

Teen styles (`normal`, `italic`, `underline`) ka matrix. Jin pairs mein fg aur bg ek hi
colour ho, wahan `--` dikhaya gaya hai.

### Bold, dim, reverse

![Matrix: bold, dim, reverse](termtint_pro_03_matrix-bold-dim-reverse.png)

Wahi pairs `bold`, `dim` aur `reverse` ke sath. `reverse` mein fg aur bg aapas mein
badal jate hain, is liye us matrix ki shakal baqi se mukhtalif hai.

### Strikethrough aur combinations

![Matrix: strikethrough, bold+italic, bold+underline](termtint_pro_04_matrix-strike-combos.png)

`strikethrough` aur do combined styles (`bold + italic`, `bold + underline`).

---

## Styles

### Styles x colours

![Styles x colours](termtint_pro_05_styles-x-colours.png)

Har style named foreground, named background aur RGB foreground colours ke muqable mein.
Is se andaza hota hai ke `bold`, `bright`, `dim` aur baqi styles alag-alag colour system
par kaisay dikhte hain.

### Style combinations

![Style combinations](termtint_pro_06_style-combinations.png)

Chhe independent styles ke saare pairs (15) aur triples (20). Neeche input syntaxes
(list, tuple, comma-separated string) aur teeno colour systems (named, 256, RGB) ke
sath combinations bhi dikhaye gaye hain.

---

## Readability

### Best 28

![Readability: best 28](termtint_pro_07_readability-best-28.png)

Har named pair ka WCAG contrast ratio, behtareen se shuru karke. `black/white` sab se
upar hai (16.7:1). Is page ke mutabiq 8 pairs AAA, 2 AA, 16 AA-L aur 30 FAIL hain.

### Worst 28

![Readability: worst 28](termtint_pro_08_readability-worst-28.png)

Mushkil se parhi jane wali aadhi list: wo combinations jin se bachna chahiye, jaise
`red/magenta`, `blue/red` aur `cyan/green`.

---

## Badges

### Status labels

![Badges: status labels](termtint_pro_09_badges-status-labels.png)

Chaudah labels (DEBUG, INFO, OK, PASS, WARN, SLOW, FAIL, ERROR, FATAL, NEW, BETA,
STABLE, DEPRECATED, SKIP) aath badge treatments mein: solid, chip, reverse, underline,
hashtag italic, dim brackets, struck aur rounded caps. Neeche status dots, keycaps aur
counters bhi hain.

### Shields-style pills

![Badges: shields pills](termtint_pro_10_badges-shields-pills.png)

Do-hissay wale label/value badges named, 256-colour aur True Color mein, square badges,
gradient progress badges aur release channel strip.

---

## UI examples

### Log viewer

![Log viewer](termtint_pro_11_log-viewer.png)

Structured logs jin mein level badges, inline markup (bold, underline, italic) aur
filters hain. Neeche ek traceback block bhi hai.

### Diff viewer

![Diff viewer](termtint_pro_12_diff-viewer.png)

Unified diff jis mein line gutters aur word-level highlights RGB backgrounds se banaye
gaye hain. Neeche file-wise summary aur legend hai.

### Tables

![Tables](termtint_pro_13_tables.png)

Box-drawn tables jo `visible_len()` se align kiye gaye hain aur badges aur bars ke sath
mile hue hain: service health, SGR reference aur colour depth tiers.

### Dashboard

![Dashboard](termtint_pro_14_dashboard.png)

Gauges, sparklines, alerts aur background colours se banai gayi latency heat-map
(viridis palette, True Color).

### CI pipeline

![CI pipeline](termtint_pro_15_ci-pipeline.png)

Stage flow, jobs ki timeline bars aur ek failing job ka tail.

### CLI help aur traceback

![CLI help and traceback](termtint_pro_16_cli-help-traceback.png)

Rangeen `--help` screen aur ek Python traceback, exit code aur timing badges ke sath.

---

## 256 colours

### Full grid

![256 colours: full grid](termtint_pro_17_256-colours-full-grid.png)

0 se 255 tak har index background (`bg_color256=N`) aur foreground (`color256=N`) dono
tarah. 0-15 system colours hain, 16-231 ka 6x6x6 cube hai aur 232-255 grayscale hain.

### Cube aur mazeed

![256 colours: cube and more](termtint_pro_18_256-colours-cube-more.png)

6x6x6 colour cube red level ke hisab se katta hua, grayscale ramp, system colours
(0-15) aur chune hue indices ka fg/bg crossover grid.

---

## True Color aur fallback

### True Color gradients

![True Color gradients](termtint_pro_19_true-color-gradients.png)

Gradient bars (har cell ke liye ek `bg_rgb`), HSV explorer, saturation ramp, rainbow
strip aur rainbow text jis mein har character ke liye ek escape sequence hai.

### Fallback: 3 tiers

![Fallback: 3 tiers](termtint_pro_20_fallback-3-tiers.png)

Wahi `fallback=True` colours `FORCE_COLOR=3` (truecolor), `FORCE_COLOR=2` (256-colour)
aur `FORCE_COLOR=1` (16-colour) par.

---

## Utilities

![Utilities and print helpers](termtint_pro_21_utilities-print.png)

`strip_ansi()` aur `visible_len()` ki misalen (len, visible width, saaf text aur raw
repr), saare `print_*` helpers, aur `supports_color`, `supports_256color`,
`supports_truecolor` ka jawab alag-alag environment variables par.

---

## Palettes

Har page par ek hi sample alag colour scheme mein: swatches, shell prompt, test
results, Python syntax highlighting, log badges, table, gradient, styles aur theme roles.

### Dracula

![Palette: Dracula](termtint_pro_22_palette-dracula.png)

### Nord

![Palette: Nord](termtint_pro_23_palette-nord.png)

### Solarized Dark

![Palette: Solarized Dark](termtint_pro_24_palette-solarized-dark.png)

### Gruvbox

![Palette: Gruvbox](termtint_pro_25_palette-gruvbox.png)

### Tokyo Night

![Palette: Tokyo Night](termtint_pro_26_palette-tokyo-night.png)

### Catppuccin Mocha

![Palette: Catppuccin Mocha](termtint_pro_27_palette-catppuccin-mocha.png)
