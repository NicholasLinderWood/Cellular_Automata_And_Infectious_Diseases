'''In this scenario we assume that most people move according to a random walk but a small proportion
    travel extensively.

    Created By: Nicholas L. Wood PhD
    Institution: United States Naval Academy
    E-mail: nwood@usna.edu
    Date Created: 04/06/2020
    Date Modified: 04/06/2020
'''

from InfectiousDisease import Country, Simulation

#Create a 100x100 country
country = Country(N = 100)

#Add 400 susceptible persons to the country who move drunkenly
for i in range(400):
    country.Add_Person('S', MoveType = 'Drunkard')

#Add 100 susceptible persons who move randomly
for i in range(100):
    country.Add_Person('S', MoveType = 'Random')

#Add a single infected person to the country who moves Drunkenly
country.Add_Person('I', MoveType = 'Drunkard')

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
