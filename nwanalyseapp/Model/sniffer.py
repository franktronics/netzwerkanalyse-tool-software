from Model.utils.functions import *
from Model.sockets import SocketInit
import threading

class Sniffer(threading.Thread):

    #Constuctor for Sniffer
    def __init__(self, subpub, PUBLISH_TOPIC_MODEL_DATA_SNIFFING):
        self._subpub = subpub
        self.PUBLISH_TOPIC_MODEL_DATA_SNIFFING = PUBLISH_TOPIC_MODEL_DATA_SNIFFING

        threading.Thread.__init__(self)
        self.daemon=True
        self._boolSniffingData:bool = False #sniffing variable (false: no sniffing, true: sniffing activated)
        self.thd_sniffer_lock = threading.Lock()
        self.thd_sniffer_cond = threading.Condition()
        
        
        self._os = self.detectOS()
        self._nics = []
        self._indexNic:bool = 0

        self.start()

    #detecting the OS
    def detectOS(self):
        os_detected = detectOS()
        print(f"Detected OS: {os_detected}")
        return os_detected

    #detecting available NICs
    def detectNic(self):
        nic_detected = detectNic()
        self._nics = nic_detected
        print(f"Detected NICs: {nic_detected}")
        return nic_detected


    #function for start sniffing data
    def changeSniffData(self, index_combobox) -> bool: 
        #mit LOCK-Objekt
        #mit Thread
        self.thd_sniffer_lock.acquire()
        try:
            self._boolSniffingData:bool = not self._boolSniffingData
            if self._boolSniffingData == False and self._socket != None:
                self._socket.close()
            elif self._boolSniffingData == True:
                self._socket = SocketInit()
                self._socket.configureSocket(self._os, self._nics[self._indexNic])

        finally:
                self.thd_sniffer_lock.release()

        if self.isSniffingData():
            with self.thd_sniffer_cond:
                self.thd_sniffer_cond.notify()
        
        self._indexNic = index_combobox
        print(self._nics[self._indexNic])

        return self.isSniffingData()
    

    #function for stop sniffing data
    def stopSniffData(self):
        if self.isSniffingData():
            
            self.thd_sniffer_lock.acquire()
            try:
                self._boolSniffingData:bool = False
            finally:
                self.thd_sniffer_lock.release()

        return self._boolSniffingData


    def isSniffingData(self) -> bool:
        boolSniffingData_temp = False

        self.thd_sniffer_lock.acquire()
        try:
            boolSniffingData_temp = self._boolSniffingData
        finally:
                self.thd_sniffer_lock.release()
        return boolSniffingData_temp
    

    #run-Method for the thread
    def run(self):
        while True:

            with self.thd_sniffer_cond:
                
                while not self.isSniffingData():
                    print("Ich bin raus")
                    self.thd_sniffer_cond.wait()
                
                print("GotU")
                self.thd_sniffer_lock.acquire()
                try:
                    rawdata,addr = self._socket.receive()
                    self._subpub.publish(self.PUBLISH_TOPIC_MODEL_DATA_SNIFFING, rawdata)
                except Exception as error:
                    print(str(error))
                finally:
                    self.thd_sniffer_lock.release()
            