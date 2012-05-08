# encoding: utf-8
"""
Alternative, procedural API for creating, connecting and recording from individual neurons

:copyright: Copyright 2006-2012 by the PyNN team, see AUTHORS.
:license: CeCILL, see LICENSE for details.
"""

from populations import IDMixin, BasePopulation, Assembly


def build_create(population_class):
    def create(cellclass, cellparams=None, n=1):
        """
        Create `n` cells all of the same type.

        Returns a Population object.
        """
        return population_class(n, cellclass, cellparams)  # return the Population or Population.all_cells?
    return create


def build_connect(projection_class, connector_class):
    def connect(source, target, weight=0.0, delay=None, synapse_type=None,
                p=1, rng=None):
        """
        Connect a source of spikes to a synaptic target.

        `source` and `target` can both be individual cells or populations/
        assemblies of cells, in which case all possible connections are made
        with probability `p`, using either the random number generator supplied,
        or the default RNG otherwise. Weights should be in nA or µS.
        """
        if isinstance(source, IDMixin):
            source = source.as_view()
        if isinstance(target, IDMixin):
            target = target.as_view()
        connector = connector_class(p_connect=p, weights=weight, delays=delay)
        return projection_class(source, target, connector, target=synapse_type, rng=rng)
    return connect


def set(cells, param, val=None):
    """
    Set one or more parameters of an individual cell or list of cells.

    param can be a dict, in which case val should not be supplied, or a string
    giving the parameter name, in which case val is the parameter value.
    """
    assert isinstance(cells, (BasePopulation, Assembly))
    cells.set(param, val)


def build_record(variable, simulator):
    if variable == "gsyn": # will be removed in PyNN 0.9
        variable_list = ['gsyn_exc', 'gsyn_inh']
    else:
        variable_list = [variable]
    def record(source, filename):
        """
        Record spikes to a file. source can be an individual cell, a Population,
        PopulationView or Assembly.
        """
        # would actually like to be able to record to an array and choose later
        # whether to write to a file.
        if not isinstance(source, (BasePopulation, Assembly)):
            source = source.parent
        source.record(variable_list, to_file=filename)
        # recorders_autowrite is used by end()
        if isinstance(source, BasePopulation):
            populations = [source]
        elif isinstance(source, Assembly):
            populations = source.populations
        for population in populations:
            simulator.write_on_end.append((population, variable_list, filename))
# NEED TO HANDLE DEPRECATION OF record_v() and record_gsyn()
    if variable == 'v':
        record.__name__ = "record_v"
        record.__doc__ = """
            Record membrane potential to a file. source can be an individual
            cell, a Population, PopulationView or Assembly."""
    elif variable == 'gsyn':
        record.__name__ = "record_gsyn"
        record.__doc__ = """
            Record synaptic conductances to a file. source can be an individual
            cell, a Population, PopulationView or Assembly."""
    return record


def initialize(cells, variable, value):
    assert isinstance(cells, (BasePopulation, Assembly)), type(cells)
    cells.initialize(variable, value)
