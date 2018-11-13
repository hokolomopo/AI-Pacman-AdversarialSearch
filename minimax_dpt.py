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
        self.maxDepth = 10

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
            return state.getScore()  

        successors = self.generateSuccessors(state, player)
        
        sol = []
        
        for s in successors:
            newState = s[0]
            minimax = self.minimaxrec(newState, self.getNextPlayer(player), dpt+1)
            if minimax != None:
                sol.append(minimax)


        best = self.getBest(sol, player)
        return best



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


