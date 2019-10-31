#TAG
###### An attempt to train a neural network to play tag

This is my first attempt at a machine learning project, and as such will most likely end poorly.

###Game Rules

There is a set amount of Hunters and Players within the game.
Hunters get points for being close to players and capturing them (the being near is more for teaching them more easily)
Players get points for the number of seconds they are alive and lose points for being near Hunters
There are walls which must be maneuvered around by both Players and Hunters, and also block the Hunter's ability to see players

###Running Simulation
'''
python3 sim.py
'''
Then simply enter the desired values and it will either read a previous network or initialize a new one

###Network
the network is just about as simple as it comes. It's just a feed forward network thats being trained with the simplest version of evolution
The layer count can be changed in the nnwk.py file 
