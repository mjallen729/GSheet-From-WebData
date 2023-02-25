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
        self.cred = Credentials.from_service_account_file('./keys/credentials.json',
                                                        scopes= scopes)
        self.gc = gspread.authorize(self.cred)
        self.gauth = GoogleAuth()
        self.drive = GoogleDrive(self.gauth)
    
    def push_data(self, spreadsheet_key, worksheet_name, csv_to_push= './exports/available_listings.csv'):
        workbook = self.gc.open_by_key(spreadsheet_key)

        df = pd.read_csv(csv_to_push, index_col=False)
        num_missing = df.isnull().sum()

        try:
            sheet = workbook.worksheet(worksheet_name)

        except:
            # create the worksheet
            sheet = workbook.add_worksheet(worksheet_name, len(df), len(df.columns))

        for i in list(num_missing):
            if i > float(0):
                print('Found missing values in csv:')
                missing = {df.columns[i]:num_missing[i] for i in range(len(df.columns))}
                print(missing)
                proceed = input('\nDo you wish to prodeed? (y/n)')

                if proceed == 'y':
                    break
                else:
                    print('Operation canceled. [43]')
                    return

        try:
            set_with_dataframe(worksheet= sheet, dataframe= df, include_index= False,
                            include_column_header= True, resize= True)
            
            sheet.columns_auto_resize(0, len(df.columns))
            sheet.resize(rows=len(df) + 15)

        except Exception as e:
            print(f'Error setting and formatting: {e} [54]')
        
    def pull_data(self, spreadsheet_key, worksheet_name) -> pd.DataFrame:
        workbook = self.gc.open_by_key(spreadsheet_key)
        sheet = workbook.worksheet(worksheet_name)

        df = get_as_dataframe(sheet)
        df = df.iloc[:-14]
        return df

if __name__ == '__main__':
    test = DataObject()
    a = test.push_data('1vVn2PuJybnMyO81SA4e1tVUGmPeSoRRd1LEbmU6jydk', 'available_listings')
    print(a if a else '')