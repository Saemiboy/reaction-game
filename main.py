from login import login
from game import main_game

def main():
    loginreturn = login()
    main_game(loginreturn[1], loginreturn[2] , loginreturn[0])

if __name__ == '__main__':
    main()