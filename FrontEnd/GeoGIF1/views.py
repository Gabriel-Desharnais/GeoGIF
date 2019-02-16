from django.shortcuts import render,redirect

# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

import os
import sys
sys.path.insert(0,"../GeoGIF/")
import GeoGIF
import tempfile
from django.contrib.auth import logout
import json
from django.core.serializers.json import DjangoJSONEncoder
from base64 import b64encode,b64decode
import django.db.utils
from .models import Source
from .models import GetCapapilities
from .models import errorLog
from django.utils import timezone

import oauth2 as oauth
import json
from urllib.parse import urlencode,parse_qsl
from TwitterAPI import TwitterAPI
from asgiref.sync import async_to_sync
import channels.layers

# Twitter API access informations
CONSUMER_KEY = "IkxwKv3IJGoOTt8vHku7gIjDJ"
CONSUMER_SECRET = "NZ72x4TDdEvONL4Vx4Vi8DhGT6Y1i451uOMic66FF3AkcdWWiq"
ACCESS_KEY = "921089567880630273-tnSLZah4NJtANk7oVAD4EVJDupXnKqr"
ACCESS_SECRET = "Uk8xRE54ndNMzxJor2hSXMK3vBCGUAp99Lb5ZdADSqUk9"

# Generate token for twitter whit oauth2
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)


# Version number
version = "Alpha 0.1"

def SendTweet(request):
    # This is used to display html form to send a tweet
    template = loader.get_template('GeoGIF1/tweet.html')
    context = {
            'version': version,
        }
    return HttpResponse(template.render(context, request))

def tweetATweet(request):
    # This function will send a tweet with a GIF stored in the session
    # and the message send as get request "status" you must be loged
    # in for it to work
    
    # We should remove the part were it save the file first
    image = b64decode(request.session["GIF"].encode("ascii"))
    
    
    
    image_size = len(image)
    print(image_size)
    param = {"command":"INIT","total_bytes":image_size,"media_type":"image/gif","media_category":"tweet_gif"}
    #param = {"media_data":request.session["GIF"]}
    client = oauth.Client(consumer, oauth.Token(key=request.session["oauth_token"], secret=request.session["oauth_token_secret"]))#access_token
    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, request.session["oauth_token"], request.session["oauth_token_secret"])
    timeline_endpoint = "https://upload.twitter.com/1.1/media/upload.json"

    body =urlencode(param)

    response, data = client.request(timeline_endpoint,"POST",body=body)
    # get media id
    media_id = eval(data)["media_id"]
    
    print(data)
    
    
    print("append")
    # append
    segment_id = 0
    bytes_sent = 0
    while bytes_sent < image_size:
        try:
            chunk = image[bytes_sent:bytes_sent + 1000*1024]
        except IndexError:
            chunk = image
        
        param = {"command":"APPEND","media_id":media_id,"segment_index":segment_id}
        body =urlencode(param)
        media = {"media":chunk}
        #response, data = client.request(timeline_endpoint,"POST",body=body,files=media)
        #req = requests.post(url=timeline_endpoint,data = param,files=media)
        r = api.request('media/upload', param,media)
        print(r.status_code)
        #print(req.text)
        segment_id+=1
        bytes_sent = len(chunk)
    
    
    # FINALIZE
    param = {"command":"FINALIZE","media_id":media_id}
    body =urlencode(param)
    response, data = client.request(timeline_endpoint,"POST",body=body)
    print(data)
    
    # Send tweet
    param = {"status":request.GET.get("status"),"media_ids":media_id}
    r = api.request('statuses/update', param)
    print(r.status_code)
    template = loader.get_template('GeoGIF1/success.html')
    context = {
            'version': version,
        }
    return HttpResponse(template.render(context, request))
    
