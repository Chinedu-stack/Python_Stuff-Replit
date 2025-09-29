import csv

###🔹 Mini Project 2 (Medium): Football Scores Tracker ⚽
###Save match results into a CSV: team, goals.
###Ask the user for 3 matches.
###Then read the file and print the team with the most goals.

high = 0

team = input("team: ")
goals = int(input("Goals: "))
team1 = input("team: ")
goals1 = int(input("Goals: "))
team2 = input("team: ")
goals2 = int(input("Goals: "))

with open("football.csv", "w", newline="") as file:
    w = csv.writer(file)
    w.writerow(["team", "goals"])
    w.writerow([team, goals])
    w.writerow([team1, goals1])
    w.writerow([team2, goals2])


with open("football.csv", "r") as file:
    read = csv.DictReader(file)
    for row in read:
        if int(row["goals"]) > high:
            high = int(row["goals"])
            topteam = row["team"]
print(f"{topteam} has the most goals with {high} goals scored")
