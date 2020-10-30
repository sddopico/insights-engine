'''
Created on Dec 27, 2018

@author: domdopico
'''
#bring in trello user client keys and tokens from secretized sheet
import keys
import json
import urllib3
import certifi

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

#base URL for the board, you can grab this from the browser
boardBaseUrl = "https://api.trello.com/1/boards/"

#ID key for trello board - you can find this by adding ".json" to the end of the full board URL in the browser
boardId = "5cdc8a58155fad155a81e064"

#establish variable for client keys, assign key 
client_id = keys.client

#establish variable for client token, assign token 
client_token = keys.token

#build JSON URL 
url = boardBaseUrl + boardId
    
querystring = {"actions":"commentCard",
               "boardStars":"none",
               "cards":"visible",
               "card_fields":"name,desc,idList,labels",
               "labels" : "all",
               "label_fields" : "name",
               "card_pluginData":"false",
               "checklists":"none",
               "customFields":"false",
               "fields":"name,desc,labelNames",
               "lists":"open",
               "list_fields":"name",
               "members":"none",
               "memberships":"none",
               "membersInvited":"none",
               "membersInvited_fields":"none",
               "pluginData":"false",
               "organization":"false",
               "organization_pluginData":"false",
               "myPrefs":"false",
               "tags":"false",
               "key":client_id,
               "token":client_token}


r = http.request('GET', url, fields=querystring)

response = json.loads(r.data.decode('utf-8'))

formatted_response = (json.dumps(response['cards'], indent=2, sort_keys=True))

cardsList = response['cards']


i=0
   
#declare empty list to sort source labels into
sourceLabelList = []

#declare empty list to sort auxiliary labels into
auxLabelList = []

#begin looping through cards indices, stop at 0 'labels' index, append label name at 0 index to sourceLabelList
for x in cardsList:
    
    #declare count variable for advancing labels index integer 
    j=0
    
    #append label name at 0 index to sourceLabelList 
    labelName = cardsList[i]['labels'][j]['name']
    if labelName not in sourceLabelList:
        sourceLabelList.append(labelName)
    
    #begin loop to check for additional "role" labels on card
    for x in cardsList:
       
        try:
            labelName = cardsList[i]['labels'][j]['name']
            if labelName not in auxLabelList and labelName not in sourceLabelList:
                auxLabelList.append(labelName)
        except IndexError:
            labelName = 'null' 
            
        j+=1           
    i+=1
    
print(sourceLabelList)
print(auxLabelList)

