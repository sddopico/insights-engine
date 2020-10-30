'''
Created on Dec 5, 2019

@author: domdopico
'''
import keys
import md_in
import json
import urllib3
import certifi
import requests
import sheet_grab


client_id = keys.client
client_token = keys.token

customers: '5f7cd99651f3e1332aa32e4d'
nonCustomers: '5f7cd99651f3e1332aa32e4f'


http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

boardBaseUrl = "https://api.trello.com/1/boards/"

boardId = "5f7cd99651f3e1332aa32e3c"


url = boardBaseUrl + boardId

querystring = {
    "lists":"open",
    "list_fields":"id,name",
    "key":client_id,
    "token":client_token
    }

cardQuerystring = {
    "fields": "id",
    "key": client_id,
    "token": client_token
    }

labelQuerystring = {
    "labels": "all",
    "key": client_id,
    "token": client_token
}


def getTags(args):
    tags = sheet_grab.main(args)
    tags.pop(0)
    return tags
    #print(tags)


def getLabels():
    r = http.request('GET', url, fields=labelQuerystring)
    response = json.loads(r.data.decode('utf-8'))
    labels = response['labels']
    return labels
    #formattedResponse = (json.dumps(labels, indent=2, sort_keys=True))
    #print(formattedResponse)


def getCardsList():
    r = http.request('GET', url, fields=querystring)
    response = json.loads(r.data.decode('utf-8'))
    formattedResponse = (json.dumps(response, indent=2, sort_keys=True))

    listId = response['lists'][0]['id']
    listURL = "https://api.trello.com/1/lists/" + listId + "/cards"

    r1 = http.request('GET', listURL, fields=cardQuerystring)
    response1 = json.loads(r1.data.decode('utf-8'))
    cardIdList = []
    i = 0
    for key in response1:
        cardIdList.append(response1[i]['id'])
        i += 1
    #print(cardIdList)
    return cardIdList


def mdInjection():
    cardIdList = getCardsList()
    
    description = [
        'Customer: ' + md_in.customer + '\n Participant: ' + md_in.participant + '\n Role: ' + md_in.role + '\n Units: ' + md_in.units + '\n Location: ' + md_in.location + '\n Notes: ' + md_in.notes + '\n SFDC: ' + md_in.sfdc]

    j = 0
    for ids in cardIdList:
        pushURL = 'https://api.trello.com/1/cards/' + ids
        pQueryString = {
            'key': client_id,
            'token': client_token,
            #'desc': description,
            'idLabels': md_in.labels
        }
        pResponse = requests.request('PUT', pushURL, params=pQueryString)
        j += 1


def tagBuilder(args):
    tagLabels = []
    tagLabelNames = []
    labels = getLabels()
    tags = getTags(args)

    for tag in tags:
        count = 0
        index = 0
        tag = str(tag).lstrip('[\'').rstrip('\']')
        for label in labels:
            if tag in labels[index]['name']:
                tagLabels.append(labels[count]['id'])
                tagLabelNames.append(labels[count]['name'])
            index += 1
            count += 1

    #print(tagLabelNames)
    return tagLabels



def main():

    cards = getCardsList()
    assocSizeTags = tagBuilder('Non-Customers!B:B')
    numAssocTags = tagBuilder('Non-Customers!F:F')
    numDoorTags = tagBuilder('Non-Customers!G:G')
    print(len(cards))
    print(len(assocSizeTags))
    print(len(numAssocTags))
    print(len(numDoorTags))

    count = 0
    for card in cards:
        pushURL = 'https://api.trello.com/1/cards/' + card
        pQueryString = {
            'key': client_id,
            'token': client_token,
            'idLabels': ['5f7cd99651f3e1332aa32e4f', assocSizeTags[count], numAssocTags[count], numDoorTags[count]]
        }
        pResponse = requests.request('PUT', pushURL, params=pQueryString)
        #print(pResponse)
        count += 1


if __name__ == '__main__':
    main()

