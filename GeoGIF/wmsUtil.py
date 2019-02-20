# -*- coding: utf-8 -*-
# =================================================================
# Copyright (c) 2017 Government of Canada
# =================================================================

from owslib.wms import WebMapService

def connectSourcesToWMS(configurations):
    # This function will create a wms connection for each layer
    
    # First mount a list (in fact a set) of all the sources
    sources = set()
    for nu, layer in configurations['base_layers'].items():
        sources.add(layer['url'])
    for nu, layer in configurations['time_layers'].items():
        sources.add(layer['url'])
    # Then for each of them create a wms connection
    wmsCon = {}
    for url in sources:
        wmsCon[url] = WebMapService(url, timeout=300, version="1.3.0")
    # Add the connection in the configuration dictionnary
    for nu, layer in configurations['base_layers'].items():
        layer['wms'] = wmsCon[layer['url']]
    for nu, layer in configurations['time_layers'].items():
        layer['wms'] = wmsCon[layer['url']]
        
def addTimeToLayerIfNoTime(configurations):
    # This function will look if a layer as no time extent specified if
    # there isn't it will lookup the time extent of the layer from the
    # wms connection
    
    if configurations['time_string'] is None:
        # Look if there is a time extent string in configurations
        
        for nu, layer in configurations['time_layers'].items():
            # Add time to time string
            try:
                layer['time_string'] = layer['wms'].contents[layer['name']].timepositions[0]
            except:
                raise Exception('time layer is not time enabled')

def configurationToTimeList(configurations):
    pass


