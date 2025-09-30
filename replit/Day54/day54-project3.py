import csv, time, os

def add(x):
    with open("author.csv", "a", newline="") as file:
        w = csv.writer(file)
        w.writerow(x)

# Write header once
with open("author.csv", "w", newline="") as file:
    w = csv.writer(file)
    w.writerow(["Title", "Author", "Year"])

# Input loop
while True:
    title = input("Title: ").lower()
    if title == "stop":
        break
    author = input("Author: ")
    year = int(input("Year: "))
    info = [title, author, year]
    add(info)
    time.sleep(1)
    os.system("cls")

booklist = []

# Print books after 2000
with open("author.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if int(row["Year"]) > 2000:   # Capital Y!
            allowed = [row["Title"], row["Author"], row["Year"]]
            booklist.append(allowed)

print("Books written after 2000: ")
for row in booklist:
    print(f"Title: {row[0]}\nAuthor: {row[1]}\nYear: {row[2]}")
    print()
