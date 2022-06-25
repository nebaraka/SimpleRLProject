import numpy as np


class Agent:
    # Actions encoded as 0: hold, 1: up, 2: down, 3: left, 4: right
    _ACTIONS = [0, 1, 2, 3, 4]

    def __init__(self, policy, state, born_iteration=0):
        self._reward = 0
        self._policy = policy
        # State (tuple): action probability distribution (list)
        self._state = state
        self._previous_state = state
        self._choice_history = []
        self._born = born_iteration

    def make_action(self, state):
        # With this method the agent makes decision which action to take according to its policy
        #
        self._previous_state = self._state
        self._state = state
        if self._state not in self._policy.keys():
            self._policy[self._state] = {0: 0.2, 1: 0.2, 2: 0.2, 3: 0.2, 4:0.2}
        distribution = self._policy[self._state]
        action = np.random.choice(list(distribution.keys()),
                                  p=list(distribution.values()))

        self._choice_history.append((self._state,
                                     action, self._reward))
        return action, self._policy

    def age(self, last_iteration):
        return last_iteration - self._born

    def update_reward(self, amount):
        self._reward += amount

    def get_policy(self):
        return self._policy

    def get_reward(self):
        return self._reward

    def get_history(self):
        return self._choice_history
