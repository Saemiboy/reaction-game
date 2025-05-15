from login_utils import TkinterLogin

def login():
    newlogin = TkinterLogin()
    answer = newlogin.show()

    if answer[0] == 'Guest':
        userid = newlogin.client.get_GaesteID(answer[2])
        spieler = False
    else:
        userid = newlogin.client.get_SpielerID(answer[2])
        spieler = True

    newlogin.client.close()
    return (spieler, userid, answer[2])


    