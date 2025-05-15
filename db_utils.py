import pymysql
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os
import bcrypt

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
        print(f'Datensatz erfolgreich eingefügt: {data}, sql: {sql}')

    def close(self):
        if self.connection:
            self.connection.close()
        if self.server:
            self.server.stop()
        print('Server Verbindung gestoppt.')

    def fetch_highscore(self):
        sql1 = f"SELECT sp.Score, sp.Zeitbenoetigt, COALESCE(s.Benutzername, g.Benutzername) AS Benutzername, sp.Datum FROM {self.table} sp LEFT JOIN Spieler s ON sp.SpielerID = s.SpielerID LEFT JOIN Gaeste g ON sp.GaesteID = g.GaesteID ORDER BY sp.Score ASC, sp.Zeitbenoetigt ASC LIMIT 10"
        
        with self.connection.cursor() as cursor:
            cursor.execute(sql1)
            highscore = cursor.fetchall()

        converted_highscore = [(a, float(b), c, str(d)) for a, b, c, d in highscore]
        
        print(sql1)
        return converted_highscore
    
    def register_user(self, userdata):
        pw: str = userdata[1]
        pw_hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        data = (userdata[0][0], userdata[0][1], userdata[0][2], pw_hashed)
        table = "Spieler"
        sql = f"INSERT INTO `{table}`(`SpielerID`, `Vorname`, `Name`, `Benutzername`, `Passwort`, `Erstellungsdatum`) VALUES (Null, %s, %s, %s, %s, NOW())"

        with self.connection.cursor() as cursor:
            cursor.execute(sql, data)
        self.connection.commit()
        print(f'Neuer Spieler erfolgreich registriert. Spieler: {data} \nsql: {sql}')

    def check_password(self, userID, pw: str):
        table = 'Spieler'
        encoded_pw = pw.encode()
        sql = f'SELECT Passwort FROM {table} WHERE SpielerID = {userID}'
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            hashed_pw = cursor.fetchone()[0].encode()
            if bcrypt.checkpw(encoded_pw, hashed_pw):
                return True
            else:
                return False





# Testklausel
if __name__ == "__main__":
    client = DBClient()
    client.fetch_highscore()
    # client.register_user((('Aneglina', 'Meile', 'Sanguel'), 'dinimamiischgay'))
    print(client.check_password(2, 'dinimamiischgay'))
    client.close()








