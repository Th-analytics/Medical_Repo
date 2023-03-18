import sqlite3
import pandas as pd


# #Creating a sql connection to db data
# conn = sqlite3.connect('db/pathlab.db')
# curr = conn.cursor()
#
# # Uploading excel file into the sqlllite db
# df = pd.read_excel('excelFile/TBTest_Consolidated.xlsx', engine='openpyxl',index_col=[0])
# df.to_sql('dtest', con=conn, if_exists='replace')
#
# # Fetching Data
# f = curr.execute("SELECT * FROM dtest").fetchall()
# df = pd.read_sql("SELECT * FROM dtest", con=conn)
# print(df)

class GetData:

    def __init__(self):
        self.dbname = 'db/pathlab.db'
        self.con = None
        self.cur = None

    def createConnection(self):
        """
        To Stablish Db Connection

        :return: None
        """
        self.con = sqlite3.connect(self.dbname)
        self.cur = self.con.cursor()

    def pullData(self, query):
        """
        Method to Pull Data From sqllite3 db

        :param query:  sql query
        :param country: countryName
        :param state: State Name
        :param product: product Name

        :return: df
        """
        df = pd.read_sql(query, con=self.con)
        return df.values

#
# if __name__ == "__main__":
#     obj = GetData()
#     obj.createConnection()
#     print(obj.pullData("SELECT Distinct `Diagnostic Test Name` FROM dtest"))
#     print(obj.cur.execute("SELECT DISTINCT `Diagnostic Test Name` FROM dtest"))
