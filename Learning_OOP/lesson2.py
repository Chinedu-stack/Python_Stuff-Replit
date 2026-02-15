# Classes from Lesson 1, now with methods

class Topic:
    def __init__(self, name):
        self.name = name
        self.done = False

    def mark_done(self):
        self.done = True
        print(f"Topic '{self.name}' marked as done!")

class Subject:
    def __init__(self, name):
        self.name = name
        self.topics = []

    def add_topic(self, topic):
        self.topics.append(topic)
        print(f"Added topic '{topic.name}' to subject '{self.name}'")

    def print_topics(self):
        print(f"Topics for {self.name}:")
        for t in self.topics:
            status = "✔️" if t.done else "❌"
            print(f" - {t.name} [{status}]")


english = Subject("english")
poetry = Topic("poetry")
prose = Topic("prose")
english.add_topic(poetry)
english.add_topic(prose)
poetry.mark_done()

print()
print()

spanish = Subject("spanish")
orals = Topic("orals")
writing = Topic("writing")
spanish.add_topic(orals)
spanish.add_topic(writing)
orals.mark_done()

english.print_topics()
print()
spanish.print_topics()

