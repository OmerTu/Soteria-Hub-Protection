This is KillerBee - Framework and Tools for Attacking ZigBee and IEEE 802.15.4
networks.

Copyright 2009, Joshua Wright <jwright@willhackforsushi.com>
Copyright 2010-14, Ryan Speers <ryan@riverloopsecurity.com>
                   Ricky Melgares <ricky@riverloopsecurity.com>
All Rights Reserved.

Distributed under a BSD license, see LICENSE for details.


REQUIREMENTS
================
KillerBee is developed and tested on Linux systems.  Windows support may be
added in the future.

We have striven to use a minimum number of software dependencies, however, it
is necessary to install the following Python modules before installation:

serial
usb
crypto  (for some functions)
pygtk   (for use of tools that have GUIs)
cairo   (for use of tools that have GUIs)

On Ubuntu systems, you can install the needed dependencies with the following
command line:

# apt-get install python-gtk2 python-cairo python-usb python-crypto python-serial python-dev libgcrypt-dev

The last two dependencies (python-dev and libgcrypt) are required for the Scapy
Extension Patch (thanks to Spencer McIntyre for the patch).

Also note that this is a fairly advanced and un-friendly attack platform.  This
is not Cain & Abel.  It is intended for developers and advanced analysts who are
attacking ZigBee and IEEE 802.15.4 networks.  I recommend you gain some
understanding of the ZigBee protocol (the book ZigBee Wireless Networks and
Transceivers by Shahin Farahani at http://bit.ly/2I5ppI is reasonable, though
still not great) and familiarity with the Python language before digging into
this framework.


INSTALLATION
================
KillerBee uses the standard Python 'setup.py' installation file.  Install
KillerBee with the following command:

# python setup.py install


DIRECTORIES
================
The directory structure for the KillerBee code is described as follows:

doc       - HTML documentation on the KillerBee library, courtesy of epydoc.
firmware  - Firmware for supported KillerBee hardware devices.
killerbee - Python library source.
sample    - Sample packet captures, referenced below.
scripts   - Shell scripts used in development.
tools     - ZigBee and IEEE 802.15.4 attack tools developed using this
            framework.

REQUIRED HARDWARE
================
The KillerBee framework is being expanded to support multiple devices.
Currently there is support for the Atmel RZ RAVEN USB Stick, the MoteIV Tmote
Sky, and the TelosB mote. Support for Freaklab's Freakduino with added hardware
and the Dartmouth arduino sketch as well as for the Zena Packet Analyzer board
are in development.

For the MoteIV Tmote Sky or TelosB mode:
This device can be loaded with firmware via USB. Attach the device, and then
within killerbee/firmware, run: ./goodfet.bsl --telosb -e -p gf-telosb-001.hex

