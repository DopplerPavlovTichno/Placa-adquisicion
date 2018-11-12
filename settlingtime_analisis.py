# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os

data = np.genfromtxt('/Doctorado/Materias/Instrumentacion/Repositorios/DopplerPavlovTichno/Placa-adquisicion/Setling_Time/freqgen1000Hz_srate50000_5canales.dat',delimiter=',',skip_header = 1,skip_footer = 1) # ojo, en el .dat hay que cambiar el ultimo rengion que tenia una enie para que lo lea 

tiempo = data[:,0]
tension_ch1 = data[:,1]
tension_ch2 = data[:,2]
canales = 5
freqadq = 250000 / canales # para cada canal
sample_rate = 1 / freqadq

plt.plot(tension_ch1, tension_ch2) # de esta elipse se puede sacar el desfasaje, y conociendo el periodo de la senial de inyeccion, el deltaT

corr = np.convolve(tension_ch1, tension_ch2)
'''
plt.figure(1)
plt.plot(tiempo, tension)

frecuencia_picos = []
fourier = np.abs(np.fft.rfft(tension))
fourier = fourier / max(fourier)
fourier_freqs = np.fft.rfftfreq(len(tension), d=1./freqadq)
plt.figure(2)
plt.plot(fourier_freqs, fourier)

amplitudes_fourier, freqs_fourier = zip(*sorted(zip(fourier, fourier_freqs)))

amplitudes_fourier_primeras10 = amplitudes_fourier[-10:]
freqs_fourier_primeras10 = freqs_fourier[-10:]

amplitudes_fourier_10 = []
for amps in amplitudes_fourier_primeras10:
    amplitudes_fourier_10.append(1/amps)
'''