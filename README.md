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
* User Makes Account

![Screenshot from 2021-07-20 21-21-13](https://user-images.githubusercontent.com/79290152/126433204-15a2cb91-fe00-4583-a71d-5d915a59d619.png)

* Home Screen

![Screenshot from 2021-07-20 21-21-37](https://user-images.githubusercontent.com/79290152/126433374-adbe590b-0468-4f42-88e4-ca69e3916572.png)

* Oauth2 Redirect

![GoogleAuth](https://user-images.githubusercontent.com/79290152/126437677-c874a7e5-d366-4e50-96b5-5b029bbf075b.png)

* Searching for gmail emails matching "Sender" and "Subject" 

![Screenshot from 2021-07-20 21-24-14](https://user-images.githubusercontent.com/79290152/126435521-8276840f-7a84-4eff-8a23-2021f2b0cb48.png)

* Leads pulled from Gmail API request

![Screenshot from 2021-07-20 22-58-25](https://user-images.githubusercontent.com/79290152/126438822-9ca47704-385d-483c-bfa2-992ee32bebd7.png)

* Lead Profile

![Screenshot from 2021-07-20 22-58-43](https://user-images.githubusercontent.com/79290152/126438965-a9e5ee2b-f2c5-4dbc-ba3b-183244d2ed4f.png)

* Edit Lead Profile

![Screenshot from 2021-07-20 22-58-54](https://user-images.githubusercontent.com/79290152/126439318-af3edf43-6776-4ec5-b7ff-e8b5a2a7abc6.png)






