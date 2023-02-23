import Crawler
from API import GoogleSheets
import pandas as pd

# Runs hourly to check for updates and serve them to the spreadsheet
def check_for_updates():
    local_data = pd.read_csv('./exports/available_listings.csv')
    local_data = local_data.drop(local_data.columns[0], axis=1)
    server_data = Crawler.fetch(write= True)

    diff = local_data.compare(server_data)

check_for_updates()