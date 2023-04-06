import sqlite3
import pandas as pd


#Creating a sql connection to db data
# conn = sqlite3.connect('db/MedicalDrug.db')
# curr = conn.cursor()
#
# # Uploading excel file into the sqlllite db
# df = pd.read_csv('excelFile/drugData_p1.csv', index_col=[0])
# df.to_sql('drugData', con=conn, if_exists='replace')
#
# # Fetching Data
# f = curr.execute("SELECT * FROM drugData").fetchall()
# df = pd.read_sql("SELECT * FROM drugData", con=conn)
# print(df)

class GetData:

    def __init__(self):
        self.dbname = 'db/MedicalDrug.db'
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


if __name__ == "__main__":
    col = ['Disease', 'Drug_name', 'Generic_name', 'Brand_names', 'Drug_class','Rx_OTC', 'Pregnancy', 'CSA', 'Alcohol']
    obj = GetData()
    obj.createConnection()
    data = obj.pullData("SELECT * FROM  drugData where Drug_name = 'aspirin'")
    df = pd.DataFrame(data, columns=col)
    print(df.head(10))

    #print(obj.cur.execute("SELECT DISTINCT `Diagnostic Test Name` FROM dtest"))
