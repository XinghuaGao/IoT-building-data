
import time
import math
from MCP3008 import MCP3008

class MQ:
    """
    Class for MQ series of gas sensors.
    """
    # Constants
    MQ_PIN = 0
    RL_VALUE = 5
    RO_CLEAN_AIR_FACTOR = 9.83
    CALIBARAION_SAMPLE_TIMES = 50
    CALIBRATION_SAMPLE_INTERVAL = 500
    READ_SAMPLE_INTERVAL = 50
    READ_SAMPLE_TIMES = 5
    GAS_LPG = 0
    GAS_CO = 1
    GAS_SMOKE = 2

    # Gas curves
    LPGCurve = [2.3, 0.21, -0.47]
    COCurve = [2.3, 0.72, -0.34]
    SmokeCurve = [2.3, 0.53, -0.44]

    def __init__(self, Ro=10, analogPin=0):
        """
        Initialize MQ sensor.

        Args:
        Ro (float): Sensor resistance in clean air.
        analogPin (int): Analog pin number.
        """
        self.Ro = Ro
        self.MQ_PIN = analogPin
        self.adc = MCP3008()
        print("Calibrating...")
        self.Ro = self.MQCalibration(self.MQ_PIN)
        print(f"Calibration is done...\nRo={self.Ro} kohm")

    def MQPercentage(self):
        """
        Calculate gas percentages.

        Returns:
        val (dict): Gas percentages.
        """
        val = {}
        read = self.MQRead(self.MQ_PIN)
        val["GAS_LPG"] = self.MQGetGasPercentage(read/self.Ro, self.GAS_LPG)
        val["CO"] = self.MQGetGasPercentage(read/self.Ro, self.GAS_CO)
        val["SMOKE"] = self.MQGetGasPercentage(read/self.Ro, self.GAS_SMOKE)
        return val

    def MQResistanceCalculation(self, raw_adc):
        """
        Calculate sensor resistance.

        Args:
        raw_adc (float): Raw ADC value.

        Returns:
        (float): Sensor resistance.
        """
        return float(self.RL_VALUE*(1023.0-raw_adc)/float(raw_adc))

    def MQCalibration(self, mq_pin):
        """
        Calibrate MQ sensor.

        Args:
        mq_pin (int): Analog pin number.

        Returns:
        val (float): Ro value of the sensor.
        """
        val = 0.0
        for _ in range(self.CALIBARAION_SAMPLE_TIMES):
            val += self.MQResistanceCalculation(self.adc.read(mq_pin))
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
        val = val/self.CALIBARAION_SAMPLE_TIMES
        val = val/self.RO_CLEAN_AIR_FACTOR
        return val

    def MQRead(self, mq_pin):
        """
        Read MQ sensor.

        Args:
        mq_pin (int): Analog pin number.

        Returns:
        rs (float): Rs value of the sensor.
        """
        rs = 0.0
        for _ in range(self.READ_SAMPLE_TIMES):
            rs += self.MQResistanceCalculation(self.adc.read(mq_pin))
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)
        rs = rs/self.READ_SAMPLE_TIMES
        return rs

    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        """
        Get gas percentage.

        Args:
        rs_ro_ratio (float): Rs/Ro ratio.
        gas_id (int): Gas ID.

        Returns:
        (float): Gas percentage.
        """
        if gas_id == self.GAS_LPG:
            return self.MQGetPercentage(rs_ro_ratio, self.LPGCurve)
        elif gas_id == self.GAS_CO:
            return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
        elif gas_id == self.GAS_SMOKE:
            return self.MQGetPercentage(rs_ro_ratio, self.SmokeCurve)
        return 0

    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        """
        Get percentage.

        Args:
        rs_ro_ratio (float): Rs/Ro ratio.
        pcurve (list): Gas curve parameters.

        Returns:
        (float): Gas percentage.
        """
        return (math.pow(10, ((math.log(rs_ro_ratio) - pcurve[1]) / pcurve[2] + pcurve[0])))
