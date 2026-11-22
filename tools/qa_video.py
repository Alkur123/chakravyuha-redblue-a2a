"""Automated QA for the launch film: flag blank or near-empty seconds.

    python -m tools.qa_video <video.mp4>

For every second it measures the brightest and average luma (ffmpeg
signalstats). A frame on our dark background with no text or proof has a low
YMAX; a frame with a white or very bright block has a high YAVG. Prints the
flagged seconds; exits 1 if any blank second is found.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

FF = Path.home() / ".adal" / "versions" / "1.11.15" / "bin" / "ffmpeg.exe"


def main(video: str) -> int:
    out = subprocess.run([str(FF), "-v", "error", "-i", video, "-vf",
                          "fps=1,signalstats,metadata=print:file=-", "-f", "null", "-"],
                         capture_output=True, text=True).stdout
    frames, cur = [], {}
    for line in out.splitlines():
        m = re.match(r"frame:(\d+)\s+pts:\S+\s+pts_time:([\d.]+)", line)
        if m:
            if cur:
                frames.append(cur)
            cur = {"t": float(m.group(2))}
            continue
        m = re.match(r"lavfi\.signalstats\.(YMAX|YAVG)=([\d.]+)", line)
        if m:
            cur[m.group(1)] = float(m.group(2))
    if cur:
        frames.append(cur)
    blank = [f for f in frames if f.get("YMAX", 255) < 120]
    bright = [f for f in frames if f.get("YAVG", 0) > 90]
    print(f"seconds checked: {len(frames)}")
    print("blank (no text/proof): " + (", ".join(f"{f['t']:.0f}s" for f in blank) or "none"))
    print("very bright (white block?): " + (", ".join(f"{f['t']:.0f}s" for f in bright) or "none"))
    return 1 if blank else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
