# `zed2i_3d_capture`

A repository containing the necessary code to record motion tracking data from the ZED 2i with or without a sitmulus.

![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)
[![LGPL--2.1 License](https://img.shields.io/badge/license-LGPL--2.1-blue.svg)](https://github.com/childmindresearch/mobi-motion-tracking/blob/main/LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://github.com/childmindresearch/zed2i_3d_capture)

Welcome to `zed2i_3d_capture`, a Python Repository designed for recording 3D motion tracking data from the ZED 2i stereo camera developed by StereoLabs (https://github.com/stereolabs/). This repository performs real time body tracking on a single person, collects the data, and saves it to an .xlsx file in the acceptable format for `mobi_motion_tracking`. This repository can be run with or without a live stimulus. 

## Supported software & devices

The package currently supports the ZED 2i and is reliant on proper installation of the `zed-sdk` (https://github.com/stereolabs/zed-sdk) and the `zed-python-api` (https://github.com/stereolabs/zed-python-api).

**Special Note**
    The ZED SDK is only supported on Windows devices. Please see https://www.stereolabs.com/docs#supported-platforms for full details on ZED supported platforms.
    

## Processing pipeline implementation

The main processing pipeline of the `zed2i_3d_capture` module can be described as follows:

- **Determine sitmulus presence**: The user provides the participant ID and sequence number in the command line. A path to a stimulus video may also be provided. If a video path is provided the cli will call with_stimulus_orchestrator.py, otherwise without_stimulus_orchestrator.py will be called.
- **Initiate the camera**: The zed camera will be triggerred to open first in both orchestrators. If the camera cannot be accessed, an error will be thrown. 
- **Begin body tracking**: Skeletal joints will begin being captured at 30 fps. Both pathways can be manually interrupted by pressing the 'q' key to quit without saving.
    - **Present stimulus**: If a video path is provided, the stimulus will be displayed.
- **Body tracking ends**: If a stimulus is being displayed, body tracking will automatically complete at the end of the stimulus video. If there is no stimulus, body tracking can be concluded by pressing the 'd' key.
    - **Trim data**: If a stimulus was played, the body tracking data will automatically by trimmed from both the start and end to be time-synced with the stimulus. If there was no sitmulus, the full data collection session will be returned.
- **Export data**: The live recording of the participant will be saved as a .svo2 file located in collected_data/svo. Joint data will be saved in an .xlsx file located in collected_data/xlsx.


## Installation

1. Install the ZED SDK from StereoLabs. Installation documentation can be found here: https://www.stereolabs.com/docs/installation/windows 
    - *** When prompted to select the folder location for the ZED SDK, you can use the default path ("C:\Program Files (x86)\ZED SDK") or change it based on your preference. However, this readme is based on the default path.

2. Grant administrative permissions to the ZED SDK. 
    - Navigate to the ZED SDK folder in "C:\Program Files (x86)" in file explorer
    - Right click on the folder -> select properties -> go to security tab -> click edit
    - Select the correct user to grant access to and tick the box next to full control under "Allow" 
    - Click apply and Ok
    - Restart your terminal

3. Create a virtual environment. Any environment management tool can be used, but the following steps describe setting up a uv venv:

create a virtual environment named zed2i_lsl_venv
```sh
uv venv zed2i_venv
```
 activate the environment
```sh
zed2i_venv\Source\activate
```

4. Install the ZED Python API. Installation support documentation can be found here on the Stereolabs website (https://www.stereolabs.com/docs/app-development/python/install). However, follow our steps below for proper CMI/MoBI-specific API installation:

ensure pip is installed 
```sh
python -m ensurepip
```
install API dependencies
```sh
uv pip install cython numpy opencv-python requests
```
run get_python_api.py
```sh
cd "C:\Program Files (x86)\ZED SDK"
```
```sh
uv run get_python_api.py
```


5. Install repository-dependent packages

```sh
uv pip install pandas
```


## Quick start

Navigate to the ZED SDK directory:

```sh
cd "C:\Program Files (x86)\ZED SDK"
```

Clone this repository inside ZED SDK:

```sh
git clone https://github.com/childmindresearch/zed2i_3d_capture.git
```

Navigate to root:

```sh
cd zed2i_3d_capture
```

Run the setup_settings.py file and follow prompts in terminal:
```sh
python -m setup_settings.py
```

#### Run participant 100 for sequence 1 WITHOUT STIMULUS:

```sh
python -m main -p "100" -s "1"
```

#### Run participant 100 for sequence 1 WITH STIMULUS:

```sh
python -m main -p "100" -s "1" --video "C:\path\to\stimulus\video.avi"
```


## Post-Processing

After data collection, saved data can be compared to a "gold standard" through `mobi_motion_tracking` https://github.com/childmindresearch/mobi-motion-tracking. 
