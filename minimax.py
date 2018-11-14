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
        return action

    def minimax(self, state):
        """
        Given a pacman game state, returns the best legal move computed with
        the minimax algorithm.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        max = -INF
        action = Directions.STOP

        # Loop on the successors of this state
        for s in state.generatePacmanSuccessors():

            # Update the best minimax score and action
            minimax = self.minimaxrec(s[0], 1)
            if minimax != None and minimax > max : 
                max = minimax
                action = s[1]

        return action


    def minimaxrec(self, state, player, dpt=0, lastPacmanMove=None, lastGhostMove=None):
        """
        Return the minimax score of a state.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - `player`: the id of the current player
        - `dpt`: the depth of the node
        - `lastPacmanMove`: the last move of Pacman
        - `lastGhostMove`: the last move of the ghost

        Return:
        -------
        - A minimax score.
        """

        # Check if we won or lost
        if state.isWin() or state.isLose():
            return state.getScore()

        # Get the unique key of this game state
        currentStateHash = self.hash_state(state, player, lastGhostMove, lastPacmanMove)

        # Check if this node is already visited
        if currentStateHash in self.visited:
            visitedNode = self.visited[currentStateHash]

            # Visited is a parent
            if visitedNode == None :
                return None

            #Visited in another branch
            dptDif = state.getScore() - visitedNode.currScore
            return visitedNode.score + dptDif
        
        # Generate the successors of this state
        successors = self.generateSuccessors(state, player, lastPacmanMove)

        # sol  will be the array conaining the minimax results of the children
        sol = []

        self.visited[currentStateHash] = None

        for s in successors:
            newState = s[0]
            direction = s[1]

            # Pacman is playing, update last Pacman move
            if(player == 0):
                minimax = self.minimaxrec(newState, self.getNextPlayer(player) \
                 ,dpt+1, direction, lastGhostMove)
            # Ghost is playing, update last ghost move
            else :
                minimax = self.minimaxrec(newState, self.getNextPlayer(player) \
                 ,dpt+1, lastPacmanMove, direction)
            if minimax != None:
                sol.append(minimax)

        # Get the best minimax score       
        best = self.getBest(sol, player)

        # Memorize the minimax score if we found one
        if best != None:
            self.visited[currentStateHash] = Node(dpt, best, state.getScore())
        # We didn't find a minimax score (all the children of this node leads
        # to a cycle)
        else:
            del self.visited[currentStateHash]

        return best

    def generateSuccessors(self, state, player, lastPacmanMove=None):
        """
        Generate successors of the node. If we give the last move of pacman
            as argument, it can possiblygenerate a successor with 
            the action STOP

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                `pacman.GameState`. 
        - `player`: the id of the current player
        - `lastPacmanMove`: the last move of Pacman

        Return:
        -------
        - The successors of the node
        """

        # Pacman player
        if player == 0:
            nextStates = state.generatePacmanSuccessors()

            # If we don't know the last move of Pacman, we cannot know if 
            # he can stop moving
            if lastPacmanMove == None:
                return nextStates
            
            # If Pacman can stop moving, add an action STOP in the successors
            if self.canPacmanStop(state, lastPacmanMove):
                nextStates.append((state, Directions.STOP))

            return nextStates
        else :
            return state.generateGhostSuccessors(1)

    def canPacmanStop(self, state, lastPacmanMove):
        """
        Check if Pacman can stay still. Pacman can stay still when he collides
            with a wall and is not given any input.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                `pacman.GameState`. 
        - `lastPacmanMove`: the last move of Pacman

        Return:
        -------
        - The successors of the node
        """

        actions = state.getLegalActions(0)

        # No wall close-by 
        if len(actions) > 4:
            return False

        # Pacman can stay still if his last move was STOP
        if lastPacmanMove == Directions.STOP:
            return True

        # Check if Pacman collided with a wall (the last move is no longer
        # available)
        if actions.count(lastPacmanMove) == 0:
            return True
        return False

    def getBest(self, solutions, player):
        """
        Given an array of minimax score, return the best score for this player.

        Arguments:
        ----------
        - `player`: the id of the current player
        - `solutions`: the array of minimax score

        Return:
        -------
        - The best minimax score for this player
        """

        if len(solutions) == 0:
            return None
        if player == 0:
            return max(solutions)
        else :
            return min(solutions)


    def getNextPlayer(self, player):
        """
        Get the id of the next player that will play.

        Arguments:
        ----------
        - `player`: the id of the current player

        Return:
        -------
        - the id of the next player that will play
        """

        if player == 0:
            return 1
        else:
            return 0

    def hash_state(self, state, player, lastGhostMove, lastPacmanMove):
        """
        Create an unique tuple representing this game state.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                    `pacman.GameState`.
        - `player`: the id of the current player
        - `lastGhostMove`: the last move of the ghost
        - `lastPacmanMove`: the last move of Pacman


        Return:
        -------
        - A unique tuple representing this game state
        """

        return (hash(state.getPacmanPosition()), hash(state.getGhostPositions()[0]),
            hash(state.getFood()), player, lastGhostMove, self.canPacmanStop(state, lastPacmanMove))

class Node:
    def __init__(self, dpt, score, currScore=0):
        self.dpt = dpt
        self.score = score
        self.currScore = currScore
