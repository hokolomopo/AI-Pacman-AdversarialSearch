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
        self.maxDpt = 5
        self.lastAction = Directions.STOP

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
        self.lastAction = action

        return action

    def minimax(self, state):
        """
        Given a pacman game state, returns the best legal move computed with
        the H-minimax algorithm with alphabeta pruning.

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

        interval = [-INF, +INF]

        # Loop on the successors of this state
        for s in self.generateSuccessors(state, 0, self.lastAction):

            minimax = self.minimaxrec(
                s[0], 1, 0, parentInterval=interval, lastPacmanMove=s[1])

            # Update the pruning interval
            self.updateInterval(interval, minimax, 0)

            # Update the best minimax score and action
            if minimax is not None and minimax > max:
                max = minimax
                action = s[1]

        return action

    def minimaxrec(self, state, player, dpt=0, parentInterval=[-INF, +INF],
                   lastPacmanMove=None):
        """
        Return the minimax score of a state.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - `player`: the id of the current player
        - `dpt`: the depth of the node
        - `parentInterval`: the interval of score as defined in the alphabeta
            prunign pseudo-code
        - `lastPacmanMove`: the last move of Pacman

        Return:
        -------
        - A minimax score.
        """

        # Check if we won or lost or it the maximum depth is reached
        if state.isWin() or state.isLose() or dpt > self.maxDpt:
            return self.getEstimate(state)

        # Generate the successors of this state
        successors = self.generateSuccessors(state, player, lastPacmanMove)

        # sol  will be the array conaining the minimax results of the children
        sol = []

        # Pruning interval
        interval = [-INF, +INF]

        for s in successors:
            newState = s[0]

            # Pacman is playing, update last Pacman move
            if(player == 0):
                minimax = self.minimaxrec(newState, self.getNextPlayer(
                    player), dpt + 1, interval, s[1])
            # Ghost is playing, update last ghost move
            else:
                minimax = self.minimaxrec(newState, self.getNextPlayer(
                    player), dpt + 1, interval, lastPacmanMove)

            sol.append(minimax)

            # Check if we can prune this node
            if self.shouldPrune(minimax, parentInterval, player):
                break

            # Update the pruning interval
            self.updateInterval(interval, minimax, player)

        # Get the best minimax score
        best = self.getBest(sol, player)

        return best

    def getEstimate(self, state):
        """
        Compute the estimated minimax score from this state.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                `pacman.GameState`.
        Return:
        -------
        - The computed estimated score
        """

        FOOD_COEF = -100
        DIST_COEF = -5
        GHOST_COEF = -1

        pacmanPosition = state.getPacmanPosition()
        ghostPosition = state.getGhostPositions()[0]
        foodMatrix = state.getFood()

        # Distance between pacman and closest food dot
        minDistance = INF

        # Number of food left
        nbFoods = 0

        for i in range(foodMatrix.width):
            for j in range(foodMatrix.height):
                if foodMatrix[i][j]:
                    nbFoods += 1
                    tmp = self.__compute_distance(pacmanPosition, (i, j))
                    if tmp < minDistance:
                        minDistance = tmp

        if minDistance == INF:
            minDistance = 0

        distToGhost = self.__compute_distance(pacmanPosition, ghostPosition)

        estimate = nbFoods * FOOD_COEF + minDistance * DIST_COEF + \
            state.getScore() + distToGhost * GHOST_COEF

        return estimate

    def shouldPrune(self, minimax, interval, player):
        """
        Check if the node should be pruned.

        Arguments:
        ----------
        - `minimax`: the current minimax score
        - `interval`: the interval of score as defined in the alphabeta
            prunign pseudo-code
        - `player`: the id of the current player

        Return:
        -------
        - True if the node should be pruned, False if we should continue
            exploring the node
        """

        # Pacman player
        if player == 0:
            if minimax >= interval[1]:
                return True
            return False
        # Ghost player
        else:
            if minimax <= interval[0]:
                return True
            return False

    def updateInterval(self, interval, minimax, player):
        """
        Update the interval used to decide the pruning of a node.

        Arguments:
        ----------
        - `interval`: the interval of score as defined in the alphabeta
            prunign pseudo-code
        - `minimax`: the current minimax score
        - `player`: the id of the current player
        """
        # Pacman player
        if player == 0:
            interval[0] = max(minimax, interval[0])
        # Ghost player
        else:
            interval[1] = min(minimax, interval[1])

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
            if lastPacmanMove is None:
                return nextStates

            # If Pacman can stop moving, add an action STOP in the successors
            if self.canPacmanStop(state, lastPacmanMove):
                nextStates.append((state, Directions.STOP))

            return nextStates
        else:
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
        else:
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


class Node:

    def __init__(self, dpt, score, currScore=0):
        self.dpt = dpt
        self.score = score
        self.currScore = currScore
