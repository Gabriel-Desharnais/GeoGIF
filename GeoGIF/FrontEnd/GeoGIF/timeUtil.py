# -*- coding: utf-8 -*-
# =================================================================
# Copyright (c) 2017 Government of Canada
# =================================================================
import isodate

def timeStringToList(tStr):
    # This function will parse the time string and return a list of
    # the time steps 
    begin, end, step = tStr.split('/')
    # Convert str to datetime object with the help of isodate
    begin = isodate.parse_datetime(begin).replace(tzinfo=None)
    end = isodate.parse_datetime(end).replace(tzinfo=None)
    step = isodate.parse_duration(step)
    # create a generator and iterate threw it and generate a list with
    # the help of the "list" function
    return list(DateTimeIntervalConstructor(begin,end,step))
    
def DateTimeIntervalConstructor(begin,end,delta):
    # This constructutor will iterate threw every dateTime position
    # between the begining and the end of the interval (excluding the
    # end) with a step of delta
    current = begin
    while current < end:
        yield current
        current += delta

def configurationToTimeList(configurations):
    # This function will generate timeList entry from time_string
    # entry in layer configuration dictionary
    for nu, layer in configurations['time_layers'].items():
        # Try to get time string for the layer
        try:
            tStr = layer['time_string']
            # Generate the list
            tLs = timeStringToList(tStr)
            # Add to configuration dictionary
            layer['timeList'] = tLs
        except KeyError:
            pass
