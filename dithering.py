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


# %%
tiempo_medicion = 1
sample_rate = 10000

device = 'Dev7'
canales = ['ai1', 'ai6']

stream = generador_placa_audio.write(tiempo_medicion, 'sin', 1)
time.sleep(0.2)
time_vec, med = adquisicion_con_placa.medir(device, canales, sample_rate,
                                            tiempo_medicion)
stream.stop_stream()
plt.plot(time_vec, med[0])
plt.plot(time_vec, med[1])
