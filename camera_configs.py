
import os
import subprocess
import time

fps = 100
configs = [
    (640, 360, 10000),

]

for w, h, fps in configs:
    env = os.environ.copy()
    env["CAMERA_WIDTH"] = str(w)
    env["CAMERA_HEIGHT"] = str(h)
    env["CAMERA_FPS"] = str(fps)

    print(f"Running with config: {w}x{h} @ {fps}fps")


    subprocess.run(['python', 'demo.py'], env=env)
    subprocess.run(['python', 'charts/plot.py'], env=env)
