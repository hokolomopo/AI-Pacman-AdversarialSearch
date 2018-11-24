from pacman_module.game import Agent
from pacman_module.pacman import Directions
from math import inf as INF
from pacman_module.util import manhattanDistance

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

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
        next = state.generatePacmanSuccessors() 
        value = -INF 
        visited = set()

        for item in next:
            #   We compute the minimax value for each successor of the state
            score = self.minimax(item[0], 1, -INF, INF, 1)
            if score is None:
                continue 
            
            #   We are looking for the largest payoff in the current state
            if score > value:     
               value = score
               action = item[1]

        return action

    def minimax(self, state, agentIndex, alpha, beta, depth):
        """
        Implementation of the H-minmiax algorithm as an improvment
        of the alpha-beta algorithm

        Arguments:
        ----------
        - `state`: the current game state
        - 'visited': a set of already visited states
        - 'agentIndex': the agent currently playing

        Return:
        -------
        - The score when Pacman loses or wins
        """

        if state.isWin() or state.isLose() or depth > 6: 
            return self.evaluationFunction(state)

        # currentState = (hash(state.getPacmanPosition()), hash(state.getGhostPosition(1)), hash(state.getFood()))
        # if currentState in visited:
        #     #   We check if the current state is already visited
        #     return None
        # visited.add(currentState)

        if agentIndex == 0:
            #   The current agent is the Pacman agent
            value = -INF
            next = state.generatePacmanSuccessors() 

        else:
            #   The current agent is the ghost agent
            value = INF
            next = state.generateGhostSuccessors(agentIndex) 

        for item in next:
            #   Je sais pas comment commenter hihi
            # newVisited = visited.copy()
            score = self.minimax(item[0], self.nextAgent(state, agentIndex), alpha, beta, depth+1)

            if score is None:
                continue

            if agentIndex == 0:
                #   The current agent is the Pacman, which corresponds to the MAXIMAX agent
                alpha = max(alpha, score)
                value = max(score, value)
                if value >= beta:
                    break

            else:
                #   The current agent is a ghost, which corresponds to a MINIMAX agent
                value = min(score, value)
                beta = min(score, beta)
                if value <= alpha:
                    break

        if value == -INF or value == INF:
            return None

        else:
            return value

    def nextAgent(self, state, agentIndex):
        """
        Returns the next player in case of multiple agents (ghosts)

        Arguments:
        ----------
        - `state`: the current game state
        - 'agentIndex': the agent currently playing

        Return:
        -------
        - The next player
        """
        nbGhost = state.getNumAgents() - 1

        if agentIndex + 1 > nbGhost:
            return 0

        else:
            return agentIndex + 1

    def evaluationFunction(self, state):
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
        GHOST_COEF = 1

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
