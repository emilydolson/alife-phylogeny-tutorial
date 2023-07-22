# Practical tutorial

## Recording phylogenies

Now that we've established why you would want to track a phylogeny, let's talk about how!
Many ALife systems already have perfect phylogeny recording built in.
If you're using one of those, the built-in approach is generally best (unless you need to do something it wasn't designed for).
To illustrate this idea, we will discuss how to use built-in phylogeny tracking in DEAP, a popular Python library for evolutionary computation.

:::{attention}
Be aware that different ALife systems can make subtly different assumptions when recording phylogenies. Make sure you understand exactly how your system is doing its tracking.
:::

If your system doesn't have built-in phylogeny tracking that supports your needs, you will need to add your own. There are two main approaches to recording phylogenies in ALife systems: 1) perfectly recording them, 2) reconstructing them after the fact.

If you don't want to implement these yourself, you can use a pre-existing library.
For perfect tracking, the only general purpose library we are currently aware of is Phylotracklib/Phylotrackpy. It should work in most C++ or Python contexts that do not involve recombination/crossover/sexual reproduction. For reconstruction, our (biased, but informed) opinion is that the best approach is hstrat. We will cover both of these techniques in this tutorial.

:::{note}
Reconstruction could potentially also be accomplished using bioinformatics-style approaches, but "here be dragons".
:::


### DEAP (example of using built-in system tools)

[DEAP](https://deap.readthedocs.io) is a popular Python library for evolutionary computation, which has simple built-in phylogeny tracking via the [deap.tools.History](https://deap.readthedocs.io/en/master/api/tools.html#history) class. It tracks phylogenies at the individual level and can handle recombination. However, because it does not handle more abstract taxon representations or pruning, it can use a lot of memory.

:::{admonition} Tip: key-words
:class: tip

One of the biggest challenges in finding built-in phylogeny trackers can be figuring out what word to search for. In DEAP, the phylogeny tracker is called "history". Other words to look for include "systematics", "genealogy", "lineage", "ancestry", "pedigree", and of course "phylogeny".
:::

For example, let's consider the simple [onemax example in DEAP](https://github.com/DEAP/deap/blob/3f8f09fc7248e7adbb28aeafc97cf81dbaa226bd/examples/ga/onemax.py). We could add phylogeny tracking by doing the following:

TODO: Test this!

```python
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator: 
#   define 'attr_bool' to be an attribute ('gene')
#   which corresponds to integers sampled uniformly
#   from the range [0,1] (i.e. 0 or 1 with equal
#   probability)
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers:
#   define 'individual' to be an individual
#   consisting of 100 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, 100)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# the goal ('fitness') function to be maximized
def evalOneMax(individual):
    return sum(individual),

#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------

#----------
# Phylogeny set-up
#----------

# Create the "History" object, which will hold the phylogeny
history = History()

# Decorate the variation operators so that each time a new
# individual is created, `history` gets notified and can
# record the event correctly
toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate", history.decorator)


def main():
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=300)

    # Notify phylogeny of initial population members
    history.update(pop)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 100 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

 
    print("-- End of (successful) evolution --")

    # TODO: output this in ALife std format
    history.genealogy_tree

if __name__ == "__main__":
    main()
```

### Phylotrack

Phylotrack refers collectively to the C++ library Phylotracklib and the Python wrapper around it, Phylotrackpy. The two function the same way, just in different languages. It can only record asexual phylogenies (each taxon has a single parent; no recombination), but is otherwise flexible.

#### Creating a systematics object

The most important choice you need to make when using Phylotrack is how you want to define taxa.
To describe your taxon definitions, you must write a function that takes a member of your population as input and returns the central piece of information that determines the taxon that that object should belong to.
When a new organism is born, its taxon will be compared to its parent's taxon. If they are different, a new node is created in the phylogeny.

For example, to build a phylogeny based on genotypes, you could do the following:

```py
from phylotrackpy import systematics

# Assuming that the objects being used as organisms have a member variable called genotype that stores their genotype,
# this will created a phylogeny based on genotypes
sys = systematics.Systematics(lambda org: org.genotype)
```

There are a couple of other decisions that you also need to make at this point. The first is whether you want to have your phylogeny automatically prune itself which lineages go extinct. Pruning will keep the memory footprint of your program much more manageable and can be done efficiently. The only downside is that you're throwing away information (but it's information you're unlikely to need in many cases). By default, pruning is on. However, you can disable it by passing `True` to the `store_all` keyword argument in the constructor.

The second decision is slightly trickier. Once you start adding organisms to the systematics manager, it will create `Taxon` objects associated with each one to keep track of which taxon it is part of. You will need to use these taxon objects when adding future organisms, to specify which taxon their parent was part of. If you have control over your organism class, it is likely that the easiest option is to add a `self.taxon` attribute and store the taxon there. However, if you cannot add arbitrary data to your organism class, keeping track of taxon objects can get annoying. In this case, phylotrackpy can manage them internally. To learn more about this approach, look up "position tracking" in the documentation.

Once you have created the systematics object, you just need to do two things: 1) notify it when something is born, and 2) notify it when something dies.

