class StudyItem:
    def __init__(self, name):
        self.name = name
        self._completed = False  # private-like attribute

    def mark_done(self):
        self._completed = True

    def get_status(self):
        if self._completed:
            return "Complete"
        else:
            return "Incomplete"
    


class Subject(StudyItem):
    def __init__(self, name):
        super().__init__(name)  # inherit name & _completed
        self.topics = []

    def add_topic(self, topic):
        self.topics.append(topic)

    def print_topics(self):
        for topic in self.topics:
            print(f"{topic.name} - {topic.get_status()}")


class Topic(StudyItem):
    def __init__(self, name):
        super().__init__(name)


class Flashcard(StudyItem):
    def __init__(self, name, content):
        super().__init__(name)
        self.content = content
    def printy(self):
        print(f"Flashcard: {self.name}\nContent: {self.content}")




NFS = Flashcard("Newton's First Law", "What comes up must come down" )
physics = Subject("physics")
forces = Topic("forces")
energy = Topic("energy")
physics.add_topic(forces)
physics.add_topic(energy)
energy.mark_done()
NFS.mark_done()
forces.mark_done()
print("-------------------------------")
print(f"{NFS.name}: {NFS.get_status()}")
print("----------------------------")
physics.print_topics()
print("--------------------------------")
NFS.printy()
print("---------------------------------")