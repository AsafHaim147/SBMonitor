from config import BOT_API_KEY,CHAT_ID,VPN_MODE,LINK
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
from nordvpn_switcher import initialize_VPN,rotate_VPN

#######################################################################################################################
#      The program will find all the "new-arrival" items in SneakerBox and compare them occasionally                  #
#      Once a new item is found, the full name tag, link name and full link will be sent to a telegram channel        #
#######################################################################################################################

# this function will check if there are any differences between the local shoe dictionary and the new dictionary we just collected from the HTML.
def checkNew(dict1, dict2):
    leftovers = [x for x in dict2 if x not in dict1]
    return leftovers


#this fuction will extract the shoe links from the scraped HTML and organize it in a dictionary

#this function has to be customized in order to get the information you really want and not the whole element.
def getShoeDict(soup):
    shoeText = soup.find_all("div", {"class": "product show w-4 new-arrivals"})
    newShoes = {}
    for tag in shoeText:
        item = tag.find('a', href=True)
        if item:
            #item link
            shoeLink = item['href']
            #item name from link
            shoeName = str(item['href'])[34:-1]
            titlePrice = item.find("div", {"class": "title-price"})
            itemTitle = titlePrice.find("div", {"class": "title"})
            #discard spaces and div tag
            shoeTag = re.sub(r"(\w)([A-Z])", r"\1 \2",str(itemTitle).replace(" ","")[18:-6])[1:]
            newShoes[shoeLink] = {"ShoeName":shoeName,
                           "ShoeTag":shoeTag,
                           "ShoeLink":shoeLink
                          }
    return newShoes

# a simple function that loads the dictionary from the JSON file
def getJSON():
    #read JSON file
        with open('assets.json') as file:
            shoes = json.load(file)
    #gather all SN into a dict
        return shoes

# a simple function that updates the JSON dictionary if theres any differences detected
def updateJSON(shoes):
    json_object = json.dumps(shoes, indent=4)
    with open('assets.json', "w") as fileout:
        fileout.write(json_object)

#this function  will send a message on our telegram bot for every new shoe that it detects.

#this function has to be customized in order to get the information you really want and not the whole element.
def sendMessage(newShoe):
    MY_MESSAGE_TEXT =f'''{newShoe["ShoeName"]}
    
{newShoe["ShoeTag"]}

{newShoe["ShoeLink"]}'''
    r = requests.get(f'https://api.telegram.org/{BOT_API_KEY}/sendMessage?chat_id={CHAT_ID}&text={MY_MESSAGE_TEXT}')
    if r.status_code == 200:
         print('new shoe!')
    else:
        print(r.text)  # Do what you want with response

#######################################################
#                       START                         #
#######################################################
#monitor current time for script intervals, you can delete lines 77 and 85 + datetime imports if you wont use nordvpn or request intervals.
now = datetime.now(); sec = int(now.strftime("%H:%M:%S")[-2:]); min = int(now.strftime("%H:%M:%S")[-5:-3])
#delete lines 78-81 and 86-87 if you're not using nordVPN
if VPN_MODE:
    settings = initialize_VPN(area_input=['complete rotation'])  # nordVPN init
    rotate_VPN(settings)  # VPN connection function
print("Here we go.")
while 1:
    #monitor current time for script intervals
    now = datetime.now(); sec = int(now.strftime("%H:%M:%S")[-2:]); min = int(now.strftime("%H:%M:%S")[-5:-3])
    #choose specific min and sec so it'll rotate once an hour.
    if min == 20 and sec == 57 and VPN_MODE:
        rotate_VPN(settings)
    #parse the updated shoe list from the server and compare items#
    #this script will run appx every 2 seconds. some websites will block your requests if you send them too often so play with it till your satisfied with the results#
    if sec % 2 == 0:
        try:
            r = requests.get(LINK)
        except:
            print(r.status_code(),r.text)
            continue
        soup = BeautifulSoup(r.content, 'html.parser')
        updatedShoeDict = getShoeDict(soup)
        # local JSON vs website
        newShoes = checkNew(getJSON(),updatedShoeDict)
        #if new shoes are found, send a message on telegram for each shoe.
        if newShoes:
            for x in newShoes:
                try:
                    sendMessage(updatedShoeDict[x])
                except:
                    print("telegram error.")
                #update JSON
                updateJSON(updatedShoeDict)