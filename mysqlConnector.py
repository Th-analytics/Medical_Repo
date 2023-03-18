import mysql.connector


class GetData:

    def __init__(self):

        self.con = None
        self.cur = None

    def createConnection(self):
        """
        To Stablish Db Connection

        :return: None
        """
        # Establishing a connection to the MySQL database
        self.con = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword",
            database="yourdatabase"
        )
        self.cur = self.con.cursor()
