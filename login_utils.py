import tkinter as tk
from db_utils import DBClient

"""
Für das folgende Tkinter login wurde KI verwendet. 
"""
class TkinterLogin:
    def __init__(self):
        # Speichert das Ergebnis des Login-/Registrierungsdialogs
        self.result = None
        self.client = DBClient()

    def center_window(self, width, height):
        # Zentriert das Fenster auf dem Bildschirm
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_error(self, message):
        # Zeigt eine Fehlermeldung zentriert im Fenster an
        error_win = tk.Toplevel(self.root)
        error_win.title("Fehler")
        error_win.resizable(False, False)
        error_win.update_idletasks()
        # Fenstergröße
        width, height = 350, 120
        # Bildschirmgröße
        screen_width = error_win.winfo_screenwidth()
        screen_height = error_win.winfo_screenheight()
        # Position berechnen
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        error_win.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(error_win, text=message, fg="red").pack(padx=30, pady=15)
        tk.Button(error_win, text="OK", width=10, command=error_win.destroy).pack(pady=(0, 10))
        error_win.grab_set()
        error_win.transient(self.root)
        error_win.wait_window()

    def on_login(self):
        # Wird beim Klick auf "Anmelden" ausgeführt
        username = self.entry_username.get().strip()
        if not username:
            self.show_error("Bitte geben Sie einen Benutzernamen ein.")
            return
        self.root.destroy()
        self.ask_password(username)

    def ask_password(self, username):
        # Öffnet ein neues Fenster zur Passworteingabe
        self.root = tk.Tk()
        self.root.title("Passwort eingeben")
        self.center_window(700, 600)
        self.root.resizable(False, False)

        tk.Label(self.root, text="Passwort:").pack(pady=(20, 5))
        entry_password = tk.Entry(self.root, show="*")
        entry_password.pack()

        def on_confirm():
            # Speichert Benutzername und Passwort und schließt das Fenster
            password = entry_password.get()
            self.result = ((None, None, username), password)
            if not self.client.check_password(username, password):
                self.show_error("Passwort ist falsch.")
                return False
            self.show_error(f"Herzlich willkommen {username}")
            self.root.destroy()
            return True

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        btn_ok = tk.Button(btn_frame, text="OK", width=15, command=on_confirm)
        btn_ok.grid(row=0, column=0, padx=10)

        btn_cancel = tk.Button(btn_frame, text="Abbrechen", width=15, command=self.root.destroy)
        btn_cancel.grid(row=0, column=1, padx=10)

        self.root.mainloop()

    def on_guest(self):
        # Wird beim Klick auf "Als Gast teilnehmen" ausgeführt
        gastname = self.entry_username.get().strip()
        if not gastname:
            self.show_error("Bitte geben Sie einen Benutzernamen ein.")
            return
        if not self.client.check_username_uniqe(gastname):
            self.show_error("Benutzername existiert bereits.")
            return 
        self.result = (('Guest', None, gastname), None)
        self.client.add_guest(gastname)
        self.show_error(f"Herzlich Willkommen {gastname}")
        self.root.destroy()

    def on_register(self):
        # Wird beim Klick auf "Registrieren" ausgeführt
        self.root.destroy()
        self.show_register()

    def show_register(self):
        # Zeigt das Registrierungsfenster an
        self.root = tk.Tk()
        self.root.title("Registrieren")
        self.center_window(700, 600)
        self.root.resizable(False, False)

        tk.Label(self.root, text="Vorname:").pack(pady=(20, 5))
        entry_firstname = tk.Entry(self.root)
        entry_firstname.pack()

        tk.Label(self.root, text="Nachname:").pack(pady=(10, 5))
        entry_lastname = tk.Entry(self.root)
        entry_lastname.pack()

        tk.Label(self.root, text="Benutzername:").pack(pady=(10, 5))
        entry_username = tk.Entry(self.root)
        entry_username.pack()

        tk.Label(self.root, text="Passwort:").pack(pady=(10, 5))
        entry_password = tk.Entry(self.root, show="*")
        entry_password.pack()

        def on_register_confirm():
            # Speichert die eingegebenen Registrierungsdaten und schließt das Fenster
            firstname = entry_firstname.get().strip()
            lastname = entry_lastname.get().strip()
            username = entry_username.get().strip()
            password = entry_password.get()
            if not firstname or not lastname or not username or not password:
                self.show_error("Bitte füllen Sie alle Felder aus.")
                return
            if not self.client.check_username_uniqe(username):
                self.show_error("Benutzername existiert bereits")
                return 
            self.result = ((firstname, lastname, username), password)
            self.client.register_user(self.result)
            self.root.destroy()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        btn_register = tk.Button(btn_frame, text="Registrieren", width=15, command=on_register_confirm)
        btn_register.grid(row=0, column=0, padx=10)

        btn_cancel = tk.Button(btn_frame, text="Abbrechen", width=15, command=self.root.destroy)
        btn_cancel.grid(row=0, column=1, padx=10)

        self.root.mainloop()

    def show(self):
        # Zeigt das Login-Fenster an
        self.root = tk.Tk()
        self.root.title("Willkommen beim Spiellogin")
        self.center_window(700, 600)
        self.root.resizable(False, False)

        # Überschrift
        tk.Label(self.root, text="Willkommen beim Spiellogin", font=("Arial", 20, "bold")).pack(pady=(30, 20))

        # Benutzername
        tk.Label(self.root, text="Benutzername:").pack(pady=(10, 5))
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        # Button-Frame für Login und Gast nebeneinander
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=30)

        btn_login = tk.Button(btn_frame, text="Anmelden", width=18, height=2, command=self.on_login)
        btn_login.grid(row=0, column=0, padx=15)

        btn_guest = tk.Button(btn_frame, text="Als Gast teilnehmen", width=18, height=2, command=self.on_guest)
        btn_guest.grid(row=0, column=1, padx=15)

        # Registrieren Button zentriert darunter
        btn_register = tk.Button(self.root, text="Registrieren", width=40, height=2, command=self.on_register)
        btn_register.pack(pady=(10, 0))

        self.root.mainloop()
        # Gibt das Ergebnis zurück: ((Vorname, Nachname, Benutzername), Passwort)
        return self.result[0]
