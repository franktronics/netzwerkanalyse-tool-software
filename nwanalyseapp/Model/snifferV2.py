from Model.utils.functions import *
from Model.sockets import SocketInit
import threading
import select

class SnifferV2(threading.Thread):

    #Constuctor for Sniffer
    def __init__(self, subpub, PUBLISH_TOPIC_MODEL_DATA_SNIFFING):
        self._subpub = subpub
        self.PUBLISH_TOPIC_MODEL_DATA_SNIFFING = PUBLISH_TOPIC_MODEL_DATA_SNIFFING

        self._socket = SocketInit()
        self._thd_running = False
        self._thd = None
        
        
        self._os = self.detectOS()
        self._nics = []
        self._indexNic:bool = 0


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
        
        if not self._thd_running:
            self.startSniffData()
        else:
            self.stopSniffData()

        return self._thd_running
    
    
    #start sniffing data
    def startSniffData(self):
        if self._thd_running:
            print("Sniffing already executing")
            return
        else:
            
            self._thd_running = True
            self._thd = threading.Thread(target=self._captureData, daemon=True)
            self._thd.start()
            print("Sniffing started")


    #start sniffing data
    def stopSniffData(self):
        if not self._thd_running:
            print("Sniffing already stopped")
            return
        else:
            
            self._thd_running = False
            if self._thd:
                self._thd.join()
                print("Sniffing stopped")
    

    def _captureData(self):
        try:
            self._socket.configureSocket(self._os, self._nics[self._indexNic])
            print("Socket configured", self._socket)

            while self._thd_running:
                readable, writable, exceptional = select.select([self._socket], [], [], 0.1)
                if readable:
                    print("Data readable")
                    rawdata = self._socket.receive()
                    retData = self.rawHexData(rawdata)
                    self._subpub.publish(self.PUBLISH_TOPIC_MODEL_DATA_SNIFFING, retData)

        except Exception as error:
            print(f"Error during capture: {error}")

        finally:
            if self._socket:
                self._socket.close()



    def rawHexData(self, rawdata:bytes, max_len:int = 64) -> str:
        rawdata = rawdata[0]
        retData = rawdata[:max_len]
        hex_string = ' '.join(f'{b:02X}' for b in retData)
        if len(rawdata) > max_len:
            hex_string + ' ...'
        return hex_string