# countdown_monitor
(c) @drakee @ gitub

## Motivation
I like the workout videos of Heather Robertson (https://heatherrobertson.com/), or
see https://www.youtube.com/watch?v=YHNnIbkmeDQ&list=PL2ov72VWpiOrEsWGIPMAoBVeYz-ahKJCR

I especially like that she doesn't talk much but simply shows. But I'd like to be
able to listen to my own music and not the one she' playing. At the same time 
I need to hear the "beep" sounds that signal the end of an exercise when the countdown 
reaches zero.

This script solves this problem by OCR'ing the countdown in the video and emitting 
sounds when the countdown reaches zero.

## Objectives
1. MacOS only. Simplest possible solution - no GUI, just a CLI tool
2. Monitor the on-screen countdown and translate it to a number using computer vision
and OCR (via the libray tesseract). Emit sounds when the countdown goes to zero. 
3. Restrictions:
  3a. Only works on MacOS.
  3b. CLI only
  3c. No full-screen mode supported (reason: this would complicate screen capture)

Usage: open a video in your browser. Open a MacOS shell and run this app in setup mode, 
then select the screen region containing the countdown (click a rectangle arounw the 
displayed countdown). Then run app in detection mode, then run video. 

To configure sounds, you can edit the dict SOUNDS = {...} in the file
countdown_monitor.py (just at the beginning)

Usage:
```
# 1. Select screen region interactively (once)
> uv run python countdown_monitor.py --setup

# 2. Run detection
> uv run python countdown_monitor.py

# 3. Optional: Test whether OCR is working
> uv run python countdown_monitor.py --test
```

## Agent coding:
Was coded with Claude. Transcript of code creation:
https://claude.ai/share/245dfdb1-cc7a-406c-8aff-4f6773d010cc


## Requirements
- Python --- I ran it on python 3.12
- see requirements.txt
- Program needs MacOS rights to read screen. When you run the app for the first time,
you will be asked to grant these rights to the MacOS app in which you run python. 
- tesseract, a tool for OCR must be installed, e.g.
```
> brew install tesseract
```

## Installation

No installation necessary.

## License

MIT — see [LICENSE](LICENSE).
