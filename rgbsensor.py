
import smbus;
import time

TCS34725_ADDRESS        = 0x29
TCS34725_CMD_BIT        = 0x80

TCS34725_ID             = 0x44
TCS34725_REG_RGBCTIME   = 0x01
TCS34725_REG_ID         = 0x92
TCS34725_REG_CL         = 0x94      # Clear data low
TCS34725_REG_RL         = 0x96      # Red data low
TCS34725_REG_GL         = 0x98      # Green data low
TCS34725_REG_BL         = 0x9A      # Blue data low

TCS34725_REG_CTRL       = 0x8F      # Control register
TCS34725_AGAIN_x1       = 0x00
TCS34725_AGAIN_x4       = 0x01
TCS34725_AGAIN_x16      = 0x02
TCS34725_AGAIN_x60      = 0x03

RCS34725_REG_ATIME      = 0x81

TCS34725_REG_ENABLE     = 0x80      # Enable register
TCS34725_ENABLE_AIEN    = 0x10      # RBGC interrupt enable (use to control LED)
TCS34725_ENABLE_PON     = 0x01      # RBGC interrupt enable (use to control LED)
TCS34725_ENABLE_AEN     = 0x02      # RBGC interrupt enable (use to control LED)


TCS34725_CMD        = 0x80

class RGBSensor(object):
    """Provides interface to the Adafruit """

    def __init__(self):
        self._dev = smbus.SMBus(1);
        self._addr = TCS34725_ADDRESS

        id = self._dev.read_byte_data(self._addr, TCS34725_REG_ID)
        if id != TCS34725_ID:
            raise RuntimeError('Unexpected chip ID read')

        self.enable()

    def enable(self):
        enable = self._dev.read_byte_data(self._addr, TCS34725_REG_ENABLE)

        enable |= TCS34725_ENABLE_PON
        self._dev.write_byte_data(self._addr, TCS34725_REG_ENABLE, enable)
        time.sleep(0.01);
        enable |= TCS34725_ENABLE_AEN
        self._dev.write_byte_data(self._addr, TCS34725_REG_ENABLE, enable)
        time.sleep(0.01);

    def disable(self):
        enable = self._dev.read_byte_data(self._addr, TCS34725_REG_ENABLE)

        enable &= ~(TCS34725_ENABLE_PON | TCS43725_ENABLE_AEN)
        self._dev.write_byte_data(self._addr, TCS34725_REG_ENABLE, enable)
        time.sleep(0.01);

    def get_rgbc(self):
        r = self._dev.read_word_data(self._addr, TCS34725_REG_RL)
        g = self._dev.read_word_data(self._addr, TCS34725_REG_GL)
        b = self._dev.read_word_data(self._addr, TCS34725_REG_BL)
        c = self._dev.read_word_data(self._addr, TCS34725_REG_CL)

        return (r,g,b,c)


    def set_integration(self, tm):
        self._dev.write_byte_data(self._addr, RCS34725_REG_ATIME, tm & 0xff)

    def set_gain_x1(self):
        self._dev.write_byte_data(self._addr, TCS34725_REG_CTRL, TCS34725_AGAIN_x1);

    def set_gain_x4(self):
        self._dev.write_byte_data(self._addr, TCS34725_REG_CTRL, TCS34725_AGAIN_x4);

    def set_gain_x16(self):
        self._dev.write_byte_data(self._addr, TCS34725_REG_CTRL, TCS34725_AGAIN_x16);

    def set_gain_x60(self):
        self._dev.write_byte_data(self._addr, TCS34725_REG_CTRL, TCS34725_AGAIN_x60);
        
    def set_led(self, on):
        enable = self._dev.read_byte_data(self._addr, TCS34725_REG_ENABLE)

        # Clear interrupt bit to turn LED on (it's active low)
        if on:
            enable &= ~TCS34725_ENABLE_AIEN
        else:
            enable |= TCS34725_ENABLE_AIEN

        self._dev.write_byte_data(self._addr, TCS34725_REG_ENABLE, enable)

    def led_on(self):
        self.set_led(True)

    def led_off(self):
        self.set_led(False)

