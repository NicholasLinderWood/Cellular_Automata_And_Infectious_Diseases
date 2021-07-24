'''This script contains class definitions which will be used by other scripts to model the spreading
    of an infectious disease through the ficticious country of Elbonia. Below are descriptions of
    each class.

    Person:
        Each instance of the Person class represents someone who lives in Elbonia. Each person has a location
        (the attribute Loc) indicating the row and column where that person is currently located. Each person additionally
        has the attribute State, indicating whether that peron is Susceptible (S), Infected (I), or Recovered (R). Finally, each
        person has an attribute MoveType, which will be used by the method Move, which dictates how this person moves
        around Elbonia.

    Country:
        Each instance of the Country class represents a country as a 2-D Grid of size NxN. A country consists of a population of
        citizens which can be added to the country using the method Add_Person. The method Move_People moves each person in
        the country according to that persons MoveType, and the method Update_People updates the people in the population,
        where a susceptible person can become sick, an infected person can recover, and a recovered person can become
        susceptible again. These updates all happen according to parameters which can be tweaked - see the Simulation class
        below for more details.

    Simulation:
        Each simulation class consists of a country and a set of attributes which define the how the disease spreads. The attribute
        radius is a positive integer defining the radius of the Moore neighborhood whereby a person can come into contact with those
        neighbors and possibly become infected. The attribute risk is a real number in (0, 1] which indicates the risk of becoming infected per
        infected person in your neighborhood. The attribute Infected_Iters is a positive integer indicating the number of iterations required
        for an infected person to become recovered. The attribute Recovered_Iters is similarly the number of iterations required for a recovered
        person to become susceptible again. Finally the attribute hospital_capacity is a real number in [0. 1] which indicates the proportion of
        the population which can be serviced by Elbonias healthcare system without being overrun.

        The method Run, runs the simulation with the given parameters.


    Simply running this script will give an example of the worst-case scenario of the SIR model.



    Created By: Nicholas L. Wood PhD
    Institution: United States Naval Academy
    E-mail: nwood@usna.edu
    Date Created: 04/05/2020
    Date Modified: 04/06/2020
'''









from random import choice, randint, random
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.colors import ListedColormap
from math import sqrt
import numpy as np


##############################################################################################################
##############################################################################################################
##############################################################################################################
class Person:

    def __init__(self, State, row, column, MoveType):
        '''State is a single character string - either 'S' (susceptible), 'I' (infected), or 'R' (recovered) - indicating
            the state of the person. row and column are integers indicating the location of the person on the two-dimensional
            grid. MoveType will define how this person moves. If the person is initialized as Infected or Recovered, start
            the appropriate counter to determine when they get better or become susceptible again.'''

        self.State = State
        self.Loc = [row, column]
        self.MoveType = MoveType

        if State == 'I':
            self.Infected_Iters = 0

        elif State == 'R':
            self.Recovered_Iters = 0


    def Move(self, N):
        '''Move the person by updating his location according to his MoveType. If you want to define
            your own way in which people move, define them for the given MoveType here.'''
        

        if self.MoveType == 'Random':
            #Every iteration a Random mover will teleport to a randomly selected location in the country.

            row = randint(0, N-1)
            col = randint(0, N-1)

            self.Loc = row, col

        elif self.MoveType == 'Drunkard':
            #Every iteration the Drunkard mover, randomly moves up, down, left, or right one square,
            #or perhaps not at all.

            ind = choice([0, 1])
            delta = choice([-1, 0, 1])

            self.Loc[ind] += delta

            if self.Loc[ind] < 0:
                self.Loc[ind] = N-1

            elif self.Loc[ind] == N:
                self.Loc[ind] = 0

        elif self.MoveType == 'Isolate':
            #Every iteration the Isolated mover does not move.

            Move = False

        else:
            raise ValueError(f'MoveType {MoveType} not defined!')
