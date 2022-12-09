# SimpleRLProject
The goal was to train model that will survive as long as possible in dangerous conditions.

### Environment
There is a 10x10 cell field. Every 4 tacts 7 3x3 explosions spawn (can be smaller when an explosion spawns in a boundary cell; 2x2 minimum). 
Explosion existance divided into two steps: 2 tacts warning in every cell which shall contain explosion (all cells have the same "warning" value); 
2 tacts of damaging explosion, whic has 3 different types of cells distinguished by damage: central - 75 dmg, up-down and left-right - 50 dmg, corner cells - 25 dmg.

### Agent
Agent is 1x1 cell entity with 100 hp that has goal to survive as long as possible. Hp regenerate at rate of 1 per tact. It can perform 5 actions: up, down, left, right and hold. 
Agent has field of view of 3x3 cell with centre in agent's coordinates. Thus agent has limited information to take action decision.
The "brain" of the agent is policy, that is list of pairs: situation/context around model — action probabilities. Agent match its current context to the one in its policy,
and then chooses action randomly with given probabilities.

### Training
The common training process in reinforcement learning is to fit N(e.g. 10000) models with randomly initialised policy, then evaluate their performance (here — age),
take top p%(e.g. 10%) of them and use their history to update the policy in soft or hard way.
The first thing here to improve is to implement policy using CNN claffifier.

### Visualisation
Here pygame framework used for visualisation. Along with field and agent it displays agent FOV, hp, age, urrent action and total # of invalid actions taken.

![me](https://media.giphy.com/media/MhhSxqK8MFakkW4Syo/giphy.gif)

Note colors meanings:
1. purple - warning,
2. yellow - 25 dmg,
3. orange - 50 dmg,
4. red - 75 dmg.

User can take the following actions:
1. ctrl+x - exit,
2. ctrl+n - new simulation,
3. ctrl+p - pause,
4. ctrl+s - resume,
5. plus - speed up,
6. minus - slow down.
