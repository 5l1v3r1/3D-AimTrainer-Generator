""" IMPORTS """
# pip install rich
# pip install colorama
import json, threading, string, colorama
from os import system
from random import choice
from requests import get, post
from time import strftime, gmtime, time, sleep
from rich.table import Table
from rich.console import Console
colorama.init()

class GenInfo:
    """ Customizable Variables """
    emailen = 8 # Length of email address (ex. 'akWEOzRr' @gmail.com)
    userlen = 8 # Length of account username
    passlen = 8 # Length of account password
    email_provider = "codeuk.is.cool" # Email provider (ex. gmail.com)

class C:
    """ Program Colors """
    r  = colorama.Fore.RED    # red
    g  = colorama.Fore.GREEN  # green
    y  = colorama.Fore.YELLOW # yellow
    re = colorama.Fore.RESET  # reset

class Register:
    """ 3D Aim Trainer Account Generator """
    def __init__(self):
        self.Clear()
        self.api = "https://back-office.3daimtrainer.com/api/"
        self.headers = {"content-type": "application/json"}
        self.payload = {}
        self.count = 0
        self.generated = 0
        self.startTime = time()
        self.emails = []
        self.email  = None
        self.password  = None
        self.username  = None
        self.passwords = []
        self.usernames = []

    def Clear(self):
        system('cls')
        print(f"""{C.r}
   ▄▄▄·  ▄▄·  ▄▄·       ▄• ▄▌ ▐ ▄ ▄▄▄▄▄     ▄▄ • ▄▄▄ . ▐ ▄ ▄▄▄ .▄▄▄   ▄▄▄· ▄▄▄▄▄      ▄▄▄  
  ▐█ ▀█ ▐█ ▌▪▐█ ▌▪▪     █▪██▌•█▌▐█•██      ▐█ ▀ ▪▀▄.▀·•█▌▐█▀▄.▀·▀▄ █·▐█ ▀█ •██  ▪     ▀▄ █·
  ▄█▀▀█ ██ ▄▄██ ▄▄ ▄█▀▄ █▌▐█▌▐█▐▐▌ ▐█.▪    ▄█ ▀█▄▐▀▀▪▄▐█▐▐▌▐▀▀▪▄▐▀▀▄ ▄█▀▀█  ▐█.▪ ▄█▀▄ ▐▀▀▄ 
  ▐█ ▪▐▌▐███▌▐███▌▐█▌.▐▌▐█▄█▌██▐█▌ ▐█▌·    ▐█▄▪▐█▐█▄▄▌██▐█▌▐█▄▄▌▐█•█▌▐█ ▪▐▌ ▐█▌·▐█▌.▐▌▐█•█▌
   ▀  ▀ ·▀▀▀ ·▀▀▀  ▀█▄▀▪ ▀▀▀ ▀▀ █▪ ▀▀▀     ·▀▀▀▀  ▀▀▀ ▀▀ █▪ ▀▀▀ .▀  ▀ ▀  ▀  ▀▀▀  ▀█▄▀▪.▀  ▀      

                            {C.y}github.com/codeuk ~ doop#4247{C.re}

>> Accounts will be written to accounts.txt! (email - username - password)
""")

    def RandomValues(self):
        """ Generates random values for the account user, pass & email """
        info = GenInfo()
        self.username = "doop" + ''.join(choice(string.ascii_letters) for i in range(info.userlen))
        self.password = "doop" + ''.join(choice(string.ascii_letters) for i in range(info.passlen))
        self.email = "doop" + ''.join(choice(string.ascii_letters) for i in range(info.emailen)) + f"@{info.email_provider}"

    def ConsoleTitle(self, checking=False):
        """ Set account generation progress to console title (threaded) """
        while self.generated == 0:
            sleep(0.2)
        while self.generated < self.count:
            time_remaining = strftime('%H:%M:%S', gmtime((time() - self.startTime) / self.generated * (self.count - self.generated)))
            system(
                f'title Total Accounts: {self.generated}/{self.count} '
                f'({round(((self.generated / self.count) * 100), 3)}%) ^| Active Threads: '
                f'{threading.active_count()} ^| Time Remaining: {time_remaining}'
            )


    def LogRegister(self, rcode, num):
        """ Logs if account is registered and writes account information to file """
        if rcode == 201:
            self.generated += 1
            print(f"[{C.g}+{C.re}] {self.username}:{self.password} - #{C.g}{num}{C.re}")
            try:
                with open("accounts.txt", "a") as file:
                    file.write(f"{self.email} - {self.username} - {self.password}\n")
                    file.close()
            except:
                print(f"[{C.r}x{C.re}] Couldn't open accounts.txt! (try closing any other instances)")
                self.Start()
        else:
            print(f"[{C.r}x{C.re}] Couldnt Register: {self.username} (Code: {rcode})")

    def RegisterAccount(self):
        """ Register 3daimtrainer.com account with random account info (threaded) """
        self.Clear()
        while True:
            for i in range(self.count):
                self.RandomValues()
                self.payload = {
                    "beta": True,
                    "newsletter": False,
                    "email": self.email,
                    "password": self.password,
                    "username": self.username
                }   
                r = post(self.api+"register/", data=json.dumps(self.payload), headers=self.headers)
                self.LogRegister(r.status_code, i+1)

            print(f"\n[{C.g}+{C.re}] {self.count} Accounts Generated!")
            break


    def AccountsTable(self):
        """ Add account emails, usernames & passwords to rich table """
        accounts = Table(title="3dAimTrainer.com Accounts")

        accounts.add_column("ID", justify="center", style="yellow", no_wrap=True)
        accounts.add_column("Email", justify="center", style="cyan", no_wrap=True)
        accounts.add_column("Username", justify="center", style="magenta")
        accounts.add_column("Password", justify="center", style="green")

        for i in range(len(self.usernames)):
            email, username, password = self.emails[i], self.usernames[i], self.passwords[i]
            accounts.add_row(str(i+1), email, username, password)
        accounts.add_row("ID", "EMAIL", "USERNAME", "PASSWORD")

        c = Console()
        c.print(accounts, justify="left")
        print(f"\n[{C.g}*{C.re}] Valid Accounts -> {len(self.usernames)}")

    def GetAccounts(self):
        """ Format all accounts in accounts.txt and add to lists """
        self.Clear()
        print(f"[{C.g}*{C.re}] Checking Accounts...\n")
        with open("accounts.txt", "r") as file:
            accounts = file.readlines()
            for account in accounts:
                if len(account) != 41:
                    i = accounts.index(account)
                    del accounts[i]
                else:
                    email, username, password = account.split(' - ')
                    self.emails.append(email)
                    self.usernames.append(username)
                    self.passwords.append(password)
            file.close()
        print(f"[{C.g}*{C.re}] Checked Accounts!")
        input("\n[\\] Press any key to see the account table...")
        self.Clear()


    def Menu(self) -> str:
        """ Get and return menu selection """
        self.Clear()
        print(f"""   
        [{C.g}1{C.re}] Account Generator
        [{C.g}2{C.re}] List Accounts
        """)
        option = input("> Option -> ")
        return option

    def Start(self):
        """ Thread option selected from Menu() """
        choice = self.Menu()
        if choice == "1":
            self.count = int(input("\n> Accounts to generate -> "))
            bot = threading.Thread(target=self.RegisterAccount)
            title = threading.Thread(target=self.ConsoleTitle)
            title.start()
            bot.start()
        elif choice == "2":
            self.GetAccounts()
            self.AccountsTable()
        else:
            print("\nInvalid Choice!")
            sleep(2)
            self.Start()

Bot = Register()
Bot.Start()
