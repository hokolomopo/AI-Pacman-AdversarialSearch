# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from math import inf as INF


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.maxDepth = 5

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

        action = self.minimax(state)
        print(action)
        return action

    def minimax(self, state):
        max = -INF
        action = Directions.STOP


        for s in state.generatePacmanSuccessors():

            minimax = self.minimaxrec(s[0], 1, 0)
            print(minimax, s[1])
            if minimax != None and minimax > max : 
                max = minimax
                action = s[1]

        print(max)
        return action


    def minimaxrec(self, state, player, dpt=0,lstGhostMove = Directions.STOP):
        if state.isWin() or state.isLose() or dpt == self.maxDepth:
            return self.getEstimate(state)

        successors = self.generateSuccessors(state, player)
        
        sol = []
        
        for s in successors:
            newState = s[0]
            minimax = self.minimaxrec(newState, self.getNextPlayer(player), dpt+1)
            if minimax != None:
                sol.append(minimax)


        best = self.getBest(sol, player)
        return best

    def getEstimate(self, state):
        """
        Compute the estimated minimax score from this state.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                `pacman.GameState`. Return:
        -------
        - The computed estimated score
        """
        
        FOOD_COEF = -10
        DIST_COEF = -1

        pacmanPosition = state.getPacmanPosition()
        foodMatrix = state.getFood()

        # Distance between pacman and farthest food dot
        maxDistance = 0

        # Number of food left
        nbFoods = 0

        for i in range(foodMatrix.width):
            for j in range(foodMatrix.height):
                if foodMatrix[i][j]:
                    nbFoods += 1
                    tmp = self.__compute_distance(pacmanPosition, (i, j))
                    if tmp > maxDistance:
                        maxDistance = tmp

        estimate = nbFoods * FOOD_COEF +  maxDistance * DIST_COEF + state.getScore()

        return estimate



    def generateSuccessors(self, state, player):
        if player == 0:
            return state.generatePacmanSuccessors()
        else :
            return state.generateGhostSuccessors(1)

    def getBest(self, solutions, player):
        if len(solutions) == 0:
            return None
        if player == 0:
            return max(solutions)
        else :
            return min(solutions)


    def getNextPlayer(self, player):
        if player == 0:
            return 1
        else:
            return 0

    def hash_state(self, state, player):
        return (hash(state.getPacmanPosition()), hash(state.getGhostPositions()[0]),
            hash(state.getFood()), player)

    def __compute_distance(self, position1, position2):
        """
        Compute the Manhattan distance beteween 2 positions.

        Arguments:
        ----------
        - `position1`, `position2`: two tuples representing
          positions`.

        Return:
        -------
        - The Manhattan distance between the 2 positions
        """

        return abs(position1[0] - position2[0]) \
            + abs(position1[1] - position2[1])

