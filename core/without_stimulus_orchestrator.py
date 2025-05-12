import pyzed.sl as sl

from core import zed_parameters
from core import export

from without_stimulus import processing


def run(participant_ID, sequence):
    print(f"Beginning Sequence {sequence}")

    zed = sl.Camera()

    # Create camera object, initialize camera parameters, start recording svo file
    zed_parameters.initialize_zed_parameters(zed)
    export.record_svo(participant_ID, sequence, zed)

    # main processing
    ordered_df = processing.body_tracking(zed)

    if ordered_df is None:
        print(
            f"Manual Quit... ZED Body tracking for Participant: {participant_ID} Sequence: {sequence} INCOMPLETED."
        )
        return

    # save data
    export.save_sequence(participant_ID, sequence, ordered_df)

    print(
        f"ZED Body tracking for Participant: {participant_ID} Sequence: {sequence} is complete"
    )
