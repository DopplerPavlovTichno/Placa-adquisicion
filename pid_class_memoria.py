# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:24:36 2018

@author: Publico
"""
import numpy as np

class PIDController:
    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0, offset=0.0,
                 cantidad_errores=-1, dt=1.0):

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.offset = offset
        self.dt = dt
        self.last_error = 0
        self.cantidad_errores = cantidad_errores
        if cantidad_errores != -1:
            self.last_errors = [0]*self.cantidad_errores
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0

    def calculate(self, feedback_value):
        error = self.setpoint - feedback_value
        delta_error = (error - self.last_error)/self.dt
        self.p_term = self.kp * error + self.offset
        if self.cantidad_errores != -1:
            self.last_errors.append(error)
            self.last_errors.pop(0)
            self.i_term = sum(self.last_errors)*self.dt
        else:
            self.i_term += error*self.dt
        self.d_term = delta_error

        self.last_error = error

        return self.p_term + (self.ki * self.i_term) + (self.kd * self.d_term)
