#DL 1st, writing files 

"""
with open("DL_CP2/notes/reading.txt", 'r+') as file:
    content = file.read()
    content += "\nI wrote on my file"
    file.write(content)

print("code end")

with open("DL_CP2/notes/reading.txt", 'a') as file:
    file.write("\nThis is more on my file!")

print("code end")
"""

import csv

with open("DL_CP2/notes/sample.csv", 'r+', newline='') as csvfile:
    fieldnames = ['username', 'color']
    reader = csv.reader(csvfile)
    for line in reader:
        print(line)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    writer.writerow({'username': 'aUser', 'color': 'pink'})
    writer.writerow({'username': 'basicPerson', 'color': 'red'})
    writer.writerow({'username': 'anotherUser', 'color': 'green'})
    writer.writerow({'username': 'thirdUser', 'color': 'blue'})

print("Code is done")