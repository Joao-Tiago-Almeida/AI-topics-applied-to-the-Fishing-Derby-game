# AI-topics-applied-to-the-Fishing-Derby-game

The practical part of the course was centred around the fishing derby game. The students completed three projects regarding the decision making of the AI system.

## [Minimax search algorithm](./Search%20Algorithms%20-%20Minimax%20algorithm)

The goal of this assignment was to compute a few movements ahead using the minimax algorithm, assuming that the computer was always making the best move. In order so, the group used a heuristic function to approximate the theoretical utility function since the possible number of plays each round is too big. As we can see on the example, each fish has a different positive or negative value, and the boats cannot overlap each-other.

![](https://user-images.githubusercontent.com/39059647/172636544-84584bec-f777-4c83-9a6c-80c32cf9c9e3.mov)

## [Hidden Markov Models](./Hidden%20Markov%20Models/grade%20A%26B%20(FishingDerby))

In this assignment, we had to predict the type of each based on their pattern. The only thing known was that there were 7 fish speacies, although each specie might has multiple swiming patterns. To correctly identify the speacies, we ahd to formulate a classifier in real "swimming" time.

![](https://user-images.githubusercontent.com/39059647/172636816-64a3fef5-7d88-49f3-8d62-52236fd61534.mov)

## [Reinforcement Learning](./Reinforcement%20Learning/grade%20A%20(FishingDerby))

The reinforcement learning assigment concerned a diver swimming until the king fish, avoiding the the jellyfish. We used the Q-Learning algorithm with an epsilon-greedy policy. The agent was rewarded +20 when he reached the king fish, -10 by touching the jellyfish, and -1 per step.

![](https://user-images.githubusercontent.com/39059647/172636176-dade4beb-c430-4886-9820-958db8cc7470.mov)
