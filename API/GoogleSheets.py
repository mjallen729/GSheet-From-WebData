import gspread
from gspread_dataframe import set_with_dataframe
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

class DataObject:
    def __init__(self) -> None:
        self.cred = Credentials.from_service_account_file('./keys/service-acct.json',
                                                        scopes= scopes)
        self.gc = gspread.authorize(self.cred)
        self.gauth = GoogleAuth()
        self.drive = GoogleDrive(self.gauth)
    
    def push_data(self, spreadsheet_key, worksheet_name, csv_to_push= './exports/available_listings.csv'):
        workbook = self.gc.open_by_key(spreadsheet_key)
        sheet = workbook.worksheet(worksheet_name)

        df = pd.read_csv(csv_to_push)
        # df = df.drop(df.columns[0], axis=1)

        try:
            set_with_dataframe(worksheet= sheet, dataframe= df, include_index= False,
                            include_column_header= True, resize= True)
            
            sheet.columns_auto_resize(0, len(df.columns))
            sheet.resize(rows=sheet.row_count + 15)

        except Exception as e:
            print(f'Error setting and formatting: {e}')
        
    def pull_data(self, spreadsheet_key, worksheet_name) -> pd.DataFrame:
        workbook = self.gc.open_by_key(spreadsheet_key)
        sheet = workbook.worksheet(worksheet_name)

        return get_as_dataframe(sheet)

if __name__ == '__main__':
    test = DataObject()
    test.push_data('1vVn2PuJybnMyO81SA4e1tVUGmPeSoRRd1LEbmU6jydk', 'remote')