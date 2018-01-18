import PyQ.config as cfg
import sympy as s
import numpy as n
from PyQ.GateInfoRegister import GateInfoRegister
from PyQ.Gatename import Gatename
from PyQ.RandomValueGenerator import RandomValueGenerator

class DisturbanceGenerator(object):

    Identity = GateInfoRegister.instance().register[Gatename.IDENTITY]
    qubit_disturbance = cfg.QUBIT_DISTURBANCE_PROBABILITY
    rotation_probability = cfg.ROTATION_PROBABILITY

    @classmethod
    def create_disturbance(cls, size):
        rotation_matrices = [cls.Identity.transformation]*size
        rotation_functions = [cls.rotation_z, cls.rotation_y, cls.rotation_x]
        for i in range(size):
            if RandomValueGenerator.binary_distribution(cls.qubit_disturbance):
                for rotation_function in rotation_functions:
                    if RandomValueGenerator.binary_distribution(cls.rotation_probability):
                        rotation_matrices[i] = n.dot(rotation_function(), rotation_matrices[i])
        rotation = rotation_matrices[0]
        for i in range(1, size):
            rotation = n.kron(rotation, rotation_matrices[i])
        return rotation

    @classmethod
    def rotation_x(cls):
        radians = cls.get_angle()
        return n.matrix([[s.cos(radians/2), -s.I*s.sin(radians/2)], [-s.I*s.sin(radians/2), s.cos(radians/2)]])

    @classmethod
    def rotation_y(cls):
        radians = cls.get_angle()
        return n.matrix([[s.cos(radians/2), -s.sin(radians/2)], [s.sin(radians/2), s.cos(radians/2)]])

    @classmethod
    def rotation_z(cls):
        radians = cls.get_angle()
        return n.matrix([[s.exp(-s.I*(radians/2)), 0], [0, s.exp(s.I*(radians/2))]])

    @classmethod
    def get_angle(cls):
        angle = RandomValueGenerator.uniform(cfg.DISTURBANCE_BOUNDS[0], cfg.DISTURBANCE_BOUNDS[1])
        return s.rad(int(angle))

    @classmethod
    def set_qubit_disturbance_probability(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Probability out of range (0,1)")
        else:
            cls.qubit_disturbance = value

    @classmethod
    def set_rotation_probability(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Probability out of range (0,1)")
        else:
            cls.rotation_probability = value


