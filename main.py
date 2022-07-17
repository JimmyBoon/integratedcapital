import asyncio
import csv
import aiohttp
import requests
import json
from os.path import exists
from utils import UserInterface, asyncTimer

clientDataList = {}

def GetAPItoken(file):
    '''Retrieves the API token from the first line of the file
    '''
    assert exists(file), "The file you have attempted to get the API token from does not exist"

    with open(file, 'r') as apiFile:
        apiToken = apiFile.readline()
        return apiToken


def GetClientDataFromFile(clientDataList, fileName):
    '''Gets the data from the csv file provided and puts it into the clientDataList
    '''
    assert exists(fileName), "The csv file you have attempted to get client data from does not exist"

    #TODO, error check that the csv file is in the correct format.
    #TODO, possible error or bug here, if there are two clients with the same name, then it will overwrite the older client.

    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        for row in reader:

            # Removes the header row
            if(row[0] == "Client Name"):
                continue

            clientDataList.update({row[0]: (row[1], row[2], row[3])})

    return clientDataList

@asyncTimer
async def SendMessage(dataList):
    '''Sends the SMS messages in the datalist, via the Mailjet API.
    Params:
    dataList: list containing dict items with message details eg: [{"From": "Sender", "To": "+61400111000", "Text": "Hello"}]
    '''

    #TODO: Still not sure if running this process as async is really faster than using simple requests. Testing required.
    apiToken = GetAPItoken("apitoken.txt")
    async with aiohttp.ClientSession() as session:

        url = "https://api.mailjet.com/v4/sms-send"
        headers = {"Authorization": f"Bearer {apiToken}",
                   "content-type": "application/json"}

        for data in dataList:
            async with session.post(url, ssl=False, headers=headers, json=data) as response:
                result = await response.json()
                print(result)


def GetTransmissionData():
    '''Gets the failed or not yet sent SMS data.
    returns the data in JSON format.
    '''
    apiToken = GetAPItoken("apitoken.txt")
    
    url = "https://api.mailjet.com/v4/sms?StatusCode=1,4,5,6,7,8,9,10,11,12,13,14"
    headers = {"Authorization": f"Bearer {apiToken}"}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def WriteTransmissionDataFile(resposeJson, fileName):
    '''Writes the data from failed sends into a CSV file
    Params: 
    responseJson: Json data from Mailjet api
    fileName: string, name of the CSV file in the format "name.csv"
    '''
    with open(fileName, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Status Code", "Description"])
        for line in resposeJson["Data"]:
            writer.writerow([line["To"], line["Status"]
                            ["Code"], line["Status"]["Description"]])


def SendIndividualSMS(name, clientDataList):
    '''Sends sms to an individual
    Params: name (string), name of the individual
    clientDataList(dict), contents of the csv file containing client data.
    '''
    print(f"Sending message to {name}")
    
    number = clientDataList[name][1]
    message = clientDataList[name][2]
    print(f"number: {number}, message: {message}")

    dataList = [{"From": "Testing", "To": number, "Text": message}]
    
    asyncio.run(SendMessage(dataList))
    

def SendStateGroupSMS(state, clientDataList, groupList):
    '''Sends sms to a state group
    Params: state (string), name of the state group
    groupList (list), containing strings of client names 
    clientDataList(dict), contents of the csv file containing client data.
    '''
    print(f"Sending messages to {state} clients")
    dataList = []
    for name in groupList:
        number = clientDataList[name][1]
        message = clientDataList[name][2]
        data = {"From": "Testing", "To": number, "Text": message}
        dataList.append(data)

    asyncio.run(SendMessage(dataList))
    

def process(clientDataList):

    clientDataList = GetClientDataFromFile(clientDataList, 'clientdata.csv')

    while True:
        
        userSelection = UserInterface(
            ["Send SMS by Individual Name", "Send multiple SMS to State Group","Send SMS to all clients", "Exit"])
        
        match userSelection:
            case 1: # Send to an individual
                print("Enter Individual Name:")
                name = input()
                if name in clientDataList:
                    SendIndividualSMS(name, clientDataList)
                else:
                    print(f"{name} is not in the client list")

            case 2: #Send to a state group
                print("Enter State Name:")
                state = input()
                group = []
                for client, value in clientDataList.items():
                    if value[0] == state:
                        group.append(client)
                
                if len(group) > 0:
                    SendStateGroupSMS(state, clientDataList, group)
                else:
                    print("State does not exist")

            case 3: #Send to all clients
                group = []
                state = "All"
                for client, value in clientDataList.items():
                    group.append(client)
                
                if len(group) > 0:
                    SendStateGroupSMS(state, clientDataList, group)
                else:
                    print("No clients in the the file")
                
            case 4: #Exit and save the failed sms transmissions
                
                #TODO: Add option to view sent message status without exiting

                result = GetTransmissionData()
                file = "status.csv"
                WriteTransmissionDataFile(result, file)
                print(f"Good bye, list of SMS tranmissions failed or not yet sent are in {file}")
                break

    
if __name__ == "__main__":

    assert exists(
        "apitoken.txt"), "There must be a file called 'apitoken.txt' with contains the API Token from MailJet see https://app.mailjet.com/sms to get a token"
    assert exists(
        "clientdata.csv"), "There must be a file called 'clientdata.csv' with contains client information"

    #TODO: create option to set the name of the sender.
    #TODO: create option to set the name of the data file.
    
    process(clientDataList)


# response from sending
# {'ID': 'e741d72e-c033-4a7c-8cb6-8aff2d07d215', 'From': 'James Boon', 'To': '+61419503320', 'Status': {'Code': 1, 'Name': 'sent_pending','Description': 'Message is being sent'}, 'Cost': {'Value': 0.028, 'Currency': 'USD'}, 'CreationTS': 1657927999, 'Text': 'Testing from csv', 'SmsCount': 1}
