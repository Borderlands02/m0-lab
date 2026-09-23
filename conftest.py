import sys
from pathlib import Path

# 让 `python -m pytest` 无论从哪个目录启动都能 import src.*
sys.path.insert(0, str(Path(__file__).resolve().parent))
