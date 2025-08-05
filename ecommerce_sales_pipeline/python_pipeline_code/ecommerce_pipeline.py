import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate with credentials
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open your Google Sheet by name
spreadsheet = client.open("ecommerce_data")  # Use the title of the sheet
sheet = spreadsheet.sheet1  # Or use .worksheet("Sheet1") for named tabs

# Load into pandas
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Preview
# print(df.head())

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove unnecessary columns 
df = df.drop(columns=['url', 'scraped_at', 'terms'], errors='ignore')

# Rename 'section' to 'gender'
df = df.rename(columns={'section': 'gender'})

# Add total price column
df['total_revenue'] = df['quantity'] * df['price']

# Flag discount such as promotion 
df['promotion'] = df['promotion'].apply(lambda x: 0 if pd.isna(x) else 1)

# Add count for Power BI
df['count'] = 1 

# Save cleaned CSV
#df.to_csv('ecommerce_data_cleaned.csv', index=False)
df.to_excel('ecommerce_data_cleaned.xlsx', index=False)

# Preview
print(df.head())