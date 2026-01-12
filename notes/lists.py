#DL 1st, lists notes

siblings = ["Bennett", "Rosalie", "Sarianne", "Brielle", "Sarianne"]

print(siblings[3])
siblings[-1] = "EGG"
print(siblings)

# tuple

fruit = ("apple", "orange", "peach", "Kiwi", "raspberry")

#set

colors = {"Orange", "Purple", "Green", "Blue", "Yellow", "Red"}

colors.add("Pink")
colors.remove("Purple")

for i in colors:
    if i == "Orange":
        print("fruit")
    print(i)
