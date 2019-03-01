# -*- coding: utf-8 -*-
# =================================================================
# Copyright (c) 2017 Government of Canada
# =================================================================
import tempfile
from PIL import Image, ImageFile


class staticFrame:
    # This class manages layers that aren't time enabled
    def __init__(self, generalParam):
        # kargs contain parameter sent to getmap request
        self.kargs = generalParam
        # layer contain layer info while waiting download
        self.layer = {}
        # result contain the download temp file for each layer
        self.result = {}
        
    def addLayer(self,no,param):
        # This function add a layer to the object
        self.layer[no] = dict(param, **self.kargs)
        
    def plan(self):
        # This function return the number of file to download
        return len(self.layer)
        
    def download(self):
        # This function will download every layer and save them in a
        # temp file and add the file in the result dictionnary
        for no, kargs in self.layer.items():
            # Create temporary file
            tf = tempfile.TemporaryFile()
            # Start download
            tf.write(kargs['wms'].getmap(**kargs).read())
            tf.seek(0)
            self.result[no] = tf
            

class frame:
    # This class manages the layers that are time enabled
    def __init__(self, generalParam):
        # kargs contain parameter sent to getmap request
        self.kargs = generalParam
        # layer contain layer info while waiting download
        self.layer = {}
        # result contain the download temp file for each layer
        self.result = {}
        
    def plan(self):
        # This function return the number of file to download
        return len(self.layer)
        
    def addLayer(self,no,param):
        # This function add a layer to the object
        self.layer[no] = dict(param, **self.kargs)
        
    def addStatic(self,statF):
        # This function add downloaded staticlayer from statF in the
        # result dict of this frame
        self.result.update(statF.result)
        
    def download(self):
        # This function will download every layer and save them in a
        # temp file and add the file in the result dictionnary
        for no, kargs in self.layer.items():
            # Create temporary file
            tf = tempfile.TemporaryFile()
            # Start download
            tf.write(kargs['wms'].getmap(**kargs).read())
            tf.seek(0)
            self.result[no] = tf
            
    def merge(self):
        # This function will merge every layer together
        
        # Create a batch list
        batch = sorted(self.result.keys())
        # Converte bytes to image object
        images = []
        for i in batch:
            # Create parser
            p = ImageFile.Parser()
            # Feed data to parser
            self.result[i].seek(0)
            p.feed(self.result[i].read())
            # Transform data in a image object
            images.append(p.close())
        # Merge each layer together
        bottomImage = images[0].convert("RGBA")
        
        for i in range(1,len(images)):
            # merge
            bottomImage = Image.alpha_composite(bottomImage, images[i].convert("RGBA"))
        return bottomImage
        
        
class frames:
    def __init__(self,generalParam,static,layers,timelist):
        # This list is containing a frame object for every time step
        self.framelist = []
        # This list will contain the resulting image for each time step
        self.result = []
        # This contain the staticframe object to be added to each frame
        self.static = static

        for time in timelist:
            # Create a new frame for each time step
            tf = frame(generalParam)
            for no, layer in layers.items():
                tf.addLayer(no,{"layers":[layer['name'],],
                                "style":layer['style'],
                                "wms":layer['wms'],
                                "time":time.isoformat()+'Z'})
            # Add static frame to the time frame
            tf.addStatic(static)
            # Add the resulting time frame to the framelist
            self.framelist.append(tf)
            
    def plan(self):
        # Return the number of download to do for the time enable layers
        number = 0
        for fr in self.framelist:
            # For every time step lookup how many download to do
            number += fr.plan()
        return number
        
    def download(self):
        # This function will download every layer and save them in a
        # temp file and add the file in the result dictionnary
        
        # Download statics layers
        self.static.download()
        # Download every time enabled layers
        for tf in self.framelist:
            # Download the layers for a time step
            tf.download()
            # Add static layers to the time frame
            tf.addStatic(self.static)
            
    def merge(self):
        # This function will merge every layer together for each time
        # step
        for fr in self.framelist:
            self.result.append(fr.merge())
        
