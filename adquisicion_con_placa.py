# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 16:14:13 2018

@author: Publico
"""
import nidaqmx
import numpy as np


def medir(device, canales, sample_rate, duracion):
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
    samples_per_channel = int(sample_rate*duracion)
    time_vec = np.arange(0, duracion, 1/sample_rate)
    med = np.nan
    with nidaqmx.Task() as task:
        for channel in canales:
            task.ai_channels.add_ai_voltage_chan('{}/{}'.format(device, channel))
        task.timing.cfg_samp_clk_timing(sample_rate,
                                        samps_per_chan=samples_per_channel)
        med = task.read(number_of_samples_per_channel=samples_per_channel)
        task.wait_until_done()
    
    return time_vec, med
