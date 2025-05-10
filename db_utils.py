import pymysql
from sshtunnel import SSHTunnelForwarder

class DBClient:
    def __init__(self, ssh_host, ssh_user, ssh_pw,
                 db_host, db_port, db_user, db_pw, db_name, db_table,
                 local_bind_port=3307, ssh_port=22):
        
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

    def insert_game(self, gamedata, spieler=None):
        sql = f'INSERT INTO {self.table} ("SpielID", {"SpielerID" if spieler else "GaesteID"}, "Score", "Zeitbenoetigt", "Datum") VALUES (Null, %s, %s, %s, NOW())'
        data = (gamedata[0], gamedata[1], gamedata[2])

        with self.connection.cursor() as cursor:
            cursor.execute(sql, data)
        self.connection.commit()



