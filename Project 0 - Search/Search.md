# Search

## What is Search?

Search problems involve an agent that is given:
- Initial State
- Goal State
= Return a solution of how to get from the former to the latter

## Terminologies

#### Agent

An entity that perceives its environment and acts upon that environment.

i.e. In the case of self-driving cars, the agent might be the car, that is perceiving all these external factors to determine where to drive towards, in order to arrive at a destination

i.e. In the case of a puzzle, the agent might be the solver

#### State

A configuration of the agent in its environment. 

i.e. In a 15 puzzle, a state is any one way that all the numbers are arranged on the board

i.e. In the case of self-driving cars, the state might be the environment, with all the different locations of roads and traffic lights

#### Initial State

The state from which the search algorithm starts. 

i.e. In a navigator app for self-driving cars, the initial state would be the current location

#### Actions

Choices that we can make in a state. Actions can be defined as a function ACTIONS(s).

So, given receiving state s as input, ACTIONS(s) returns as output the set of actions that cna be executed in state s. 

#### Transition Model

A description of what state we get after we perform any applicable action in any state.

In this case, transition model will be RESULT(s, a) -> given action a in state s, RESULT.

#### State Space

Set of all states reachable from the initial state, by any possible sequence of actions. 

It is usually described in a graph of nodes with directions between each node (state). 

#### Goal Test

Way to determine whether a given state is a goal state. 

i.e. In a navigator app, the goal test would be whether the current location of the agent is at the destination. 

#### Path Cost

Numerical cost associated with a given path. We formulate the cost of each solution, and how costly it would be. We would want to find the path with the least path cost (save time, save money, save power, etc)

i.e. A navigator app does not bring you to your goal, and make detours. 

## Search Problems

Consider:
- Initial State
- Actions
- Transition Model
- Goal Test
- Path Cost

#### Solution

A solution that has the lowest path cost among all solutions, considering the initial state, actions, goal test, etc. 

## Solvng Search Problems

We use a node in our search problems:
- It is a data structure that keeps track of
- A state 
- A parent (the node that generated this node)
- An action (action applied to parent to get node)
- A path cost (from initial state to node)

### Approach

From a given state, we have multiple options. We need to explore these options. We need to store all these nodes.

Since nodes don't search, they just hold information, thus to search these information, we need to use the frontier.

#### Frontier

Frontier is a mechanism that manages these nodes.

The frontier starts by containing the initial state. That is the only state we know of at the start. 

Our search process repeats the process over and over again.

- If the frontier is empty, then there is no solution.
- Otherwise, we will remove a node from the frontier. 
- If node contains goal state, return the solution. Stop
- Else, expand node, add resulting nodes to the frontier. (To look at the neighbours of the nodes)

At a high level, we constantly remove nodes and add to it, and check for solutions. If empty, no solutions. 

Given the information, here is a revised approach. 

#### Revised Approach

1. Start with a frontier that contains the initial state
2. Start with an empty explored set
3. Repeat:
- If frontier is empty, then no solution
- Remove a node from the frontier
- If node contains goal state, return the solution
- Add the node to the explored set (so that we know that we have already explored the node before)
- Expand node, add resulting nodes to the frontier if they aren't already in the frontier or explored set

For the frontier, we would require the use of a stack as the data structure. (Last in, first out data type)

### Search Algorithms

1. Depth First Search

- We always expands the deepest node in the frontier. 
- If hit a dead end, we back up and keep backing up.
- Utilizes a stack (Last in, first out)
- Keep going down a specific branch

2. Breadth First Search

- Search algorithm that always expands the shallowest node in the frontier
- Utilizes queue (First in, first out -> The earlier you are put in, the earlier you get explored) 
- 1 state away, 2 state away, 3 state away, until hits a solution
