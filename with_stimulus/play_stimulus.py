import time
import subprocess
from datetime import datetime


def play_video(vlc_path, video_path, sharedstate):
    sharedstate.wait_for_thread.wait()

    DETACHED_PROCESS = 0x00000008
    process = subprocess.Popen([
        vlc_path,
        video_path,
        "--play-and-exit",
        "--no-video-title-show",
        "--no-video-deco",
        "--fullscreen",
        "--quiet",
        "--directx-device=\\.\DISPLAY2",  # Windows-specific
    ], creationflags=DETACHED_PROCESS)

    # Optionally: Wait until process starts running a bit
    time.sleep(2)

    start_time = datetime.now()
    sharedstate.timing_container["start"] = start_time

    process.wait()

    end_time = datetime.now()
    sharedstate.timing_container["end"] = end_time

    sharedstate.stop_event.set()
