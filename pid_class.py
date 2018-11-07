# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:24:36 2018

@author: Publico
"""

class PIDController:
    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0, dt=1.0):

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.last_error = 0
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0

    def calculate(self, feedback_value):
        error = self.setpoint - feedback_value

        delta_error = (error - self.last_error)/self.dt

        self.p_term = self.kp * error
        self.i_term += error*self.dt
        self.d_term = delta_error

        self.last_error = error

        return self.p_term + (self.ki * self.i_term) + (self.kd * self.d_term)
