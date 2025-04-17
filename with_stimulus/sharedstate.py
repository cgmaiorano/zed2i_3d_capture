import pandas as pd
import threading
import pyzed.sl as sl

class SharedState:
    def __init__(self):
        self.zed = sl.Camera()
        self.ordered_df = pd.DataFrame(columns=["timestamps", "frames"])
        self.timing_container = {}
        self.df_lock = threading.Lock()
        self.wait_for_thread = threading.Barrier(2)
        self.stop_event = threading.Event()
        self.quit = False