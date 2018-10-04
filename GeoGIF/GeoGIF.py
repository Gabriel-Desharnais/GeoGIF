#! python3-env/bin/python3
# -*- coding: utf-8 -*-
# =====================================================================
# Copyright (c) 2017 Government of Canada
# =====================================================================

# This is the main file of GeoGIF this is the part of the code that
# glues every module together in order to generate the animation 
# and publish it in the different formats.
import yamlInterpreter
import sys
from os import path
from wmsUtil import connectSourcesToWMS
from wmsUtil import addTimeToLayerIfNoTime
from timeUtil import configurationToTimeList
from timeUtil import timeStringToList
from frameUtil import staticFrame
from frameUtil import frames
from videoEditor import generate_animation,\
			 generate_gif,\
			 generate_video

def parseAndGo(yaml, output_path):
    # This function will parse the yaml file and lauch the creation of
    # the animation
    
    
    # To support multiple yaml just put that in a loop
    # Generate the configuration data structure from the yaml file
    configuration = yamlInterpreter.parse(yaml)
    generateAnimation(configuration,output_path)

def generateAnimation(configurations, output_path,getCap=None):
    # start new wms requests and add them to configuration of layers
    # Should not start new connection if layers share the same source
    if getCap is not None:
        pass
    else:
        connectSourcesToWMS(configurations)
    # Generate time string for evry layers
    addTimeToLayerIfNoTime(configurations)
    # Generate time list for evry layer
    configurationToTimeList(configurations)
    # Generate global time list if time_string exist
    if configurations['time_string'] is not None:
        configurations['timeList'] = timeStringToList(configurations['time_string'])
    else:
        # create a set
        timeSet = set()
        # Iterate threw every time layer and try to add timeList to set
        for nu, layer in configurations['time_layers'].items():
            timeSet |= set(layer['timeList'])
        # Add to configuration dictionnary
        configurations['timeList'] = sorted(list(timeSet))
        
    ## (To add) Generate anchor
    # General parameters definition
    generalParams={"srs" : configurations['projection'],
                   "format" : 'image/png',
                   "bbox" : configurations['bbox'],
                   "size" : list(map(float, configurations['map_size'])),
                   "transparent" : False}
    ## Prepare the requests to send
    # Base layer
    sf = staticFrame(generalParams)
    for no, layer in configurations['base_layers'].items():
        sf.addLayer(no,{"layers":[layer['name'],],
                        "style":layer['style'],
                        "wms":layer['wms']})

    frame=frames(generalParams,sf,configurations['time_layers'],configurations['timeList'])
    # Time layer

    ## Send requests
    sf.download()
    frame.download()
    
    ## Generate clip of animation
    # Merging every layer for each frame
    frame.merge()
    # Create the animation
    clip = generate_animation(frame.result, fps = configurations['frame_rate'])
    ## Export animation
    # Export path
    the_output_path = path.join(output_path, configurations['file_name'])
    
    if 'gif' in configurations['list_of_format']:
        generate_gif(clip, path = the_output_path+'.gif', fps = configurations['frame_rate'])
    if 'mp4' in configurations['list_of_format']:
        generate_video(clip, path = the_output_path+'.mp4', fps = configurations['frame_rate'])
    if 'ogv' in configurations['list_of_format']:
        generate_video(clip, path = the_output_path+'.ogv', fps = configurations['frame_rate'])
    return None




if __name__ == '__main__':
    # This script needs two input from the command line arguments
    if len(sys.argv) != 3:
        # If there is the wrong number of arguments the script displays
        # an error and is terminated with an error
        print('Usage: %s <geogif_yaml|geogif_yaml_folder>  <output_folder>' % sys.argv[0])
        sys.exit(1)
    # If there is the good number of argument the script launch the
    # function that will do all the work
    parseAndGo(sys.argv[1], sys.argv[2])
