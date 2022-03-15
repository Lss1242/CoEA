# Competitive CoEA search of the one max / MaxMinHill optimization problem
from mimetypes import init
from operator import ge
from numpy.random import randint
from numpy.random import rand
from numpy.random import randn
from numpy.random import seed
import random
import time
import copy
import pandas as pd
import numpy as np
from pyparsing import java_style_comment


# Initialization2 (n_pop: number of population; m: length of bitstrings) 
def initial_generationCoEA(n_pop,m): 
    
    population=[]
        
    for _ in range(n_pop):
        genes = []
        for j in range(m):
            genes.append(random.randint(0,1))   # Uniform distribution on {0,1}
        f = oneMax(genes)                    # fitness evaluation
        ind = {'genes':genes, 'OneMax':f} 
        population.append(ind)
        
    return population

# fitness Evaluation (take OneMax function as an example)
def oneMax(genes):
    numberOfOne = 0
    
    for gene in genes:
        if gene==1:
            numberOfOne = numberOfOne + 1
    return numberOfOne

# a, b are two parameters, m is length of bitstrings    
def MaxMinHill(a,b,genes1,genes2,m):
    value=abs( (b-oneMax(genes1)/m)*(a-oneMax(genes2)/m)  )- abs(b-oneMax(genes1)/m ) + abs(a-oneMax(genes2)/m)
    
    return value

def fitness(genes1,genes2):
    a=0.2
    b=0.4
    m=10
    return MaxMinHill(a,b,genes1,genes2,m)
     
# mutation operator
def mutate(genes, r_mut):
    for j in range(len(genes)):
        if random.random()< r_mut:
            if genes[j]==1:
                genes[j]=0
            else:
                genes[j]=1

    return genes

# Competitive Selection for two individuals
def CompetitiveSelection(ind1, ind2,r_mut):
    if fitness(ind1,mutate(ind2,r_mut)) <= fitness(ind1,ind2):
            ind2 = mutate(ind2,r_mut)
    else:
            ind2 = ind2
    
    if fitness(ind1,ind2) <= fitness(mutate(ind1,r_mut),ind2):
            ind1 = mutate(ind1,r_mut)
    else:
            ind1 = ind1
            
    return [ind1,ind2]
     
# Tournament Selection
def TournamentSelection(population,n_pop):
    parents = []
    
    for i in range(n_pop):
        ind1 = population[random.randint(0, n_pop-1)]
        ind2 = population[random.randint(0, n_pop-1)]
        winner = {}
        if ind1['fitness']<=ind2['fitness']:
            winner = {'genes':ind1['genes']}
        else:
            winner = {'genes':ind2['genes']}
        parents.append(winner)
        
    return parents
 
# Reproduction 2 (r_cross: rate of crossover; r_mut: mutation rate; m: length of bitstring) 
# This mutation operator only mutates one inviduals in single population once
def reproduction(parents,r_cross, r_mut, m):
    offsprings = []
    i = 0
    # crossover range(0, n_pop, 2)
     # crossover
    for i in range(0,len(parents),2):
        parent1 = parents[i]
        parent2 = parents[i+1]
        child1 = {}
        child2 = {}
        if rand() < r_cross:
            child1['genes'] = parent1['genes'][0:int(m/2)] + parent2['genes'][int(m/2):m]
            child2['genes'] = parent2['genes'][0:int(m/2)] + parent1['genes'][int(m/2):m]
        else:            
            child1=parent1
            child2=parent2
            
        offsprings.append(child1)
        offsprings.append(child2)
        
    # mutation
    for offspring in offsprings:
        for j in range(len(offspring['genes'])):
            if random.random()< r_mut:
                if offspring['genes'][j]==1:
                    offspring['genes'][j]=0
                else:
                    offspring['genes'][j]=1

    return offsprings

                  
# Competitve Co (1+1) EA (fitness: fitness function; n_iter: number of iterations; n_pop: number of population; r_cross: rate of crossover; m: number of bitstrings)
def CoEA(fitness, n_iter, n_pop, r_mut,m):
    
    population1 = initial_generationCoEA(n_pop,m)
    population2 = initial_generationCoEA(n_pop,m)

    # Keep track of the best solution & start with an initial point
    best1 = 0
    best2 = 0
    best_eval = fitness(population1[best1]['genes'], population2[best2]['genes']) 

    for gen in range(n_iter):
        
        score = []

        
     # evaluate all candidates in the population
        for i in range(len(population1)):
            for j in range(len(population2)):
                f = fitness(population1[i]['genes'], population2[j]['genes'])
                candidate ={'pairs':[i,j], 'fitness': f}
                score.append(candidate)

                
     # check for new best solution
        for k in range(len(score)):
            if score[k]['fitness']>best_eval:
                best1,best2, best_eval = score[k]['pairs'][0],score[k]['pairs'][1],score[k]['fitness'] # best1,2 refer to their index
        
        ind1 = population1[best1]['genes']
        ind2 = population2[best2]['genes']
        
        offsprings = CompetitiveSelection(ind1,ind2,r_mut)
        
        population1 = [{'genes': offsprings[0],'OneMax': oneMax(offsprings[0])}]
        population2 = [{'genes': offsprings[1],'OneMax': oneMax(offsprings[1])}]
        #print(population1)
        #print(population2)
            
    return [population1, population2, best_eval]
    

# define the total iterations
n_iter = 10
# define the population size (1+1)-CoEA so size is 1 on each population
n_pop = 1
# crossover rate
r_cross = 0
# mutation rate
r_mut = 0.5
m=10
time1=time.time()
best1, best2, score = CoEA(fitness, n_iter, n_pop, r_mut, m)
time2=time.time()
#print(best,score)
#best.sort()
#print(best)
print('total runtime:', time2-time1)
print('best individual pairs: ',[best1,best2])
print(' fitness :', score)
