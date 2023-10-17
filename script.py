#!/usr/bin/env python3

import csv
import datetime
import requests
from bs4 import BeautifulSoup

class Paste:
    def __init__(self, id, title, username, language, date, content):
        self.id = id
        self.title = title
        self.username = username
        self.language = language
        self.date = date
        self.content = content


def getPasteInfo(paste_id):
    r = requests.get(f"https://pastebin.com/{paste_id}")
    soup = BeautifulSoup(r.text, "html.parser")

    # Retrieve username
    div = soup.find("div", {"class": "username"})
    div = div.find("a", href=True)
    username = div.text

    # Retrieve date
    div = soup.find("div", {"class": "date"})
    date = div.find("span")['title']
    
    # Retrieve title
    div = soup.find("div", {"class": "info-top"})
    title = div.find("h1").text

    # Retrieve content
    content = requests.get(f"https://pastebin.com/raw/{paste_id}").text

    # Retrieve language
    div = soup.find("div", {"class": "highlighted-code"})
    language = div.find("a", href=True, recursive=True).text

    return Paste(paste_id, title, username, language, date, content)


def getRecentPastes():
    pastes = []
    r = requests.get("https://pastebin.com/archive")
    soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.find_all("div")

    for d in divs:
        if d.has_attr("data-key"):
            elem = d.find_all("a", href=True)
            paste_id = elem[0]['href'][1:]
            print(f"Getting paste {paste_id}...")
            pastes.append(getPasteInfo(paste_id))
    return pastes


if __name__ == "__main__":
    print("Getting recent pastes...")
    pastes = getRecentPastes()
    
    print("Writing to CSV...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


    with open(f"./pastes/pastes_{timestamp}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "username", "language", "date", "content"])
        for p in pastes:
            writer.writerow([p.id, p.title, p.username, p.language, p.date, p.content])
