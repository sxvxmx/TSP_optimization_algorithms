import random
import struct
import numpy as np


class Gen:
    def __init__(self, func: callable, bounds: list[int,int], population_size:int, mutation_chance:float = 0.2):
        self.function = func
        self.bounds: tuple = bounds
        self.population_size: int = population_size + population_size%2
        self.min_value: float = None
        self.current_population: list = []
        self.vpopulation: list = []
        self.function_values: list = []
        self.min_point = None
        self.mutchance: float = mutation_chance

    def getpopul(self) -> list[list[int]]:
        return self.current_population
    
    def getfuncval(self) -> list[list[int]]:
        return self.function_values
    
    def getmin(self) -> float:
        return self.min_value
    
    def getpoint(self) -> list:
        return self.min_point
    
    def setbounds(self, b:list[int]):
        self.bounds = b
        
    def setpsize(self,s:int):
        self.population_size = s
        
    def setmchance(self,m:float):
        self.mutchance = m
    
    def setmode(self, q:int):
        if q == 1:
            self.mode = self.__discr
        else:
            self.mode = self.__real 
    
    def rpopulation(self) -> None:
        for i in range(self.population_size):
            a, b = random.uniform(self.bounds[0],self.bounds[-1]),random.uniform(self.bounds[0],self.bounds[-1])
            self.current_population.append([a, b])
            self.function_values = np.append(self.function_values, self.function(a, b))
            self.vpopulation.append([self.function_values[-1], self.current_population[-1]])
        self.vpopulation = sorted(self.vpopulation)
        self.min_value = self.vpopulation[0][0]
        self.min_point = self.vpopulation[0][-1]

    def npopulation(self) -> None:
        self.mode()
        self.vpopulation = sorted(self.vpopulation)
        self.vpopulation = self.vpopulation[:self.population_size]
        self.current_population = list(map(lambda p: p[-1], self.vpopulation))
        self.function_values = np.array((list(map(lambda q: q[0], self.vpopulation))))
        self.min_value = self.vpopulation[0][0]
        self.min_point = self.vpopulation[0][-1]

    #Single-point crossover
    def __discr(self):
        for i in range(int(self.population_size/2)):
            p1 = [''.join('{:0>8b}'.format(c) for c in struct.pack('!f', self.current_population[i][0])),''.join('{:0>8b}'.format(c) for c in struct.pack('!f', self.current_population[i][-1]))]
            p2 = [''.join('{:0>8b}'.format(c) for c in struct.pack('!f', self.current_population[self.population_size - i-1][0])),''.join('{:0>8b}'.format(c) for c in struct.pack('!f', self.current_population[self.population_size-i-1][-1]))]
            s = random.randrange(3,int(len(p1[0]) - 15))
            mem = [p1[0][s:], p1[-1][s:]]
            p1[0] = struct.unpack('!f',struct.pack('!I', int(p1[0][:s] + p2[0][s:], 2)))[0] + self.__mutation()
            p1[-1] = struct.unpack('!f',struct.pack('!I', int(p1[-1][:s] + p2[-1][s:], 2)))[0] + self.__mutation()
            p2[0] =  struct.unpack('!f',struct.pack('!I', int(p2[0][:s] + mem[0], 2)))[0] + self.__mutation()
            p2[-1] =  struct.unpack('!f',struct.pack('!I', int(p2[1][:s] + mem[1], 2)))[0] + self.__mutation()
            self.vpopulation.append([self.function(p1[0],p1[-1]),[p1[0],p1[-1]]])
            self.vpopulation.append([self.function(p2[0],p2[-1]),[p2[0],p2[-1]]])

    #Intermediate recombination
    def __real(self):
        for i in range(int(self.population_size/2)):
            a = [random.uniform(-0.25,1.25),random.uniform(-0.25,1.25),random.uniform(-0.25,1.25),random.uniform(-0.25,1.25)]
            for o in range(2):
                self.vpopulation.append([self.function(self.__norm(self.current_population[i][0]+a[o]*(self.current_population[i][0] - self.current_population[i+1][0]) + self.__mutation()),
                                                       self.__norm(self.current_population[i][-1]+a[o+1]*(self.current_population[i][-1] - self.current_population[i+1][-1])+ self.__mutation())),
                                         [self.__norm(self.current_population[i][0]+a[o]*(self.current_population[i][0] - self.current_population[i+1][0]) + self.__mutation()),
                                         self.__norm(self.current_population[i][-1]+a[o+1]*(self.current_population[i][-1] - self.current_population[i+1][-1])+ self.__mutation())]])
    
    def __mutation(self) -> float:
        if random.uniform(0,1) > self.mutchance:
            return random.uniform(self.bounds[0],self.bounds[-1])
        else:
            return 0
    
    def __norm(self, val) -> float:
        if val < self.bounds[0]:
            return self.bounds[0]
        if val > self.bounds[1]:
            return self.bounds[1]
        return val