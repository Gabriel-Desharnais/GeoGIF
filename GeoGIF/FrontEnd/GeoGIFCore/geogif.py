#! python3-env/bin/python3
# -*- coding: utf-8 -*-
# =====================================================================
# Copyright (c) 2019 Gabriel Desharnais for Government of Canada
# Under MIT License
# =====================================================================
import mapycli
import isodate
import PIL.Image
import io
import moviepy.editor as mpy
import numpy as np

# This file will declare the main classes to make it work.

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
    while current <= end:
        yield current
        current += delta


class picture:
    # This object is meant to store the maps downloaded from the layer object
    # It can store one picture file and can store the timeStamp (if needed)
    def __init__(self, picture, timeStamp):
        self.picture = picture
        self.timeStamp = timeStamp
        self.followed = None
    def IsBlank(self):
        # This function should check if the picture is blank
        if self.picture is None:
            return True
        else:
            return False

class layer:
    # a layer object as a time dimention, it is intended to store every
    # information needed for the download and post treatment of the
    # different layers
    def __init__(self, update = print):
        self.timeExtent = None
        self.source = ""
        self.name = ""
        self.extraParameters = {}
        self.bbox = "-90,-180,90,180"
        self.width = "320"
        self.height = "200"
        self.format = "image/png"
        self.picture = {}
        self.update = update

    def download(self):
        wmsSession = mapycli.wms.session()
        wmsSession.autoDecode = "utf-8"
        getCapFromSource = wmsSession.add(self.source)
        layer = getCapFromSource.getLayerByName(self.name)
        if self.timeExtent is None:
            # If timeExtent is None download one copy of it
            mapResponse = layer.getMap(bbox=self.bbox, width=self.width, height=self.height, format=self.format)
            if mapResponse.success:
                self.picture[None] = picture(PIL.Image.open(io.BytesIO(mapResponse.response.content)), None)
            else:
                self.picture[None] = picture(None, None)
        else:
            #evaluate the time steps to download and downlad them
            timesteps = timeStringToList(self.timeExtent)
            mapNumber = 0
            for time in timesteps:
                # Download a copy of it
                mapNumber += 1 # increase conter
                # Convert time to isodate
                isoTime = time.strftime("%Y-%m-%dT%H:%M:%SZ")

                mapResponse = layer.getMap(bbox=self.bbox, width=self.width, height=self.height, format=self.format, time=isoTime)
                if mapResponse.success:
                    self.picture[time] = picture(PIL.Image.open(io.BytesIO(mapResponse.response.content)), time)
                else:
                    self.picture[time] = picture(None, time)
            #mapResponse.saveImageAs("test.png")
    def FillBlanks(self, rescale = None):
        # check if blank picture  surounded by good ones
        if rescale is not None and None not in self.picture.keys():
            for timeStep in timeStringToList(rescale):
                if timeStep not in self.picture:
                    self.picture[timeStep] = picture(None, timeStep)

        good = False
        for picTime in sorted(list(self.picture.keys())) :
            pic = self.picture[picTime]
            if pic.IsBlank():
                if good:
                    pic.followed = True
                else:
                    pic.followed = False
            else:
                pic.followed = True
                good = True

        for picTime in reversed(sorted(list(self.picture.keys()))):
            pic = self.picture[picTime]
            if pic.IsBlank():
                if pic.followed:
                    pic.followed = False
            else:
                break
        # Add frame for followed frame
        # Create loop that can access actual frame and previous one at same time
        prevFrames = sorted(list(self.picture.keys()))
        actualFrames = iter(prevFrames) # Create a syncronous frame with prevFrame
        next(actualFrames) # Give an one frame advance
        for prevTime, actTime in zip(prevFrames, actualFrames):
            prev = self.picture[prevTime]
            act = self.picture[actTime]
            if act.IsBlank() and act.followed:
                act.picture = prev.picture
    def __add__(self, l2):
        # This function merges the layers
        if l2 == 0:
            # if l + 0 return l
            return self

        # Create the layer object to return
        l = layer()
        bg = False
        # create a timeStep list with no dublicate time steps
        if None not in self.picture and None not in l2.picture:
            # Both layers are time enabled
            timeSteps = set(self.picture.keys()) | set(l2.picture.keys())
        elif None in self.picture and None not in l2.picture:
            # l2 is time enabled but self is not
            timeSteps = set(l2.picture.keys())
            bg = self
        elif None not in self.picture and None in l2.picture:
            # self is time enabled but l2 is not
            timeSteps = set(self.picture.keys())
            bg = l2
        else:
            timeSteps = [None]

        for timeStep in timeSteps:
            # Check if there is a background
            if bg is not False:
                # There is a background
                if bg is self:
                    # if the fixed image is self
                    l.picture[timeStep] = picture(PIL.Image.alpha_composite(bg.picture[None].picture.convert("RGBA"), l2.picture[timeStep].picture.convert("RGBA")),timeStep)
                    continue
                # if the fixed image is l2
                l.picture[timeStep] = picture(PIL.Image.alpha_composite(bg.picture[timeStep].picture.convert("RGBA"), l2.picture[None].picture.convert("RGBA")),timeStep)
                continue
            # if there is no or both picture are fixed
            try:
                l.picture[timeStep] = picture(PIL.Image.alpha_composite(self.picture[timeStep].picture.convert("RGBA"), l2.picture[timeStep].picture.convert("RGBA")),timeStep)
            except KeyError:
                try:
                    l.picture[timeStep] = picture(l2.picture[timeStep].picture.convert("RGBA"), timeStep)
                except KeyError:
                    l.picture[timeStep] = picture(self.picture[timeStep].picture.convert("RGBA"), timeStep)

        return l

    def __radd__(self, l2):
        return self + l2

