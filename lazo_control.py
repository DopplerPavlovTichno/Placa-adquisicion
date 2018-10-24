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

# %%
frecuencia = 100
periodo = 1 / frecuencia
tiempo_medicion = 5 * periodo

device = 'Dev7'
canales = ['ai1']
sample_rate = int(250000/len(canales))
time_vec, med = adquisicion_con_placa.medir(device, canales, sample_rate,
                                            tiempo_medicion)
stream_out = generador_placa_audio.write(1, 'sin', 2 , f_signal=10)
stream_out.close()
