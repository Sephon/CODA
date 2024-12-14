import gspread
from google.oauth2.service_account import Credentials

# Path to your downloaded JSON credentials file
CREDENTIALS_FILE = './savvy-summit-346321-feb57bcd3238.json'

# Google Sheet URL or ID
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1Uesyw5Myla-f2dRS0uW3BmR03GtMzVkKBrlBL_LryOA/edit#gid=0'

# Connect to Google Sheets
def connect_to_sheet():
    # Define the scope
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Authenticate using the service account file
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
    client = gspread.authorize(credentials)

    # Open the spreadsheet
    sheet = client.open_by_url(SPREADSHEET_URL)
    return sheet

# Fetch reflections for the current day
def fetch_reflection(sheet, date):
    worksheet = sheet.get_worksheet(0)  # Get the first sheet
    data = worksheet.get_all_records()  # Fetch all rows as a list of dictionaries
    
    # Filter by the current date (assumes a 'Date' column in the sheet)
    for row in data:
        if row.get('Date') == date:
            return row.get('Reflection')  # Return the reflection text
    
    return "No reflection found for today."

# Main function
if __name__ == "__main__":
    import datetime

    # Get today's date in the format used in your sheet (e.g., 'YYYY-MM-DD')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Connect and fetch
    sheet = connect_to_sheet()
    reflection = fetch_reflection(sheet, today)
    print("Today's Reflection:", reflection)
