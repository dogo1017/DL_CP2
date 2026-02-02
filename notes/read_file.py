#DL 1st, read file 
import csv
try:
    with open("DL_CP2/notes/reading.txt", "r") as file:
        for line in file:
            print(f"Hello {line.strip()}")
except:
    print("That file can't be found")

else:
    print("Code ends")

try:
    with open("DL_CP2/notes/sample.csv", mode = "r") as csv_file:
        content = csv.reader(csv_file)
        headers = next(content)
        rows = []
        for line in content:
            rows.append({headers[0]: line[0], headers[1]: line[1]})
except:
    print("Can't find the CSV")
else:
    for line in rows:
        print(line)