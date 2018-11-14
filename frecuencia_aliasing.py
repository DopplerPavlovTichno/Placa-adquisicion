# -*- coding: utf-8 -*-
"""
Script que calcula la frecuencia de aliasing fA de una señal a partir de la frecuencia real de la misma y de la frecuencia de sampleo
Para ello utiliza la fórmula dada en la presentación de Germán Patterson en la materia Instrumentación y Control (en la bibliografía debe estar en casi cualquier referencia sobre el tema)
La misma indica que la frecuencia del pico va a estar en min|k * f - fs| donde fs es la frecuencia de sampleo, k el entero que haga que se minimice el módulo, y f la frecuencia de la señal
En este caso la función fA está armada de modo de admitir un array como input, y el output es un array también de las frecuencias de aliasing
Si no hay aliasing (porque fseñal < 2 * fsampleo) se devuelve fseñal
"""

import numpy as np
import matplotlib.pyplot as plt

def fA(freqs, fs):
    ans = []
    for f in freqs:
        if fs > 2 * f:
            ans.append(f)
        else:
            q = abs(fs - f)
            k = 2
            out = 0
            while out == 0: 
                r = abs(k * fs - f)
                if r < q:
                    q = r
                    k = k + 1
                else:
                    ans.append(q)
                    out = 1
    return ans

# Lo aplico al caso de una cuadrada de 50 Hz con f de sampleo de 490 Hz

fundamental = 50
paso = 2 * fundamental
final = 50 * fundamental
freqs = np.arange(fundamental, final, paso)
amplitudes = fundamental/freqs
fsampleo = 280

freqs_aliasing = fA(freqs, fsampleo)

# Grafico los puntos que deberían ser los picos de la FFT

plt.scatter(freqs_aliasing, amplitudes)

freqs_aliasing, amplitudes = zip(*sorted(zip(freqs_aliasing, amplitudes)))

plt.plot(freqs_aliasing,amplitudes)