def backFromTwitter(request):
    # This function should be called by the callback in twitter login
    # procedure. it's supposed to complete the authentification
    
    oauth_verifier = request.GET.get("oauth_verifier","")
    oauth_token = request.GET.get("oauth_token","")
    param = {"oauth_verifier":oauth_verifier}
    client = oauth.Client(consumer, oauth.Token(key=oauth_token, secret=request.session["oauth_token_secret"]))#access_token

    timeline_endpoint = "https://api.twitter.com/oauth/access_token"

    body =urlencode(param)

    response, data = client.request(timeline_endpoint,"POST",body=body)
    
    
    da = dict(parse_qsl(data))
    request.session["oauth_token_secret"] = da[b'oauth_token_secret'].decode()
    request.session["oauth_token"] = da[b'oauth_token'].decode()
    
    template = loader.get_template('GeoGIF1/success.html')
    context = {
            'version': version,
        }
    return HttpResponse(template.render(context, request))
    
def twitterSignIn(request):
    # This is the first part in twitter signin process
    
    client = oauth.Client(consumer, access_token)

    timeline_endpoint = "https://api.twitter.com/oauth/request_token"

    body =urlencode({"oauth_callback":"/"+request.GET.get("callback","")}) #This might not work

    response, data = client.request(timeline_endpoint,"POST",body=body)
    da = dict(parse_qsl(data))
    request.session["oauth_token_secret"] = da[b'oauth_token_secret'].decode()
    request.session["oauth_token"] = da[b'oauth_token'].decode()
    
    url = "https://api.twitter.com/oauth/authenticate?"
    param = {'oauth_token':request.session["oauth_token"]}
    url+=urlencode(param)
    return redirect(url)
def home(request):
    # This will show the home page of GeoGIF project
    
    template = loader.get_template('GeoGIF1/HOME.html')
    context = {
            'version':version
        }
    return HttpResponse(template.render(context, request))

def log(request):
    # This will show the last 24 hours logs from the database
    template = loader.get_template('GeoGIF1/log.html')
    context = {
              'version':version,
              'log': errorLog.objects.all()
             }
    return HttpResponse(template.render(context, request))

def SourceDB(request):
    # This will show every information stored in source and layer
    # Database
    
    template = loader.get_template('GeoGIF1/sourceDB.html')
    context = {
            'version': version,
            'sources': Source.objects.all(),
            'layers': GetCapapilities.objects.all()
        }
    return HttpResponse(template.render(context, request))
    
def updateASource(request):
    # This is supposed to update the information about a source in the
    # DB. Write now it just delete the information and regenerate it 
    # (not great but actually works)
    
    sourceToUpdate = request.GET.get("source","")
    if sourceToUpdate == "":
        return HttpResponseNotFound('')
    else:
        from owslib.wms import WebMapService
        # Delete old files
        GetCapapilities.objects.filter(source=sourceToUpdate).delete()
        t=Source.objects.get(source=sourceToUpdate)
        t.lastUpdate = timezone.now()
        t.save()
        wms = WebMapService(sourceToUpdate, timeout=300)
        wmsl = list(wms.contents)
        for la in wmsl:
            try:
                if wms.contents[la].timepositions is not None:
                    timeE = True
                    timeEx = wms.contents[la].timepositions[0]
                else:
                    timeE = False
                    timeEx = ""
            except:
                timeE = False
            s = GetCapapilities(source = sourceToUpdate, prodName = la, timeEnabled = timeE, timeExtent=timeEx, lastUpdate = timezone.now())
            s.save()
        return HttpResponse("done")
def AddSource(request):
    # This add a source to the source DB
    
    sourceToAdd = request.GET.get("source","")
    nameToAdd = request.GET.get("name","")
    
    if (sourceToAdd == "") or (nameToAdd == ""):
        return HttpResponseNotFound('')
    else:
        s = Source(source = sourceToAdd, name = nameToAdd, lastUpdate = timezone.now())
        s.save()
        return HttpResponse("done")
