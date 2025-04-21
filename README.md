# `zed2i_3d_capture`

A repository containing the necessary code to record motion tracking data from the ZED 2i with or without a sitmulus.

![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)
[![LGPL--2.1 License](https://img.shields.io/badge/license-LGPL--2.1-blue.svg)](https://github.com/childmindresearch/mobi-motion-tracking/blob/main/LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://github.com/cgmaiorano/zed2i_3d_capture)

Welcome to `zed2i_3d_capture`, a Python Repository designed for recording 3D motion tracking data from the ZED 2i stereo camera developed by StereoLabs (https://github.com/stereolabs/). This repository performs real time body tracking on a single person, collects the data, and saves it to an .xlsx file in the acceptable format for `mobi_motion_tracking`. This repository can be run with or without a live stimulus. 

## Supported software & devices

The package currently supports the ZED 2i and is reliant on proper installation of the `zed-sdk` (https://github.com/stereolabs/zed-sdk) and the `zed-python-api` (https://github.com/stereolabs/zed-python-api).

**Special Note**
    The ZED SDK is only supported on Windows devices. Please see https://www.stereolabs.com/docs#supported-platforms for full details on ZED supported platforms.
    

## Processing pipeline implementation

The main processing pipeline of the `zed2i_3d_capture` module can be described as follows:

- **Determine sitmulus presence**: The user provides the participant ID and sequence number in the command line. A path to a stimulus video may also be provided. If a video path is provided the cli will call with_stimulus_orchestrator.py, otherwise without_stimulus_orchestrator.py will be called.
- **Initiate the camera**: The zed camera will be triggerred to open first in both orchestrtaors. If the camera cannot be accessed, an error will be thrown. 
- **Begin body tracking**: Skeletal joints will begin being captured at 30 fps. Both pathways can be manually interrupted by pressing the 'q' key.
    - **Present stimulus**: If a video path is provided, the stimulus will be displayed.
- **Body tracking ends**: If a stimulus is being displayed, body tracking will automatically complete at the end of the stimulus video. If there is no stimulus, body tracking can be concluded by pressing the 'd' key.
    - **Trim data**: If a stimulus was played, the body tracking data will automatically by trimmed from both the start and end to be time-synced with the stimulus. If there was no sitmulus, the full data collection session will be returned.
- **Export data**: The live recording of the participant will be saved as a .svo2 file located in collected_data/svo. Joint data will be saved in an .xlsx file located in collected_data/xlsx.

## Installation

Install this package via :

To use this package, you must have the ZED SDK and ZED Python API installed correctly. Follow our installation directions here: 
https://docs.google.com/document/d/13imtvds5D-c08G4WPb0nZ8Oea45oRec8gE41mZBs8WE/edit?usp=sharing

After following the directions above and creating and activating your python environment install the rest of the dependencies:

```sh
pip install pandas pygetwindow
```

## Quick start

### Using zed2i_3d_capture through powershell:

Navigate to the ZED SDK directory:

```sh
cd "C:\Program Files (x86)\ZED SDK"
```

Clone this repository inside ZED SDK:

```sh
git clone https://github.com/cgmaiorano/zed2i_3d_capture.git
```

Navigate to root:

```sh
cd zed2i_3d_capture
```

**Special Note**
    
    Prior to running the commands below: 
        - create directories to store collected data: `collected_data\xlsx` and `collected_data\svo`
        - navigate to `core\with_stimulus_orchestrator.py` and replace `vlc_path` with the correct path to your vlc player executable.


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