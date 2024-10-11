import smbus2  
import random  
import Adafruit_BMP.BMP085 as BMP085
from mpu6050 import MPU6050
from Adafruit_ADS1x15 import ADS1x15

bus = smbus2.SMBus(1) 
bmp = BMP085.BMP085()  
mpu = MPU6050(0x68)  
ads = ADS1x15()  

def get_temperature():
    try:
        temperature = bmp.read_temperature()
        return round(temperature, 2)
    except Exception as e:
        return "Erro ao ler temperatura: " + str(e)

def get_acceleration():
    try:
        accel_data = mpu.get_accel_data()
        return {
            'x': round(accel_data['x'], 2),
            'y': round(accel_data['y'], 2),
            'z': round(accel_data['z'], 2)
        }
    except Exception as e:
        return "Erro ao ler aceleração: " + str(e)

def get_voltage():
    try:
        raw_value = ads.read_adc(0, gain=1) 
        voltage = raw_value * (4.096 / 32767.0)  
        return round(voltage, 2)
    except Exception as e:
        return "Erro ao ler voltagem: " + str(e)

def get_current():
    try:
        return round(random.uniform(0.5, 2.0), 2)  
    except Exception as e:
        return "Erro ao ler corrente: " + str(e)

if __name__ == "__main__":
    print("Leitura dos sensores:")
    print(f"Temperatura: {get_temperature()} °C")
    print(f"Aceleração: {get_acceleration()}")
    print(f"Voltagem: {get_voltage()} V")
    print(f"Corrente: {get_current()} A")
