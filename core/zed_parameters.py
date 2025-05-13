import pyzed.sl as sl

from settings import DEPTH_MODE, DETECTION_MODEL


def initialize_zed_parameters(zed):
    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.camera_fps = 30
    init_params.coordinate_units = sl.UNIT.METER  # Set coordinate units
    init_params.depth_mode = getattr(sl.DEPTH_MODE, DEPTH_MODE)
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open", err, "Exit program.")
        exit(1)


def initialize_tracking_parameters(zed):
    # Enable Positional tracking (mandatory for object detection)
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    positional_tracking_parameters.set_as_static = True  # camera is static
    zed.enable_positional_tracking(positional_tracking_parameters)

    # Set Body Tracking parameters
    body_param = sl.BodyTrackingParameters()
    body_param.enable_tracking = True  # Track people across images flow
    body_param.enable_body_fitting = True  # Smooth skeleton move
    body_param.detection_model = getattr(sl.BODY_TRACKING_MODEL, DETECTION_MODEL)
    body_param.body_format = (
        sl.BODY_FORMAT.BODY_38
    )  # Choose the BODY_FORMAT you wish to use
    zed.enable_body_tracking(body_param)

    # Set Body Tracking Runtime parameters
    body_runtime_param = sl.BodyTrackingRuntimeParameters()
    body_runtime_param.detection_confidence_threshold = 50

    return body_param, body_runtime_param


def display_utilities(zed):
    # Get ZED camera information
    camera_info = zed.get_camera_information()

    # 2D viewer utilities
    display_resolution = sl.Resolution(
        min(camera_info.camera_configuration.resolution.width, 1280),
        min(camera_info.camera_configuration.resolution.height, 720),
    )
    image_scale = [
        display_resolution.width / camera_info.camera_configuration.resolution.width,
        display_resolution.height / camera_info.camera_configuration.resolution.height,
    ]

    return display_resolution, image_scale