##############################################################################################################
##############################################################################################################
##############################################################################################################



        
##############################################################################################################
##############################################################################################################
##############################################################################################################
class Country:

    def __init__(self, N = 100):
        '''N is a positive integer indicating the size of the country. You can add people to the country using the Add_Person method.
            The methods Move_People, Update_People, and GetInfectedNeighbors are used by the Simulation Class.'''

        #Set the size of the country
        self.N = N

        #Create an empty list which will contain the people living in this country
        self.People = []


    def Add_Person(self, State, row = None, column = None, MoveType = None):
        '''If no row or column is given, the person is added randomly to the country. If no MoveType is given,
            then this will be a random mover.'''

        N = self.N

        if row == None:
            #Randomly chose a row
            row = randint(0, N-1)

        if  column == None:
            #Randomly chose a column
            column = randint(0, N-1)

        if MoveType == None:
            MoveType = 'Random'

        #Add this person to the list of people.
        self.People.append(Person(State, row, column, MoveType))


    def Move_People(self):
        #Move each person in the country.
        for P in self.People:
            P.Move(self.N)

    def GetInfectedNeighbors(self, radius = 1):
        '''Determines the number of infected neighbors (within Moore Neighborhood radius r) on each location
            in the city and returns that information in an NxN matrix.'''

        #First find all of the infected persons
        pI = [P for P in self.People if P.State == 'I']

        #Create a Grid based on the infected persons locations
        N = self.N
        Grid = np.zeros((N, N))

        #For each infected person, add 1 to the location in the Grid
        for p in pI:
            r, c = p.Loc
            Grid[r][c] += 1

        #Now create an extended Grid which will hold the number of infected neighbors at each location
        ExtendedGrid = np.zeros((N + 2*radius, N + 2*radius))

        #Insert the Grid into the ExtendedGrid
        ExtendedGrid[radius:N+radius, radius:N+radius] = Grid

        #Now the last radius rows become the first radius rows, and so forth.
        #Don't forget the corners!

        #Make the first rows the last rows
        ExtendedGrid[0:radius, radius:N+radius] = Grid[-radius:, :]

        #Make the last rows the first rows
        ExtendedGrid[N:N+radius, radius:N+radius] = Grid[0:radius, :]

        #Make the first columns the last columns
        ExtendedGrid[radius:N+radius, 0:radius] = Grid[:, -radius:]

        #Make the last columns the first columns
        ExtendedGrid[radius:N+radius, N:N+radius] = Grid[:, 0:radius]

        #Now do the corners

        #Top Left = Bottom Right
        ExtendedGrid[0:radius, 0:radius] = Grid[-radius:, -radius:]

        #Bottom Right = Top Left
        ExtendedGrid[-radius:, -radius:] = Grid[0:radius, 0:radius]

        #Top Right = Bottom Left
        ExtendedGrid[0:radius, -radius:] = Grid[-radius:, 0:radius]

        #Bottom Left = Top Right
        ExtendedGrid[-radius:, 0:radius] = Grid[0:radius, -radius:]

        #Now add up the number of Infected Neighbors at each cell (including the cell itself)
        Neighbors = np.zeros((N,N))
        for i in range(radius+2):
            for j in range(radius+2):
                Neighbors += ExtendedGrid[i:N+i, j:N+j]

        return Neighbors
            

    def Update_People(self, risk, radius, Infected_Iters, Recovered_Iters):
        '''For each suceptible person, determine the number of infected persons (nI) in their Moore neighborhood of the given radius.
            That susceptible person will become infected with a probability of nI*risk. If any Infected person has been infected for Infected_Iters
            number of iterations, he becomes Recovered. Similarly, and Recovered person who has been recovered for Recovered_Iters iterations
            becomes susceptible again.'''

        #Find each type of person in the country.
        Susceptible = [P for P in self.People if P.State == 'S']
        Infected = [P for P in self.People if P.State == 'I']
        Recovered = [P for P in self.People if P.State == 'R']

        #For each location in the country, determine the number of infected neighbors.
        Neighbors = self.GetInfectedNeighbors(radius)

        #Update each infected person
        for pI in Infected:
            pI.Infected_Iters += 1
            if pI.Infected_Iters == Infected_Iters:
                pI.State = 'R'
                pI.Recovered_Iters = 0

        #Update each susceptible person
        for pS in Susceptible:
            row, col = pS.Loc
            nI = Neighbors[row][col]

            if random() < nI*risk:
                pS.State = 'I'
                pS.Infected_Iters = 0

        #Update each recovered person
        for pR in Recovered:
            pR.Recovered_Iters += 1
            if pR.Recovered_Iters == Recovered_Iters:
                pR.State = 'S'
##############################################################################################################
##############################################################################################################
##############################################################################################################




