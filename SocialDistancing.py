''' This script is the same as the worst-case scenario except it makes the country a little bigger to
        simulate social distancing.

    Created By: Nicholas L. Wood PhD
    Institution: United States Naval Academy
    E-mail: nwood@usna.edu
    Date Created: 04/06/2020
    Date Modified: 04/06/2020
'''

from InfectiousDisease import Country, Simulation

#Create a 150x150 country
country = Country(N = 150)

#Add 500 susceptible persons to the country who move randomly
for i in range(500):
    country.Add_Person('S', MoveType = 'Random')

#Add a single infected person to the country who moves randomly
country.Add_Person('I', MoveType = 'Random')

#Set the model parameters
radius = 1
risk = 0.10
Infected_Iters = 100
Recovered_Iters = 1000000000
hospital_capacity = 0.40
    
#Create the simulation
Sim = Simulation(country, radius, risk, Infected_Iters, Recovered_Iters, hospital_capacity)

#Run!
Sim.Run()
