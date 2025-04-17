import pandas as pd

def format_data(data, parts, x_HEAD, y_HEAD, z_HEAD, frames, timestamps, sharedstate):

    # Save keypoint coordinates and head centroid coordinates to a dataframe
    data_df = pd.DataFrame(data, columns = parts)
    
    head_df = pd.DataFrame()
    head_df['x_HEAD'] = pd.Series(x_HEAD)
    head_df['y_HEAD'] = pd.Series(y_HEAD)
    head_df['z_HEAD'] = pd.Series(z_HEAD)
    
    data_df = pd.concat((data_df, head_df), axis=1)

    mobi_motion_tracking_ordered_columns = ["x_Hip",	"y_Hip", "z_Hip", 
                                            "x_LowerSpine", "y_LowerSpine", "z_LowerSpine", 
                                            "x_MiddleSpine", "y_MiddleSpine", "z_MiddleSpine", 
                                            "x_Chest", "y_Chest", "z_Chest",	
                                            "x_Neck", "y_Neck", "z_Neck", 
                                            "x_Head", "y_Head", "z_Head",
                                            "x_RClavicle", "y_RClavicle", "z_RClavicle",
                                            "x_RShoulder", "y_RShoulder", "z_RShoulder",
                                            "x_RForearm", "y_RForearm", "z_RForearm", 
                                            "x_RHand", "y_RHand", "z_RHand",
                                            "x_LClavicle", "y_LClavicle", "z_LClavicle",
                                            "x_LShoulder", "y_LShoulder", "z_LShoulder",
                                            "x_LForearm", "y_LForearm", "z_LForearm", 
                                            "x_LHand", "y_LHand", "z_LHand",
                                            "x_RThigh",	"y_RThigh",	"z_RThigh",	
                                            "x_RShin",	"y_RShin",	"z_RShin",	
                                            "x_RFoot",	"y_RFoot",	"z_RFoot",	
                                            "x_LThigh",	"y_LThigh",	"z_LThigh",	
                                            "x_LShin",	"y_LShin",	"z_LShin",	
                                            "x_LFoot",	"y_LFoot",	"z_LFoot"
                                            ]

    zed_ordered_columns = ['x_PELVIS',	'y_PELVIS',	'z_PELVIS', 
                        'x_SPINE_1', 'y_SPINE_1', 'z_SPINE_1', 
                        'x_SPINE_2', 'y_SPINE_2', 'z_SPINE_2', 
                        'x_SPINE_3','y_SPINE_3','z_SPINE_3', 
                        'x_NECK', 'y_NECK', 'z_NECK', 
                        'x_HEAD', 'y_HEAD', 'z_HEAD', 
                        'x_RIGHT_CLAVICLE',	'y_RIGHT_CLAVICLE',	'z_RIGHT_CLAVICLE',	
                        'x_RIGHT_SHOULDER',	'y_RIGHT_SHOULDER',	'z_RIGHT_SHOULDER',	
                        'x_RIGHT_ELBOW', 'y_RIGHT_ELBOW', 'z_RIGHT_ELBOW', 
                        'x_RIGHT_WRIST',	'y_RIGHT_WRIST', 'z_RIGHT_WRIST',	
                        'x_LEFT_CLAVICLE', 'y_LEFT_CLAVICLE', 'z_LEFT_CLAVICLE', 
                        'x_LEFT_SHOULDER', 'y_LEFT_SHOULDER', 'z_LEFT_SHOULDER', 
                        'x_LEFT_ELBOW', 'y_LEFT_ELBOW', 'z_LEFT_ELBOW',
                        'x_LEFT_WRIST',	'y_LEFT_WRIST',	'z_LEFT_WRIST',	
                        'x_RIGHT_HIP', 'y_RIGHT_HIP', 'z_RIGHT_HIP', 
                        'x_RIGHT_KNEE', 'y_RIGHT_KNEE', 'z_RIGHT_KNEE', 
                        'x_RIGHT_HEEL', 'y_RIGHT_HEEL', 'z_RIGHT_HEEL',	
                        'x_LEFT_HIP', 'y_LEFT_HIP',	'z_LEFT_HIP', 
                        'x_LEFT_KNEE', 'y_LEFT_KNEE',	'z_LEFT_KNEE',	
                        'x_LEFT_HEEL',	'y_LEFT_HEEL',	'z_LEFT_HEEL'
                        ]
    
    # based on order of zed_ordered_columns, assign corresponding data from data_df to ordered_df
    for idx, column in enumerate(zed_ordered_columns):
        with sharedstate.df_lock:
            sharedstate.ordered_df[mobi_motion_tracking_ordered_columns[idx]] = data_df[column]

    # rename the headers of ordered_df to be mobi_motion_tracking_ordered_columns
    # Append corresponding frames and timestamps as first columns of ordered_df
    with sharedstate.df_lock:
        sharedstate.ordered_df["timestamps"] = timestamps
        sharedstate.ordered_df["frames"] = frames

        # Remove first row of zeros
        sharedstate.ordered_df = sharedstate.ordered_df.iloc[1:]


def trim_dataframe(sharedstate):
    with sharedstate.df_lock:
        # Filter rows where timestamps are between video start and end
        sharedstate.ordered_df = sharedstate.ordered_df[
            (sharedstate.ordered_df['timestamps'] >= sharedstate.timing_container['start']) & 
            (sharedstate.ordered_df['timestamps'] <= sharedstate.timing_container['end'])
            ]
        # Remove timestamps column for saving in mobi_motion_tracking acceptable format
        sharedstate.ordered_df.drop("timestamps", axis=1, inplace=True)