def updateALayer(request):
    # This update the information about a layer in the DB
    
    sourceToUpdate = request.GET.get("source","")
    layerToUpdate = request.GET.get("name","")
    if (sourceToUpdate == "") or (layerToUpdate == ""):
        return HttpResponseNotFound('')
    else:
        from owslib.wms import WebMapService
        # Delete old files
        GetCapapilities.objects.filter(source=sourceToUpdate,prodName=layerToUpdate).delete()
        wms = WebMapService(sourceToUpdate, timeout=300)
        wmsl = list(wms.contents)
        try:
            if wms.contents[layerToUpdate].timepositions is not None:
                timeE = True
                timeEx = wms.contents[layerToUpdate].timepositions[0]
            else:
                timeE = False
                timeEx = ""
        except:
            timeE = False
        s = GetCapapilities(source = sourceToUpdate, prodName = layerToUpdate, timeEnabled = timeE, timeExtent=timeEx, lastUpdate = timezone.now())
        s.save()
        return HttpResponse("done")
def foo(request):
    # This should not exist please delete it sometime soon 
    
    #Source.objects.all().delete()
    #s = Source(name = "gebco",source = "http://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv")
    #s.save()
    text = ""
    for sou in GetCapapilities.objects.all():
        text += sou.source +"\t"+ sou.prodName+"\t" +str(sou.timeEnabled) +"\r\n"
    return HttpResponse(text)
def updateCap(request):
    # This update the DB not sure why. it should be deleted (or not)
    
    GetCapapilities.objects.all().delete()
    from owslib.wms import WebMapService
    url = request.GET.get("source","http://geo.weather.gc.ca/geomet-beta")
    wms = WebMapService(url, timeout=300)
    wmsl = list(wms.contents)
    for la in wmsl:
        try:
            if wms.contents[la].timepositions is not None:
                timeE = True
                timeEx = wms.contents[la].timepositions[0]
            else:
                timeE = False
                timeEx = ""
        except:
            timeE = False
        s = GetCapapilities(source = url, prodName = la, timeEnabled = timeE, timeExtent=timeEx)
        s.save()
    text = ""
    for sou in GetCapapilities.objects.all():
        text += sou.source +"\t"+ sou.prodName+"\t" +str(sou.timeEnabled) +"\t" + sou.timeExtent +"\r\n"
    return HttpResponse(text)
    
def getCap(request):
    # This list all layer from a source
    
    evr = GetCapapilities.objects.filter(source=request.GET.get("source",""))
    template = loader.get_template('GeoGIF1/getCap.html')
    context = {
        'gc': evr,
    }
    if list(evr) == []:
        return HttpResponseNotFound('')
    else:
        return HttpResponse(template.render(context, request))
        
def isItTimeEnabled(request):
    # This return the information if a layer is timeEnabled
    
    evr = GetCapapilities.objects.get(source=request.GET.get("source",""),prodName=request.GET.get("prodName",""))
    template = loader.get_template('GeoGIF1/isItTimeEnabled.html')
    context = {
        'gc': evr,
    }
    print(evr)
    if evr == []:
        return HttpResponseNotFound('')
    else:
        return HttpResponse(template.render(context, request))
        
def getTimeExtent(request):
    # This return the time extent of a layer return "" if layer as no time extent
    
    evr = GetCapapilities.objects.get(source=request.GET.get("source",""),prodName=request.GET.get("prodName",""))
    context = {
        'gc': evr,
    }
    print(evr)
    if evr == []:
        return HttpResponseNotFound('')
    else:
        return HttpResponse(evr.timeExtent)
        
def requestStatus(request):
    # This trys to return the current status of a request. It is poorly
    # made and should be made properly but yeah it kinda work (or not)
    #this should be deleted
    
    try:
        try:
            return HttpResponse(request.session["status"])
        except django.db.utils.OperationalError:
            return HttpResponse("")
    except KeyError:
        return HttpResponse("No job is running")
def END(request):
    # This delete the informations stored in a session not sure if we
    # really want that but yeah it works
    
    request.session.flush()
    return HttpResponse("")
    
def THE(request):
    # This return the GIF image (name is pure crap and should 
    # absolutely be changed)
    
    #print("voila")
    #return HttpResponse("vvd")
    #Get format
    typ = request.session["user_format"]
    if typ == "gif":
        typ = "image/gif"
    elif typ == "mp4":
        typ = "video/mp4"
    elif typ == "ogv":
        typ = "video/ogg"
        
    try:
        return HttpResponse(b64decode(request.session["result"].encode("ascii")),content_type=typ)
    except KeyError:
        return HttpResponseNotFound('<h1>Page not found</h1>')
                
