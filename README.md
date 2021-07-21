# Lead-Flow
Sales CRM Application

## Description

* Lead-Flow is a sales CRM Application written in Python, utilizing the Gmail API, Flask web framework and SQLAlchemy. 
* The user makes an account, connects their gmail account with Oauth2, starts a search query to pull specific emails matching search criteria.
* Lead-Flow then takes the lead info in the email message, parses the data and adds to the SQLAlchemy database. 
* An editable profile is then made of each potential lead. 

## Getting Started

* Since Lead-Flow utilizes the Gmail API, it cannot be hosted unless an SSL certificate is provided. Because of this I have enabled it to run locally. 
* To make your own credentials.json file, you will need to make a free account with Google Cloud Platform, then make a new app. After App is created, you can create your own credentials to save within the Lead-Flow file system to connect to your Gmail.

### Dependencies

* Flask
* Google Cloud Platform credentials.json file

### Installing

```
pip install requirements.txt
```

### Executing program

```
cd Lead-Flow
```
```
python3 application.py
```

```
python3 Blackjack.py
```