class animation:
    def __init__(self, fps = 1, bbox = "-90,-180,90,180", width = "320", height = "200", fillBlanks = True, update = print):
        update("Setting up annimation parameters")
        self.fps = fps
        self.timeExtent = None
        self.bbox = bbox
        self.width = width
        self.height = height
        self.layer = []
        self.fillBlanks = fillBlanks
        self.update = update

    def addLayer(self, source, name, timeExtent = None):
        # This function add a layer in annimation
        l = layer(update = self.update)
        l.timeExtent = timeExtent
        l.source = source
        l.name = name
        l.bbox = self.bbox
        l.width = self.width
        l.height = self.height
        self.layer.append(l)

    def download(self):
        # This function download every frame of every layer
        self.update("starting download of layers")
        for l in self.layer:
            l.download()

        # fill blanks if needed
        if self.fillBlanks:
            for l in self.layer:
                l.FillBlanks(rescale = self.timeExtent)

    def animate(self):
        self.update("Creation of clip in memory")
        l = sum(self.layer)
        self.clip = mpy.ImageSequenceClip([np.array(l.picture[p].picture) for p in sorted(l.picture.keys())], fps=self.fps)

    def exportGif(self):
        self.update("Generation and exporting of gif")
        self.clip.write_gif("test.gif", fps =1, opt="OptimizePlus", fuzz=10)

if __name__ == "__main__":
    a = animation(bbox = "-90,-180,90,180", width = "640", height = "400")
    a.timeExtent = "2019-04-06T12:00:00Z/2019-04-10T00:00:00Z/PT3H"
    a.addLayer("https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv", "GEBCO_LATEST")
    a.addLayer("http://geo.weather.gc.ca/geomet/", "GDPS.ETA_TT", "2019-04-06T12:00:00Z/2019-04-10T00:00:00Z/PT6H")
    a.addLayer("http://geo.weather.gc.ca/geomet/", "GDPS.ETA_NT", "2019-04-06T12:00:00Z/2019-04-10T00:00:00Z/PT3H")

    a.download()
    a.animate()
    a.exportGif()

    #l1 = layer()
    #l1.timeExtent = "2019-04-06T12:00:00Z/2019-04-07T00:00:00Z/PT3H"
    #l1.source = "http://geo.weather.gc.ca/geomet/"
    #l1.name = "GDPS.ETA_NT"
    #l1.bbox = "-90,-180,90,180"
    #l1.width = "320"
    #l1.height = "200"


    #l2 = layer()
    #l2.defineSource("https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv")
    #l2.defineName("GEBCO_LATEST")
    #l2.download()

    #l3 = l2 + l1
    #l3.picture[0].show()

    #clip = mpy.ImageSequenceClip([np.array(p.picture) for p in l3.picture], fps=1)
    #clip.write_gif("test.gif", fps =1, opt="OptimizePlus", fuzz=10)
    #a1 = animation(l3, "mp4")
