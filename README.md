# FeatherS2 NTP Clock

![feather s2 ntp clock](https://github.com/mattura/feathers2-ntp-clock/blob/main/doc/powered.jpg)

## Hardware

1. Feather S2 [Pimoroni](https://shop.pimoroni.com/products/feathers2-esp32-s2) | [Adafruit](https://www.adafruit.com/product/4769)
2. Quad-alphanmeric display [Pimoroni](https://shop.pimoroni.com/products/adafruit-0-54-quad-alphanumeric-featherwing-display) | [Adafruit](https://www.adafruit.com/product/2157)
3. [Optional] Capacitive touch breakout (STEMMA/QT) [Pimoroni](https://shop.pimoroni.com/products/adafruit-mpr121-12-key-capacitive-touch-sensor-gator-breakout-stemma-qt-qwiic) | [Adafruit](https://www.adafruit.com/product/4830)
4. STEMMA cables [Pimoroni 1](https://shop.pimoroni.com/products/jst-sh-cable-qwiic-stemma-qt-compatible?variant=31910609846355) [Pimoroni 2](https://shop.pimoroni.com/products/jst-sh-cable-qwiic-stemma-qt-compatible?variant=31910609813587) | [Adafruit 1](https://www.adafruit.com/product/4210) [Adafruit 2](https://www.adafruit.com/product/4209)
5. [Optional] LiPo Battery

## Requirements

Libraries from Adafruit ([CircuitPython bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle)):

1. adafruit_datetime
2. adafruit_ht16k33 (For the Quad Alpha)
3. adafruit_mpr121 (For the Capacitive touch)

Modified Adafruit Library from this repo:

4. [adafruit_ntp modified library](https://github.com/mattura/feathers2-ntp-clock/blob/main/lib/adafruit_ntp.py)

## Installation

1. Create a `secrets.py` file as follows:
```python
secrets = {
  "ssid": "YOUR_WIFI_SSID",
  "password": "YOUR_WIFI_PASSWORD"
}
```
2. Copy the `code.py` and your `secrets.py` to the root of your feather s2
3. Copy the Adafruit libraries and the modified adafruit_ntp library to your `/lib` directory
4. Run your clock!

