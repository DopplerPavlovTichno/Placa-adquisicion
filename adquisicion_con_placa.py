# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 16:14:13 2018

@author: Publico
"""
import nidaqmx
import numpy as np


def medir(device, canales, sample_rate, duracion, min_vals = -5.0, max_vals = 5.0):
    """
    Hace una medicion usando la placa de adquisicion.
    
    Parametros
    ----------
    device: string
        Nombre del dispositivo (ver en NI MAX)
    
    canales: list of strings
        Lista de canales
    
    sample_rate: float
        Frecuencia de adquisicion
    
    duracion: float
        Duracion de la medicion
    
    Returns
    -------
    time_vec: array
        Vector de tiempos
    
    med: array
        Vector de mediciones
    """
    if type(min_vals) == int or type(min_vals) == float:
        min_vals = np.ones(len(canales)) * min_vals
        max_vals = np.ones(len(canales)) * max_vals        
    elif len(min_vals) != len(max_vals):
        raise ValueError('min_vals y max_vals deben tener la misma longitud')
    elif len(min_vals) != len(canales):
        raise ValueError('min_vals, max_vals y canales deben tener la misma longitud')

    time_vec = np.arange(0, duracion, 1/sample_rate)
    samples_per_channel = len(time_vec)
    med = np.nan
    with nidaqmx.Task() as task:
        for i, channel in enumerate(canales):
            task.ai_channels.add_ai_voltage_chan('{}/{}'.format(device, channel), min_val = min_vals[i], max_val = max_vals[i])
        task.timing.cfg_samp_clk_timing(sample_rate,
                                        samps_per_chan=samples_per_channel)
        med = task.read(number_of_samples_per_channel=samples_per_channel)
        task.wait_until_done()
    
    return time_vec, med


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    device = 'Dev6'
    canales = ['ai1']
    sample_rate = 10000
    duracion = 1
    time, med = medir(device=device, canales=canales, sample_rate=sample_rate,
                duracion=duracion)
    plt.plot(time, med)