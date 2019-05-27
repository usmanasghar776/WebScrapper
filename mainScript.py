import pymongo
myclient = pymongo.MongoClient("mongodb+srv://usman:usman@cluster0-h1prq.mongodb.net/test?retryWrites=true")
mydb = myclient["jobsdata"]
mycol = mydb['jobs']
from bs4 import BeautifulSoup
import requests

_alldata = mycol.find()
print("\nTotal " + str(_alldata.count()) + " jobs are found which are already stored in database \n")
print("Scrapping script is in progress. Please Wait....!")
soup = BeautifulSoup(requests.get('https://news.ycombinator.com/jobs').content, "html.parser")

alltr = soup.find_all("tr",{"class":"athing"})
for x in alltr:
    full_des = x.find('a').text

    try:
      location = full_des.lower().split("in ")[1]
    except:
      location = "NA"

    try:
      company = full_des.lower().split("is hiring")[0]
    except:
      company = "NA"

    try:
      job = full_des.lower().split("is hiring")[1].split("in ")[0]
    except:
      job = "NA"

    dummy = {'Company_Name':company,'Job_Position':job,'location':location}
    _result = mycol.find_one(dummy)
    if _result == None:
        main_insert = mycol.insert(dummy)
        print("New Records found and added \n")

print("Scrapping done sucessfully \n")
_alldata = mycol.find()
print("Total " + str(_alldata.count()) + " jobs are stored in database successfully...! ")