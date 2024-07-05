
class FieldManager(object):
    def __init__(self, dac):
        # Output PWM frequency
        self.pwmFreq = 500 # Hz
        # Pin numbers for the pwm and direction outputs
        self.pinXpwm = 17
        self.pinXdir = 27
        self.pinYpwm = 23
        self.pinYdir = 24
        self.pinZpwm = 25
        self.pinZdir = 8
        # Object for controlling RPi GPIO using gpiozero
        self.dac = dac
        # Set up GPIO for coil control
        self.dac.pi.set_PWM_frequency(self.pinXpwm, self.pwmFreq)
        self.dac.pi.set_PWM_frequency(self.pinYpwm, self.pwmFreq)
        self.dac.pi.set_PWM_frequency(self.pinYpwm, self.pwmFreq)
        self.dac.set_pin_to_write_mode(self.pinXdir)
        self.dac.set_pin_to_write_mode(self.pinYdir)
        self.dac.set_pin_to_write_mode(self.pinZdir)
        # Coil analog output conversion factors determined from coil calibration.
        # (NOT VALID ANYMORE SINCE WE ARE USING POLYNOMIAL FITTING CURVE)
        self.aoFactorX = 0.746 #[mT/V]
        self.aoFactorY = 1.190 #[mT/V]
        self.aoFactorZ = 2.038 #[mT/V]
        # Coil analog conversion factors determined from coil
        # calibration
        self.aiFactorX = 0.767 #[mT/A]
        self.aiFactorY = 0.755 #[mT/A]
        self.aiFactorZ = 0.720 #[mT/A]
        # Coil cutoff frequencies determined from coil calibration
        self.freqCutoffX = 13.0 #[Hz]
        self.freqCutoffY = 17.9 #[Hz]
        self.freqCutoffZ = 28.7 #[Hz]
        # Power supply voltage
        self.VsupplyX = 24.16 #[V]
        self.VsupplyY = 24.14 #[V]
        self.VsupplyZ = 24.12 #[V]
        # Initial requested field values
        self.bxSetpoint = 0 #[mT]
        self.bySetpoint = 0 #[mT]
        self.bzSetpoint = 0 #[mT]
        # Initial field values estimated from measured coil currents
        self.bxEstimate = 0 #[mT]
        self.byEstimate = 0 #[mT]
        self.bzEstimate = 0 #[mT]
        self.ix1 = 0
        self.ix2 = 0
        self.iy1 = 0
        self.iy2 = 0
        self.iz1 = 0
        self.iz2 = 0


    def setX(self, mT):
        """Generate a zero-gradient magnetic flux density in the x-direction.
        """
        # The coils are controlled via PWM output from the Raspberry Pi
        # that is amplified by a motor driver. The duty cycle of the PWM
        # output is determined based on the desired voltage and the
        # supply voltage.
        if mT>=0:
            self.dac.output_voltage_pwm(self.pinXpwm, self.pinXdir, 0.0065*(mT**3)-0.0494*(mT**2)+1.4534*mT , self.VsupplyX)
        else:
            self.dac.output_voltage_pwm(self.pinXpwm, self.pinXdir, 0.0065*(mT**3)+0.0494*(mT**2)+1.4534*mT , self.VsupplyX)
        self.bxSetpoint = mT

    def setY(self, mT):
        """Generate a zero-gradient magnetic flux density in the x-direction.
        """
        # The coils are controlled via PWM output from the Raspberry Pi
        # that is amplified by a motor driver. The duty cycle of the PWM
        # output is determined based on the desired voltage and the
        # supply voltage.
        if mT>=0:
            self.dac.output_voltage_pwm(self.pinYpwm, self.pinYdir, 0.0036*(mT**3)-0.0314*(mT**2)+0.9386*mT , self.VsupplyY)
        else:
            self.dac.output_voltage_pwm(self.pinYpwm, self.pinYdir, 0.0036*(mT**3)+0.0314*(mT**2)+0.9386*mT , self.VsupplyY)
        self.bySetpoint = mT

    def setZ(self, mT):
        """Generate a zero-gradient magnetic flux density in the x-direction.
        """
        # The coils are controlled via PWM output from the Raspberry Pi
        # that is amplified by a motor driver. The duty cycle of the PWM
        # output is determined based on the desired voltage and the
        # supply voltage.
        if mT>=0:
            self.dac.output_voltage_pwm(self.pinZpwm, self.pinZdir, 0.0014*(mT**3)-0.0178*(mT**2)+0.571*mT , self.VsupplyZ)
        else:
            self.dac.output_voltage_pwm(self.pinZpwm, self.pinZdir, 0.0014*(mT**3)+0.0178*(mT**2)+0.571*mT , self.VsupplyZ)
        self.bzSetpoint = mT

    def setXYZ(self, x_mT, y_mT, z_mT):
        """Generate a zero-gradient magnetic flux density in xyz."""
        self.setX(x_mT)
        self.setY(y_mT)
        self.setZ(z_mT)

    def getXYZ(self): #fake estimate
        # Calculate an estimate of the magnetic flux density in mT from the
        # measured coil currents.
        self.bxEstimate = self.bxSetpoint
        self.byEstimate = self.bySetpoint
        self.bzEstimate = self.bzSetpoint
