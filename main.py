import pytchat
import os
from time import sleep

#GLOBAL CONTAINERS:
author_list = []
holds = []
alerts = []
is_queue_open = True
is_hidden = True
NEXT = ''
STREAMER = ''

#FUNCTIONS:
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
def Screen():
    clear()
    print(f"<<< STREAMER: {STREAMER} >>>\n")
    
    print("On Holds: (empty!)", end="") if not len(holds) else print("On Holds:", end=" ")
    for ind, hold in enumerate(holds):
        print(f"{ind+1}. {hold}", end=" | ")
    print()
    
    print("\nNext: (nobody!)\n") if not NEXT else print(f"\nNext: {NEXT}\n")
    
    if is_queue_open:
        print("Queue: (empty!)\n") if not len(author_list) else print(f"Queue: (Total --> {len(author_list)})\n")
    else: print("Queue: (closed!)\n")
    for index, item in enumerate(author_list):
        if is_hidden and index >= 11:
            break
        print(f"{index+1}. {item}")
        
    print("\n\n\nPosition Alerts:\n") if len(alerts) else print("\n\n\nPosition Alerts: (no alerts!)\n")
    for alert in alerts:
        print('-', alert)

#INIT
wrong_link = True
clear()
while wrong_link:      
    try:
        id = input("Enter the stream url: ").strip()
        STREAMER = input("Enter your exact streamer channel name: ").strip()
        chat = pytchat.create(video_id=id)
        wrong_link = False
    except:
        clear()
        print("connection failed!\nmaybe wrong link? try again?\n")

#CONNECTION ANIMATION:
clear()
print("connecting")
sleep(0.25)
clear()
print("connecting.")
sleep(0.25)
clear()
print("connecting..")
sleep(0.25)
clear()
print("connecting...")
sleep(1)

Screen()

#COMMANDS
while chat.is_alive():
    for c in chat.get().sync_items():
        # AUDIENCE COMMANDS
        # !join
        if c.message.lower() == '!join' and c.author.name != STREAMER:
            if is_queue_open:
                if c.author.name not in author_list:
                    author_list.append(c.author.name)
                else:
                    alerts.insert(0, f"{c.author.name} --> already in the queue!")
                
            Screen()
            
        # !leave
        if c.message.lower() == '!leave' and c.author.name != STREAMER:
            if c.author.name not in author_list:
                alerts.insert(0, f"{c.author.name} --> not in the queue!")
            else:
                author_list.remove(c.author.name)
                
            Screen()
            
        # !position
        if c.message.lower() == '!position' and c.author.name != STREAMER:
            if c.author.name not in author_list:
                alerts.insert(0, f"{c.author.name} --> not in the queue!")
            else:
                alerts.insert(0, f"{c.author.name} --> {author_list.index(c.author.name)+1}")
                
            Screen()
            
        
        # STREAM CONTROLLER
        # !next
        if c.message.lower() == "!next" and c.author.name == STREAMER:
            if len(author_list):
                NEXT = author_list.pop(0)
            else:
                alerts.insert(0, "EMPTY QUEUE!")
            
            Screen()
            
        # !hold
        if c.message.lower() == "!hold" and c.author.name == STREAMER:
            if NEXT:
                holds.append(NEXT)
                NEXT = ''
                if len(author_list):
                    NEXT = author_list.pop(0)
                else:
                    alerts.insert(0, "EMPTY QUEUE!")
            else:
                alerts.insert(0, "FIRST CALL NEXT TO HOLD SOMEONE!")
            
            Screen()
            
        # !release 
        if "!release" in c.message.lower() and c.author.name == STREAMER:
            try:
                release_candidate_pos = int(c.message.split(" ")[1])
                if len(holds) >= release_candidate_pos:
                    holds.pop(release_candidate_pos-1)
                else:
                    alerts.insert(0, f"{release_candidate_pos} --> NOT ON HOLD!")
            except:
                if not len(holds):
                    alerts.insert(0, "NOBODY'S ON HOLD!")
                else:
                    alerts.insert(0, "FAILED! --> format: !release position")
            
            Screen()
            
        # !clear
        if c.message.lower() == "!clear" and c.author.name == STREAMER:
            alerts = []
            
            Screen()
            
        # !close
        if c.message.lower() == "!close" and c.author.name == STREAMER:
            is_queue_open = False
            alerts.insert(0, "CLOSED THE QUEUE")
            
            Screen()
            
        # !open
        if c.message.lower() == "!open" and c.author.name == STREAMER:
            is_queue_open = True
            alerts.insert(0, "OPENED THE QUEUE")
            
            Screen()
            
        # !show
        if c.message.lower() == "!show" and c.author.name == STREAMER:
            is_hidden = False
            
            Screen()
            
        # !hide
        if c.message.lower() == "!hide" and c.author.name == STREAMER:
            is_hidden = True
            
            Screen()
            
        # !remove<pos>
        if "!remove" in c.message.lower() and c.author.name == STREAMER:
            try:
                ind = int(c.message.split(" ")[1])-1
                alerts.insert(0, f"REMOVED --> {author_list[ind]}")
                author_list.pop(ind)
            except:
                alerts.insert(0, "REMOVING FAILED! --> (format: !remove position)")
            
            Screen()
        
        pass