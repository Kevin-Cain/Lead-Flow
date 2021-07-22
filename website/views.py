from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from oauthlib.oauth2 import WebApplicationClient
import os
import flask
import requests
import json

from .models import User, db, Leads
from flask_sqlalchemy import SQLAlchemy
import base64
import email
import re

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "credentials.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly'
]
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

views = Blueprint('views', __name__)



@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("account-home.html", user=current_user)



@views.route('/test', methods=['GET', 'POST'])
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

    
    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    
    flask.session['credentials'] = credentials_to_dict(credentials)

    # Requesting/Submitting User info for Email Search criteria

    if request.method == 'POST':
        senderEmail = request.form.get('senderEmail')
        subject = request.form.get('subject')
        #keywords = request.form.get('keywords')

      
        #GET MESSAGES/INFO REQUEST
        service = build('gmail', 'v1', credentials=credentials)


        # Looping through messages matching search criteria and getting message info

        search_id = service.users().messages().list(userId='me' ,q=f'from: {senderEmail} subject: {subject}').execute()
        try:
            message_ids = search_id['messages']
            for text in message_ids:
                email_id = text['id']     
                message = search_id = service.users().messages().get(userId='me', id=f'{email_id}', format='raw').execute()
                msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
                msg_str = email.message_from_bytes(msg_raw)
                content_types = msg_str.get_payload()
                content1, content2 =content_types
                payload = str(content1.get_payload())
                

                new_list = []
                strings = payload.replace('*', ' ')
                stringss = strings.replace('\r', ' ')
                stringsss = stringss.replace('\n',':')
                stringssss = stringsss.split(':')
                for words in stringssss:
                    new_list.append(words.strip())
                

                keyword_list = ['Name','Your Email','Your Message','Account Name','DBA Account Name', 'Account Address','Account City','Account State','Account Zip', 'Lead Source','Lead Name','Email','Phone','Phone No.','Build City', 'Build State','Model of Interest', 'Bedrooms','Bathrooms','Square Footage','Product Series','Construction Code','Construction Type','Customer Comments', 'Timing','Home Placement','Has Financing','Budget','Down Payment']
                

                database_terms = []
                for searchTerm in keyword_list:
                    searchTerm = searchTerm.replace(".", " ")
                    searchTerm = searchTerm.replace(" ", "")
                    database_terms.append(searchTerm)

                final_data_list = []
                YourMessage = ''
                CustomerComments = ''


                for selector in keyword_list:
                    counter = 1  
                    for lines in new_list:
                        if selector == lines:
                            if selector == 'Your Message':
                                for your_message in new_list[counter:]:    
                                    if your_message == '':
                                        break
                                    else:
                                        YourMessage += (your_message + " ")
                                selectors = selector.replace(" ", "")
                                final_data_list.append(f'{selectors}')
                                final_data_list.append(YourMessage)
                                break


                            if selector == 'Customer Comments':
                                for your_message in new_list[counter:]:
                                    if your_message == '':
                                        break
                                    if your_message == 'Account Name' or your_message == 'Questions?':
                                        break
                                    else:
                                        CustomerComments += (your_message + " ")
                                selectors = selector.replace(" ", "")
                                final_data_list.append(f'{selectors}')
                                final_data_list.append(CustomerComments)
                                break
                            
                            if selector == 'Home Placement':
                                removed_unicode = new_list[counter].replace('=E2=80=99', "'")
                                selectors = selector.replace(" ", "")
                                final_data_list.append(f'{selectors}')
                                final_data_list.append(removed_unicode)
        
                            selectors = selector.replace(" ", "")
                            final_data_list.append(f'{selectors}')
                            final_data_list.append(new_list[counter])

                        counter += 1


                # ADDING DATA TO DATABASE
                
                
                def data_to_database(final_data_list, x):
                    if x in final_data_list:
                        location = final_data_list.index(x)
                        x = final_data_list[location+1]
                    else:
                        x = "N/A"
                    return x
                
            
                Name1 = data_to_database(final_data_list, 'Name')
                Name2 = data_to_database(final_data_list, 'LeadName')
                if len(Name1) > len(Name2):
                    Name = Name1
                else:
                    Name = Name2
                
                Email1 = data_to_database(final_data_list, 'YourEmail')
                Email2 = data_to_database(final_data_list, 'Email')
                if len(Email1) > len(Email2):
                    Email = Email1
                else:
                    Email = Email2

                CustomerComments1 = data_to_database(final_data_list, 'CustomerComments')
                CustomerComments2 = data_to_database(final_data_list, 'YourMessage')
                if len(CustomerComments1) > len(CustomerComments2):
                    CustomerComments = CustomerComments1
                else:
                    CustomerComments = CustomerComments2

                Phone1 = data_to_database(final_data_list, 'Phone')
                PhoneNo = data_to_database(final_data_list, 'PhoneNo.')
                if len(Phone1) > len(PhoneNo):
                    Phone = Phone1
                else:
                    Phone = PhoneNo

                    
                AccountName = data_to_database(final_data_list, 'AccountName')
                DBAAccountName = data_to_database(final_data_list, 'DBAAccountName')
                AccountAddress = data_to_database(final_data_list, 'AccountAddress')
                AccountCity = data_to_database(final_data_list, 'AccountCity')
                AccountState = data_to_database(final_data_list, 'AccountState')
                AccountZip = data_to_database(final_data_list, 'AccountZip')
                LeadSource = data_to_database(final_data_list, 'LeadSource')
                BuildCity = data_to_database(final_data_list, 'BuildCity')
                BuildState = data_to_database(final_data_list, 'BuildState')
                ModelofInterest = data_to_database(final_data_list, 'ModelofInterest')
                Bedrooms = data_to_database(final_data_list, 'Bedrooms')
                Bathrooms = data_to_database(final_data_list, 'Bathrooms')
                SquareFootage = data_to_database(final_data_list, 'SquareFootage')
                ProductSeries = data_to_database(final_data_list, 'ProductSeries')
                ConstructionCode = data_to_database(final_data_list, 'ConstructionCode')
                ConstructionType = data_to_database(final_data_list, 'ConstructionType')
                Timing = data_to_database(final_data_list, 'Timing')
                HomePlacement = data_to_database(final_data_list, 'HomePlacement')
                HasFinancing = data_to_database(final_data_list, 'HasFinancing')
                Budget = data_to_database(final_data_list, 'Budget')
                DownPayment = data_to_database(final_data_list, 'DownPayment')
                Notes = 'N/A'
            

                
                check_duplicates = db.session.query(Leads).filter_by(user_id=current_user.id).all()
                for name in check_duplicates:
                    if name.Name == Name:
                        break
                    
               
                else:
                    NewLead = Leads(user_id=current_user.id, Name=Name, Email=Email, AccountName=AccountName, CustomerComments=CustomerComments, Phone=Phone, DBAAccountName=DBAAccountName, 
                    AccountAddress=AccountAddress, AccountCity=AccountCity, AccountState=AccountState, AccountZip=AccountZip, LeadSource=LeadSource, BuildCity=BuildCity, BuildState=BuildState,
                    ModelofInterest=ModelofInterest, Bedrooms=Bedrooms, Bathrooms=Bathrooms, SquareFootage=SquareFootage, ProductSeries=ProductSeries, ConstructionCode=ConstructionCode, ConstructionType=ConstructionType, Timing=Timing, 
                    HomePlacement=HomePlacement, HasFinancing=HasFinancing, Budget=Budget, DownPayment=DownPayment, Notes=Notes)
                    db.session.add(NewLead)
                    db.session.commit()
              
                
            return redirect(url_for('views.home'))

        except KeyError:
            print('No messages found')
        
    return render_template('emailSearch.html', user=current_user)




