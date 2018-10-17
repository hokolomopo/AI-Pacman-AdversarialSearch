# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
import heapq as hq
import random

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.optimalActions = None

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        if self.optimalActions is None :
            self.optimalActions = self.__generate_optimal_actions(state)
        
        if len(self.optimalActions) > 0:
            action = self.optimalActions[0]
            del self.optimalActions[0]
            return action

        return Directions.STOP

    def __generate_optimal_actions(self, state) :
        """
        Given a pacman game state, returns a list of action allowing to win the game.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of moves (as defined in game.Directions) that allows Pacman to win the game
        """


        heuri = self.__get_heuristic(state)
        fringe = [Node(state, [], heuri, heuri)]

        globalVisited = set()

        #Loop while we didn't go through the whole decision tree
        while len(fringe) > 0:
            currentNode = hq.heappop(fringe)

            if self.__hash_state(currentNode.state) in globalVisited:
                continue
                
            #Check if we won
            if currentNode.state.isWin():
                return currentNode.moves
            
            #Get next possible states/actions
            nextElements = currentNode.state.generatePacmanSuccessors()

            #If we visit the same state in another branch, we can ignore it because the branch will
            # lead at best to a solution of the same cost (in aster, the cost the nodes explored after
            # the current one will have a cost >= that the current cost)
            globalVisited.add(self.__hash_state(currentNode.state))

            #Prevent Pacman to go back to visited states
            nextElements = [item for item in nextElements 
                if not self.__hash_state(item[0]) in globalVisited]

            #Add new nodes to the list
            for item in nextElements:
                newState = item[0]
                moves = currentNode.moves.copy()
                moves.append(item[1])

                heurisitc = self.__get_heuristic(newState)
                newNode = Node(newState, moves, len(moves) + heurisitc, heurisitc)
                hq.heappush(fringe, newNode)


            
        return []

    def __compute_cost(self, node):
        return len(node.moves) + self.__get_heuristic(node.state)

    def __get_heuristic(self, state):
        pacmanPosition = state.getPacmanPosition()

        foodMatrix = state.getFood()
        cost = 0

        for i in range(foodMatrix.width - 1):
            for j in range(foodMatrix.height - 1):
                if foodMatrix[i][j]:
                    tmp = self.__compute_distance(pacmanPosition, (i, j))
                    if tmp > cost:
                        cost = tmp

        return cost

        

    def __compute_distance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])
    
    def __hash_state(self, state):
        return (hash(state.getPacmanPosition()), hash(state.getFood()))


class Node:
    def __init__(self, state, moves, cost, heurisitc):
        self.state = state
        self.moves = moves
        self.cost = cost
        self.heurisitc = heurisitc
        
    def __lt__(self, other):
        if self.cost == other.cost:
            return self.state.getScore() > other.state.getScore()
        return self.cost < other.cost

