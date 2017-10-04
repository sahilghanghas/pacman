import numpy as np
import matplotlib.pyplot as plt


Grid_HEIGHT = 4

Grid_WIDTH = 12

EPSILON = 0.1

ALPHA = 0.5

GAMMA = 1

# all possible actions
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3
actions = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]


stateActionValues = np.zeros((Grid_HEIGHT, Grid_WIDTH, 4))
startState = [3, 0]
goalState = [3, 11]

Rewards = np.zeros((Grid_HEIGHT, Grid_WIDTH, 4))
Rewards[:, :, :] = -1.0
Rewards[2, 1:10, ACTION_DOWN] = -100.0
Rewards[3, 0, ACTION_RIGHT] = -100.0

actionDest = []
for i in range(0, Grid_HEIGHT):
    actionDest.append([])
    for j in range(0, Grid_WIDTH):
        dest = dict()
        dest[ACTION_UP] = [max(i - 1, 0), j]
        dest[ACTION_LEFT] = [i, max(j - 1, 0)]
        dest[ACTION_RIGHT] = [i, min(j + 1, Grid_WIDTH - 1)]
        if i == 2 and 1 <= j <= 10:
            dest[ACTION_DOWN] = startState
        else:
            dest[ACTION_DOWN] = [min(i + 1, Grid_HEIGHT - 1), j]
        actionDest[-1].append(dest)
actionDest[3][0][ACTION_RIGHT] = startState


def chooseAction(state, stateActionValues):
    if np.random.binomial(1, EPSILON) == 1:
        return np.random.choice(actions)
    else:
        return np.argmax(stateActionValues[state[0], state[1], :])


def sarsa(stateActionValues, expected=False, stepSize=ALPHA):
    currentState = startState
    currentAction = chooseAction(currentState, stateActionValues)
    rewards = 0.0
    while currentState != goalState:
        newState = actionDest[currentState[0]][currentState[1]][currentAction]
        newAction = chooseAction(newState, stateActionValues)
        reward = Rewards[currentState[0], currentState[1], currentAction]
        rewards += reward
        if not expected:
            valueTarget = stateActionValues[newState[0], newState[1], newAction]
        else:
            valueTarget = 0.0
            bestActions = np.argmax(stateActionValues[newState[0], newState[1], :], unique=False)
            for action in actions:
                if action in bestActions:
                    valueTarget += ((1.0 - EPSILON) / len(bestActions) + EPSILON / len(actions)) * stateActionValues[newState[0], newState[1], action]
                else:
                    valueTarget += EPSILON / len(actions) * stateActionValues[newState[0], newState[1], action]
        valueTarget *= GAMMA
        stateActionValues[currentState[0], currentState[1], currentAction] += stepSize * (reward +
            valueTarget - stateActionValues[currentState[0], currentState[1], currentAction])
        currentState = newState
        currentAction = newAction
    return rewards


def qLearning(stateActionValues, stepSize=ALPHA):
    currentState = startState
    rewards = 0.0
    while currentState != goalState:
        currentAction = chooseAction(currentState, stateActionValues)
        reward = Rewards[currentState[0], currentState[1], currentAction]
        rewards += reward
        newState = actionDest[currentState[0]][currentState[1]][currentAction]
        stateActionValues[currentState[0], currentState[1], currentAction] += stepSize * (
            reward + GAMMA * np.max(stateActionValues[newState[0], newState[1], :]) -
            stateActionValues[currentState[0], currentState[1], currentAction])
        currentState = newState
    return rewards

def printOptimalPolicy(stateActionValues):
    optimalPolicy = []
    for i in range(0, Grid_HEIGHT):
        optimalPolicy.append([])
        for j in range(0, Grid_WIDTH):
            if [i, j] == goalState:
                optimalPolicy[-1].append('G')
                continue
            bestAction = np.argmax(stateActionValues[i, j, :])
            if bestAction == ACTION_UP:
                optimalPolicy[-1].append('U')
            elif bestAction == ACTION_DOWN:
                optimalPolicy[-1].append('D')
            elif bestAction == ACTION_LEFT:
                optimalPolicy[-1].append('L')
            elif bestAction == ACTION_RIGHT:
                optimalPolicy[-1].append('R')
    for row in optimalPolicy:
        print(row)


def figure():
    averageRange = 10

    nEpisodes = 500

    runs = 20

    rewardsSarsa = np.zeros(nEpisodes)
    rewardsQLearning = np.zeros(nEpisodes)
    for run in range(0, runs):
        stateActionValuesSarsa = np.copy(stateActionValues)
        stateActionValuesQLearning = np.copy(stateActionValues)
        for i in range(0, nEpisodes):
            rewardsSarsa[i] += max(sarsa(stateActionValuesSarsa), -100)
            rewardsQLearning[i] += max(qLearning(stateActionValuesQLearning), -100)

    rewardsSarsa /= runs
    rewardsQLearning /= runs

    smoothedRewardsSarsa = np.copy(rewardsSarsa)
    smoothedRewardsQLearning = np.copy(rewardsQLearning)
    for i in range(averageRange, nEpisodes):
        smoothedRewardsSarsa[i] = np.mean(rewardsSarsa[i - averageRange: i + 1])
        smoothedRewardsQLearning[i] = np.mean(rewardsQLearning[i - averageRange: i + 1])

    
    plt.figure(1)
    plt.plot(smoothedRewardsSarsa, label='Sarsa')
    plt.plot(smoothedRewardsQLearning, label='Q-Learning')
    plt.xlabel('Episodes')
    plt.ylabel('Sum of rewards during episode')
    plt.legend()

figure()
plt.show()