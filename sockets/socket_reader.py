from sockets import SocketInit
import queue
import threading
import time
from db import PacketDatabase


class SocketReader:
    def __init__(self, socket_obj: SocketInit, reader):
        self.socket_obj = socket_obj
        self.reader = reader
        self.stop_event = threading.Event()
        self.packet_queue = queue.Queue(maxsize=1000)
        self.reader_thread = threading.Thread(target=self.packet_reader, daemon=True)
        self.parser_thread = threading.Thread(target=self.packet_parser, daemon=True)

    def packet_reader(self):
        while not self.stop_event.is_set():
            try:
                raw_data, addr = self.socket_obj.receive()
                if not self.packet_queue.full():
                    self.packet_queue.put(raw_data)
            except Exception as e:
                print(f"Error reading packet: {e}")
                break

    def packet_parser(self):
        packet_database = PacketDatabase()
        while not self.stop_event.is_set():
            try:
                if not self.packet_queue.empty():
                    raw_data = self.packet_queue.get()
                    data = self.reader(raw_data)
                    packet_database.insert_packet(parsed_data=data, raw_data=raw_data)
                    self.packet_queue.task_done()
            except Exception as e:
                print(f"Error parsing packet: {e}")
                break

    def run(self):
        db = PacketDatabase()
        db.initialize_database()
        db.close()

        self.reader_thread.start()
        self.parser_thread.start()

        time.sleep(10)
        self.stop_event.set()
        self.packet_queue.join()
        self.reader_thread.join()
        self.parser_thread.join()