# Phylogenies: how and why to track them in artificial life

(A tutorial at ALife 2023)

Phylogenies (i.e., ancestry trees) group extant organisms by ancestral relatedness to render the history of hierarchical lineage branching events within an evolving system. These relationships reveal the evolutionary trajectories of  populations through a genotypic or phenotypic space. As such, phylogenies open a direct window through which to observe ecology, differential selection, genetic potentiation, emergence of complex traits, and other evolutionary dynamics in artificial life (ALife) systems. In evolutionary biology, phylogenies are often estimated from the fossil record, phenotypic traits, and extant genetic information. Although substantially limited in precision, such phylogenies have profoundly advanced our understanding of the evolution of life on Earth. In digital systems, we often have the ability to create perfect (or near perfect) phylogenies that reveal the step-by-step process by which evolution unfolds. However, phylogeny tracking and phylogeny-based analyses are not yet commonplace in ALife. Fortunately, a number of software tools have recently become available to facilitate such analyses, such as [Phylotrackpy](https://phylotrackpy.readthedocs.io/en/latest/), [DEAP](https://deap.readthedocs.io/en/master/api/tools.html?highlight=history#deap.tools.History), [Empirical](https://empirical.readthedocs.io/en/latest/), [MABE](https://github.com/Hintzelab/MABE), and [hstrat](https://hstrat.readthedocs.io/en/latest/?badge=latest).

Biologists have developed many sophisticated and powerful phylogeny-based analysis techniques. For example, existing work uses properties of tree topology to infer characteristics of the evolutionary processes acting on a population. With an understanding of the differences between biology and artificial life, these approaches can be imported into ALife systems. For example, phylodiversity metrics can be used to detect diversity-maintaining ecological interactions and ongoing generation of significant evolutionary innovations.

This tutorial will provide an introduction to phylogenies, how to record them in digital systems, and use cases for phylogenetic analyses in an artificial life context. We will open with a quick discussion of prior research enabled by and based on phylogenies in digital evolution systems. We will then survey existing phylogeny software tools and lead interactive tutorials on tracking phylogenies in both traditional and distributed computing environments. Next, we will demonstrate measurements and data visualizations that phylogenetic data enables, including Muller plots, phylogenetic topology metrics, and annotated phylogeny visualizations. Lastly, we will discuss open questions and future directions related to phylogenies in artificial life.

## When & Where

This tutorial session is organized as part of the [2023 Conference on Artificial Life](https://2023.alife.org), held July 24-28 in Sapporo, Japan at Hokkaido University.

Time & room assignment TBD.
Hybrid attendance options will be provided.

## Organizers

- [Emily Dolson](https://cse.msu.edu/~dolsonem/), *Assistant Professor*, Michigan State University
- [Matthew Andres Moreno](https://mmore500.com/), *Postdoctoral Fellow*, University of Michigan
- [Alexander Lalejini](https://lalejini.com/), *Assistant Professor*, Grand Valley State University

## Tutorial Outline (tentative)

- Introduction to what phylogenies are and considerations for using them in artificial life contexts
- Practical tutorial on measuring phylogenies:
  - Brief DEAP demo
  - Code-Along Tutorial on adding phylogeny tracking to your ALife platform using Phylotrackpy/Empirical
  - Tutorial on using hstrat for distributed phylogeny tracking
- Introduction to measurements, statistics, and data visualizations you can do with phylogenies
- Practical tutorial on statistics + data visualizations
  - Muller plots
  - Metrics
