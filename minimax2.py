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
        self.visited = {}



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

            minimax = self.minimaxrec(s[0], 1)
            if minimax != None and minimax > max : 
                max = minimax
                action = s[1]

        print(max)
        return action


    def minimaxrec(self, state, player, dpt=0):
        if state.isWin() or state.isLose():
            return state.getScore()

        currentStateHash = self.hash_state(state, player)

        if currentStateHash in self.visited:
            visitedNode = self.visited[currentStateHash]

            # Visited is a parent
            if visitedNode == None :
                return None

            #Visited is another branch
            # dptDif = dpt - visitedNode.dpt
            dptDif = state.getScore() - visitedNode.currScore
            return visitedNode.score + dptDif
        
        successors = self.generateSuccessors(state, player)
        
        sol = []
        self.visited[currentStateHash] = None

        for s in successors:
            newState = s[0]
            minimax = self.minimaxrec(newState, self.getNextPlayer(player), dpt+1)
            if minimax != None:
                sol.append(minimax)
                
        best = self.getBest(sol, player)

        if best != None:
            self.visited[currentStateHash] = Node(dpt, best, state.getScore())

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

class Node:
    def __init__(self, dpt, score, currScore=0):
        self.dpt = dpt
        self.score = score
        self.currScore = currScore
