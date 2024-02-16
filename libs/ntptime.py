import utime

# Set your UTC offset here, this is UTC-4 'aka' East Coast U.S. Time
UTC_OFFSET = 28800
try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = "ntp1.aliyun.com"  # Changed from pool.ntp.org, better results in my opinion.
# The NTP socket timeout can be configured at runtime by doing: ntptime.timeout = 2
timeout = 4  # bumped up timeout just in case to ensure we get our NTP time.


def time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(timeout)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]

    EPOCH_YEAR = utime.gmtime(0)[0]
    if EPOCH_YEAR == 2000:
        # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 3155673600
    elif EPOCH_YEAR == 1970:
        # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 2208988800
    else:
        raise Exception("Unsupported epoch: {}".format(EPOCH_YEAR))

    return val - NTP_DELTA


# There's currently no timezone support in MicroPython, and the RTC is set in UTC time.

# Statement above if from the official Micropython code. I have slightly modified the
# setttime function below to adjust for my UTC offset which as stated at the top of this
# file is UTC -4 'aka' East Coast U.S time
def settime():
    t = time()
    import machine
    # Line below was edited from gmtime to localtime and added offset
    tm = utime.localtime(t + UTC_OFFSET)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    # Now you can call rtc.datetime() and you will get the correct date and time in terms
    # of your local time in 24hr format. For now intial testing looks good. This means you
    # are overriding the built-in frozen ntptime module requiring you to store this one
    # on your MCU. You can  decide if that is worthwhile or not.

    #                           ****IMPORTANT**** 
    # ONLY TESTED ON ESP32 S3 microcontroller. The ESP32 MCUs have very bad time 
    # accuracy and drift quickly so a call to ntptime.settime() needs to be called
    # on a regular basis to ensure accurate time. If time is "VERY" critical to your project
    # I would recommend a seperate hardware RTC module such as a DS3231 or something similar.
    # AGAIN THIS HAS BEEN MODIFIED AND TESTED FOR ESP32 S3 Microcontrollers. Your milage
    # may vary. You may edit, use and otherwise distribute this file so long as you follow
    # the conditions determined by Micropython.org themselves. No promises on how it will
    # function for you. That's why we tinker :)