##############################################################################################################
##############################################################################################################
##############################################################################################################
class Simulation:

    def __init__(self, country, radius = 1, risk = 0.10, Infected_Iters = 100, Recovered_Iters = 1000000000, hospital_capacity = 0.40):
        '''country is a country object on which we will run the simulation. radius, risk, Infected_Iters, Recovered_Iters, and hospital_capacity are
            all parameters for the simulation. The method Run will run the simulation.'''

        #The country in which the people live
        self.country = country

        #store the number of iterations for when we run the simulation
        self.iters = 0

        #The radius of the Moore Neighborhood
        self.radius = radius

        #The risk of getting infected per infected person within the Moore radius
        self.risk = risk

        #The number of iterations required before an infected person recovers
        self.Infected_Iters = Infected_Iters

        #The number of iterations required before a recovered person becomes susceptible again
        self.Recovered_Iters = Recovered_Iters

        #The hospital capacity, given as a proportion of the population
        self.hospital_capacity = hospital_capacity


    def Run(self):
        '''Run the simulation!!!'''

        #Create the figure
        fig = plt.figure(figsize = (6, 4))

        #The left axis will be for plotting the distribution over time
        #The right axis will be for plotting the people moving
        #Below we set many features of these two axes
        ax_Left = fig.add_subplot(121)
        ax_Left.set_ylim([0, 1.01])
        ax_Left.set_xlabel('Time', fontsize = 10)
        ax_Right = fig.add_subplot(122)
        ax_Right.set_title('The Country\nof Elbonia', fontsize = 10)
        ax_Right.set_xticks([])
        ax_Right.set_xticklabels([])
        ax_Right.set_yticks([])
        ax_Right.set_yticklabels([])
        ax_Right.tick_params(axis=u'both', which=u'both',length=0)


        #Colormap
        #Let 0 be white (unoccupied), 1 be Susceptible, 2 be Infected, 3 be Recovered
        cmap = ListedColormap(['w', 'y', 'r', 'b'])

        #Dictionary for determine what number to give each cell in the grid.
        StateDict = {'S':1, 'I':2, 'R':3}

        #Initialize several data series which will be updated over time as the simulation runs
        tData = [self.iters]
        SData = [len([P for P in self.country.People if P.State == 'S'])/len(self.country.People)]
        IData = [len([P for P in self.country.People if P.State == 'I'])/len(self.country.People)]
        RData = [len([P for P in self.country.People if P.State == 'R'])/len(self.country.People)]
        HCData = [self.hospital_capacity]

        


        #The function below is used by FuncAnimation to update the plot each frame
        def func(frame):

            #Move all the people in the country
            self.country.Move_People()

            #Update the people in the country
            self.country.Update_People(self.risk, self.radius, self.Infected_Iters, self.Recovered_Iters)

            #add one to the number of iterations
            self.iters += 1

            #Update the series data that are plotted
            tData.append(self.iters)
            SData.append(len([P for P in self.country.People if P.State == 'S'])/len(self.country.People))
            IData.append(len([P for P in self.country.People if P.State == 'I'])/len(self.country.People))
            RData.append(len([P for P in self.country.People if P.State == 'R'])/len(self.country.People))
            HCData.append(self.hospital_capacity)

            #Create the grid
            Grid = np.zeros((self.country.N, self.country.N))

            #For each person in the country, paint his square according to his state
            for P in self.country.People:
                Grid[P.Loc[0]][P.Loc[1]] = StateDict[P.State]


            #Set the data
            mat.set_data(Grid)
            lineS.set_data(tData, SData)
            lineI.set_data(tData, IData)
            lineR.set_data(tData, RData)
            lineHC.set_data(tData, HCData)

            #Update aspect ratio and xaxis limit
            ax_Left.set_xlim([0, self.iters])
            ax_Left.set_aspect(self.iters)

            #If there are zero infected persons, stop the simulation
            if IData[-1] == 0:
                ani.event_source.stop()


        #Initialize the Grid
        Grid = np.zeros((self.country.N, self.country.N))

        #For each person in the city, paint his square according to his state
        for P in self.country.People:
            Grid[P.Loc[0]][P.Loc[1]] = StateDict[P.State]

        #Initialize the plots on the first frame
        mat = ax_Right.matshow(Grid, cmap = cmap, vmin = 0, vmax = 3)
        lineS, = ax_Left.plot(tData, SData, 'y', label = 'S')
        lineI, = ax_Left.plot(tData, IData, 'r', label = 'I')
        lineR, = ax_Left.plot(tData, IData, 'b', label = 'R')
        lineHC, = ax_Left.plot(tData, HCData, 'k--')

        #Create the animation
        ani = animation.FuncAnimation(fig, func, interval = 25, repeat = False)

        #Legend
        ax_Left.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),
          fancybox=True, shadow=True, ncol=3, fontsize = 10)

        #Animate the simulation!
        plt.show()
##############################################################################################################
##############################################################################################################
##############################################################################################################
        



##############################################################################################################
##############################################################################################################
##############################################################################################################
if __name__ == '__main__':

    #Run the standard SIR model
    country = Country(N = 100)

    #Create a 500 susceptible persons who will move about the city randomly
    for i in range(700):
        country.Add_Person('S', MoveType = 'Random')

    #Create a single infected person who also moves about randomly
    country.Add_Person('I', MoveType = 'Random')

    #Set the model parameters
    radius = 1
    risk = 0.075
    Infected_Iters = 100
    Recovered_Iters = 75
    hospital_capacity = 0.40
    
    Sim = Simulation(country, radius, risk, Infected_Iters, Recovered_Iters, hospital_capacity)

    Sim.Run()
##############################################################################################################
##############################################################################################################
##############################################################################################################

    






            

        
        
