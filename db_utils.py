import pymysql
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os

load_dotenv()

# SSH ENV_Variables
SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = int(os.getenv("SSH_PORT"))
SSH_USER = os.getenv("SSH_USER")
SSH_PW = os.getenv("SSH_PW")

# DB ENV_Variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_TABLE = os.getenv("MYSQL_TABLE")

class DBClient:
    def __init__(self, ssh_host=SSH_HOST, ssh_user=SSH_USER, ssh_pw=SSH_PW,
                 db_host=MYSQL_HOST, db_port=MYSQL_PORT, db_user=MYSQL_USER, db_pw=MYSQL_PASSWORD, db_name=MYSQL_DB, db_table=MYSQL_TABLE,
                 local_bind_port=3307, ssh_port=SSH_PORT):
        
        self.server = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_pw,
            remote_bind_address=(db_host, db_port),
            local_bind_address=('127.0.0.1', local_bind_port)
        )
        try:
            self.server.start()
        except Exception as e:
            print(f'Fehler bei der Verbindung: {e}')

        try:
            self.connection = pymysql.connect(
                host=db_host,
                port=self.server.local_bind_port,
                user=db_user,
                password=db_pw,
                database=db_name,
            )
        except pymysql.Error as er:
            print(f'Fehler bei DB Verbindung: {er}')

        self.table = db_table

    def insert_game(self, gamedata, spieler=True):
        id_spalte = "SpielerID" if spieler else "GaesteID"
        sql = f'INSERT INTO `{self.table}` (`SpielID`, `{id_spalte}`, `Score`, `Zeitbenoetigt`, `Datum`) VALUES (Null, %s, %s, %s, NOW())'
        data = gamedata

        with self.connection.cursor() as cursor:
            cursor.execute(sql, data)
        self.connection.commit()
        print(f'Datensatz erfolgreich eingefügt: {data}')

    def close(self):
        if self.connection:
            self.connection.close()
        if self.server:
            self.server.stop()


if __name__ == "__main__":
    client = DBClient()

    client.insert_game((1, 2342, 23.55))

    client.close()








