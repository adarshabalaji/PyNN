

from numpy.testing import assert_array_almost_equal

import pyNN.nest as sim
from pyNN.random import RandomDistribution as RD
from pyNN.network import Network
from pyNN.serialization import export_to_sonata, import_from_sonata

sim.setup()

p1 = sim.Population(10,
                    sim.IF_cond_exp(
                        v_rest=-65,
                        tau_m=lambda i: 10 + 0.1*i,
                        cm=RD('normal', (0.5, 0.05))),
                    label="population_one")
p2 = sim.Population(20,
                    sim.IF_curr_alpha(
                        v_rest=-64,
                        tau_m=lambda i: 11 + 0.1*i),
                    label="population_two")

prj = sim.Projection(p1, p2,
                     sim.FixedProbabilityConnector(p_connect=0.5),
                     synapse_type=sim.StaticSynapse(weight=RD('uniform', [0.0, 0.1]),
                                                    delay=0.5),
                     receptor_type='excitatory')

net = Network(p1, p2, prj)

export_to_sonata(net, "tmp_serialization_test", overwrite=True)

net2 = import_from_sonata("tmp_serialization_test/circuit_config.json", sim)


for orig_population in net.populations:
    imp_population = list(net2.assemblies)[0].get_population(orig_population.label)
    assert orig_population.size == imp_population.size
    for name in orig_population.celltype.default_parameters:
        assert_array_almost_equal(orig_population.get(name), imp_population.get(name), 12)