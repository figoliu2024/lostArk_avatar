import numpy
import math



def eucliDist(A,B):
    A = numpy.array(A)
    B = numpy.array(B)
    return numpy.sqrt(sum(numpy.power((A - B), 2)))    