For the Atmel RZ RAVEN USB Stick:
(http://www.atmel.com/dyn/products/tools_card.asp?tool_id=4396).  This hardware 
is convenient as the base firmware is open source with a freely-available IDE.
The KillerBee firmware for the RZ RAVEN included in the firmware/ directory is
a modified version of the stock firmware distributed by Atmel to include
attack functionality.

The RZ RAVEN USB Stick is available from common electronics resellers for
approximately $40/USD:
Mouser: http://bit.ly/vZ2pt
Digi-Key: http://bit.ly/3T8MaK

The stock firmware shipped with this hardware allows you to leverage the passive
functionality included in the KillerBee tools and framework (such as receiving
frames), but does not allow you to do packet injection, or to impersonate
devices on the network.

In order to get the full functionality included in KillerBee, the RZ RAVEN USB
Stick must be flashed with the custom firmware included in the firmware/ 
directory.  This process requires additional hardware and software:

  + Hardware: Atmel RZ Raven USB Stick
  + Hardware: Atmel JTAGICE mkII On-Chip Programmer
  + Software: AVR Studio for Windows (free)
  + Software: KillerBee Firmware for the RZUSBSTICK (free)
  + A Windows host for programming the RZ Raven USB Stick (one time operation)

The problematic component in this list of the JTAGICE mkII programmer, as this
device retails for $300.  While often available in EBay for much less (beware
imitators, however, as these knock-off programmers may not work properly on all
Atmel hardware), this device is required to flash the KillerBee firmware onto a
RZ RAVEN USB Stick using the included 10-pin header interface.

You can flash the RZ RAVEN USB Stick using the AVR Studio Software (Tools ->
Program AVR) and the supplied firmware with the JTAGICE mkII programmer.  The
firmware included in KillerBee should applied to the Flash memory of the RZ USB
Stick.  See http://bit.ly/3ttLTc for an additional example, or contact the
author for additional information.

If you are able to catch us at a conference, bring your RZ RAVEN USB Stick
and we'll happily flash it for you.


TOOLS
================
KillerBee includes several tools designed to attack ZigBee and IEEE 802.15.4
networks, built using the KillerBee framework.  Each tool has its own usage
instructions documented by running the tool with the "-h" argument, and
summarized below.


zbopenear    -  Assists in data capture where devices are operating on multiple 
                channels or fast-frequency-hopping. It assigns multiple 
                interfaces sequentially across all channels.
zbassocflood -  Repeatedly associate to the target PANID in an effort to cause
                the device to crash from too many connected stations.
zbconvert    -  Convert a packet capture from Libpcap to Daintree SNA format,
                or vice-versa.
zbdsniff     -  Captures ZigBee traffic, looking for NWK frames and over-the-air
                key provisioning.  When a key is found, zbdsniff prints the
                key to stdout.  The sample packet capture
                sample/zigbee-network-key-ota.dcf can be used to demonstrate
                this functionality.
zbdump       -  A tcpdump-like took to capture IEEE 802.15.4 frames to a libpcap
                or Daintree SNA packet capture file.  Does not display real-time
                stats like tcpdump when not writing to a file.
zbfind       -  A GTK GUI application for tracking the location of an IEEE
                802.15.4 transmitter by measuring RSSI.  Zbfind can be passive
                in discovery (only listen for packets) or it can be active by
                sending Beacon Request frames and recording the responses from
                ZigBee routers and coordinators.
                If you get a bunch of errors after starting this tool, make
                sure your DISPLAY variable is set properly.  If you know how
                to catch these errors to display a reasonable error message,
                please drop me a note.
zbgoodfind   -  Implements a key search function using an encrypted packet
                capture and memory dump from a legitimate ZigBee or IEEE
                802.15.4 device.  This tool accompanies Travis Goodspeed's
                GoodFET hardware attack tool, or other binary data that could
                contain encryption key information such as bus sniffing with
                legacy chips (such as the CC2420).  Zbgoodfind's search file
                must be in binary format (obj hexfile's are not supported). To
                convert from the hexfile format to a binary file, use the
                objcopy tool: objcopy -I ihex -O binary mem.hex mem.bin
zbid         -  Identifies available interfaces that can be used by KillerBee
                and associated tools.
zbreplay     -  Implements a replay attack, reading from a specified Daintree
                DCF or libpcap packet capture file, retransmitting the frames.
                ACK frames are not retransmitted.
zbstumbler   -  Active ZigBee and IEEE 802.15.4 network discovery tool.
                Zbstumbler sends beacon request frames out while channel
                hopping, recording and displaying summarized information about
                discovered devices.  Can also log results to a CSV file.
zbwardrive   -	Discovers available interfaces and uses one to inject beacon 
                requests and listen for respones across channels. Once a network
                is found on a channel, it assigns another device to continuously
                capture traffic on that channel to a PCAP file. Scapy must be 
                installed to run this.
zbscapy      -  Provides an interactive Scapy shell for interacting via a
                KillerBee interface. Scapy must be installed to run this.
zbwireshark  -  Similar to zbdump but exposes a named pipe for real-time 
                capture and viewing in Wireshark.

Additional tools, that are for special cases or are not stable, are stored in
    the Api-Do project repository: http://code.google.com/p/zigbee-security/

Additional tools are coming.  Stay tuned.


FRAMEWORK
==============
KillerBee is designed to simplify the process of sniffing packets from the air
interface or a supported packet capture file (libpcap or Daintree SNA), and for
injecting arbitrary packets.  Helper functions including IEEE 802.15.4, ZigBee
NWK and ZigBee APS packet decoders are available as well.

The KillerBee API is documented in epydoc format, with HTML documentation in 
the doc/ directory of this distribution.  If you have epydoc installed, you can
also generate a convenient PDF for printing, if desired, as shown:

$ cd killerbee
$ mkdir pdf
$ epydoc --pdf -o pdf killerbee/

The pdf/ directory will have a file called "api.pdf" which includes the
framework documentation.

To get started using the KillerBee framework, take a look at the included tools
(zbdump and zbreplay are good examples to get started) and the simple test
cases in the t/ directory.

Since KillerBee is a Python library, it integrates well with other Python
software as well.  For example, the Sulley library is a fuzzing framework
written in Python by Pedram Amini.  Using the Sulley mutation features and
KillerBee's packet injection features, it is staightforward to build a
mechanism for generating and transmitting malformed ZigBee data to a target.


QUESTIONS/COMMENTS/CONCERNS
==============
Please drop us a note: 
The original version was written by: jwright@willhackforsushi.com
The current version, fixes, etc are handled by: ryan@riverloopsecurity.com

THANKS
==============
A word of thanks to several folks who helped out with this project:

Travis Goodspeed
Mike Kershaw (dragorn)
Chris Wang (aikiba)
Nick DePetrillo
Ed Skoudis
Matt Carpenter
Sergey Bratus (research support at Dartmouth)
Jeff Spielberg

