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
## inicio comunicacion con el generador de funciones

resource_name = 'USB0::0x0699::0x0346::C036492::INSTR'
rm = pyvisa.ResourceManager()
print(rm.list_resources()) # con esto veo el string que le tengo que dar en resource_name por si falla
# Abre la sesion VISA de comunicacion
fungen = rm.open_resource(resource_name, resource_pyclass=MessageBasedResource)

# %%
    
datosappend = []
def callback(task_handle, every_n_samples_event_type, 
             number_of_samples, callback_data):
    global datos
    datos = task.read(number_of_samples)
#    fft_senial = abs(np.fft.rfft(datos-np.mean(datos)))
#    frecuencias_fft = np.fft.rfftfreq(len(datos),1/sample_rate)
#    frecuencia_detectada = frecuencias_fft[np.argmax(fft_senial)]
#    fungen.write('FREQ %f' % frecuencia_detectada)
    offset = np.mean(datos)*100
    fungen.write('VOLT:OFFS % f' % offset)
    
#    print(frecuencia_detectada)
#    plt.plot(datos)
    datosappend.append([x for x in datos])
    return 0
fungen.write('VOLT % f' % 0.02)
frecuencia_senial = 25
stream_out = generador_placa_audio.write(duracion = 5, tipo = 'sin', 
                                         amplitud = 2, f_signal = frecuencia_senial)
device = 'Dev7'
canales = ['ai0']
sample_rate = int(250000/len(canales))
with nidaqmx.Task() as task:
    for i, channel in enumerate(canales):
        task.ai_channels.add_ai_voltage_chan('{}/{}'.format(device, channel))
    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
    task.register_every_n_samples_acquired_into_buffer_event(sample_interval=100000, 
                                                             callback_method=callback)
    task.start()
    fungen.write('output1 on')
    time.sleep(5)
    task.stop()
fungen.write('output1 off')
stream_out.close()
