import sys
from file_checker import checkFile
from blockchain import Blockchain

def main():
    if len(sys.argv) != 2:
        print("""
Invalid arguments given!
This program is to check if a given file is probable malware or not.

Usage: python3 main.py [file]
Try: python3 main.py malwares/Ransomware/Locky.exe
""")
        exit(1)

    filename = sys.argv[1]
    legitimate = checkFile(filename)

    blockchain = Blockchain()
    blockchain.load_blockchain()

    if legitimate:
        print(f"File {filename} seems legitimate!")
    else:
        print(f"File {filename} is probably a MALWARE!!!")
        blockchain.add_block(filename)
        print(f"File {filename} added to blockchain!")

    # Optional: Check if the blockchain is valid
    if blockchain.is_chain_valid():
        print("Blockchain is valid.")
    else:
        print("Blockchain is invalid!")

if __name__ == "__main__":
    main()
