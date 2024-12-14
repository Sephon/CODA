import pyperclip
import datetime
import gspread
from google.oauth2.service_account import Credentials
from translate import Translator

# Path to your downloaded JSON credentials file
CREDENTIALS_FILE = './savvy-summit-346321-feb57bcd3238.json'

# Google Sheet URL or ID
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1Uesyw5Myla-f2dRS0uW3BmR03GtMzVkKBrlBL_LryOA/edit#gid=0'

def generate_message(date, title, reflection, swedish_translation, spanish_translation):
    # Format the message
    message = f"🌞 *In This Moment, Daily Meditation Book {date}* 🌞\n\n*{title}*\n\n{reflection}\n\n🇸🇪 *Swedish:* {swedish_translation}\n\n🇪🇸 *Spanish:* {spanish_translation}"

    # Copy the message to clipboard
    pyperclip.copy(message)
    print("Message copied to clipboard. Ready to paste into WhatsApp!")
    
def split_and_translate(text, target_language, chunk_size=500):
    from translate import Translator
    translator = Translator(to_lang=target_language)
    
    # Split the text into chunks of 'chunk_size'
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Translate each chunk and combine the results
    translated_chunks = [translator.translate(chunk) for chunk in chunks]
    return " ".join(translated_chunks)

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

def fetch_reflection(sheet, date):
    worksheet = sheet.get_worksheet(0)  # Get the first sheet
    data = worksheet.get_all_records()  # Fetch all rows as a list of dictionaries
    
    # Extract the current month and day
    target_month_day = date.strftime('%m-%d')

    # Search for a matching reflection (ignoring the year)
    for row in data:
        sheet_date = row.get('Date')  # Example: '2024-12-14'
        if sheet_date:
            month_day = '-'.join(sheet_date.split('-')[1:])  # Extract 'MM-DD'
            if month_day == target_month_day:
                title = row.get('Title')  # Extract the title
                reflection = row.get('Reflection')  # Extract the reflection text
                return title, reflection  # Return both the title and reflection
    
    return "No reflection found for today."

# Main function
if __name__ == "__main__":
    import datetime
    
    # Connect and fetch
    sheet = connect_to_sheet()
    date = datetime.datetime.now()
    title, reflection = fetch_reflection(sheet, date)

    # Translate to Swedish and Spanish
    swedish_translation = split_and_translate(reflection, "sv")
    spanish_translation = split_and_translate(reflection, "es")

    generate_message(date.strftime('%Y-%m-%d'), title, reflection, swedish_translation, spanish_translation)