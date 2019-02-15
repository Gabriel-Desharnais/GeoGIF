"""FrontEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# Adding the static files url
from django.conf import settings
from django.conf.urls.static import static

# get access to views function
import GeoGIF1.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),						# Admin page
    url(r'^$',views.home, name='home' ),					# Home page
    # Stuff related to the data base
    url(r'sourceDB/$',views.SourceDB,name='sourceDB'),				# See the database content
    url(r'updateASource/$',views.updateASource,name='updateASource'),		# Update a sourceDB
    url(r'AddSource/$',views.AddSource,name='AddSource'),			# Add a source to DB
    url(r'updateALayer/$',views.updateALayer,name='updateALayer'),		# Update a layer
    url(r'updateCap/$',views.updateCap),					# I don't know
    url(r'log/$',views.log, name='log'),                                                    # See the logs
    # Get access to the result content
    url(r'THE/$',views.THE,name='THE'),						# Show the GIF
    url(r'GIF/$',views.gif,name='GIF'),						# Show the GIF
    # Retrive information from DB
    url(r'GetCAP',views.getCap,name='GetCAP'),					# Get layers of source
    url(r'isItTimeEnabled',views.isItTimeEnabled,name='isItTimeEnabled'),	# Get if layer is time Enabled
    url(r'getTimeExtent',views.getTimeExtent,name='getTimeExtent'),		# Get layer time extent
    # Getting server status
    url(r'requestStatus/$',views.requestStatus,name='requestStatus'),		# Get the request status
    # main page of GeoGIF1
    url(r'GeoGIF1/$', views.index, name='GeoGIF1'),				# Show the form to generate GIF
    url(r'END/$',views.END,name='END'),						# End the session of GeoGIF1
    # Twitter stuff
    url(r'twitterSignIn/$',views.twitterSignIn,name='twitterSignIn'),		# Twitter sign in first step
    url(r'backFromTwitter/$',views.backFromTwitter,name='backFromTwitter'),	# Twitter sign in second step
    url(r'tweetATweet/$',views.tweetATweet,name='tweetATweet'),			# Send a tweet
    url(r'SendTweet/$',views.SendTweet,name='SendTweet'),			# Tweeting form
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)		# Add static URLs
