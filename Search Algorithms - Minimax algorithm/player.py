#!/usr/bin/env python3
import math
import time

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


def compute_distance(fish, hook):
    x = abs(fish[0] - hook[0])
    y = abs(fish[1] - hook[1])
    x = min(x, 20 - x)
    return x + y


class Model:
    def heuristic(self, node):
        p1, p2 = node.state.get_player_scores()
        nearest_d = math.inf
        score = 0
        final = 0
        for i in node.state.fish_positions:
            distance = compute_distance(node.state.fish_positions[i], node.state.hook_positions[0])
            if distance == 0:
                final = final + node.state.fish_scores[i]
            elif node.state.fish_scores[i] > 0 and distance < nearest_d:
                nearest_d = distance
                score = node.state.fish_scores[i]
        final = final + score / nearest_d / 2
        return final + 10*(p1 - p2)

    def iterative_deepening(self, init_node, alpha, beta):
        init_time = time.time()
        starting_depth = 1
        visited = {}

        while True:
            try:
                best_action = self.run_alpha_beta(init_node, starting_depth, alpha, beta, init_time, visited)
                #print("reached depth", starting_depth)
                starting_depth = starting_depth + 1
            except:
                # print("Timeout depth", starting_depth)
                break
        return best_action

    def order_children(self, children):
        #ordered = children[1:] + [children[0]]
        ordered = sorted(children, key=self.heuristic, reverse=True)
        return ordered

    def encode(self, node):
        state = node.state
        hash_key = ""
        for (idx, fp), (_, fs) in zip(state.fish_positions.items(), state.fish_scores.items()):
            hash_key = hash_key + str(idx) + ":" + str(fp) + "," + str(fs) + ";"
        return (str(state.hook_positions) + ";" + hash_key).replace(" ", "")

    def alpha_beta(self, node, depth, alpha, beta, init_time, visited):
        if time.time() - init_time > 0.056:
            raise TimeoutError
        else:
            key = self.encode(node)
            if key in visited and depth <= visited[key][0]:
                # when we are deeper or the same depth as the saved node return the saved value
                # if we are not deeper, the highest one in tree will get saved
                return visited[key][1]
            children = self.order_children(node.compute_and_get_children())
            if depth == 0 or len(children) == 0:
                v = self.heuristic(node)
            elif node.state.get_player() == 0:
                v = -math.inf
                for child in children:
                    n = self.alpha_beta(child, depth - 1, alpha, beta, init_time, visited)
                    if n > v:
                        v = n
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break
            else:
                v = math.inf
                for child in children:
                    n = self.alpha_beta(child, depth - 1, alpha, beta, init_time, visited)
                    if n < v:
                        v = n
                    beta = min(beta, v)
                    if beta <= alpha:
                        break
            visited[key] = [depth, v]
            return v

    def run_alpha_beta(self, init_node, depth, alpha, beta, init_time, visited):
        max_v = -math.inf
        # important DO NOT sort the children here
        # if the score is the same for more actions the default order of moves is the best
        for node in init_node.compute_and_get_children():
            v = self.alpha_beta(node, depth - 1, alpha, beta, init_time, visited)
            if v > max_v:
                max_v = v
                action = node.move
        return action


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3},
          'fish1': {'score': 2, 'type': 1},
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        return Model()

    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """
        action = model.iterative_deepening(init_node=initial_tree_node, alpha=-math.inf, beta=math.inf)
        # action = model.run_alpha_beta(init_node=initial_tree_node, depth=5, alpha=-math.inf, beta=math.inf)

        return ACTION_TO_STR[action]
