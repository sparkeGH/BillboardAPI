#some imports
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import random
import urllib, urllib.request
from urllib.request import urlopen

#establish app and api
app = Flask(__name__)
api = Api(app)

#primary method
def getTopSongs():
    #identify url, proxy as Mozilla, scrape html into a string and clean up escaped chars
    url= "https://www.billboard.com/charts/hot-100"
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urlopen(req)
    scrapedBytes = page.read()
    html = scrapedBytes.decode("utf-8")
    html = html.encode('utf-8').decode('ascii', 'ignore')
    html = html.replace('&#039;', "\'")
    html = html.replace('&amp;', "&")

    #traverse html string, find all song and artist names, and store them in arrays defined below
    # NOTE: this section is a little obtuse because it is mostly dependent 
    # on what the HTML from the webscrape looks like
    titles = []
    artists = []
    startIndex = html.find("primary\">") + len("primary\">")
    endIndex = html.find("<", startIndex)
    while (startIndex > -1):
        titles.append(html[startIndex:endIndex])
        startIndex = html.find("secondary\">", endIndex)
        if(startIndex > -1):
            startIndex += len("secondary\">")
        endIndex = html.find("<", startIndex)
        artists.append(html[startIndex:endIndex])
        startIndex = html.find("primary\">", endIndex)
        if(startIndex > -1):
            startIndex  += len("primary\">")
        endIndex = html.find("<", startIndex)

    #append a dictionary for each song to a list and return the songList
    #could add more dictionary entries later with a larger webscrape
    songs = []
    for i in range(100):
        thisSong = {
            "title":titles[i],
            "artist":artists[i]
        }
        songs.append(thisSong)
    return songs

#define class with GET method
class Songs(Resource):
    def get(self):
        topSongs = getTopSongs()
        return topSongs, 200
    pass
#establish url for class
api.add_resource(Songs, '/songs')

#automatically starts the app on script execution
if __name__ == "__main__":
    app.run(debug = True)
