
import os
import subprocess

configs = [
    (640,480, 30),
    (1280, 720, 60),
    (1920, 1080, 60),
    (640,480, 100),
]

for w, h, fps in configs:
    env = os.environ.copy()
    env["CAMERA_WIDTH"] = str(w)
    env["CAMERA_HEIGHT"] = str(h)
    env["CAMERA_FPS"] = str(fps)

    print(f"Running with config: {w}x{h} @ {fps}fps")

    demo_process = subprocess.Popen(['python', 'demo.py'], env=env) 

    subprocess.run(['python', 'buffer_test.py', 'consume'], env=env)
