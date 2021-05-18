import matplotlib.pyplot as plt
import json
import glob
import os
from datetime import datetime
import dateutil.relativedelta

base_path = "./data/messages/inbox"
plt.figure(figsize=(25, 17))

all_msg = dict()
for frien in os.listdir(base_path):
    messages = dict()
    for message_file in glob.glob(f"{base_path}/{frien}/*.json"):
        with open(message_file, "r" ) as f:

            temp = json.loads( f.read() )
            if len(messages) == 0:
                messages.update(temp)
            else:
                messages["messages"] +=  temp["messages"]
    all_msg.update({frien: messages})


talked_much = dict()
YEARS_MAX = 1
for frien, messages in all_msg.items():
    if len(messages["participants"])>2:
        #print(f"{frien} is a group, skip")
        continue
    messages = messages["messages"]
    if len(messages) < 50:
        continue
    all_time = [mess["timestamp_ms"] for mess in messages]
    max_timestamp = max(all_time)
    min_timestamp = min(all_time)
    if (datetime.now() - datetime.fromtimestamp(int(max_timestamp)/1000)).days > int(YEARS_MAX*365): # x ans
        #print(f"{frien} last talk together is old af ({datetime.fromtimestamp(int(max_timestamp)/1000)})")
        continue
    total_messages = len(messages)
    #print(f"{frien} has {total_messages} messages, first at {datetime.fromtimestamp(int(min_timestamp)/1000)}")
    # x axis values
    talked_much.update({frien: total_messages})

    times = list()
    for ti in sorted(all_time, reverse=True):
        times.append(datetime.fromtimestamp(int(ti)/1000))

    x = list()
    # corresponding y axis values
    y = list()
    for r in range(int(12*YEARS_MAX),0,-1):
        mess_count = 0
        now = datetime.now()
        for date in times:
            if (now - (now - dateutil.relativedelta.relativedelta(months=r))).days < (now - date).days < (now - (now - dateutil.relativedelta.relativedelta(months=r+1))).days:
                mess_count += 1
        x.append(now - dateutil.relativedelta.relativedelta(months=r))
        y.append(mess_count)

    # plotting the points
    plt.plot(x, y, label = frien.split("_")[0])

print(f"Chatted the most with:")
for i, frien in enumerate(sorted(talked_much, key=talked_much.get, reverse=True)):
    if i > 10:
        break
    print(f"{frien} with {talked_much[frien]} messages")

# naming the y axis
plt.ylabel('messages')
plt.legend()
# giving a title to my graph
plt.title('frien :> ')

# function to show the plot
plt.savefig('frien.png')
