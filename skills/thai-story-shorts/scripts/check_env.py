"""Report which required tools are installed."""
import shutil
import sys

missing = [tool for tool in ("ffmpeg", "ffprobe", "node", "npx") if not shutil.which(tool)]
print("python", sys.version.split()[0])
print("missing:", ", ".join(missing) if missing else "none")
sys.exit(1 if missing else 0)
