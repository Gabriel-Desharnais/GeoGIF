# -*- coding: utf-8 -*-
# =================================================================
# Copyright (c) 2017 Government of Canada
# =================================================================

import ruamel.yaml

def parse(yamlFilePath):
    # This function will parse the yaml file. It will generate and 
    # return a parameter dictionary
    
    # Open and read the yaml file
    with open(yamlFilePath, 'r') as contentFile:
        rawContent = contentFile.read()

    # Parsing the yaml to a queryable data structure
    content = ruamel.yaml.round_trip_load(rawContent)
    
    # Create a dictionary that will be filled up
    paramsDict = {}
    
    # Insert the name of the yaml file
    paramsDict['yaml_name'] = yamlFilePath.split('/')[-1] # This should use the path standart library
    
    # These parameter are not optionals if they are not there parse 
    # must return false 
    try:
        # Add GIF specific options
        # Get the output name of the file
        paramsDict['file_name'] = content['gif_options']['name']
        # Get the list of the output format type
        paramsDict['list_of_format'] = content['gif_options']['format']
        # Get the frame rate of the animation
        paramsDict['frame_rate'] = content['gif_options']['frame_rate']
        # Add query specific options
        # Get the projection used for the layers
        paramsDict['projection'] = content['query_options']['projection']
        # Get the map resolution
        mapSize = content['query_options']['map_size']
        paramsDict['map_size'] = tuple(map(int, mapSize.split(' ')))
        # Get the bounding box
        BBox = content['query_options']['bbox']
        paramsDict['bbox'] = tuple(map(int, BBox.split(' ')))
        # Add layer specific options
        # Create layer dictionary
        paramsDict['time_layers'] = {}
        paramsDict['base_layers'] = {}
        
        
        # Go threw every layer
        for layerName in content['layers']:
            # Create default layer
            layer = {'style' : None,
                     'legend': False}
            # Add information to layer
            layer['name'] = content['layers'][layerName]['layer_name']
            layer['url'] = content['layers'][layerName]['server_url']
            # optional parameters
            try:
                layer['style'] = content['layers'][layerName]['style']
            except KeyError: pass
            try:
                layer['style'] = content['layers'][layerName]['legend']
            except KeyError: pass
            # Add layer to the right dictionary
            if content['layers'][layerName]['timeEnabled']:
                paramsDict['time_layers'][content['layers'][layerName]['order']] = layer
            else:
                paramsDict['base_layers'][content['layers'][layerName]['order']] = layer
        
    except KeyError:
        # Should add information about what went wrong
        return False
        
    # Default optional value
    # Add GIF specific options
    paramsDict['clean_begin_frames'] = False
    paramsDict['clean_end_frames'] = False
    paramsDict['persist_layers'] = False
    paramsDict['anchor'] = None
    # Add query specific options
    paramsDict['time_string'] = None
    
    # Replacing the default values
    # Add GIF specific options
    try:
        paramsDict['clean_begin_frames'] = content['gif_options']['clean_begin_frames']
    except KeyError: pass
    try:
        paramsDict['clean_end_frames'] = content['gif_options']['clean_end_frames']
    except KeyError: pass
    try:
        paramsDict['persist_layers'] = content['gif_options']['persist_layers']
    except KeyError: pass
    try:
        anchor = content['gif_options']['thumbnail']
        paramsDict['anchor'] = {'color':(230,230,230),
                                'has_time': True,
                                'has_layers': True,
                                'length':65,
                                'sources':[]}
        paramsDict['anchor']['color'] = tuple(map(int,anchor['color'].split(' ')))
        paramsDict['anchor']['has_time'] = anchor['has_time']
        paramsDict['anchor']['has_layers'] = anchor['has_layers']
        paramsDict['anchor']['length'] = int(anchor['length'])
        paramsDict['anchor']['sources'] = anchor['sources']
        
    except KeyError: pass
    # Add query specific options
    try:
        paramsDict['time_string'] = '/'.join([
          content['query_options']['time']['time_begin'].isoformat(),
          content['query_options']['time']['time_end'].isoformat(),
          content['query_options']['time']['time_step']])
    except (KeyError,TypeError): pass
    
    return paramsDict
