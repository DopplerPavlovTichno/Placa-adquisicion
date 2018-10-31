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
#print(rm.list_resources()) # con esto veo el string que le tengo que dar en resource_name por si falla
# Abre la sesion VISA de comunicacion
fungen = rm.open_resource(resource_name, resource_pyclass=MessageBasedResource)

# %%
tiempo_medicion = 3

device = 'Dev7'
canales = ['ai0', 'ai1']
sample_rate = int(250000/len(canales))
for x in range(5):
    frecuencia_senial = 1+9*np.random.rand()
    stream_out = generador_placa_audio.write(duracion = 5, tipo = 'sin', amplitud = 2, f_signal = frecuencia_senial)
    time_vec, med = adquisicion_con_placa.medir(device, canales, sample_rate,
                                                tiempo_medicion)    
    fotodiodo = med[0]
    placa_audio = med[1]
    fft_senial = abs(np.fft.rfft(fotodiodo-np.mean(fotodiodo)))
    frecuencias_fft = np.fft.rfftfreq(len(fotodiodo),1/sample_rate)
    frecuencia_detectada = frecuencias_fft[np.argmax(fft_senial)]
    fungen.write('FREQ %f' % frecuencia_detectada)
    fungen.write('output1 on')
    time.sleep(5)
    stream_out.close()
    fungen.write('output1 off')
    print(frecuencia_senial)
#plt.figure(1)
#plt.plot(time_vec,placa_audio)
#
#plt.figure(2)
#plt.plot(time_vec, fotodiodo)
