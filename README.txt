FIVE-O POKER

Authors:
	Shai Aharon
	Moshe Mandel

****Files****
agents.py				The various agents of the game (Monte, Expectiminimax, Greedy, Reflex, etc.).
cardsDict.py			A dictionary used to convert cards represented as ints to their respective ranks/suit/string.
display.py				GUI.
fiveopoker.py			Parses the command line, and runs the game/s.
game.py					Holds various objects needed to run the game (Card, Configuration, AgentState, etc.)
greedyEval.py			State evaluation function.
greedyEval2.py			State evaluation function. Also holds hand evaluation functions used by reflex agents.
handEvaluator.py		Handles the C poker evaluation library, and allows the library to be used in python.
keyboardAgent.py		Human agent.
monteCarloEvaluator.py	Evaluates states and hands by simulation.
probTable.py			Calculates exact winning probabilities of hands.
util.py					Holds various tools used in the program.
valueDict.py			A dictionary of (<tuple>, <int>), which holds values for incomplete hands (keys are a tuple of the hand's ranks).


****Usage****
For using the program the user must specify the players names and types, for certain agent types an evaluation function
should be provided.
To run the program one may type the following at the command line:
		
		python fiveopoker.py

	This will by default run the game with a human and a greedy agent (using greedyEval2).
For help:
		
		python fiveopoker.py -h

For usage instructions:
		
		python fiveopoker.py -u

One may choose different agents by specifying a name and agent type:
	A name be any string of chars.
	An agent type can be one of the following:
		1. human				a human agent
		Computer agents:
		2. random				
		3. hminimax
		4. greedy
		5. relfex1
		6. reflex2
		7. reflex3
		8. monte
		9. prob
	Each player command must be preceded by -1 (for player 1) or/and -2 (for player 2).
	For example for a game against the expectiminimax, one may type the following in the command line:
		
		python fiveopoker.py -1 Moshe human -2 Shai approxHMinimax
	
	When using one of the agents that use a state evaluation function (hminimax or greedy agents)
	one can choose a specific function by preceding the function name ('greedyEval1', 'greedyEval2' or 'fastGreedyEval2')
	with -a (for player 1) of -b (for player 2). For instance :
		
		python fiveopoker.py -1 Shai greedy -a greedyEval2 -2 Moshe hminimax -b fastGreedyEval2

		If function name is not specified, it will by default run with 'greedyEval2'.

	By default the GUI is activated, one may choose to deactivate it by typing '-g n' in the
	command.
	If one wishes to simulate a number of games, he may add to command: '-n <Integer>'.
	If one wishes to make the program non-verbose, he may add to the command: '-v n'.
	For example, when running a thousand games of a reflex1 agent against a greedy agent (using greedyEval1),
	one may type the following:
		
		python fiveopoker.py -1 Shai reflex1 -2 Moshe greedy -b greedyEval1 -g n -n 1000 -v n

****Prerequisites****
The Five O-Poker game uses some python libraries that are not common house-holds.
To save time and frustration, we add them in the "Imports" folder.

	1) numexpr-1.4.1.win32-py2.7.exe
	2) numpy-MKL-1.8.1rc1.win32-py2.7.exe
	3) pygame-1.9.1.win32-py2.7.msi
	4) scipy-0.13.3-win32-superpack-python2.7.exe
	5) tables-3.1.0.win32-py2.7.exe
The game is implemented in python V2.7.6, 32-bit.