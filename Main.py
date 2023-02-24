import Crawler
from API import GoogleSheets
import pandas as pd

# Run hourly to check for updates and serve them to the spreadsheet
def check_for_updates(spreadsheet, workbook_name):
    dao = GoogleSheets.DataObject()

    local_data = dao.pull_data(spreadsheet, workbook_name)  # data from Spreadsheet
    server_data = Crawler.fetch(write= True)  # data from AirBNB server

    try:
        diff = len(local_data.compare(server_data))

        if diff != 0:
            print('Value change found!')
            dao.push_data(spreadsheet, workbook_name)

        else:
            print('No change found.')

    except Exception as e:
        print('Structure change found! (error thrown)')
        dao.push_data(spreadsheet, workbook_name)

spreadsheet = '1vVn2PuJybnMyO81SA4e1tVUGmPeSoRRd1LEbmU6jydk'
workbook = 'available_listings'
check_for_updates(spreadsheet, workbook)