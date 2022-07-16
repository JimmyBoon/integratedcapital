from mailjet_rest import Client
import os
api_key = '77461f8056686dd745ed32771f4ef4f4'
api_secret = '9815c6bceda66dbd8c0904fcad477688'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
    'Messages': [
        {
            "From": {
                "Email": "jwboon79@gmail.com",
                "Name": "James"
            },
            "To": [
                {
                    "Email": "jwboon79@gmail.com",
                    "Name": "James"
                }
            ],
            "Subject": "Greetings from Mailjet.",
            "TextPart": "My first Mailjet email",
            "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
            "CustomID": "AppGettingStartedTest"
        }
    ]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())
