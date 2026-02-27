#!/usr/bin/env python3
"""
Workout Countdown Detector
Monitors a screen region for countdown numbers and plays alert sounds.
"""

import mss
import cv2
import numpy as np
import time
import subprocess
import json
from pathlib import Path

try:
    import pytesseract
except ImportError:
    print("pytesseract not found. Install with: pip install pytesseract")
    print("Also install Tesseract OCR: brew install tesseract")
    exit(1)

CONFIG_FILE = Path(__file__).parent / "countdown_region.json"

# macOS system sounds
SOUNDS = {
    4: "/System/Library/Sounds/Pop.aiff",
    3: "/System/Library/Sounds/Pop.aiff",
    2: "/System/Library/Sounds/Pop.aiff",
    1: "/System/Library/Sounds/Glass.aiff",
}


def play_sound(number: int):
    sound_file = SOUNDS.get(number)
    if sound_file:
        subprocess.Popen(["afplay", "-v", "8.0", sound_file],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)


def capture_region(region: dict) -> np.ndarray:
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def extract_number(img: np.ndarray) -> int | None:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    # OCR config: single line, digits only
    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(thresh, config=config).strip()

    try:
        return int(text)
    except ValueError:
        return None


def select_region() -> dict:
    """Interactive region selection using OpenCV."""
    print("\n=== Region Selection ===")
    print("1. Taking full screenshot...")

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Resize for display if too large
    h, w = img.shape[:2]
    scale = min(1.0, 1600 / w, 1000 / h)
    display_img = cv2.resize(img, None, fx=scale, fy=scale)

    print("2. Select the countdown region (drag a rectangle)")
    print("   Press ENTER to confirm, C to cancel")

    roi = cv2.selectROI("Select Countdown Region", display_img, fromCenter=False)
    cv2.destroyAllWindows()

    if roi == (0, 0, 0, 0):
        print("Selection cancelled.")
        return None

    # Scale back to actual coordinates
    x, y, w, h = roi
    region = {
        "left": int(x / scale) + monitor["left"],
        "top": int(y / scale) + monitor["top"],
        "width": int(w / scale),
        "height": int(h / scale),
    }

    print(f"3. Selected region: {region}")

    # Test OCR on selected region
    test_img = capture_region(region)
    number = extract_number(test_img)
    print(f"4. Test OCR result: {number}")

    return region


def save_region(region: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(region, f)
    print(f"Region saved to {CONFIG_FILE}")


def load_region() -> dict | None:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return None


def run_detection(region: dict):
    """Main detection loop."""
    print("\n=== Running Detection ===")
    print("Monitoring for countdown... Press Ctrl+C to stop.")
    print("-" * 40)

    last_number = None
    alert_triggered = set()

    max_number = max(SOUNDS.keys())

    try:
        while True:
            img = capture_region(region)
            number = extract_number(img)

            if number is not None:

                # try to detect mis-recognition
                if last_number is not None and last_number - number > 5:
                    print(f"  {number} misrecognized, expected {last_number-1}")
                    continue

                if number != last_number:
                    print(f"  {number}", end="", flush=True)

                    # Reset alerts when countdown restarts (number increases)
                    if last_number is not None and number > last_number:
                        alert_triggered.clear()

                    # Play sound for key values (only once per countdown)
                    if number in SOUNDS and number not in alert_triggered:
                        play_sound(number)
                        alert_triggered.add(number)
                        print(" 🔔", end="", flush=True)

                    print()
                    last_number = number

            time.sleep(0.15)

    except KeyboardInterrupt:
        print("\n\nStopped.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Workout Countdown Detector")
    parser.add_argument("--setup", action="store_true", help="Select screen region")
    parser.add_argument("--test", action="store_true", help="Test OCR on current region")
    args = parser.parse_args()

    if args.setup:
        region = select_region()
        if region:
            save_region(region)
    elif args.test:
        region = load_region()
        if not region:
            print("No region configured. Run with --setup first.")
            return
        img = capture_region(region)
        cv2.imwrite("test_capture.png", img)
        number = extract_number(img)
        print(f"Captured region saved to test_capture.png")
        print(f"Detected number: {number}")
    else:
        region = load_region()
        if not region:
            print("No region configured. Run with --setup first.")
            return
        run_detection(region)


if __name__ == "__main__":
    main()