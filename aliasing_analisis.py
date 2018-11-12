# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os

data = np.genfromtxt('/Doctorado/Materias/Instrumentacion/Repositorios/DopplerPavlovTichno/Placa-adquisicion/aliasing cuadrada input 50Hz/freqadq490Hz.dat',delimiter=',',skip_header=1)

tiempo = data[:,0]
tension = data[:,1]
freqadq = 490
sample_rate = 1 / freqadq

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