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
frecuencia = 100
periodo = 1 / frecuencia

# %%
tiempo_medicion = 5 * periodo

device = 'Dev7'
#canales = ['ai1','ai0','ai7','ai2','ai3','ai4','ai5','ai6']
#min_vals = [-5.0, -0.5, -5.0, -0.5, -5.0, -0.5, -5.0, -5.0]
#max_vals = list(-np.array(min_vals))
for canales_a_borrar in range(0,7):
    canales = ['ai1','ai0','ai7','ai2','ai3','ai4','ai5','ai6']
    min_vals = [-5.0, -0.5, -5.0, -0.5, -5.0, -0.5, -5.0, -5.0]  
    max_vals = list(-np.array(min_vals))
    if canales_a_borrar < len(canales) - 1:
        for i in range(canales_a_borrar):
            canales.pop(1)
            min_vals.pop(1)
            max_vals.pop(1)
    else:
        raise ValueError('No borrar tantos canales')
    sample_rate = int(250000/len(canales))
    
    time_vec, med = adquisicion_con_placa.medir(device, canales, sample_rate,
                                                tiempo_medicion)#, min_vals = min_vals, max_vals = max_vals)
    
    corr = signal.correlate(med[0], med[-1], mode='full')
    delay = (np.argmax(corr)/sample_rate)%max(time_vec)
    fig, ax = plt.subplots(1, figsize=(6, 4))
    ax.plot(time_vec, med[0], label = 'Canal 1')
    ax.plot(time_vec, med[-1], label = 'Canal 6')
    ax.legend()
    ax.set_title('{} canales, Delay: {}s'.format(len(canales), delay))
    fig.tight_layout()
#    
#    fname = '{}/freqgen{}Hz_srate{}_{}canales_consaltosdeganancia.dat'.format(folder, frecuencia, sample_rate, len(canales))
#    coment = 'Medimos una señal de {}Hz en {} canales a fs {} con saltos de ganancia'.format(frecuencia, len(canales), sample_rate)
#    if not os.path.isfile(fname):
#        np.savetxt(fname, np.transpose([time_vec, med[0], med[-1]]), delimiter = ',', header = 'tiempo (s), tension (V)', footer=coment)
#        fig.savefig('{}/{}Hz_{}canales.png'.format(folder, frecuencia, len(canales)))
#    else:
#        print('NO GUARDO NADA')
#        print('Ya existe guachin')