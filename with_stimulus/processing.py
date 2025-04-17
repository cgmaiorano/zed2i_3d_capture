import cv2
import pyzed.sl as sl
import numpy as np
from datetime import datetime

from core import zed_parameters
from with_stimulus import formatting
from viewers import tracking_viewer


def body_tracking(sharedstate):

    body_param, body_runtime_param = zed_parameters.initialize_tracking_parameters(sharedstate.zed)
    
    display_resolution, image_scale = zed_parameters.display_utilities(sharedstate.zed)

    # Create objects filled in the main loop
    bodies = sl.Bodies()
    image = sl.Mat()
    key_wait = 10
    key = ''

    # Create initial list of body part names with coordinates (1, 114)-- to be used as column headers in data_df
    parts = []
    for i, part in enumerate(sl.BODY_38_PARTS):
        if i < 38:
            x_part = 'x_' + str(part.name)
            y_part = 'y_' + str(part.name)
            z_part = 'z_' + str(part.name)
            parts.append(x_part)
            parts.append(y_part)
            parts.append(z_part)
    f = 0
    frames = [f]
    timestamps = [0]
    x_HEAD = [0]
    y_HEAD = [0]
    z_HEAD = [0]

    # Create empty array to store body part coordinates (to be merged into df later)
    data = np.array(np.zeros((1,114)))
    
    # Start body tracking
    print("Press 'q' to exit")

    sharedstate.wait_for_thread.wait()

    # while not sharedstate.stop_event.is_set():
    while True: # Infinite loop, will break manually or through stop event
        # Check if stop event is set or quit is triggered by keypress
        if sharedstate.stop_event.is_set():
            print("Stop event triggered, exiting loop...")
            break
        
        key = cv2.waitKey(1) & 0xFF  # Non-blocking key press check
        
        if key == ord('q'):  # If 'q' is pressed, break the loop
            print("Quitting...")
            sharedstate.quit = True
            sharedstate.stop_event.set()
            break

        # Grab a frame
        if sharedstate.zed.grab() == sl.ERROR_CODE.SUCCESS:

            # retrieve all bodies in frame 
            sharedstate.zed.retrieve_bodies(bodies, body_runtime_param)

            # count frames
            f += 1
            frames.append(f)

            # retrieve timestamps
            time_reference = datetime.now()
            timestamps.append(time_reference)

            # label first body and store head centroid coordinates for current frame
            first_body = bodies.body_list[0]
            x_HEAD.append(first_body.head_position[0])
            y_HEAD.append(first_body.head_position[1])
            z_HEAD.append(first_body.head_position[2])

            # Create empty list to temporarily store keypoint coordinates of first body in current frame
            row = [] 
            for i, part in enumerate(sl.BODY_38_PARTS):
                if i < 38:
                    # put coordinates of keypoints in row
                    kp = bodies.body_list[0].keypoint[i] # get 1x3 array of current body part in x, y, z. bodies.body_list[0].keypoint: 38x3 array of xyz coordinates of all body parts
                    row.append(kp[0])
                    row.append(kp[1])
                    row.append(kp[2])
                else:
                    # when all body part coordinates have been added to row, convert to array, reshape, and add to data array
                    row = np.array(row)
                    row = row.reshape((1,114))
                    data = np.append(data, row, axis = 0)
            
            # Display skeletons
            sharedstate.zed.retrieve_image(image, sl.VIEW.LEFT, sl.MEM.CPU, display_resolution)
            image_left_ocv = image.get_data()
            tracking_viewer.render_2D(image_left_ocv,image_scale, bodies.body_list, body_param.enable_tracking, body_param.body_format)
            cv2.imshow("ZED | 2D View", image_left_ocv)
            cv2.moveWindow("ZED | 2D View", 100, 100)

            
        # Zed connection failed
        elif sharedstate.zed.grab() != sl.ERROR_CODE.SUCCESS:
            print("Failed ZED connection")
            break
    
    # Close the viewer
    sharedstate.zed.disable_body_tracking()
    sharedstate.zed.disable_positional_tracking()
    sharedstate.zed.close()
    cv2.destroyAllWindows()
    
    if sharedstate.quit: # if user press 'q' to quit, break out
        return
    else: # format the data
        formatting.format_data(data, parts, x_HEAD, y_HEAD, z_HEAD, frames, timestamps, sharedstate)