import pytchat
import os

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

chat = pytchat.create(video_id="nSVceoK2CXA")
count = 0
author_list = []
clear()
while chat.is_alive():
    for c in chat.get().sync_items():
        # print(f"{c.datetime} [{c.author.name}]- {c.message}")
        # print(c.json())
        
        # file = open("list.txt", 'r')
        # prev_file_content = file.read()
        # file = open("list.txt", 'w')
        # file.write(prev_file_content + f"{count}. {c.author.name}\n")
        # file.close()
        
        if "!join" in c.message.lower() and c.author.name not in author_list and c.author.name and len(c.message) == 5:
            author_list.append(c.author.name)
            print("updating...")
            clear()
            for index, item in enumerate(author_list):
                print(f"{index+1}. {item}")

            # count += 1
            # file = open("list.txt", 'r')
            # prev_file_content = file.read()
            # file = open("list.txt", 'w', encoding="utf-8")
            # file.write(prev_file_content + f"{count}. {c.author.name}\n")
            # file.close()
        pass