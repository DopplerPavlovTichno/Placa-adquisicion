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

stream = generador_placa_audio.write(duracion=tiempo_medicion, tipo='random',
                                     amplitud=0.,
                                     f_signal=10, noise=False)
time.sleep(0.25)
time_vec, med = adquisicion_con_placa.medir(device, canales, sample_rate,
                                            tiempo_medicion)
stream.stop_stream()
plt.plot(time_vec, med[0])
plt.plot(time_vec, med[1])
# %%
samples_per_channel = int(sample_rate*tiempo_medicion)
with nidaqmx.Task() as task:
    ai_channel = task.ai_channels.add_ai_voltage_chan('{}/{}'.format(device, canales[0]),)
    task.timing.cfg_samp_clk_timing(sample_rate,
                                    samps_per_chan=samples_per_channel)
#    ai_channel.ai_resolution = 2
    print(ai_channel.ai_resolution)
#    ai_channel.ai