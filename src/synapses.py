"""
Definition of default parameters (and hence, standard parameter names) for
standard dynamic synapse models. 

Classes for specifying short-term plasticity (facilitation/depression):
    TsodyksMarkramMechanism
    
Classes for defining STDP rules:
    AdditiveWeightDependence
    MultiplicativeWeightDependence
    AdditivePotentiationMultiplicativeDepression
    GutigWeightDependence
    SpikePairRule
    
"""

from common import ShortTermPlasticityMechanism, STDPWeightDependence, STDPTimingDependence

class TsodyksMarkramMechanism(ShortTermPlasticityMechanism):
    """
    Synapse exhibiting facilitation and depression, implemented using the model
    of Tsodyks and Markram.
    """
    default_parameters = {
        'U': 0.5,   # use parameter
        'tau_rec': 100.0, # depression time constant (ms)
        'tau_facil': 0.0,   # facilitation time constant (ms)
        'u0': 0.0,  # }
        'x0': 1.0,  # } initial values
        'y0': 0.0   # }
    }
    
    def __init__(self, U=0.5, tau_rec=100.0, tau_facil=0.0, u0=0.0, x0=1.0, y0=0.0):
        raise NotImplementedError
    

class AdditiveWeightDependence(STDPWeightDependence):
    """
    The amplitude of the weight change is fixed for depression (`A_minus`)
    and for potentiation (`A_plus`).
    If the new weight would be less than `w_min` it is set to `w_min`. If it would
    be greater than `w_max` it is set to `w_max`.
    """
    default_parameters = {
        'w_min':   0.0,
        'w_max':   1.0,
        'A_plus':  0.01,
        'A_minus': 0.01
    }
    
    def __init__(self, w_min=0.0, w_max=1.0, A_plus=0.01, A_minus=0.01): # units?
        raise NotImplementedError


class MultiplicativeWeightDependence(STDPWeightDependence):
    """
    The amplitude of the weight change depends on the current weight.
    For depression, Dw propto w-w_min
    For potentiation, Dw propto w_max-w
    """
    default_parameters = {
        'w_min'  : 0.0,
        'w_max'  : 1.0,
        'A_plus' : 0.01,
        'A_minus': 0.01,
    }
    
    def __init__(self, w_min=0.0, w_max=1.0, A_plus=0.01, A_minus=0.01):
        raise NotImplementedError
    

class AdditivePotentiationMultiplicativeDepression(STDPWeightDependence):
    """
    The amplitude of the weight change depends on the current weight for
    depression (Dw propto w) and is fixed for potentiation.
    """

    default_parameters = {
        'w_min'  : 0.0,
        'w_max'  : 1.0,
        'A_plus' : 0.01,
        'A_minus': 0.01,
    }

    def __init__(self, w_min=0.0,  w_max=1.0, A_plus=0.01, A_minus=0.01):
        raise NotImplementedError

    
class GutigWeightDependence(STDPWeightDependence):
    
    default_parameters = {
        'w_min'   : 0.0,
        'w_max'   : 1.0,
        'A_plus'  : 0.01,
        'A_minus' : 0.01,
        'mu_plus' : 0.5,
        'mu_minus': 0.5
    }

    def __init__(self, w_min=0.0,  w_max=1.0, A_plus=0.01, A_minus=0.01,mu_plus=0.5,mu_minus=0.5):
        raise NotImplementedError

# Not yet implemented for any module
#class PfisterSpikeTripletRule(STDPTimingDependence):
#    raise NotImplementedError


class SpikePairRule(STDPTimingDependence):
    
    default_parameters = {
        'tau_plus':  20.0,
        'tau_minus': 20.0,
    }
    
    def __init__(self, tau_plus=20.0, tau_minus=20.0):
        raise NotImplementedError #_abstract_method(self)