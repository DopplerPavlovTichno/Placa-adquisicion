# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 16:14:13 2018

@author: Publico
"""
import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
import os
import pyaudio as pa
import adquisicion_con_placa
import generador_placa_audio
import time
from scipy import signal

# %%
folder = 'Multiplexado'
frecuencia = 60000

# %%
tiempo_medicion = 1
sample_rate = 125000

device = 'Dev7'
canales = ['ai1', 'ai6']

time_vec, med = adquisicion_con_placa.medir(device, canales, sample_rate,
                                            tiempo_medicion)
fig, ax = plt.subplots(1, figsize=(6, 4))
ax.plot(time_vec, med[0])
ax.plot(time_vec, med[1])
fig.tight_layout()
fig.savefig('{}/{}Hz.png'.format(folder, frecuencia))
corr = signal.correlate(med[0], med[1], mode='valid')
delay = np.argmax(corr)/sample_rate
fname = '{}/freqgen{}Hz_srate{}.dat'.format(folder, frecuencia, sample_rate)
coment = 'Medimos una señal de {}Hz end dos canales a fs {}'.format(frecuencia, sample_rate)
if not os.path.isfile(fname):
    np.savetxt(fname, np.transpose([time_vec, med[0], med[1]]), delimiter = ',', header = 'tiempo (s), tension (V)', footer=coment)
else:
    print('NO GUARDO NADA')
    print('Ya existe guachin')