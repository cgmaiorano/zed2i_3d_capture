import threading

from core import zed_parameters
from core import export

from with_stimulus import formatting
from with_stimulus import processing
from with_stimulus import play_stimulus

from with_stimulus.sharedstate import SharedState


def run(participant_ID, sequence, video):
    print(f"Beginning Sequence {sequence}")

    sharedstate = SharedState()

    # Create camera object, initialize camera parameters, start recording svo file
    zed_parameters.initialize_zed_parameters(sharedstate.zed)
    export.record_svo(participant_ID, sequence, sharedstate.zed)

    # Path to the VLC player executable
    vlc_path = r"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"

    # Threads
    body_tracking_thread = threading.Thread(
        target=processing.body_tracking, args=(sharedstate,)
    )
    video_thread = threading.Thread(
        target=play_stimulus.play_video, args=(vlc_path, str(video), sharedstate)
    )

    body_tracking_thread.start()
    video_thread.start()

    # Wait for the threads to finish
    video_thread.join()
    body_tracking_thread.join()

    if sharedstate.quit:
        print(
            f"Manual Quit... ZED Body tracking for Participant: {participant_ID} Sequence: {sequence} INCOMPLETED."
        )
        return

    # trim data
    formatting.trim_dataframe(sharedstate)

    # save data
    export.save_sequence(participant_ID, sequence, sharedstate.ordered_df)

    print(
        f"ZED Body tracking for Participant: {participant_ID} Sequence: {sequence} is complete"
    )
