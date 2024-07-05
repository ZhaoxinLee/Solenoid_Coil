import pigpio
import numpy as np

class PIDIO(object):
    def __init__(self):
        # Initialize connection to RPi GPIO
        self.pi = pigpio.pi()
        
    
    def output_voltage_pwm(self,pinPWM,pinDIR,Vout,Vsupply):
        """ Output a desired DC voltage by modifying the duty cycle
        of the PWM output and changing the level of the sign pin.
        """
        # The motor driver has two inputs: PWM and sign. The duty
        # cycle of the output matches the duty cycle of the input.
        # The sign of the output is based on the level of the sign
        # pin. High (1) results in positive output, and low (0)
        # results in negative output.
        range = self.pi.get_PWM_range(pinPWM)
        # Saturate requested voltage to supply voltage
        if abs(Vout/Vsupply) >= 1.0:
            dutyCycle = range
        else:
            dutyCycle = range*abs(Vout/Vsupply)
        self.pi.set_PWM_dutycycle(pinPWM, dutyCycle)
        if np.sign(Vout) >= 0:
            # Pull direction pin lo (current out of channel A)
            self.pi.write(pinDIR,0)
        else:
            # Set direction pin hi (current out of channel B)
            self.pi.write(pinDIR,1)
    
    def set_pin_to_write_mode(self,pin):
        """ Set a Pi GPIO pin to write mode. """
        self.pi.set_mode(pin, pigpio.OUTPUT)