## Adversarial Game Playing Agent for knights isolation

#### Isolation


#### Minimax agents and variations
Minimax is an algorithm for 'zero sum games', where at each step of the game, the agent tries to minimize the 
worst possible loss. In minimax, all the nodes of the tree is searched, thus it is not a very effective
algorithm to use in practice. Instead, there are more advanced variations that limit how many nodes are
searched, such as alpha beta pruning, principal variation search, MTD(f), etc. 

In this project, I added iterative deepening (ie, the agent progressive search to greater depths in order to 
make use of all the available time and not run into a time limit) and also experimented with the alpha-beta agent with transposition table, and also
node sorting. I also implemented a version of the alpha beta agent in iterative deepening where instead of starting 
from -infinty to infinity for each search, the iterative deepening algorithm saves the values of alpha and beta to reduce 
the search window.

The transposition table stores the state and the best alpha/beta value it takes to reach that state. This is because
in the alpha beta search, it doesn't matter so much how the state is reached, but rather what is the 'best' value for
that state. By saving the 'best' values it has obtained in the search so far, the nodes agent will rerun a search on 
is much less and the agent should be more efficient.

Node sorting-- in one version of the alpha beta 

#### Heuristic function
I decided to implement a custom heuristic function based on the baseline
`availabe_my_moves - available_opponent_moves` heuristic. I added in 
an extra param to minimize the manhattan distance for my agent while maximizing the 
manhattan distance to the adversary-- this is implemented by adding in the 
`manhattan_opponent - manhattan_own` to the base heuristic. In addition, I also
expect the depth at which the cost function is evaluated will have 
an effect-- a higher depth means the further in the future the agent searches. In one 
experiment, I multipled my custom heuristic score by `x ^ depth` where x is varied. I expected
that x would have a optimal value just below 1 (so deeper depths are less important) for the 
agent to win. Surprisingly, it is the other way round, with to optimal x value around 2. (and afterwards the win rates
seems to more or less saturate)

| Scoring        | Agent           | games  | time limit| win rate|
| ------------- |-------------:| -----:|-------------:|-------------:|
| my_moves - opp_moves  | alpha-beta | 100 | 200ms| 75%|
| my_moves - opp_moves + manhattan_opponent - manhattan_own| alpha-beta | 100 | 200ms| 87%|
| (my_moves - opp_moves + manhattan_opponent - manhattan_own) * 2.5 ^ depth| alpha-beta | 100 | 200ms| 77%|

 