#### Notifying the systematics object of births

You must notify the systematics manager of births using the `add_org` family of functions. These functions require that you provide the newly born organism as well as either the taxon object of its parent or the position of its parent (if the systematics manager is tracking positions).

Example of tracking taxa as object attributes (assume we're building on our example above, and already have created a systematics manager called `sys`):

```py
# Do whatever you would normally do to create your first organism
# Here, we're assuming we can just call a constructor called Organism()
my_org = Organism()

# Notify systematics manager of this organism's birth
# This is the first org, so it doesn't have a parent
# so we do not pass a second argument/
# add_org will return this organism's taxon object, which we
# store in my_org.taxon for future reference
my_org.taxon = sys.add_org(my_org)

# Assume stuff happens here that leads to my_org having offspring
# Here, we'll pretend that our organism class has a Reproduce method that
# returns a new offspring organism. You should handle this however you
# normally would
org_2 = my_org.Reproduce()

# Notify the systematics manager of org_2's birth. Since it has a parent,
# we pass the taxon of that parent in as the second argument
# Again, we store the returned taxon object in the organism for safe keeping
org_2.taxon = sys.add_org(org_2, my_org.taxon)

```

An example of tracking positions is coming soon. For now, feel free to contact us with questions!

#### Notifying the systematics object of deaths

You must notify the systematics manager of deaths using the `remove_org` family of functions. 

As an example (again, building on the previous examples):
```py
# Assume stuff happens that causes my_org to die

# We notify the systematics manager that this has happened by calling remove_org
# Note that remove_org takes the taxon of the dead organism as an argument, not
# the organism itself
sys.remove_org(my_org.taxon)

```

### Hstrat

## Phylogeny Data Formats

The most popular format for representing phylogenies in biology is newick format, which represents ancestry relationships with nested parentheses. ALife phylogenies can be represented in this format, but doing so can be unwieldy, as ALife phylogenies are often very large and the nested format makes it impossible to operate on individual taxa without loading the entire tree.

For this reason, the ALife Phylogeny Data Standard Format was created. We will use that data format here for easy interoperability. Converters exist between ALife standard format and other phylogeny formats.

## Phylogeny Statistics

A wealth of statistics can be calculated to describe the topology of phylogenies.

## Phylogeny Visualizations

Visualizing phylogenies is a powerful way to build intuition for the evolutionary dynamics that are occurring in an ALife system. There are a variety of approaches:

### Trees

Drawing a tree is an obvious way to represent a phylogeny. However, there are a large number of choices that go into this seemingly straightforward approach.

#### Branch lengths

Branch lengths can be:

- Literal time
- Number of mutational steps
- Number of unifurcations along that node (if you have compressed them)

#### Tree layout

- Circular
- Vertical or horizontal
- Axes (if using time, it often makes sense to log it)

#### Node/edge colors

Coloring edges and node based on properties of the taxa they correspond to can make patterns jump out.

#### Node shape

There are also various variations on trees, which often involve replacing nodes (traditionally represented as circles), with other objects. In bioinformatics, pie charts are often used as a technique for  conveying uncertainty. When using time as branch lengths/node positions, it can make sense to replace nodes with rectangles representing the lifespans of various taxa.

#### Visualizing large trees

A challenge with visualizing ALife phylogenies is that they are often huge. This is not a solved problem, but some strategies include:

- Collapsing parts of the tree (these are often represented with large triangles)
- Removing taxa that never had a large population size (or descendants with large population sizes)

### Muller Plots (a.k.a. Fish Plots)

While not purely a phylogeny visualization, Muller plots are a powerful technique for showing fluctuations in the population sizes of different lineages over time.

To make a Muller plot, we need two things: 1) a phylogeny showing how a set of taxa are related to each other, and 2) a time series data-set indicating the number of individuals of each taxon at each point in time.