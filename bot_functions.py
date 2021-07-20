import urllib.request
import re

def song_url(user_request: str):
    search_template = 'https://www.youtube.com/results?search_query='
    link_template = "https://www.youtube.com/watch?v="

    search_link = search_template + str(user_request.replace(" ", "+"))

    html = urllib.request.urlopen(search_link)
    id = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]

    link = link_template + id

    return link