from calendar import c
import csv
import requests
import json
from os.path import exists
from utils import UserInterface


clientDataList = {}

# data = {"From" : "James Boon", "To" : "+61419503320", "Text" : "It works"}

def SendMessage(data):
    apiToken = "ae4252b653ea4995aea6074d8b4b97a0"
    url = "https://api.mailjet.com/v4/sms-send"
    headers = {"Authorization": f"Bearer {apiToken}",
           "content-type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    return json.loads(response.text)

def GetTransmissionData():
    apiToken = "ae4252b653ea4995aea6074d8b4b97a0"
    url = "https://api.mailjet.com/v4/sms?StatusCode=1,2,3,4,5,6,7,8,9,10,11,12,13,14"
    headers = {"Authorization": f"Bearer {apiToken}"}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def WriteTransmissionDataFile(resposeJson, fileName):
    
    with open(fileName, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Status Code", "Description"])
        for line in resposeJson["Data"]:
            writer.writerow([line["To"], line["Status"]
                            ["Code"], line["Status"]["Description"]])

def GetClientDataFromFile(clientDataList, fileName):
    '''Gets the data from the csv file and puts it into the client data list
    '''
    assert exists(fileName), "The csv file you have attempted to get client data from does not exist"

    # Todo, error check that the csv file is in the correct format.

    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            
            # Removes the header row
            if(row[0] == "Client Name"):
                continue

            clientDataList.update({row[0] : (row[1], row[2], row[3])})
            
    return clientDataList

def SendIndividualSMS(name, clientDataList):
    print(f"Sending message to {name}")
    
    number = clientDataList[name][1]
    message = clientDataList[name][2]
    print(f"number: {number},message: {message}")

    data = {"From": "James Boon", "To": number, "Text": message}

    # Todo: work out what to do with the response.
    print(SendMessage(data))

def SendStateGroupSMS(state, clientDataList, groupList):
    print(f"Sending messages to {state} group")
    for name in groupList:
        SendIndividualSMS(name,clientDataList)


def process(clientDataList):
    
    while True:
        clientDataList = GetClientDataFromFile(clientDataList, 'integratedTestData.csv')
        userSelection = UserInterface(
            ["Send SMS by Individual Name", "Send multiple SMS to State Group", "Exit"])
        
        match userSelection:
            case 1:
                print("Enter Individual Name:")
                name = input()
                if name in clientDataList:
                    SendIndividualSMS(name, clientDataList)
                else:
                    print(f"{name} is not in the client list")

            case 2:
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

            case 3:
                print("Good bye")
                break

        


    
if __name__ == "__main__":
    
    process(clientDataList)
    # result = GetTransmissionData()
    # print(result)
    # WriteTransmissionDataFile(result, "status.csv")
    # jsonresult = json.loads(result)
    # print(jsonresult["Data"])
    # for item in jsonresult["Data"]:
    #     print(item["ID"])
    # print("Emergency Contact Application")
    # GetClientDataFromFile(clientDataList, 'integratedTestData.csv')
    # 
    # print(UserInterface(["Send SMS by Individual Name", "Send multiple SMS to State Group", "Exit"]))


# response from sending
# {'ID': 'e741d72e-c033-4a7c-8cb6-8aff2d07d215', 'From': 'James Boon', 'To': '+61419503320', 'Status': {'Code': 1, 'Name': 'sent_pending','Description': 'Message is being sent'}, 'Cost': {'Value': 0.028, 'Currency': 'USD'}, 'CreationTS': 1657927999, 'Text': 'Testing from csv', 'SmsCount': 1}
