'''This script shows how, by adjsting the parameter Recovered_Iters, we can transform the previous
    SIR model to an SIRS model, where we allow Recovered persons to become susceptible again.

    Created By: Nicholas L. Wood PhD
    Institution: United States Naval Academy
    E-mail: nwood@usna.edu
    Date Created: 04/06/2020
    Date Modified: 04/06/2020
'''

from InfectiousDisease import Country, Simulation

#Create a 100x100 country
country = Country(N = 100)

#Add 500 susceptible persons to the country who move randomly
for i in range(500):
    country.Add_Person('S', MoveType = 'Drunkard')

#Add a single infected person to the country who moves randomly
for i in range(5):
    country.Add_Person('I', MoveType = 'Random')

#Set the model parameters
radius = 1
risk = 0.10
Infected_Iters = 100
Recovered_Iters = 125
hospital_capacity = 0.40
    
#Create the simulation
Sim = Simulation(country, radius, risk, Infected_Iters, Recovered_Iters, hospital_capacity)

#Run!
Sim.Run()
