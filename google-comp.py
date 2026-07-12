import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Local Excel Implementation
def write_to_excel(file_name, data_dict):
    df = pd.DataFrame(data_dict)
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")

# 2. Google Sheets Implementation
def write_to_google_sheet(sheet_id, worksheet_name, data_dict):
    # Setup connection (requires a 'credentials.json' from Google Cloud Console)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    # Open sheet and update
    sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
    df = pd.DataFrame(data_dict)
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    print("Data saved to Google Sheets")
