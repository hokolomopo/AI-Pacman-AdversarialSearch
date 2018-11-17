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
        return action

    def minimax(self, state):
        """
        Given a pacman game state, returns the best legal move computed with
        the minimax algorithm with alphabeta pruning.

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

        self.lastAction = action
        return action

    def minimaxrec(self, state, player, dpt=0, parentInterval=[-INF, +INF],
                   lastPacmanMove=None, lastGhostMove=None):
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
        - `lastGhostMove`: the last move of the ghost

        Return:
        -------
        - A minimax score.
        """

        # Check if we won or lost
        if state.isWin() or state.isLose():
            return state.getScore()

        # Get the unique key of this game state
        currentStateHash = self.hash_state(
            state, player, lastGhostMove, lastPacmanMove)
        successors = None

        # Check if this node is already visited
        if currentStateHash in self.visited:
            visitedNode = self.visited[currentStateHash]

            # Visited is a parent
            if visitedNode is None:
                return None

            # Visited in another branch and we know it's minimax score
            elif visitedNode.score is not None:
                scrDif = state.getScore() - visitedNode.currScore
                return visitedNode.score + scrDif
            # Visited in another branch but we don't know it's minimax score
            else:
                successors = visitedNode.successors

        # Generate successors if we didn't memorize them from a visited state
        if successors is None:
            successors = self.generateSuccessors(state, player, lastPacmanMove)

        self.visited[currentStateHash] = None

        # sol  will be the array conaining the minimax results of the children
        sol = []

        # Pruning interval
        interval = [-INF, +INF]
        pruned = False

        for s in successors:
            newState = s[0]
            direction = s[1]

            # Pacman is playing, update last Pacman move
            if player == 0:
                minimax = self.minimaxrec(newState, self.getNextPlayer(
                    player), dpt + 1, interval, direction, lastGhostMove)
            # Ghost is playing, update last ghost move
            else:
                minimax = self.minimaxrec(newState, self.getNextPlayer(
                    player), dpt + 1, interval, lastPacmanMove, direction)

            if minimax is not None:
                sol.append(minimax)

                # Check if we can prune this node
                if self.shouldPrune(minimax, parentInterval, player):
                    pruned = True
                    break

                # Update the pruning interval
                self.updateInterval(interval, minimax, player)

        # Get the best minimax score
        best = self.getBest(sol, player)

        # We didn't find a minimax score (all the children of this node leads
        # to a cycle)
        if best is None:
            del self.visited[currentStateHash]

        # We pruned this node. Memorize successors for the next time.
        elif pruned:
            self.visited[currentStateHash] = Node(
                dpt, None, state.getScore(), successors)

        # Memorize the minimax score
        elif best is not None:
            self.visited[currentStateHash] = Node(dpt, best, state.getScore())

        return best

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

        return (hash(state.getPacmanPosition()),
                hash(state.getGhostPositions()[0]),
                hash(state.getFood()), player, lastGhostMove,
                self.canPacmanStop(state, lastPacmanMove))


class Node:

    def __init__(self, dpt, score, currScore=0, successors=None):
        self.dpt = dpt
        self.score = score
        self.currScore = currScore
        self.successors = successors