@views.route('/lead-profile/<id>', methods=['POST','GET'])
def leadprofile(id):
    profile = db.session.query(Leads).filter_by(user_id=current_user.id, Name=id).first()
    
    if request.form.get("delete"):
        #Leads.query.filter_by(Name=id).delete()
        db.session.query(Leads).filter_by(user_id=current_user.id, Name=id).delete()
        db.session.commit()
        return redirect(url_for(".home"))
    elif request.form.get("save"):
        return render_template('edit_user_profile.html', user=current_user, profile=profile)

    return render_template('lead-profile.html', user=current_user, profile=profile)
   

@views.route('/update', methods=['POST','GET'])
def update():
    updatedCity = request.form.get("updatedCity")
    beforeCity = request.form.get("beforeCity")
    City = Leads.query.filter_by(BuildCity=beforeCity).first()
    City.BuildCity = updatedCity

    updatedState = request.form.get("updatedState")
    beforeState = request.form.get("beforeState")
    State = Leads.query.filter_by(BuildState=beforeState).first()
    State.BuildState = updatedState

    updatedModelofInterest = request.form.get("updatedModelofInterest")
    beforeModelofInterest = request.form.get("beforeModelofInterest")
    Model = Leads.query.filter_by(ModelofInterest=beforeModelofInterest).first()
    Model.ModelofInterest = updatedModelofInterest

    updatedBedrooms = request.form.get("updatedBedrooms")
    beforeBedrooms = request.form.get("beforeBedrooms")
    rooms = Leads.query.filter_by(Bedrooms=beforeBedrooms).first()
    rooms.Bedrooms = updatedBedrooms

    updatedBathrooms = request.form.get("updatedBathrooms")
    beforeBathrooms = request.form.get("beforeBathrooms")
    bath = Leads.query.filter_by(Bathrooms=beforeBathrooms).first()
    bath.Bathrooms = updatedBathrooms

    updatedSquareFootage = request.form.get("updatedSquareFootage")
    beforeSquareFootage = request.form.get("beforeSquareFootage")
    footage = Leads.query.filter_by(SquareFootage=beforeSquareFootage).first()
    footage.SquareFootage = updatedSquareFootage

    updatedProductSeries = request.form.get("updatedProductSeries")
    beforeProductSeries = request.form.get("beforeProductSeries")
    series = Leads.query.filter_by(ProductSeries=beforeProductSeries).first()
    series.ProductSeries = updatedProductSeries

    updatedTiming = request.form.get("updatedTiming")
    beforeTiming = request.form.get("beforeTiming")
    timing = Leads.query.filter_by(Timing=beforeTiming).first()
    timing.Timing = updatedTiming

    updatedHomePlacement = request.form.get("updatedHomePlacement")
    beforeHomePlacement = request.form.get("beforeHomePlacement")
    placement = Leads.query.filter_by(HomePlacement=beforeHomePlacement).first()
    placement.HomePlacement = updatedHomePlacement
    
    updatedConstructionCode = request.form.get("updatedConstructionCode")
    beforeConstructionCode = request.form.get("beforeConstructionCode")
    code = Leads.query.filter_by(ConstructionCode=beforeConstructionCode).first()
    code.ConstructionCode = updatedConstructionCode

    updatedConstructionType = request.form.get("updatedConstructionType")
    beforeConstructionType = request.form.get("beforeConstructionType")
    type = Leads.query.filter_by(ConstructionType=beforeConstructionType).first()
    type.ConstructionType = updatedConstructionType

    id = request.form.get("updatedName")
    beforeName = request.form.get("beforeName")
    person = Leads.query.filter_by(Name=beforeName).first()
    person.Name = id
    
    updatedEmail = request.form.get("updatedEmail")
    beforeEmail = request.form.get("beforeEmail")
    contact = Leads.query.filter_by(Email=beforeEmail).first()
    contact.Email = updatedEmail

    updatedPhone = request.form.get("updatedPhone")
    beforePhone = request.form.get("beforePhone")
    connect = Leads.query.filter_by(Phone=beforePhone).first()
    connect.Phone = updatedPhone

    updatedHasFinancing = request.form.get("updatedHasFinancing")
    beforeHasFinancing = request.form.get("beforeHasFinancing")
    money = Leads.query.filter_by(HasFinancing=beforeHasFinancing).first()
    money.HasFinancing = updatedHasFinancing

    updatedBudget = request.form.get("updatedBudget")
    beforeBudget = request.form.get("beforeBudget")
    pricerange = Leads.query.filter_by(Budget=beforeBudget).first()
    pricerange.Budget = updatedBudget

    updatedDownPayment = request.form.get("updatedDownPayment")
    beforeDownPayment = request.form.get("beforeDownPayment")
    down = Leads.query.filter_by(DownPayment=beforeDownPayment).first()
    down.DownPayment = updatedDownPayment

    updatedAccountName = request.form.get("updatedAccountName")
    beforeAccountName = request.form.get("beforeAccountName")
    acc = Leads.query.filter_by(AccountName=beforeAccountName).first()
    acc.AccountName = updatedAccountName

    updatedAccountAddress = request.form.get("updatedAccountAddress")
    beforeAccountAddress = request.form.get("beforeAccountAddress")
    add = Leads.query.filter_by(AccountAddress=beforeAccountAddress).first()
    add.AccountAddress = updatedAccountAddress

    updatedAccountCity = request.form.get("updatedAccountCity")
    beforeAccountCity = request.form.get("beforeAccountCity")
    ac_city = Leads.query.filter_by(AccountCity=beforeAccountCity).first()
    ac_city.AccountCity = updatedAccountCity

    updatedAccountState = request.form.get("updatedAccountState")
    beforeAccountState = request.form.get("beforeAccountState")
    acc_state = Leads.query.filter_by(AccountState=beforeAccountState).first()
    acc_state.AccountState = updatedAccountState

    updatedAccountZip = request.form.get("updatedAccountZip")
    beforeAccountZip = request.form.get("beforeAccountZip")
    zip = Leads.query.filter_by(AccountZip=beforeAccountZip).first()
    zip.AccountZip = updatedAccountZip

    updatedCustomerComments = request.form.get("updatedCustomerComments")
    beforeCustomerComments = request.form.get("beforeCustomerComments")
    customer_comments = Leads.query.filter_by(CustomerComments=beforeCustomerComments).first()
    customer_comments.CustomerComments = updatedCustomerComments

    updatedNotes = request.form.get("updatedNotes")
    beforeNotes = request.form.get("beforeNotes")
    note = Leads.query.filter_by(Notes=beforeNotes).first()
    note.Notes = updatedNotes

    db.session.commit()
    return redirect(url_for(".leadprofile", id=id))



@views.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  # The URI created here must exactly match one of the authorized redirect URIs
  # for the OAuth 2.0 client, which you configured in the API Console. If this
  # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
  # error.
  flow.redirect_uri = flask.url_for('views.oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)




def credentials_to_dict(credentials):
    return {'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}




@views.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('views.oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)

  #return render_template('linked-email.html', user=current_user)
  return flask.redirect(flask.url_for('views.home'))
