from runPlot import run
import matplotlib.pyplot as plt

saveFolderPath = "graphs/"
fileType = ".eps"

if __name__ == '__main__':
    layouts = ["small_adv", "medium_adv", "large_adv"]
    agents = ["minimax.py", "alphabeta.py", "hminimax.py"]
    ghosts = ["greedy", "smarty", "dumby"]


    colors = ["black", "blue", "red", "green"]
    # agents = ["dfs.py", "bfs.py"]
    scores = []
    times = []
    nodes = []

    # N = number of runs to determine the mean time
    N = 100

    for i in range(len(ghosts)):
        for j in range(len(agents)):
            print((i * len(ghosts) + j )/ (len(ghosts)*len(agents))*100, "%")
            time = 0
            for k in range(N):
                result = run(agent=agents[j], ghost=ghosts[i], layout=layouts[0])

                # Nodes explored and scores won't change, we just take them the first time
                if k == 0:
                    scores.append(result[0])
                    nodes.append(result[2])

                time += result[1]

            # Do the mean of execution times
            times.append(time/N)


    # Draw plots
    for i in range(len(ghosts)):
        N = len(agents)

        # Remove .py
        x = [item[:-3] for item in agents]

        # Width of bars in bar plot
        width = 1/1.2

        # Draw score diagram
        y = scores[i*N:(i+1)*N]
        plt.figure()
        plt.bar(x, y, width, color=colors)
        plt.title(ghosts[i].capitalize() + " : Scores")
        plt.ylabel("Score")
        for j in range(N):
            plt.text(x[j], y[j]+max(y)*0.01, str(y[j]), horizontalalignment='center')

        plt.savefig(saveFolderPath + "score" + ghosts[i].capitalize() +"Ghost" + fileType)

        # Draw time diagram
        y = times[i*N:(i+1)*N]
        plt.figure()
        y = [float("{0:.4f}".format(item)) for item in y]
        plt.bar(x, y, width, color=colors)
        plt.title(ghosts[i].capitalize() + " : Times")
        plt.ylabel("Time (secondes)")
        for j in range(N):
            plt.text(x[j], y[j]+max(y)*0.01, str("{0:.4f}".format(y[j])), horizontalalignment='center')

        plt.savefig(saveFolderPath + "time" + ghosts[i].capitalize() +"Ghost" + fileType)

        # Draw nodes diagram
        y = nodes[i*N:(i+1)*N]
        plt.figure()
        plt.bar(x, y, width, color=colors)
        plt.title(ghosts[i].capitalize() + " : Nodes")
        plt.ylabel("Explored Nodes")
        for j in range(N):
            plt.text(x[j], y[j]+max(y)*0.01, str(y[j]), horizontalalignment='center')

        plt.savefig(saveFolderPath + "nodes" + ghosts[i].capitalize() +"Ghost" + fileType)


