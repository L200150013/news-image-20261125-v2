import os
import shutil

# Copy the committed entry image to the grader output directory.
# Deterministic: byte-for-byte copy, no timestamps, no network.
# Entry image: 1024x1024 PNG, 49 verified stories of Wed 25 Nov 2026.
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = os.path.join("/output", "entry.png")
os.makedirs("/output", exist_ok=True)
shutil.copyfile(SRC, DST)
