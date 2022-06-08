#!/usr/bin/env python3
from logging import DEBUG
import math
import time

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

DEBUG=False

def compute_distance(fish, hook):
    x = abs(fish[0] - hook[0])
    y = abs(fish[1] - hook[1])
    x = min(x, 20 - x)
    return x + y

class Model:

    def __init__(self) -> None:
        self.heuristic_computations = 0
        self.starting_depth = 1
        self.best_action = 0
        self.repeated_states = {}

    def heuristic(self, node):
        p1, p2 = node.state.get_player_scores()
        nearest_d = math.inf
        score = 0
        final = 0
        for i in node.state.fish_positions:
            distance = compute_distance(node.state.fish_positions[i], node.state.hook_positions[0])

            if distance == 0:
                final = final + node.state.fish_scores[i]

            elif node.state.fish_scores[i] > 0 and (distance < nearest_d\
                 # or same distance but higher points
                 or (distance == nearest_d and node.state.fish_scores[i]>score))\
                 and (compute_distance(node.state.fish_positions[i], node.state.hook_positions[1])) != 0 : # and fish is not in red's hook

                nearest_d = distance
                score = node.state.fish_scores[i]

        final = final + score/nearest_d/2

        self.heuristic_computations+=1
        if DEBUG: print(self.heuristic_computations)

        return final + 1.01*p1 - p2

    def iterative_deepening(self, init_node, alpha, beta):
        init_time = time.time()
        timeout = False
        
        while not timeout:
            try:
                self.best_action = self.run_alpha_beta(init_node, self.starting_depth, alpha, beta, init_time)
                self.starting_depth += 1
                if DEBUG: print("\treached depth", self.starting_depth)
                breakpoint
            except:
                if DEBUG: print("Timeout depth", self.starting_depth)
                timeout = True
        #self.best_action = self.run_alpha_beta(init_node, self.starting_depth, alpha, beta, init_time)

        return self.best_action

    def order_children(self, children):
        ordered = sorted(children, key=self.heuristic, reverse=True)
        return ordered

    def hash_key(self, state) -> str:

        good_fishes = {"hook":list(state.hook_positions.values())}
        for idx,fp in state.fish_positions.items():
            dist_to_green = compute_distance(fp, state.hook_positions[0])
            dist_to_red = compute_distance(fp, state.hook_positions[1])

            # fishes that realy interest
            if dist_to_green <= dist_to_red and dist_to_green <= self.starting_depth:
                good_fishes.update(
                    { state.fish_scores[idx] : state.fish_positions[idx] }
                )

        #return "" if len(good_fishes)==1 else str(good_fishes).replace(" ", "")
        return str(good_fishes).replace(" ", "")
        
    def alpha_beta(self, node, depth, alpha, beta, init_time):

        if DEBUG: print(f"MOVES: {node.parent.move, node.move}")

        if time.time() - init_time > 0.055:
            raise TimeoutError
        else:
            # Repeated state
            key = self.hash_key(node.state)
            if key in self.repeated_states and\
                (node.depth == self.starting_depth or node.depth < self.repeated_states[key][0]):
                if DEBUG: print("repeated state")
                self.repeated_states[key] = (node.depth,self.repeated_states[key][1])
                return self.repeated_states[key][1]

            if depth == 0 or len(node.compute_and_get_children()) == 0:
                if DEBUG: print("new state")
                v = self.heuristic(node)

            elif node.state.get_player() == 0:
                v = -math.inf
                for child in self.order_children(node.compute_and_get_children()):
                    n = self.alpha_beta(child, depth - 1, alpha, beta, init_time)
                    if n > v:
                        v = n
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        if DEBUG: print("pruning 0")
                        break

            else:
                v = math.inf
                for child in self.order_children(node.compute_and_get_children()):
                    n = self.alpha_beta(child, depth - 1, alpha, beta, init_time)
                    if n < v:
                        v = n
                    beta = min(beta, v)
                    if beta <= alpha:
                        if DEBUG: print("pruning 1")
                        break
            
            # Add new states
            if key not in self.repeated_states:  
                self.repeated_states[key] = (node.depth, v)

            # Update the states if the value is better
            if self.repeated_states[key][1] < v:
                self.repeated_states[key] = (node.depth,v)
            # Or if the same result is described by a less deep level and the value is the same
            elif self.repeated_states[key][1] == v and self.repeated_states[key][0] > node.depth:
                self.repeated_states[key] = (node.depth,v)

            return v

    def run_alpha_beta(self, init_node, depth, alpha, beta, init_time):
        max_v = -math.inf
        for node in self.order_children(init_node.compute_and_get_children()):
            v = self.alpha_beta(node, depth - 1, alpha, beta, init_time)
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
        #action = model.run_alpha_beta(init_node=initial_tree_node, depth=5, alpha=-math.inf, beta=math.inf)

        return ACTION_TO_STR[action]
