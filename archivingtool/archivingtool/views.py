from django.shortcuts import render, redirect

from django.urls import reverse

from .forms import PostUrlForm

import asyncio

from scrapers import facebook_scraper, tiktok_scraper, youtube_scraper

import google.oauth2.credentials
from googleapiclient.discovery import build

def home(request):
	
	if request.method == "POST":
		# Create a form instance and populate it with data from the request (binding):
		form = PostUrlForm(data=request.POST)

		if form.is_valid():
			url = form.cleaned_data['url'].strip()
			if "facebook" in url:
				scraped_data = facebook_scraper.scrape(url)
			elif "tiktok" in url:
				scraped_data = asyncio.run(tiktok_scraper.scrape(url))
			elif "youtube" in url:
				scraped_data = youtube_scraper.scrape(url)
				
			# convert dictionary to oauth2 credentials
			credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])

			service = build("sheets", "v4", credentials=credentials)

			if not ('spreadsheet' in request.session):
				spreadsheet = {"properties": {"title": "WTF Archived Data"}}
				spreadsheet = (
					service.spreadsheets()
					.create(body=spreadsheet)
					.execute()
				)
			
				request.session['spreadsheet'] = spreadsheet

				(service.spreadsheets()
					.values()
					.append(
					spreadsheetId=request.session['spreadsheet']['spreadsheetId'], 
					range="A:A", 
					body={"values" : [[
						"Count",
						"Month/Year",
						"Date of Submission",
						"Monitors",
						"Unique Code",
						"Link to Disinformative Content",
						"Date Posted",
						"Summary",
						"Topic",
						"Sub-topic",
						"Possible Violation of Community Guidelines",
						"Platform",
						"Format",
						"Views",
						"Likes",
						"Subscribers",
						"Followers",
						"Account Name",
						"Original Name",
						"Date Created",
						"Primary Country",
						"Account Verification",
						"Account Type",
						"Status of the Post",
						"Screenshot of Post",
						"Notes",
						]]}, 
					valueInputOption='USER_ENTERED').execute(),
				)
			
			(service.spreadsheets()
			.values()
			.append(
				spreadsheetId=request.session['spreadsheet']['spreadsheetId'], 
				range="A:A", 
				body={"values" : [[
					scraped_data.get("Count"),
					scraped_data.get("Month/Year"),
					scraped_data.get("Date of Submission"),
					scraped_data.get("Monitors"),
					scraped_data.get("Unique Code"),
					scraped_data.get("Link to Disinformative Content"),
					scraped_data.get("Date Posted"),
					scraped_data.get("Summary"),
					scraped_data.get("Topic"),
					scraped_data.get("Sub-topic"),
					scraped_data.get("Possible Violation of Community Guidelines"),
					scraped_data.get("Platform"),
					scraped_data.get("Format"),
					scraped_data.get("Views"),
					scraped_data.get("Likes"),
					scraped_data.get("Subscribers"),
					scraped_data.get("Followers"),
					scraped_data.get("Account Name"),
					scraped_data.get("Original Name"),
					scraped_data.get("Date Created"),
					scraped_data.get("Primary Country"),
					scraped_data.get("Account Verification"),
					scraped_data.get("Account Type"),
					scraped_data.get("Status of the Post"),
					scraped_data.get("Screenshot of Post"),
					scraped_data.get("Notes"),
					]]}, 
				valueInputOption='USER_ENTERED').execute(),
			)		

	else:
		form = PostUrlForm()

	context = {
		'form' : form,
	}

	return render(request, "index.html", context)


import google_auth_oauthlib.flow
from .settings import BASE_URL

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# home view
def generate_token(request):
	# if we have the credentials stored in the session
	if ('credentials' in request.session):
		# # convert dictionary to oauth2 credentials
		# credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])

		# # access Google Sheets API with oauth2 credentials
		# service = build('sheets', 'v4', credentials=credentials)

		# # fetch rows
		# rows = service.spreadsheets().values().get(spreadsheetId="1LSZ5vsoTSNRNyBNLB3PhLRZ7TG_bPKHVadl4NYwJVQQ", range="A:D").execute()
		print("great success")

		return render(request, "index.html")

	else:
		# create flow from client credentials downloaded from Google cloud
		flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('creds.json', scopes=SCOPES)

		# URI where the oauth2's response will be redirected this must match with one of the authorized URIs configured in Google Cloud
		flow.redirect_uri = BASE_URL + 'oauthcallback/'

		# configuring the authorization url which will be used to request from oauth2
		authorization_url, state = flow.authorization_url(include_granted_scopes='true')

		# store the state in the session
		request.session['state'] = state
		
		# redirect to the authorization url which will redirect back to the callback view
		return redirect(authorization_url)

# callback used to extract the credentials. this will have a URL with query parameters set to the necessary arguments to extract the credentials e.g. http://localhost/oauthcallback/?state=K15TtnzoBKKepgg0Z3Ph86nEgGiubM&code=4%2F0AWgavdeDqFt44lGsb24OidcJrpSeLUja1OZkhfHNgNsacb00BrKgyeA-6pY7Uw08lt7s9g&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets
def callback(request):
	# get URL of the callback
	response = request.build_absolute_uri()

	# extract the state stored from the home view
	state = request.session['state']

	# create a new flow note that scopes were not defined because it gets appended to the previous scopes
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	 'creds.json', scopes=None, state=state)

	# same redirect uri as before
	flow.redirect_uri =  BASE_URL + 'oauthcallback/'

	# function call to get the credentials
	flow.fetch_token(authorization_response=response)

	# store the fetched credentials
	credentials = flow.credentials

	# convert credentials to dictionary
	request.session['credentials'] = credentials_to_dict(credentials)

	# go back to the home page
	return redirect(reverse('home'))

def credentials_to_dict(credentials):
	return {
		'token': credentials.token,
		'refresh_token': credentials.refresh_token,
		'token_uri': credentials.token_uri,
		'client_id': credentials.client_id,
		'client_secret': credentials.client_secret,
		'scopes': credentials.scopes
	}