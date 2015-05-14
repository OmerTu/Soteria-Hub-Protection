__author__ = 'omerturgeman'

import threading
import InternalZBHandler


def analyze_packet(sniffed_packet):
    if InternalZBHandler.packet_source_is_hub(sniffed_packet) \
            and InternalZBHandler.packet_type_is_light_command(sniffed_packet):
        print "Found command packet"

while True:
    packet = InternalZBHandler.sniff_packet()
    t = threading.Thread(target=analyze_packet, args=(packet,))
    t.daemon = True
    t.start()