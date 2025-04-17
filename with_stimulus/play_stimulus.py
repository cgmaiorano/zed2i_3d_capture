import time
import subprocess
import screeninfo
import os
import pygetwindow as gw
from datetime import datetime


def play_video(vlc_path, video_path, sharedstate):
    sharedstate.wait_for_thread.wait()

    process = subprocess.Popen([vlc_path, video_path, '--play-and-exit', '--fullscreen'])
    
    # Wait for the window to appear
    filename = os.path.basename(video_path)
    vlc_window = None
    for _ in range(10):  # Try for a limited number of times
        time.sleep(0.5)  # Wait half a second before checking again
        windows = gw.getWindowsWithTitle(filename)
        if windows:
            vlc_window = windows[0]
            break

    if vlc_window:
        # # Get the dimensions of the displays
        # monitors = screeninfo.get_monitors()
        # if len(monitors) > 1:  # Check if there is an extended display
        #     extended_monitor = monitors[1]  # Assuming the second monitor is the extended one
        #     # Move the window to the extended display
        #     vlc_window.move(extended_monitor.x, extended_monitor.y)

        vlc_window.activate()

        time.sleep(0.1)
        start_time = datetime.now()
        sharedstate.timing_container['start'] = start_time

    process.wait()

    end_time = datetime.now()
    sharedstate.timing_container['end'] = end_time

    sharedstate.stop_event.set()