from PyQt6.QtCore import QObject, pyqtSignal
from collections import defaultdict
import threading

class SubscriberV2(QObject):
    messageReceived = pyqtSignal(object)

    def __init__(self, callback):
        super().__init__()
        self.messageReceived.connect(callback)

    def onNext(self, message):
        self.messageReceived.emit(message)


class SubPubV2:
    def __init__(self):
        self._subscribers = defaultdict(list)
        self._lock = threading.Lock()
    
    def subscribe(self, topic:str, callback: callable):
        subscriber = SubscriberV2(callback)
        with self._lock:
            self._subscribers[topic].append(subscriber)
        print(f"Subscribed to topic: {topic}")
        return subscriber
    
    def unsubscribe(self, topic:str, subscriber:SubscriberV2):
        with self._lock:
            if subscriber in self._subscribers.get(topic, []):
                self._subscribers[topic].remove(subscriber)
                print(f"Unsubscribed from topic: {topic}")
            
            if not self._subscribers[topic]:
                del self._subscribers[topic]
    
    def publish(self, topic: str, message):
        
        def notify():
            with self._lock:
                subscribers = list(self._subscribers.get(topic, []))
            for sub in subscribers:
                sub.onNext(message)

        thread = threading.Thread(target=notify, daemon=True)
        thread.start()