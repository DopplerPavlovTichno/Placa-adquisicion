# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy
from scipy.signal import correlate
import PyAstronomy
from PyAstronomy import pyaC

canales = [2, 3, 4, 5, 6, 7, 8]
freqsadq_name = [125000, 83333, 62500, 50000, 41666, 35714, 31250]
diftiempo = []
err_diftiempo = []
err_inversadiftiempo = []
inversadiftiempo = []
consaltos = True

for ind in range(len(canales)):
    numcanales = canales[ind]
    freqadqname = freqsadq_name[ind]
    data = np.genfromtxt('/Doctorado/Materias/Instrumentacion/Repositorios/DopplerPavlovTichno/Placa-adquisicion/Setling_Time/freqgen1000Hz_srate{}_{}canales.dat'.format(freqadqname, numcanales),delimiter=',',skip_header = 1,skip_footer = 1) # ojo, en el .dat hay que cambiar el ultimo rengion que tenia una enie para que lo lea 
    if consaltos == True:
        data = np.genfromtxt('/Doctorado/Materias/Instrumentacion/Repositorios/DopplerPavlovTichno/Placa-adquisicion/Setling_Time/freqgen1000Hz_srate{}_{}canales_consaltosdeganancia.dat'.format(freqadqname, numcanales),delimiter=',',skip_header = 1,skip_footer = 1) # ojo, en el .dat hay que cambiar el ultimo rengion que tenia una enie para que lo lea 
    tiempo = data[:,0]
    tension_ch1 = data[:,1]
    tension_ch2 = data[:,2]
    freqadq = 250000 / numcanales # para cada canal
    sample_rate = 1 / freqadq # para cada canal
    freq_senial = 1000 # en Hz
    periodo_senial = 1 / freq_senial # en segundos
    indice_dosperiodos = np.argmin(abs(tiempo - 2 * periodo_senial)) + 1
    
    plt.figure(1)
    plt.plot(tiempo, tension_ch1)
    plt.plot(tiempo, tension_ch2)
    
    tension_ch1_dosperiodos = tension_ch1[:indice_dosperiodos]
    tension_ch2_dosperiodos = tension_ch2[:indice_dosperiodos]
    tiempo_dosperiodos = tiempo[:indice_dosperiodos]
    
    plt.figure(2)
    plt.plot(tiempo_dosperiodos, tension_ch1_dosperiodos)
    plt.plot(tiempo_dosperiodos, tension_ch2_dosperiodos)
    
    
    plt.figure(3)
    plt.plot(tension_ch1, tension_ch2) # de esta elipse se puede sacar el desfasaje, y conociendo el periodo de la senial de inyeccion, el deltaT
    
    corr = correlate(tension_ch1_dosperiodos, tension_ch2_dosperiodos, mode = 'full')
    am = np.argmax(corr)
    
    ch1_sorted, ch2_sorted = zip(*sorted(zip(tension_ch1, tension_ch2)))
    
    plt.figure(4)
    plt.plot(corr)
    
    # Encontrando los cruces por cero de las seniales
    
    zero_crossings_ch1 = np.where(np.diff(np.sign(tension_ch1)))[0]
    zero_crossings_ch2 = np.where(np.diff(np.sign(tension_ch2)))[0]
    
    # haciendo una interpolacion para encontrar el cruce por cero con mas precision
    tiempos_ceros_ch1 = []
    tiempos_ceros_ch2 = []
    
    for zc in zero_crossings_ch1:
        t1 = tiempo[zc]
        t2 = tiempo[zc + 1]
        y1 = tension_ch1[zc]
        y2 = tension_ch1[zc + 1]
        pendiente = (y2 - y1) / (t2 - t1)
        tiempos_ceros_ch1.append(t1 - y1 / pendiente) # saco el tiempo via interpolacion
        
    for zc in zero_crossings_ch2:
        t1 = tiempo[zc]
        t2 = tiempo[zc + 1]
        y1 = tension_ch2[zc]
        y2 = tension_ch2[zc + 1]
        pendiente = (y2 - y1) / (t2 - t1)
        tiempos_ceros_ch2.append(t1 - y1 / pendiente) # saco el tiempo via interpolacion
        
    plt.figure(5)
    plt.scatter(np.linspace(0, len(tiempos_ceros_ch1) - 1, len(tiempos_ceros_ch1)), tiempos_ceros_ch1)
    plt.scatter(np.linspace(0, len(tiempos_ceros_ch2) - 1, len(tiempos_ceros_ch2)), tiempos_ceros_ch2)
    
    a = np.polyfit(np.linspace(0, len(tiempos_ceros_ch1) - 1, len(tiempos_ceros_ch1)), tiempos_ceros_ch1, 1, cov = True)
    m1 = a[0][0]
    b1 = a[0][1]
    V1 = a[1] # matriz de covarianza
    errb1 = (V1[1][1])**0.5
    
    a = np.polyfit(np.linspace(0, len(tiempos_ceros_ch2) - 1, len(tiempos_ceros_ch2)), tiempos_ceros_ch2, 1, cov = True)
    if consaltos is not True and numcanales == 5: # correcting the method (in this case it performed badly because of indexing, one signal began with a zero crossing and the other no, I think)
        a = np.polyfit(1 + np.linspace(0, len(tiempos_ceros_ch2) - 1, len(tiempos_ceros_ch2)), tiempos_ceros_ch2, 1, cov = True)

    m2 = a[0][0]
    b2 = a[0][1]
    V2 = a[1] # matriz de covarianza
    errb2 = (V2[1][1])**0.5
    
    diftiempo.append(abs(b2 - b1))
    inversadiftiempo.append(1/abs(b2 - b1))
    err_diftiempo.append((errb2**2 + errb1**2)**0.5)
    err_inversadiftiempo.append((errb2**2 + errb1**2)**0.5/(b2 - b1)**2)

fig = plt.figure(6)
plt.plot(tiempo * 1000, tension_ch1, label = 'Canal 1')
plt.plot(tiempo * 1000, tension_ch2, label = 'Canal 2')
plt.scatter(np.array(tiempos_ceros_ch1) * 1000,np.zeros_like(tiempos_ceros_ch1))
plt.scatter(np.array(tiempos_ceros_ch2) * 1000,np.zeros_like(tiempos_ceros_ch2))
plt.xlabel('Tiempo (ms)')
plt.ylabel('Voltaje (V)')
plt.legend()
matplotlib.rcParams.update({'font.size': 22})

plt.figure(7)
plt.scatter(np.linspace(0, len(tiempos_ceros_ch1) - 1, len(tiempos_ceros_ch1)), 1000 * np.array(tiempos_ceros_ch1))
plt.scatter(np.linspace(0, len(tiempos_ceros_ch2) - 1, len(tiempos_ceros_ch2)), 1000 * np.array(tiempos_ceros_ch2))
x = np.linspace(0, len(tiempos_ceros_ch1) - 1, len(tiempos_ceros_ch1))
plt.plot(x,1000 * (m1 * x + b1), label = 'Canal 1')
x = np.linspace(0, len(tiempos_ceros_ch2) - 1, len(tiempos_ceros_ch2))
plt.plot(x,1000 * (m2 * x + b2), label = 'Canal 2')
plt.xlabel('Número de cruce por cero')
plt.ylabel('Tiempo del cruce (ms)')
plt.legend()
matplotlib.rcParams.update({'font.size': 22})

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