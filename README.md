# countdown_monitor

## Motivation
I like the workout videos of Heather Robertson (https://heatherrobertson.com/), or
see https://www.youtube.com/watch?v=YHNnIbkmeDQ&list=PL2ov72VWpiOrEsWGIPMAoBVeYz-ahKJCR

I especially like that she doesn't talk but simply does. However, I'd like to be
able to listen to my own music and not the one she selects. But I need to hear
the "beep" sounds that signal the end of an exercise when the countdown goes to zero.

## Objective
1. Simplest solution - no GUI, just a CLI tool for MacOS
2. Monitor the on-screen countdown and translate it to a number using computer vision.
Emit sounds when the countdown goes to zero. 
3. Restrictions:
  3a. Only works on MacOS.
  3b. CLI only
  4b. No full-screen mode supported (reason: this would complicate screen capture)

Usage: open a video in your browser. Open the shell and run this app in setup mode 
to select the screen region containing the countdown (click a rectangle arounw the 
displayed countdown). Then run app in detection mode, then run video. 

To configure sounds, you can edit the dict SOUNDS = {...} in the code.

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

- Python >= 3.12
- tesseract, a tool for OCR must be installed, e.g.
```
> brew install tesseract
```

## Installation

No installation necessary.

## License

MIT — see [LICENSE](LICENSE).
