import csv

with open("scores.csv") as file:
    reader = csv.DictReader(file)
    high_scores = []
    for row in reader:
        if row["score"] >= 90:   # ❌ PROBLEM
            high_scores.append(row)

# now save high scores to a new CSV
with open("high_scores.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "score"])
    writer.writerow(high_scores)   # ❌ PROBLEM

print("Hello World")
