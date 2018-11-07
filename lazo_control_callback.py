# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 16:14:13 2018

@author: Publico
"""
import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
import pyaudio as pa
import adquisicion_con_placa
import generador_placa_audio
from scipy import signal
import pyvisa
from pyvisa import resources, util
from pyvisa.resources import MessageBasedResource
import scipy
import time
import pid_class
## inicio comunicacion con el generador de funciones

resource_name_control = 'USB0::0x0699::0x0346::C033248::INSTR'
resource_name_perturb = 'USB0::0x0699::0x0346::C036493::INSTR'
rm = pyvisa.ResourceManager()

print(rm.list_resources()) # con esto veo el string que le tengo que dar en resource_name por si falla
# Abre la sesion VISA de comunicacion
fungen_control = rm.open_resource(resource_name_control, resource_pyclass=MessageBasedResource)
fungen_perturb = rm.open_resource(resource_name_perturb, resource_pyclass=MessageBasedResource)

# %% Calibracion sensor
device = 'Dev6'
canales = ['ai0']
fungen_perturb.write('output1 on')
fungen_control.write('output1 on')
fungen_control.write('VOLT % f' % 0.02)
fungen_control.write('FREQ % f' % 0.000001)
fungen_perturb.write('VOLT:OFFS % f' % 4)
fungen_perturb.write('FREQ % f' % 0.000001)
#fungen_perturb.write('VOLT % f' % 0.02)
#fungen_perturb.write('FREQ % f' % 0.000001)
tension_led = np.linspace(0, 8, num=100)
tension_fotodiodo = np.zeros_like(tension_led)
error_fotodiodo = np.zeros_like(tension_led)
for index, offset in enumerate(tension_led):
    fungen_control.write('VOLT:OFFS % f' % offset)
    time_vec, med = adquisicion_con_placa.medir(device, canales, sample_rate=1000, duracion=1)
    tension_fotodiodo[index] = np.mean(med)
    error_fotodiodo[index] = np.std(med)
fungen_control.write('output1 off')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(tension_led, tension_fotodiodo)
ax.set_xlabel('Tension led perturbacion (V)')
ax.set_ylabel('Tension R fotodiodo (V)')
#fig.savefig('calibracion_led-fotodiodo_luzprendida_perturbprendido4V.png')
#np.savetxt('calibracion_ledperturbacion-fotodiodo_luzprendida_perturbprendido4V.dat', np.transpose([tension_led, tension_fotodiodo]))

# %%
datos_series = []
control_series = []
error_series = []
previous = 0

calibracion = np.loadtxt('calibracion_led-fotodiodo_luzapagada.dat')
tension_led = [x[0] for x in calibracion]
tension_fotodiodo = [x[1] for x in calibracion]

calibracionpert = np.loadtxt('calibracion_ledperturbacion-fotodiodo_luzapagada.dat')
tension_led_pert = [x[0] for x in calibracionpert]
tension_fotodiodo_pert = [x[1] for x in calibracionpert]

def callback(task_handle, every_n_samples_event_type, 
             number_of_samples, callback_data):
    global previous
    datos = task.read(number_of_samples)
    pid_value = lazo.calculate(datos[0])
    v_fotodiodo_previous = np.interp(previous, tension_led, tension_fotodiodo)
    actuador = np.interp(pid_value + v_fotodiodo_previous, tension_fotodiodo, tension_led)# + previous
    actuador = pid_value + previous
    control_series.append(actuador)
    error_series.append(lazo.last_error)
    fungen_control.write('VOLT:OFFS % f' % actuador)
#    print(previous)
    previous = actuador
    datos_series.append(datos[0])
    return 0

freq_pert = 1
fungen_perturb.write('VOLT:OFFS % f' % 3)
fungen_perturb.write('VOLT % f' % 1.5)
fungen_perturb.write('FREQ % f' % freq_pert)
fungen_perturb.write('output1 on')

fungen_control.write('VOLT % f' % 0.02)
fungen_control.write('FREQ % f' % 0.000001)
fungen_control.write('VOLT:OFFS % f' % 0)
fungen_control.write('output1 on')

device = 'Dev6'
canales = ['ai0']
callback_dt = 0.02
sample_rate = int(1/callback_dt)
tipo_lazo = 'P'
kp_crit = 110
p_crit = 2
ki = 0
kd = 0.0
if tipo_lazo == 'P':
    kp = 100
    ki = 0
    kd = 0.0
elif tipo_lazo == 'PI':
    kp = 0.45*kp_crit
    ki = 1.2*kp/p_crit*callback_dt
else:
    kp = 0.6*kp_crit
    ki = 2*kp/p_crit*callback_dt
    kd = kp*p_crit*callback_dt
setpoint = 0.04
lazo = pid_class.PIDController(setpoint=setpoint, dt=callback_dt,
                               kp=kp, ki=ki, kd=kd)

with nidaqmx.Task() as task:
    for i, channel in enumerate(canales):
        task.ai_channels.add_ai_voltage_chan('{}/{}'.format(device, channel))
    task.timing.cfg_samp_clk_timing(sample_rate,
                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
    task.register_every_n_samples_acquired_into_buffer_event(sample_interval=int(callback_dt*sample_rate), 
                                                             callback_method=callback)
    task.start()
    time.sleep(5)
    task.stop()

time_vec = np.arange(len(datos_series))/sample_rate
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time_vec, datos_series, label='sensor')
ax.axhline(y=setpoint, label='objetivo', c='red')
ax.plot(time_vec, np.asarray(error_series), label='error')
ax.legend()
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Tension (V)')
#fig.savefig('proporcional_kp{}_pert{}Hz.png'.format(kp, freq_pert))
