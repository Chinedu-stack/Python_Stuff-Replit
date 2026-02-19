class Subject:
    def __init__(self,name):
        self.name = name
        self._topics = []
        
    
    def add_topic(self, topic):
        topic = Topic(topic)
        self._topics.append(topic)
        
    def mark_done(self,topic_name):
        for topic in self._topics:
            if topic.name == topic_name:
                topic.done()
                break
    
    def show(self):
        print(f"""Subject: {self.name}""")
        for topic in self._topics:
            print(f"{topic.name}: {topic.status()}")



class Topic:
    def __init__(self,name):
        self.name = name
        self.__status = False

    def done(self):
        self.__status = True

    def status(self):
        if self.__status: return "done"
        else: return "incomplete"
        


math = Subject("math")
english = Subject("english")
geo = Subject("geo")

math.add_topic("algebra")
english.add_topic("poetry")
geo.add_topic("volcanoes")

math.mark_done("algebra")
geo.mark_done("volcanoes")



math.show()
english.show()
geo.show()