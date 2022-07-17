# integratedCapital code challenge:
This application sends SMS messages from a client data file. It has a simple command line UI and can send messages to
an individual client, clients by state group or all clients. On exit a csv file is created with the sms transmissions
which have failed or are still pending.

Requirements:
Built and tested on Python 3.10.2

Installation:

git clone https://github.com/JimmyBoon/integratedcapital.git

cd integratedcapital

pip3 install -r requirements.txt

create a file called 'apitoken.txt' and put in an API token from https://app.mailjet.com/sms

populate the clientdata.csv file, with the client information

Run:
python3 sendsms.py

