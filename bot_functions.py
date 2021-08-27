import urllib.request
import re

def song_url(user_request: str):
    
    #Template for youtube search URL
    search_template = 'https://www.youtube.com/results?search_query='
    
    #URL to watch a video
    link_template = "https://www.youtube.com/watch?v="

    #Add the user input (play command made by user) to the search template
    search_link = search_template + str(user_request.replace(" ", "+"))

    #Read HTML of search template result
    html = urllib.request.urlopen(search_link)
    
    #Grab the first video id of the search result
    id = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]

    #Add the watch URL with the video id to have a complete link to a song
    link = link_template + id

    return link
