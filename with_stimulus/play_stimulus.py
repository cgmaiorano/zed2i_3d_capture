import time
import subprocess
import os

import pygetwindow as gw
from datetime import datetime
from screeninfo import get_monitors


def move_vlc_to_second_monitor(vlc_window):
    monitors = get_monitors()
    if len(monitors) > 1:
        second = monitors[1]
        vlc_window.moveTo(second.x, second.y)
        vlc_window.resizeTo(second.width, second.height)
        vlc_window.activate()
    else:
        vlc_window.maximize()
        vlc_window.activate()


def play_video(vlc_path, video_path, sharedstate):
    sharedstate.wait_for_thread.wait()

    process = subprocess.Popen([
        vlc_path,
        video_path,
        "--play-and-exit",
        "--no-video-title-show",
    ])

    # Wait for VLC window to appear
    filename = os.path.basename(video_path)
    vlc_window = None
    timeout = 10  # seconds
    poll_interval = 0.5
    start_time_check = time.time()

    while time.time() - start_time_check < timeout:
        windows = gw.getWindowsWithTitle(filename)
        if windows:
            vlc_window = windows[0]
            break
        time.sleep(poll_interval)

    if not vlc_window:
        process.terminate()
        raise RuntimeError(
            f"VLC window with title '{filename}' failed to open within {timeout} seconds."
        )

    move_vlc_to_second_monitor(vlc_window)

    start_time = datetime.now()
    sharedstate.timing_container["start"] = start_time

    process.wait()

    end_time = datetime.now()
    sharedstate.timing_container["end"] = end_time

    sharedstate.stop_event.set()
