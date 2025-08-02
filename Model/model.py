from Model.settings_view import Settings_View
from Model.utils import detectNic
from Model.analyser import NetworkAnalyserPort, NetworkAnalyser
from Model.analyser import DatabasePort

class Model:
    PUBLISH_TOPIC_WINDOW_CONFIG = "windowconfig"

    PUBLISH_TOPIC_STATUSSNIFFINGDATA = "statussniffingdata"
    PUBLISH_TOPIC_TERMINAL_NIC = "nicterminal"
    PUBLISH_TOPIC_ADAPTER_DATA_SNIFFING = "adapterdatasniffing"

    PUBLISH_TOPIC_RAWDATA_NIC = "rawdata_nic"
    PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA = "rawdata_sniffingdata"
    PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA = "rawdata_statussniffingdata"
    
    PUBLISH_TOPIC_ANALYZEDDATA_STATE = "analyzeddata_state"
    PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS = "analyzeddata_analysis"
    PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE = "analyzeddata_package"
    PUBLISH_TOPIC_ANALYZEDDATA_SHOW = "analyzeddata_show"
    PUBLISH_TOPIC_ANALYZEDDATA_STATS = "analyzeddata_stats"

    def __init__(self, subpub):
        
        self._settings_view = Settings_View()
        
        self._subpub = subpub
        self._nics = []
        self._analyser: NetworkAnalyserPort = NetworkAnalyser()
        self._storage: DatabasePort = self._analyser.database


    def initialize(self):
        self.viewAnalyzedInit()
        self.snifferDetectNic()
        self._storage.init_db()
        #self.get_all_analyses()

    def close(self):
        self._storage.close_db()


    def snifferDetectNic(self):
        # Detect available NICs
        if len(self._nics) == 0:
            pass
        else:
            self._nics.clear()
        
        self._nics = detectNic()
        self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_NIC, self._nics)



    #for index_combobox : integer
    def snifferChangeSniffData(self, index_combobox:int):
        # Sniffer: change Sniffer State
        if self._analyser.is_running():
            self.snifferStopSniffData()
        else:
            analysis_id, timestamp, nic = self._analyser.record(
                self._nics[index_combobox],
                lambda _: self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA, (analysis_id, timestamp, nic))
            )
            self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA, False if analysis_id is None else True)


    #for str_combobox : string
    def snifferChangeSniffData(self, str_combobox:str):
        # Sniffer: change Sniffer State
        if self._analyser.is_running():
            self.snifferStopSniffData()
        else:
            analysis_id, timestamp, nic = self._analyser.record(
                str_combobox,
                lambda _: self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA, (analysis_id, timestamp, nic))
            )
            self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA, False if analysis_id is None else True)


    def snifferStopSniffData(self):
        #Sniffer: Stop Sniffing
        self._analyser.stop_record()
        self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA, False)


    #for index_combobox : int
    def snifferStartSniffData(self, index_combobox:int):
        #Sniffer: Start Sniffing
        analysis_id, timestamp, nic = self._analyser.record(
                self._nics[index_combobox],
                lambda _: self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA, (analysis_id, timestamp, nic))
            )
        self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA, False if analysis_id is None else True)

    #for str_combobox : string
    def snifferStartSniffData(self, str_combobox:str):
        #Sniffer: Start Sniffing
        analysis_id, timestamp, nic = self._analyser.record(
                str_combobox,
                lambda _: self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_SNIFFINGDATA, (analysis_id, timestamp, nic))
            )
        self._subpub.publish(self.PUBLISH_TOPIC_RAWDATA_STATUSSNIFFINGDATA, False if analysis_id is None else True)
        
    def viewAnalyzedInit(self):
        temp = self._settings_view.initializeState()
        self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_STATE, temp)

    def viewAnalyzedNext(self):
        temp = self._settings_view.next()
        if temp == self._settings_view.STATEDATABASE:
            self.get_all_analyses()
        self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_STATE, temp)

    def viewAnalyzedStatistics(self):
        if self.retViewAnalyzedState() == self._settings_view.STATEDATABASE:
            temp = self._settings_view.show_statistics()
            self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_STATE, temp)

    def viewAnalyzedBack(self):
        temp = self._settings_view.back()
        if temp == self._settings_view.STATEDATABASE:
            self.get_all_analyses()
        self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_STATE, temp)

    def retViewAnalyzedState(self) -> int:
        return self._settings_view.retState()
    

    #get all analysis
    def get_all_analyses(self): # -> list[Tuple[str, str, str]] | None:
        temp = self._storage.get_all_analyses()
        self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_ANALYSIS, temp)
    
    #delete analysis
    def delete_analysis(self, analysis_id): # -> bool:
        self._storage.delete_analysis(analysis_id)

    #get packages from analysis
    def get_packets_by_analysis_id(self, analysis_id: int): # -> list[Tuple[str, str, str, str, str, str]] | None:
        temp = self._storage.get_packets_by_analysis_id(analysis_id)
        temp_stat = self._analyser.get_participants_map(temp)
        self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_PACKAGE, temp)
        self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_STATS, temp_stat)


    #analyze package
    def get_packet_dict(self, packet_id: int):
        packet_data = self._storage.get_packet_by_id(packet_id)
        raw_data = packet_data[4]
        temp = self._analyser.parse_one_packet(raw_data)
        self._subpub.publish(self.PUBLISH_TOPIC_ANALYZEDDATA_SHOW, temp)
