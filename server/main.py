import pytchat
import os
from time import sleep

#GLOBAL CONTAINERS:
author_list = []
holds = []
alerts = []
is_queue_open = False
# is_hidden = True
NEXT = ''
cmd = ''
STREAMER = ''

#FUNCTIONS:
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
def Screen():
    clear()
    print(f"<<< ADMIN: {STREAMER} >>>\n")
    
    print("On Holds: (empty!)", end="") if not len(holds) else print("On Holds:", end=" ")
    for ind, hold in enumerate(holds):
        print(f"{ind+1}. {hold}", end=" | ")
    print()
    
    print("\nCurrent: (nobody!)") if not NEXT else print(f"\nCurrent: {NEXT}")
        
    print("\n\n\nAlerts:\n") if len(alerts) else print("\n\n\nAlerts: (no alerts!)\n")
    for alert in alerts:
        print('-', alert)
        
def write():
    file = open("queue.html", "w", encoding='utf-8')
    file.write("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Queue</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      .container {
        padding: 20px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        min-height: 100vh;
        height: 100%;
        width: 100%;
        gap: 10px;
        background-color: #4f7;
      }

      .container .title {
        font-size: 3rem;
        margin-bottom: 20px;
        color: #fff;
        text-shadow: 0 5px 5px rgba(0, 0, 0, 0.15);
      }

      .container li {
        text-align: center;
        word-wrap: break-word;
        width: 95%;
        max-width: 420px;
        padding: 12px 12px;
        list-style: none;
        font-size: 2rem;
        border-radius: 6px;
        background-color: #fff;
        color: #232323;
        cursor: pointer;
        box-shadow: 0 10px 10px rgba(0, 0, 0, 0.15);
        transition: all 0.05s ease-out;
      }

      .container li:hover {
        transform: translateY(-1px);
        box-shadow: 0 20px 10px rgba(0, 0, 0, 0.15);
      }
      
      .container li span{
        font-weight: bold;
      }
    </style>
  </head>
  <body>
    <ol class="container">
    """)
    
    file.write(f"""
      <h1 class="title">The Queue - {len(author_list)}</h1>
    """)
    
    if len(author_list):
        for index, author in enumerate(author_list):
            file.write(f"""
      <li><span>{index+1}.</span> {author}</li>""")
    
    file.write("""
    </ol>
  </body>
</html>
""")
    file.close()

#INIT
wrong_link = True
clear()
while wrong_link:      
    try:
        id = input("Enter the stream url: ").strip()
        STREAMER = input("Exact Admin Name: ")
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
write()

#COMMANDS
while chat.is_alive():
    for c in chat.get().sync_items():
    #test
        if c.author.name not in author_list:
            author_list.insert(0, c.author.name)
            write()
    #test
        
        # AUDIENCE COMMANDS
        # !join
        if c.message.lower() == '!join' and c.author.name != STREAMER:
            if is_queue_open:
                if c.author.name not in author_list:
                    author_list.append(c.author.name)
                    alerts.insert(0, f"{c.author.name} --> joined the queue!")
                    write()
                else:
                    alerts.insert(0, f"{c.author.name} --> already in the queue!")
                
            Screen()
            
        # !leave
        if c.message.lower() == '!leave' and c.author.name != STREAMER:
            if c.author.name not in author_list:
                alerts.insert(0, f"{c.author.name} --> not in the queue!")
            else:
                author_list.remove(c.author.name)
                alerts.insert(0, f"{c.author.name} --> left the queue!")
                write()
                
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
        if c.message.lower() == '!next' and c.author.name == STREAMER:
            if len(author_list):
                NEXT = author_list.pop(0)
                write()
            else:
                alerts.insert(0, "EMPTY QUEUE!")
            
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
        
        pass