class Subject:
    def __init__(self, name):
        self.name = name
        self.topics = []


sciences = Subject("sciences")
sciences.topics.append("chemistry")
sciences.topics.append("physics")
sciences.topics.append("biology")


english = Subject("english")
english.topics.append("Grammer")
english.topics.append("Creative Writing")
english.topics.append("Poetry")

spanish = Subject("spanish")
spanish.topics.append("Oral")
spanish.topics.append("Writing")
spanish.topics.append("Listening")


print(f"Subject: {sciences.name}, Topics: {sciences.topics}")
print(f"Subject: {english.name}, Topics: {english.topics}")
print(f"Subject: {spanish.name}, Topics: {spanish.topics}")