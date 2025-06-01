import threading

class SubPub:
    
    _subscribers = []
    
    @property
    def subscribers(self):
        return type(self)._subscribers
    
    @subscribers.setter
    def subscribers(self, val):
        type(self)._subscribers = val

    #------------------------------------------------
    _topic = []

    @property
    def topic(self):
        return type(self)._topic
    
    @topic.setter
    def topic(self, val):
        type(self)._topic = val

    @classmethod
    def addTopic(self, itemtopic):
        if not itemtopic in self._topic:
            self._topic.append(itemtopic)

    #-------------------------------------------------
    @classmethod
    def __init__(self):
        print("Constructor-Subscriber")
        pass

    @classmethod
    def subscribe(self, itemtopic:str, itemclass):
        print("subscribe()-Subscriber")
        self.addTopic(itemtopic)
        self._subscribers.append(itemtopic)
        self._subscribers.append(itemclass)
        itemclass.onSubscribe("Subscription successful")
    
    @classmethod
    def thread_function(self, itemtopic, itemmessage):
        print("Thread")
        indextopic = [index+1 for (index, item) in enumerate(self._subscribers) if item == itemtopic]
        for index in indextopic:
            self._subscribers[index].onNext(itemmessage)

    @classmethod
    def publish(self, itemtopic:str, itemmessage):
        print("publish")
        x = threading.Thread(target=self.thread_function, args=(itemtopic, itemmessage))
        x.start()

