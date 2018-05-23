
## Classical Planning project

In this project, a classical search agent is implemented to planning task. In this project, the planning problems are variations on an Air Cargo logistic problem-- if you have certain number of cargo and a set amount of planes, how do you get them from place to place?

### Problem set:
The following lists the problems set

```
Note:
C1, C2 etc are the cargo,
P1, P2 etc are the planes
the rest, e.g. SFO are airports

```

problem1. 
```
precondition: [ At(C1, SFO) AND At(C2, JFK)AND At(P1, SFO) AND At(P2, JFK) AND At(P3, ATL)]
goal: [At(C1, JFK) AND At(C2, SFO)]
```

problem2. 
```
precondition: [ At(C1, SFO) AND At(C2, JFK)  AND At(C3, ATL)  AND At(P1, SFO) AND At(P2, JFK)]
goal: [At(C1, JFK) AND At(C2, SFO) AND At(C3, SFO)]
```

problem3. 
```
precondition: [ At(C1, SFO) AND At(C2, JFK) AND At(C3, ATL) AND At(C4, ORD) AND At(P1, SFO) AND At(P2, JFK)]
goal: [At(C1, JFK) AND At(C2, SFO) AND At(C3, JFK) AND At(C4, SFO)]
```

problem4. 
```
precondition: [At(C1, SFO) AND At(C2, JFK) AND At(C3, ATL) AND At(C4, ORD) AND At(C5, ORD) AND At(P1, SFO) AND At(P2, JFK)]
goal: [At(C1, JFK) AND At(C2, SFO) AND At(C3, JFK) AND At(C4, SFO) AND At(C5, JFK)]
```

### Experiments
11 different search algorithms are compared: 3 uninformed search methods (breadth first, depth first, and uniform cost searc), and 8 with heuristics (A star and greedy best first graph search with the heuristics of unmet goals, maxlevel, levelsum and setlevel), are tested against 4 different planning problems. The planning problems are of increasing complexity, and the searches are done through a planning graph. All experiments are run using pypy rather than normal python to speed up calculation speeds.

