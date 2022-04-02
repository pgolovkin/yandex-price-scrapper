# yandex-price-scrapper
This project gets the information about the price of the goods specified in the code and USD CBRF rate.
The result is saved on the google drive https://docs.google.com/spreadsheets/d/1vuQZDHKR8k7htqynK0G34dQ1enClkAcFNrf7uP0RHd4/edit?usp=sharing

## Google OAuth
Use the example https://developers.google.com/drive/api/quickstart/python in order to get the token.

```python
from google_auth_oauthlib.flow import InstalledAppFlow

GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

flow = InstalledAppFlow.from_client_secrets_file('secret.json', GOOGLE_SCOPES)
creds = flow.run_local_server(port=0)
print(creds.to_json())
```

where `secret.json` is a json file that you can download from the Google console. 
