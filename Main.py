from WebScrapers import AirBNBWishlist
from API import GoogleSheets
import pandas as pd

# Run hourly to check for updates and serve them to the spreadsheet
def check_for_updates(spreadsheet, workbook_name, link):
    dao = GoogleSheets.DataObject()

    local_data = dao.pull_data(spreadsheet, workbook_name)  # data from Spreadsheet
    server_data = AirBNBWishlist.fetch(link, write= True)  # data from AirBNB server

    try:
        diff = local_data.compare(server_data)

        if len(diff) != 0:
            print('Value change found:')
            print(diff)
            dao.push_data(spreadsheet, workbook_name)

        else:
            print('No change found.')

    except Exception as e:
        print('Structure change found! (error thrown)')
        dao.push_data(spreadsheet, workbook_name)

spreadsheet = '1vVn2PuJybnMyO81SA4e1tVUGmPeSoRRd1LEbmU6jydk'
workbook = 'available_listings'
wishlist_link = 'https://www.airbnb.com/wishlists/v/1250433647?s=67&unique_share_id=26a5887d-15af-4bc3-92ef-fa74ea9da81f'

check_for_updates(spreadsheet, workbook, wishlist_link)