### Code implementation
The code for this project is at [this github repo](https://github.com/wwymak/udacity-ai-nd-projects/tree/master/2_Classical%20Planning) Most of this is 'boilerplate' code from Udacity, and my implementation is only in the [planning graph section](https://github.com/wwymak/udacity-ai-nd-projects/blob/master/2_Classical%20Planning/my_planning_graph.py) 

_An interesting todo is to implement my own planning / search code_ 🤓 

### Measuring algorithm performance

As per the [AIMA book](http://aima.cs.berkeley.edu/), the performance of search algorithms are measured in terms of:

> Completeness: Is the algorithm guaranteed to find a solution when there is one?

> Optimality: Does the strategy find the optimal solution (it has the lowest path cost among all solutions) 

> Time complexity: How long does it take to find a solution?

> Space complexity: How much memory is needed to perform the search?

In the experiment set, we can think of space complexity as the number of nodes expanded, time complexity as the time taken to run the algorithm on a problem, and as we know the path plan for each of the strategies, we also know which algorithms are optimal.

### Experiment results
The complete experiment output can be found [here](https://github.com/wwymak/udacity-ai-nd-projects/blob/master/2_Classical%20Planning/run_search_output.csv):
and is also shwon in the table below.

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>problem</th>
      <th>algo</th>
      <th>action</th>
      <th>nodes_expanded</th>
      <th>goal_test</th>
      <th>new_nodes</th>
      <th>plan_length</th>
      <th>time_to_run</th>
      <th>time_run_pypy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>breadth_first_search</td>
      <td>20</td>
      <td>43</td>
      <td>56</td>
      <td>178</td>
      <td>6</td>
      <td>0.006867</td>
      <td>0.032478</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>depth_first_graph_search</td>
      <td>20</td>
      <td>21</td>
      <td>22</td>
      <td>84</td>
      <td>20</td>
      <td>0.005211</td>
      <td>0.007989</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>uniform_cost_search</td>
      <td>20</td>
      <td>60</td>
      <td>62</td>
      <td>240</td>
      <td>6</td>
      <td>0.013549</td>
      <td>0.019776</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>greedy_best_first_graph_search with h_unmet_goals</td>
      <td>20</td>
      <td>7</td>
      <td>9</td>
      <td>29</td>
      <td>6</td>
      <td>0.001590</td>
      <td>0.003040</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>greedy_best_first_graph_search with h_pg_levelsum</td>
      <td>20</td>
      <td>6</td>
      <td>8</td>
      <td>28</td>
      <td>6</td>
      <td>0.643192</td>
      <td>0.668640</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>greedy_best_first_graph_search with h_pg_maxlevel</td>
      <td>20</td>
      <td>6</td>
      <td>8</td>
      <td>24</td>
      <td>6</td>
      <td>0.375530</td>
      <td>0.187120</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>greedy_best_first_graph_search with h_pg_setlevel</td>
      <td>20</td>
      <td>6</td>
      <td>8</td>
      <td>28</td>
      <td>6</td>
      <td>0.627370</td>
      <td>0.514928</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>astar_search with h_unmet_goals</td>
      <td>20</td>
      <td>50</td>
      <td>52</td>
      <td>206</td>
      <td>6</td>
      <td>0.009225</td>
      <td>0.015860</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1</td>
      <td>astar_search with h_pg_levelsum</td>
      <td>20</td>
      <td>28</td>
      <td>30</td>
      <td>122</td>
      <td>6</td>
      <td>1.589226</td>
      <td>0.267637</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1</td>
      <td>astar_search with h_pg_maxlevel</td>
      <td>20</td>
      <td>43</td>
      <td>45</td>
      <td>180</td>
      <td>6</td>
      <td>1.448989</td>
      <td>0.209042</td>
    </tr>
    <tr>
      <th>10</th>
      <td>1</td>
      <td>astar_search with h_pg_setlevel</td>
      <td>20</td>
      <td>33</td>
      <td>35</td>
      <td>138</td>
      <td>6</td>
      <td>1.558533</td>
      <td>0.409566</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2</td>
      <td>breadth_first_search</td>
      <td>72</td>
      <td>3343</td>
      <td>4609</td>
      <td>30503</td>
      <td>9</td>
      <td>2.293861</td>
      <td>0.335592</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2</td>
      <td>depth_first_graph_search</td>
      <td>72</td>
      <td>624</td>
      <td>625</td>
      <td>5602</td>
      <td>619</td>
      <td>3.429965</td>
      <td>0.541581</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2</td>
      <td>uniform_cost_search</td>
      <td>72</td>
      <td>5154</td>
      <td>5156</td>
      <td>46618</td>
      <td>9</td>
      <td>3.829271</td>
      <td>0.724422</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2</td>
      <td>greedy_best_first_graph_search with h_unmet_goals</td>
      <td>72</td>
      <td>17</td>
      <td>19</td>
      <td>170</td>
      <td>9</td>
      <td>0.021665</td>
      <td>0.024978</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2</td>
      <td>greedy_best_first_graph_search with h_pg_levelsum</td>
      <td>72</td>
      <td>9</td>
      <td>11</td>
      <td>86</td>
      <td>9</td>
      <td>15.307723</td>
      <td>0.721489</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2</td>
      <td>greedy_best_first_graph_search with h_pg_maxlevel</td>
      <td>72</td>
      <td>27</td>
      <td>29</td>
      <td>249</td>
      <td>9</td>
      <td>23.846908</td>
      <td>1.121079</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2</td>
      <td>greedy_best_first_graph_search with h_pg_setlevel</td>
      <td>72</td>
      <td>9</td>
      <td>11</td>
      <td>84</td>
      <td>9</td>
      <td>18.951996</td>
      <td>1.206637</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2</td>
      <td>astar_search with h_unmet_goals</td>
      <td>72</td>
      <td>2467</td>
      <td>2469</td>
      <td>22522</td>
      <td>9</td>
      <td>2.476773</td>
      <td>0.569513</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2</td>
      <td>astar_search with h_pg_levelsum</td>
      <td>72</td>
      <td>357</td>
      <td>359</td>
      <td>3426</td>
      <td>9</td>
      <td>410.255449</td>
      <td>15.562978</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2</td>
      <td>astar_search with h_pg_maxlevel</td>
      <td>72</td>
      <td>2887</td>
      <td>2889</td>
      <td>26594</td>
      <td>9</td>
      <td>2136.789477</td>
      <td>85.678390</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2</td>
      <td>astar_search with h_pg_setlevel</td>
      <td>72</td>
      <td>1037</td>
      <td>1039</td>
      <td>9605</td>
      <td>9</td>
      <td>1632.333792</td>
      <td>90.568004</td>
    </tr>
    <tr>
      <th>22</th>
      <td>3</td>
      <td>breadth_first_search</td>
      <td>88</td>
      <td>14663</td>
      <td>18098</td>
      <td>129625</td>
      <td>12</td>
      <td>11.422025</td>
      <td>0.817486</td>
    </tr>
    <tr>
      <th>23</th>
      <td>3</td>
      <td>depth_first_graph_search</td>
      <td>88</td>
      <td>408</td>
      <td>409</td>
      <td>3364</td>
      <td>392</td>
      <td>1.173182</td>
      <td>0.179323</td>
    </tr>
    <tr>
      <th>24</th>
      <td>3</td>
      <td>uniform_cost_search</td>
      <td>88</td>
      <td>18510</td>
      <td>18512</td>
      <td>161936</td>
      <td>12</td>
      <td>15.097682</td>
      <td>1.362900</td>
    </tr>
    <tr>
      <th>25</th>
      <td>3</td>
      <td>greedy_best_first_graph_search with h_unmet_goals</td>
      <td>88</td>
      <td>25</td>
      <td>27</td>
      <td>230</td>
      <td>15</td>
      <td>0.040227</td>
      <td>0.007026</td>
    </tr>
    <tr>
      <th>26</th>
      <td>3</td>
      <td>greedy_best_first_graph_search with h_pg_levelsum</td>
      <td>88</td>
      <td>14</td>
      <td>16</td>
      <td>126</td>
      <td>14</td>
      <td>29.806606</td>
      <td>1.349766</td>
    </tr>
    <tr>
      <th>27</th>
      <td>3</td>
      <td>greedy_best_first_graph_search with h_pg_maxlevel</td>
      <td>88</td>
      <td>21</td>
      <td>23</td>
      <td>195</td>
      <td>13</td>
      <td>32.883521</td>
      <td>1.508719</td>
    </tr>
    <tr>
      <th>28</th>
      <td>3</td>
      <td>greedy_best_first_graph_search with h_pg_setlevel</td>
      <td>88</td>
      <td>35</td>
      <td>37</td>
      <td>345</td>
      <td>17</td>
      <td>100.439219</td>
      <td>5.700636</td>
    </tr>
    <tr>
      <th>29</th>
      <td>3</td>
      <td>astar_search with h_unmet_goals</td>
      <td>88</td>
      <td>7388</td>
      <td>7390</td>
      <td>6511</td>
      <td>12</td>
      <td>10.053471</td>
      <td>0.930212</td>
    </tr>
    <tr>
      <th>30</th>
      <td>3</td>
      <td>astar_search with h_pg_levelsum</td>
      <td>88</td>
      <td>369</td>
      <td>371</td>
      <td>3403</td>
      <td>12</td>
      <td>589.944548</td>
      <td>23.097150</td>
    </tr>
    <tr>
      <th>31</th>
      <td>3</td>
      <td>astar_search with h_pg_maxlevel</td>
      <td>88</td>
      <td>9580</td>
      <td>9582</td>
      <td>86312</td>
      <td>12</td>
      <td>NaN</td>
      <td>446.624085</td>
    </tr>
    <tr>
      <th>32</th>
      <td>3</td>
      <td>astar_search with h_pg_setlevel</td>
      <td>88</td>
      <td>3423</td>
      <td>3425</td>
      <td>31596</td>
      <td>12</td>
      <td>NaN</td>
      <td>485.887562</td>
    </tr>
    <tr>
      <th>33</th>
      <td>4</td>
      <td>breadth_first_search</td>
      <td>104</td>
      <td>99736</td>
      <td>114953</td>
      <td>944130</td>
      <td>14</td>
      <td>115.053001</td>
      <td>6.027091</td>
    </tr>
    <tr>
      <th>34</th>
      <td>4</td>
      <td>depth_first_graph_search</td>
      <td>104</td>
      <td>25174</td>
      <td>25175</td>
      <td>22849</td>
      <td>24132</td>
      <td>NaN</td>
      <td>1341.340737</td>
    </tr>
    <tr>
      <th>35</th>
      <td>4</td>
      <td>uniform_cost_search</td>
      <td>104</td>
      <td>113339</td>
      <td>113341</td>
      <td>1066413</td>
      <td>14</td>
      <td>74.787319</td>
      <td>13.715020</td>
    </tr>
    <tr>
      <th>36</th>
      <td>4</td>
      <td>greedy_best_first_graph_search with h_unmet_goals</td>
      <td>104</td>
      <td>29</td>
      <td>31</td>
      <td>280</td>
      <td>18</td>
      <td>NaN</td>
      <td>0.016012</td>
    </tr>
    <tr>
      <th>37</th>
      <td>4</td>
      <td>greedy_best_first_graph_search with h_pg_levelsum</td>
      <td>104</td>
      <td>17</td>
      <td>19</td>
      <td>165</td>
      <td>17</td>
      <td>NaN</td>
      <td>2.443730</td>
    </tr>
    <tr>
      <th>38</th>
      <td>4</td>
      <td>greedy_best_first_graph_search with h_pg_maxlevel</td>
      <td>104</td>
      <td>56</td>
      <td>58</td>
      <td>580</td>
      <td>17</td>
      <td>NaN</td>
      <td>6.415941</td>
    </tr>
    <tr>
      <th>39</th>
      <td>4</td>
      <td>greedy_best_first_graph_search with h_pg_setlevel</td>
      <td>104</td>
      <td>107</td>
      <td>109</td>
      <td>1164</td>
      <td>23</td>
      <td>NaN</td>
      <td>26.430064</td>
    </tr>
    <tr>
      <th>40</th>
      <td>4</td>
      <td>astar_search with h_unmet_goals</td>
      <td>104</td>
      <td>34330</td>
      <td>34332</td>
      <td>328509</td>
      <td>14</td>
      <td>NaN</td>
      <td>4.468241</td>
    </tr>
    <tr>
      <th>41</th>
      <td>4</td>
      <td>astar_search with h_pg_levelsum</td>
      <td>104</td>
      <td>1208</td>
      <td>1210</td>
      <td>12210</td>
      <td>15</td>
      <td>NaN</td>
      <td>154.348373</td>
    </tr>
    <tr>
      <th>42</th>
      <td>4</td>
      <td>astar_search with h_pg_maxlevel</td>
      <td>104</td>
      <td>62077</td>
      <td>62079</td>
      <td>599376</td>
      <td>14</td>
      <td>NaN</td>
      <td>4474.719203</td>
    </tr>
    <tr>
      <th>43</th>
      <td>4</td>
      <td>astar_search with h_pg_setlevel</td>
      <td>104</td>
      <td>22606</td>
      <td>22608</td>
      <td>224229</td>
      <td>14</td>
      <td>NaN</td>
      <td>4942.232729</td>
    </tr>
  </tbody>
</table>
</div>




### Measuring space complexity:  Nodes expanded vs actions (i.e. problem complexity) and algorithm used

The following slice of the results table shows how the number nodes expanded increases as the problem space increases. As expected, the number of nodes increased as the problem space increased. However, the greedy best first search expanded the smallest number of nodes and more importantly, as the number of actions increased, the nodes expanded increases sublinearly, i.e. the search space doesn't 'explode' like most of the other algorithms tested. 

We can also see that the informed searches does better than all 3 of the uniformed search algorithms, especially as the problem becomes more complex. With the exception of the depth first search, all the uniformed search methods expanded a much larger number of nodes than the informed searches. This is becuase the uniformed search methods have no guidance on where the goal state is, and therefore need to explore more space in order to find the goal. 

Among uninformed search methods, depth first search is the most efficient, with the least number of nodes expanded. Depth first search expands the deepest node first as opposed to _all_ the nodes in a layer as per breadth first/uniform cost search, and therefore has a much smaller branching factor. 

For the search algorithms with heuristics, we can see that the greedy best first search does much better than a* , and that the level sum heuristic is the best in guiding the agent towards the final goal as both algorithms when using this heuristic expands the least number of nodes. Since the greedy algorithm does not take into account the cost of the path it takes to reach a particular node, it does not need to consider previous nodes so it's memory requirements are smaller. 


```python
pivot = pd.pivot_table(df, 'nodes_expanded', 'algo', 'action')
pivot
```




<div>
<style>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>action</th>
      <th>20</th>
      <th>72</th>
      <th>88</th>
      <th>104</th>
    </tr>
    <tr>
      <th>algo</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>astar_search with h_pg_levelsum</th>
      <td>28</td>
      <td>357</td>
      <td>369</td>
      <td>1208</td>
    </tr>
    <tr>
      <th>astar_search with h_pg_maxlevel</th>
      <td>43</td>
      <td>2887</td>
      <td>9580</td>
      <td>62077</td>
    </tr>
    <tr>
      <th>astar_search with h_pg_setlevel</th>
      <td>33</td>
      <td>1037</td>
      <td>3423</td>
      <td>22606</td>
    </tr>
    <tr>
      <th>astar_search with h_unmet_goals</th>
      <td>50</td>
      <td>2467</td>
      <td>7388</td>
      <td>34330</td>
    </tr>
    <tr>
      <th>breadth_first_search</th>
      <td>43</td>
      <td>3343</td>
      <td>14663</td>
      <td>99736</td>
    </tr>
    <tr>
      <th>depth_first_graph_search</th>
      <td>21</td>
      <td>624</td>
      <td>408</td>
      <td>25174</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_levelsum</th>
      <td>6</td>
      <td>9</td>
      <td>14</td>
      <td>17</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_maxlevel</th>
      <td>6</td>
      <td>27</td>
      <td>21</td>
      <td>56</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_setlevel</th>
      <td>6</td>
      <td>9</td>
      <td>35</td>
      <td>107</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_unmet_goals</th>
      <td>7</td>
      <td>17</td>
      <td>25</td>
      <td>29</td>
    </tr>
    <tr>
      <th>uniform_cost_search</th>
      <td>60</td>
      <td>5154</td>
      <td>18510</td>
      <td>113339</td>
    </tr>
  </tbody>
</table>
</div>




```python
# using an alternative pivot for plotting
pivot2 = pd.pivot_table(df, 'nodes_expanded', 'action', 'algo')
ax = pivot2.plot(title="Nodes expanded vs problem size for different planning search algorithms", figsize=(12,8))
ax.set_xlabel("actions")
ax.set_ylabel("nodes expanded")
```


![png](https://github.com/wwymak/udacity-ai-nd-projects/blob/master/2_Classical%20Planning/output_9_1.png)


### Measuring time complexity:  Time required vs problem size and algorithm used

The following table and plot shows how the different algorithms perform in terms of time. For uniformed searches, the breadth first search takes the least time, as opposed to the depth first search, which takes much longer, especially as the problem size increases. This is because in the depth first search, if it goes down the 'wrong' path it will have to backtrack, and a bigger problem means it will spend a lot of time backtracking.

For the informed search algorithms, we can see that the heuristic chosen has a large impact on the time, e.g. using the unmet goals heuristic is about 1000 times faster than the set level heuristic! This is likely because the more complex heuristics take longer to compute, especially if the implementation is not efficient. However, if we compare the heuristics against the node expanded, we can see that the fastest heuristics also ended up with a lot more nodes expanded.


```python
pivot3 = pd.pivot_table(df, 'time_run_pypy', 'algo', 'action')
pivot3
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>action</th>
      <th>20</th>
      <th>72</th>
      <th>88</th>
      <th>104</th>
    </tr>
    <tr>
      <th>algo</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>astar_search with h_pg_levelsum</th>
      <td>0.267637</td>
      <td>15.562978</td>
      <td>23.097150</td>
      <td>154.348373</td>
    </tr>
    <tr>
      <th>astar_search with h_pg_maxlevel</th>
      <td>0.209042</td>
      <td>85.678390</td>
      <td>446.624085</td>
      <td>4474.719203</td>
    </tr>
    <tr>
      <th>astar_search with h_pg_setlevel</th>
      <td>0.409566</td>
      <td>90.568004</td>
      <td>485.887562</td>
      <td>4942.232729</td>
    </tr>
    <tr>
      <th>astar_search with h_unmet_goals</th>
      <td>0.015860</td>
      <td>0.569513</td>
      <td>0.930212</td>
      <td>4.468241</td>
    </tr>
    <tr>
      <th>breadth_first_search</th>
      <td>0.032478</td>
      <td>0.335592</td>
      <td>0.817486</td>
      <td>6.027091</td>
    </tr>
    <tr>
      <th>depth_first_graph_search</th>
      <td>0.007989</td>
      <td>0.541581</td>
      <td>0.179323</td>
      <td>1341.340737</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_levelsum</th>
      <td>0.668640</td>
      <td>0.721489</td>
      <td>1.349766</td>
      <td>2.443730</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_maxlevel</th>
      <td>0.187120</td>
      <td>1.121079</td>
      <td>1.508719</td>
      <td>6.415941</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_setlevel</th>
      <td>0.514928</td>
      <td>1.206637</td>
      <td>5.700636</td>
      <td>26.430064</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_unmet_goals</th>
      <td>0.003040</td>
      <td>0.024978</td>
      <td>0.007026</td>
      <td>0.016012</td>
    </tr>
    <tr>
      <th>uniform_cost_search</th>
      <td>0.019776</td>
      <td>0.724422</td>
      <td>1.362900</td>
      <td>13.715020</td>
    </tr>
  </tbody>
</table>
</div>




```python
pivot4 = pd.pivot_table(df, 'time_run_pypy', 'action', 'algo')
ax = pivot4.plot(title="Time required vs problem size for different planning search algorithms", figsize=(12,8))
ax.set_xlabel("actions")
ax.set_ylabel("time needed (s)")
```


![png](https://github.com/wwymak/udacity-ai-nd-projects/blob/master/2_Classical%20Planning/output_12_1.png)


### Optimality-- which algorithms can achieve the optimal (shortest plan length) solution?

For the uniformed search algorithms, both breadth first and uniform cost searches are optimal. For the informed searches, both A star and greedy search are optimal for smaller problems, but as the problem size increases, A star gives the optimal solution for all the heuristics except for the level sum heuristic whereas the greedy algorithm slowly diverges away from the optimal solution-- likely because as the problem size increases, the cost of the previous path has a bigger and bigger impact on the final cost and as the previous cost is ignored in greedy search, this means it doesn't find the most optimal solution.


```python
pivot5 = pd.pivot_table(df, 'plan_length', 'algo', 'action')
pivot5
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>action</th>
      <th>20</th>
      <th>72</th>
      <th>88</th>
      <th>104</th>
    </tr>
    <tr>
      <th>algo</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>astar_search with h_pg_levelsum</th>
      <td>6</td>
      <td>9</td>
      <td>12</td>
      <td>15</td>
    </tr>
    <tr>
      <th>astar_search with h_pg_maxlevel</th>
      <td>6</td>
      <td>9</td>
      <td>12</td>
      <td>14</td>
    </tr>
    <tr>
      <th>astar_search with h_pg_setlevel</th>
      <td>6</td>
      <td>9</td>
      <td>12</td>
      <td>14</td>
    </tr>
    <tr>
      <th>astar_search with h_unmet_goals</th>
      <td>6</td>
      <td>9</td>
      <td>12</td>
      <td>14</td>
    </tr>
    <tr>
      <th>breadth_first_search</th>
      <td>6</td>
      <td>9</td>
      <td>12</td>
      <td>14</td>
    </tr>
    <tr>
      <th>depth_first_graph_search</th>
      <td>20</td>
      <td>619</td>
      <td>392</td>
      <td>24132</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_levelsum</th>
      <td>6</td>
      <td>9</td>
      <td>14</td>
      <td>17</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_maxlevel</th>
      <td>6</td>
      <td>9</td>
      <td>13</td>
      <td>17</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_pg_setlevel</th>
      <td>6</td>
      <td>9</td>
      <td>17</td>
      <td>23</td>
    </tr>
    <tr>
      <th>greedy_best_first_graph_search with h_unmet_goals</th>
      <td>6</td>
      <td>9</td>
      <td>15</td>
      <td>18</td>
    </tr>
    <tr>
      <th>uniform_cost_search</th>
      <td>6</td>
      <td>9</td>
      <td>12</td>
      <td>14</td>
    </tr>
  </tbody>
</table>
</div>



### Applying search algorithms to various scenarios:

> <strong>Which algorithm or algorithms would be most appropriate for planning in a very restricted domain (i.e., one that has only a few actions) and needs to operate in real time?</strong>

For real time, we want an algorithm that runs very fast, as well as giving a short plan length. With the exception of depth first search, all of the other algorithms give an optimal solution. Since the greedy search algorithm gives the shortest times among them as well as the least number of nodes expanded (and hence uses less memory, it is probably a good choice in this scenario.

><strong>Which algorithm or algorithms would be most appropriate for planning in very large domains (e.g., planning delivery routes for all UPS drivers in the U.S. on a given day)</strong>

We would need an algorithm that runs fairly fast even on large problem size (otherwise the day will be over before the planning calculation finishes), and does not expand too many nodes( otherwise the planning computation will run out of memory). A good choice is the greedy search algorithm-- even if it doesn't give the most optimal solution, the solution isn't too far off optimal, and it runs quicker and expands less nodes as problem size increases as compared to the others.


><strong>Which algorithm or algorithms would be most appropriate for planning problems where it is important to find only optimal plans?</strong>

From the experiments, we can see that A star, breadth first and uniform cost search all return the optimal plan, even as the problem size increases. If optimality is the only consideration, all of them are appropiate choices. If we need to optimise for memory and/or time as well, then we should use A star (with unmet goal heuristic) since this algorithm + heuristic combination gives the least  increase in both memory and time as problem size increases.

### Conclusion

From this set of experiments, we can see that informed search algorithms with the right heuristics can perform much better than uninformed search algorithms in terms of both speed and memory requirements, and still return optimal plans. from the experiments, the unmet goals heuristic is the most optimal for time, and the level sum heuristic is the most optimal for memory. Depending on the scenario complexity and computation requirements, we can tune the heuristic to suit.
