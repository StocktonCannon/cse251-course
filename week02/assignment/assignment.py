"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
from unittest import result
from django.http import JsonResponse
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    def __init__(self,url, name="",urlList=None):
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}
        self.urlList = urlList
        self.outputList = []
        self.listName = name
        

    def run(self):
      global call_count
      if self.urlList != None:
        for url in self.urlList:
          call_count += 1
          response = requests.get(url)
          jsonResponse = response.json()
          self.outputList.append(jsonResponse["name"])
      else:
        call_count += 1 
        response = requests.get(self.url)
        self.response = response.json()
        

# TODO Add any functions you need here


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    print("----------------------------------------")

    # TODO Retrieve Top API urls
    MainUrlThread = Request_thread(TOP_API_URL)
    MainUrlThread.start()
    MainUrlThread.join()
    urlDict = MainUrlThread.response
    # print(urlDict)
    filmUrl = urlDict.get("films")
    

    # TODO Retireve Details on film 6
    filmThread = Request_thread(filmUrl+"6/")
    filmThread.start()
    filmThread.join()
    filmSix = filmThread.response
    print(f'Title: {filmSix.get("title")}')
    print(f'Director: {filmSix.get("director")}')
    print(f'Producer: {filmSix.get("producer")}')
    print(f'Released: {filmSix.get("release_date")}', end="\n\n")
    # print(filmSix)

    characterList = filmSix.get("characters")
    planetList = filmSix.get("planets")
    starshipList = filmSix.get("starships")
    vehicleList = filmSix.get("vehicles")
    speciesList = filmSix.get("species")

    characterThread = Request_thread('', "character",characterList)
    planetThread = Request_thread('', "planets",planetList)
    starshipThread = Request_thread('', "starships",starshipList)
    vehicleThread = Request_thread('', "vehicle",vehicleList)
    speciesThread = Request_thread('', "species",speciesList)

    characterThread.start()
    planetThread.start()
    starshipThread.start()
    vehicleThread.start()
    speciesThread.start()

    characterThread.join()
    planetThread.join()
    starshipThread.join()
    vehicleThread.join()
    speciesThread.join()

    # TODO Display results

    print(f'{characterThread.listName}: {len(characterThread.urlList)}')
    for name in characterThread.outputList:
      print(name, end=", ")
    print("\n")
        
    print(f'{planetThread.listName}: {len(planetThread.urlList)}')
    for name in planetThread.outputList:
      print(name, end=", ")
    print("\n")
    
    print(f'{starshipThread.listName}: {len(starshipThread.urlList)}')
    for name in starshipThread.outputList:
      print(name, end=", ")
    print("\n")
    
    print(f'{vehicleThread.listName}: {len(vehicleThread.urlList)}')
    for name in vehicleThread.outputList:
      print(name, end=", ")
    print("\n")
    
    print(f'{speciesThread.listName}: {len(speciesThread.urlList)}')
    for name in speciesThread.outputList:
      print(name, end=", ")
    print("\n")  

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
