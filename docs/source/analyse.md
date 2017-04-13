# Results and Analysis Tools

φ-evo has a module dedicated to the analysis of the results. The results are stored in a *Simulation* object that contains a set of method that give a quick access to the most relevant observable of a run. To start analyzing the `evo_dir` project, you need to create a *Simulation* object associated to it.

```python
from phievo.AnalysisTools import Simulation

sim = Simulation("evo_dir")
```

From there it is pretty straight forward to explore the architecture of the results. A simulation contains Seeds which themselves contain Network. In order not to overload the memory, the Seeds do not contain exactly the networks but a link to them. As an example, here is how you would load the best network for generation 326 in the seed number 2:

```python
sim = Simulation("evo_dir")
best_net_2_326 = sim.Seeds[2].get_best_net(326)
# Equivalent to
sim = Simulation("evo_dir")
best_net_2_326 = sim.get_best_net(2,326)
```

## Organization  of the results

If you want to understand why the *Simulation* object is organized the way it is and how to go beyond its possibilities, you will need to have an idea of how φ-evo stores the results of a simulation.

By default, for every generation *g* only one *Network* is stored using pickle in a file labelled `Bests_g.net`. When the simulation has only one fitness objective, this network is the one with the best fitness in the population. However when the evolution is run using a multiobjective criterium (like pareto optimisation), the best net is chosen randomly amongst the network of rank 1.

The former storing method limits the disk space usage. However you might want to store the whole population either for restarting the algorithm from a given generation or to analyze every member of the generation. To add this feature, you can specify a storing period by setting the `prmt['restart']['freq']` parameter in the initialization file before launching the simulation. For example, if you set it to 50, the complete population will be stored every 50 generations in a python *shelve* named `restart_file`.

Other files created:

 - `data` is a quick access shelve file to elementary informations stored as lists at the following keys:
    - *generation*: index of the generation
    - *fitness*: fitness of the best network
    - *n_species*: number of species in the best network
    - *n_interactions*: number of interaction in the best network
- `parameters` is a copy of the parameter dictionnaries (defined for the non default in the initialization file) that were used during the simulation.
- `log_#.c` Copy of the input, fitness, history, etc. **c** files used for the simulation.

## Analysis Tools

In this section we will explore the built in functions that are bound to a *Simulation* object.


### custom_plot

Plots the seed two observables one against each other. The available observables are the ones present in the `data` file ("generation", "fitness", "n_species", "n_interactions").

```python
sim.seeds[1].custom_plot("generation","fitness")
# Similarly can use the shortcut
sim.custom_plot(1,"generation","fitness")
```

### plot_fitness
There also exists a method to plot the fitness directly:

```python
sim.seeds[1].show_fitness()
# Similarly can use the shortcut
sim.show_fitness(1)
```
### get_best_net
Get the best net found in a given generation (the function reads the `Bests_g.net` file and return the Network object)

```python
bestnet_g5_seed3 = sim.seeds[3].get_best_net(5)
# or
bestnet_g5_seed3 = sim.get_best_net(3,5)
```

### get_backup_net

If you want to extract a network from a entirely stored generation, you can use *get_backup_net*. Be careful though, not every population is stored in the `restart_file`.
```python
net8_g50_seed3 = sim.seeds[3].get_backup_net(50,8)
# Or
net8_g50_seed3 = sim.get_backup_net(3,50,8)
```

### stored_generation_indexes
 The *stored_generation_indexes* is a reminder of which generations are stored.

```python
lost_stored = sim.seeds[1].stored_generation_indexes()
# Or
lost_stored = sim.stored_generation_indexes(1)
```

### Running a network's dynamics

By construction φ-evo does not allow yet allow to quickly run the dynamics of a network. Namely a Network object has no method that directly returns the derivative from at a given state. Instead φ-evo has a method to write a **c** file containing the derivative function and that runs the dynamics on pre-defined inputs. This may seem a bit bulky but the software was initially written to evaluate the fitness of a given network and that is better done in **c**.

However the *Simulation* has the method *run_dynamics* to ease the access to the results the dynamics.

```python
net = sim.get_best_net(3,5)
dyn_buffer = sim.run_dynamics(net=net,trial=1)
```

This runs the dynamics that would be run in the evolution algorithm with the history and input **c** files you provided in the project directory. You can specify the number of trial you want to run if the dynamics is stochastic. The buffer returned by the function is dictionary where the main the "time" and "net" keys give you access to respectively the time vector and the network used for the run. The other keys are the index of the trial for which you want to access the data. Note that the buffer  is also stored in the *Simulation* object as *buffer_data*.

### Plotting the results of a dynamics

The simulation object allows you  to plot the two most obvious result you would like to see after running a dynamics:

1) The time course of the genes in a given cell with *Plot_TimeCourse*
2) The evolution of the genes along the system at a given time point with *Plot_Profile*

```python
sim.Plot_TimeCourse(trial_index=1,cell=1)
sim.Plot_Profile(trial_index=1,time=1)
```

## Notebook

To facilitate the use of the former functions, φ-evo as a class *Notebook* that is used to run them in a [jupyter notebook](https://jupyter.org). The nice think

The point of having a full class in the Notebook is for dependencies handling between widgets. For example when you load a new seed, you want that all the widget thats