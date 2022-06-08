from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
from hmm import HMM

class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.models = [HMM(2, N_EMISSIONS) for _ in range(N_SPECIES)]
        self.fish = [[] for _ in range(N_FISH)]
        self.guessed = set()

    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """

        for i in range(N_FISH):
            self.fish[i].append(observations[i])
        # This code would make a random guess on each step:
        if N_STEPS - N_FISH >= step:
            return None
        else:
            probs = [[model.sequnceProbabilities(self.fish[i]) for model in self.models]
                     if i not in self.guessed else [-1 for _ in self.models] for i in range(N_FISH)]
            f_probs = [max(m_prob) for m_prob in probs]
            m = max(f_probs)
            f_i = f_probs.index(m)
            m_i = probs[f_i].index(m)
            return f_i, m_i

    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        if not correct:
            self.models[true_type].train(self.fish[fish_id], 10)
        self.guessed.add(fish_id)