def gif(request):
    # This will generate the GIF and video files if works and calls the 
    # backend proberly
    # Create update function
    update = lambda message : updateStatus(request, message)
    # Send status to client
    update('Configuring parameters')
    cwd = os.getcwd()   #Useless to delete sometimes
    # Create a tempdir to store intermediate pictures and stuff
    tempdir = tempfile.TemporaryDirectory()
    # Create a params dictionnary to transfert to "execute"
    params = {}
    params['list_of_format']=[request.POST.get("formatType","gif"),]
    #params['file_type'] = "gif"
    params['file_name'] = request.POST.get("file_name","")
    params['frame_rate'] = int(request.POST.get("fps",1))
    params['clean_end_frames'] = bool(request.POST.get("clean_end_frames",""))
    params['clean_begin_frames'] = bool(request.POST.get("clean_begin_frames",""))
    params['persist_layers'] = bool(request.POST.get("persist_layers",""))
    params['map_size'] = (int(request.POST.get("x",800)),int(request.POST.get("y",600)))
    params['thumbnail'] = {'color':(230,230,230),
                           'has_time': True,
                           'has_layers': True,
                           'length':65,
                           'sources':["test","test2"]}
    params['bbox']=(float(request.POST.get("bboxW",-180)),
                    float(request.POST.get("bboxS",-90)),
                    float(request.POST.get("bboxE",180)),
                    float(request.POST.get("bboxN",90)))
    params['projection'] = request.POST.get("projection","EPSG:4326")
    if request.POST.get("custom_time",""):
        params['time_string']="%sT%02i:%02i:%02i/%sT%02i:%02i:%02i/%s"%(request.POST.get("fromdate"  ,""),
                    int(request.POST.get("Bhour"  ,"")),
                    int(request.POST.get("Bminute","")),
                    int(request.POST.get("Bsecond","")),
                    request.POST.get("todate"  ,""),
                    int(request.POST.get("Ehour"  ,"")),
                    int(request.POST.get("Eminute","")),
                    int(request.POST.get("Esecond","")),
                    request.POST.get("time_step",""),  )
    # Get list of product to download
    else:
      params['time_string']=None
    listOfProduct = request.POST.get("prodList","").split("\r\n")[:-1]
    order = 1
    params['time_layers'] = {}
    params['base_layers'] = {}
    for prod in listOfProduct:
        par = prod.split("\t")
        if par[2] =="true":
            params['time_layers'][order] = {'style' : None,
                                            'name'  : par[1],
                                            'url'   : par[0],
                                            'legend': False}
        else:
            params['base_layers'][order] = {'style' : None,
                                            'name'  : par[1],
                                            'url'   : par[0],
                                            'legend': False}
        order += 1
    if params['file_name']=="":
        return HttpResponse("erreur")
    # Launch execute
    update('Begining of download')
    GeoGIF.generateAnimation(params,tempdir.name,update=update)
    update('Saving result in DB')
    for format in params['list_of_format']:
        update('Saving video format %s in db'%(format,))
        file = open("%s/%s"%(tempdir.name,params["file_name"]+"."+format),"rb")
        fil = file.read()
        # Save file in user session
        request.session["result"] = b64encode(fil).decode("ascii")
        request.session["user_format"] = format
        file.close()
    request.session.set_expiry(86400)
    update('Job done')
    return HttpResponse("animation done")
    
def index(request):
    # Set up session
    request.session["status"] = "welcome"
    request.session.save()
    # This should be deleted because it is crap
    latest_question_list = ['test','test2']
    template = loader.get_template('GeoGIF1/index.html')
    context = {
        'sourceList': Source.objects.all(),
        'GetCapapilities': GetCapapilities.objects.all(),
        'version':version
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    # This should be deleted
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
  # This should be deleted
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
  # This should be deleted
    return HttpResponse("You're voting on question %s." % question_id)

def updateStatus(request, status):
    # This function acts as a messager interface between the server and the client
    async_to_sync(channels.layers.get_channel_layer().send)(request.session["channel_name"], {'type': 'status','status':status})
