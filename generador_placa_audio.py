# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 16:14:13 2018

@author: Publico
"""
import pyaudio
import numpy as np


def senoidal(f_sampleo=44100, frecuencia=100, num_puntos=1024, vpp=1.,
             offset=0.):
    """
    Genera una señal senoidal de frecuencia y numero de puntos definida
    
    Parameters
    ----------
    f_sampleo(float) = frecuencia de sampleo de la señal
    frecuencia(float) = frecuencia de la señal
    duracion(float) = duracion de la señal
    vpp(float) = valor pico a pico
    offset(float) = valor dc de la señal
    dtype = data type de la señal
    Returns
    -------
    Devuelve array
    """
    times = np.arange(num_puntos)
    return (vpp/2*(np.sin(2*np.pi*times*frecuencia/f_sampleo))
            + offset).astype(np.float32)


def take(arr, partlen):
    larr = len(arr)
    while True:
        cursor = 0
        while cursor < larr-partlen:
            tmp = arr[cursor:cursor+partlen]
            yield tmp
            cursor = min(cursor+partlen, larr+1)


def create_callback(gen):
    def callback_output(out_data, frame_count, time_info, status):
        out_data = next(gen)
        return out_data, pyaudio.paContinue
    return callback_output


def write(duracion, tipo, amplitud, f_signal=1000, fs=192000, offset=0,
          noise=False, noise_amplitude=0.1):
    """
    Envia señal a la placa de audio
    
    Parametros
    ----------
    duracion: float
        Duracion en segundos de la señal a enviar

    tipo: string
        Tipo de señal: senoidal ('sin') o random ('random')

    amlitud: float
        Amplitud pico a pico de la señal
    
    Devuelve
    --------
    stream_out: stream
    """
    CHUNK = 1024
    pa = pyaudio.PyAudio()
    if tipo=='sin':
        tmp = senoidal(f_sampleo=fs, frecuencia=f_signal,
                       num_puntos=fs*duracion,
                       vpp=amplitud, offset=offset)
    elif tipo=='random':
        tmp = (np.random.rand(fs*duracion)-0.5)*amplitud+offset
    else:
        raise ValueError("Tipo puede ser 'sin' o 'random'")
    if noise:
        tmp_ruido = (np.random.rand(fs*duracion)-0.5)*noise_amplitude
        tmp += tmp_ruido
    stream_out = pa.open(format=pyaudio.paFloat32,
                         channels=1,
                         rate=fs,
                         output=True,
                         frames_per_buffer=CHUNK,
                         stream_callback=create_callback(take(tmp, CHUNK)))
    return stream_out


# %%
#if __name__=='main':
#stream1 = write(5, 'random', 1)
#stream2 = write(5, 'sin', 1)
