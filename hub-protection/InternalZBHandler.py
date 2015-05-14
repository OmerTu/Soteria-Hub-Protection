__author__ = 'omerturgeman'


import logging
import sys

sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages')
log_killerbee = logging.getLogger('scapy.killerbee')

try:
    from scapy.all import *
except ImportError:
    print 'This Requires Scapy To Be Installed.'
    from sys import exit
    exit(-1)

from killerbee.scapy_extensions import *
del hexdump


class CommandType:
    TURN_OFF, TURN_ON = range(2)


#class InternalZBHandler:


DEFAULT_KB_CHANNEL = 11
#DEFAULT_KB_DEVICE = '10.10.10.2'
RZ_USB_VEND_ID      = 0x03EB
DEFAULT_KB_DEVICE = None


LEVEL_CONTROL_CLUSTER = 8
ON_OFF_CLUSTER = 6
command_packet_file = "command_packet_format"
LINK_KEY = '\xdf\x42\xb5\x95\x6a\x2b\xbd\x46\x18\x8d\x59\x0a\xdb\x04\xb6\x09'


def sniff_packet():
    packets_list = kbsniff(channel = DEFAULT_KB_CHANNEL, count = 1, iface = DEFAULT_KB_DEVICE, store = 1)
    return packets_list[0]


def packet_type_is_light_command(packet):

    # 802.15.4 frame_type is Data
    if packet.fields['fcf_frametype'] != 1:
        return False

    # ZigBee Network layer frame_type is Data
    if packet.getlayer(ZigbeeNWK).fields['frametype'] != 0:
        return False

    # Decrypt packet payload:
    decrypted_payload = decrypt_packet(packet)

    # App layer is command type
    if decrypted_payload.fields['frame_control'] != 4:
        return False

    # Cluster type is On\Off
    if decrypted_payload.fields['cluster'] != ON_OFF_CLUSTER:
        return False

    # ZCL frame type is cluster-specific-command
    if decrypted_payload.payload.fields['zcl_frametype'] != 1:
        return False

    # If passed all above tests:
    return True

def packet_source_is_hub(packet):
    # 802.15.4's source is HUB
    if not (packet.haslayer(Dot15d4Data) and packet.getlayer(Dot15d4Data).fields['src_addr'] == 0):
        return False

    # ZigBee Network layer's source is HUB
    if not (packet.haslayer(ZigbeeNWK) and packet.getlayer(ZigbeeNWK).fields['source'] == 0):
        return False

    return True


def get_command(packet):
    # Decrypt packet payload:
    decrypted_payload = decrypt_packet(packet)

    if decrypted_payload.payload.fields['command_identifier'] == CommandType.TURN_ON:
        return CommandType.TURN_ON
    elif decrypted_payload.payload.fields['command_identifier'] == CommandType.TURN_OFF:
        return CommandType.TURN_OFF


def decrypt_packet(packet):
    # Extracting the MIC from the packet payload:
    packet.mic = packet.payload.payload.payload.fields['data'][-6:-2]

    # Omitting the data by 6 (to get rid of the FCS + MIC):
    packet.payload.payload.payload.fields['data'] = packet.payload.payload.payload.fields['data'][:-6]

    return kbdecrypt(packet, key = LINK_KEY, verbose = 0)


# # Load command packet from file:
# encrypted_command_packet = dill.load(open(command_packet_file))
#
# is_a_command = True
#
# # Sniff packets to a list, print it to screen and extract data:
# print "Sniffing broadcast packets..."
# found_hub_link_status = False
# while not found_hub_link_status:
#     packetsList = kbsniff(channel = DEFAULT_KB_CHANNEL, count = 1, iface = DEFAULT_KB_DEVICE, store = 1)
#     sniffed_packet = packetsList[0]
#     print "Got packet"
#     if (sniffed_packet.fields['fcf_frametype'] == 1 and sniffed_packet.getlayer(ZigbeeNWK).fields['frametype'] == 0 and sniffed_packet.payload.fields['src_addr'] == 0):
#         print "frame type: Data AND ZigBee NWK frame type: Data"
#         found_hub_link_status = True
#         print "Found packet from hub with sequence number " + str(sniffed_packet.fields['seqnum'])
#
#
# # Omitting the data by 6 (to get rid of the FCS + MIC):
# encrypted_command_packet.payload.payload.payload.fields['data'] = encrypted_command_packet.payload.payload.payload.fields['data'][:-6]
# print "Payload is encrypted!"
# print "Decrypting message..."
# print "Encrypted: " + encrypted_command_packet.payload.payload.payload.fields['data'].encode('hex')
# decrypted_command_packet_payload = kbdecrypt(encrypted_command_packet, key = LINK_KEY, verbose = 0)
# PrintHelper.reaviling_string("Decrypted: ", decrypted_command_packet_payload.do_build().encode('hex'), 0.006)
# print ""
#
#
#
# if (decrypted_command_packet_payload.fields['frame_control'] == 4):
#     print "App layer is command type"
# else:
#     is_a_command = False
#
# if (decrypted_command_packet_payload.fields['cluster'] == ON_OFF_CLUSTER):
#     print "On\Off cluster"
# else:
#     is_a_command = False
#
# if (decrypted_command_packet_payload.payload.fields['zcl_frametype'] == 1):
#     print "Cluster specific command"
# else:
#     is_a_command = False
#
# if (decrypted_command_packet_payload.payload.fields['command_identifier'] == TURN_ON_COMMAND_CODE):
#     print "Command is turn on"
# elif (decrypted_command_packet_payload.payload.fields['command_identifier'] == TURN_OFF_COMMAND_CODE):
#     print "Command is turn off"
# else:
#     is_a_command = False
#
# if (is_a_command):
#     print "-----------------"
#     print "Command was sniffed!!"