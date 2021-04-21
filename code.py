import board
import time
import socketpool
import adafruit_ntp     #Modified library
import rtc
import adafruit_datetime as datetime    #from adafruit circuitpython bundle
import adafruit_dotstar

#RGB LED
dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5, auto_write=True)

# === i2c bus Devices: ===
i2c = board.I2C() 

# (1) Capacitive touch:
import adafruit_mpr121
mpr121 = adafruit_mpr121.MPR121(i2c)

# (2) Quad Alphanumeric display:
import adafruit_ht16k33.segments
display = adafruit_ht16k33.segments.Seg14x4(i2c)

# === Connect to wifi: ===
import wifi
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets not found, please add secrets['ssid'] and secrets['password']")
    raise

while wifi.radio.ipv4_address == None:
    try:
        display.blink_rate=2
        display.print("WiFi")
        wifi.radio.connect(secrets['ssid'], secrets['password'])
    except Exception as e:
        display.blink_rate=0
        display.print("    ")
        print(e)
        display._scroll_marquee(str(e), 0.2)
        time.sleep(3)

display.blink_rate=0

print("ESP32-S2 Wifi Connection:")
n = wifi.radio.ap_info
print(" SSID: {}\n Signal: {}\n Channel: {}".format(n.ssid, n.rssi, n.channel))
print(" IP: {}\n Hostname: '{}'\n Gateway: {}".format(wifi.radio.ipv4_address,wifi.radio.hostname,wifi.radio.ipv4_gateway))

#Get an NTP socket pool
# !!!Must use modified adafruit ntp library!!!
# Increase the timeout if you rarely get successful NTP updates
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, socket_timeout=0.5)  

#Get a RealTimeClock instance to read between NTP updates:
rtclock = rtc.RTC()

# NTP settings:
ntp_interval = 20    #Seconds between ntp updates (minimised by next_sync in lib)
ntp_next_update = datetime.datetime(1,1,1)
ntp_last_update = ntp_next_update
ntp_retry = 5

while True:
    #Get the time from the RTC instance:
    utctimestamp = time.mktime(rtclock.datetime)
    now = datetime.datetime.fromtimestamp(utctimestamp)
    
    #Display the time on the Alphanumeric display:
    display.print("{:02}{:02}".format(now.hour, now.minute))
    #display.print("{:02}{:02}".format(now.minute,now.second))  #Good for debugging!

    if now > ntp_next_update:   #Time to get a new NTP update:
        try:
            rtclock.datetime = ntp.datetime
            ntp_next_update = now + datetime.timedelta(seconds=ntp_interval)
            ntp_last_update = now
            dotstar[0] = (0, 20, 0, 0.2)    #Green LED indicates successful NTP update
            print("Update time: {} (interval={})".format(ntp_next_update, ntp_interval))
        except Exception as e:   #Socket timeout, connection issues etc:
            print("Failed to get NTP update at {}, last update {} trying again in {} seconds...({})".format(now, ntp_last_update, ntp_retry, e))
            dotstar[0] = (255, 0, 0, 0.6) #Red LED indicates NTP update failure (display still runs from RTC)
            ntp_next_update = now + datetime.timedelta(seconds=ntp_retry)
