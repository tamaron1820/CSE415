#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Tuple, Callable, List

import toh_mdp as tm


def value_iteration(
        mdp: tm.TohMdp, v_table: tm.VTable
) -> Tuple[tm.VTable, tm.QTable, float]:
    """Computes one step of value iteration.

    Hint 1: Since the terminal state will always have value 0 since
    initialization, you only need to update values for nonterminal states.

    Hint 2: It might be easier to first populate the Q-value table.

    Args:
        mdp: the MDP definition.
        v_table: Value table from the previous iteration.

    Returns:
        new_v_table: tm.VTable
            New value table after one step of value iteration.
        q_table: tm.QTable
            New Q-value table after one step of value iteration.
        max_delta: float
            Maximum absolute value difference for all value updates, i.e.,
            max_s |V_k(s) - V_k+1(s)|.
    """
    new_v_table: tm.VTable = v_table.copy()
    q_table: tm.QTable = {}
    # noinspection PyUnusedLocal
    max_delta = 0.0
    # *** BEGIN OF YOUR CODE ***
    new_v_table[mdp.nonterminal_states]=0
    
    for s1 in mdp.nonterminal_states:
        max_val=-float("inf")
        for a in mdp.actions:
            if a=='Exit':
                q_table[(s1,a)]=mdp.reward(s1,a,mdp.terminal)
            else:
                q_table[(s1,a)]=0
                for s2 in mdp.nonterminal_states:
                    p=mdp.transition(s1,a,s2)
                    q_table[(s1,a)]+=p*(mdp.reward(s1,a,s2)+mdp.config.gamma*v_table[s2])
            max_val=max(max_val,q_table[(s1,a)])
        new_v_table[s1]=max_val
        max_delta=max(max_delta,abs(v_table[s1]-new_v_table[s1]))
    # ***  END OF YOUR CODE  ***
    return new_v_table, q_table, max_delta


def extract_policy(
        mdp: tm.TohMdp, q_table: tm.QTable
) -> tm.Policy:
    """Extract policy mapping from Q-value table.

    Remember that no action is available from the terminal state, so the
    extracted policy only needs to have all the nonterminal states (can be
    accessed by mdp.nonterminal_states) as keys.

    Args:
        mdp: the MDP definition.
        q_table: Q-Value table to extract policy from.

    Returns:
        policy: tm.Policy
            A Policy maps nonterminal states to actions.
    """
    # *** BEGIN OF YOUR CODE ***
    tm.Policy={}
    
    for s1 in mdp.nonterminal_states:
        max_val=-float("inf")
        action=""
        for a in mdp.actions:
            if q_table[(s1,a)]>max_val:
                max_val=q_table[(s1,a)]
                action=a
        tm.Policy[s1]=action
    return tm.Policy



    


def q_update(
        mdp: tm.TohMdp, q_table: tm.QTable,
        transition: Tuple[tm.TohState, tm.TohAction, float, tm.TohState],
        alpha: float) -> None:
    """Perform a Q-update based on a (S, A, R, S') transition.

    Update the relevant entries in the given q_update based on the given
    (S, A, R, S') transition and alpha value.

    Args:
        mdp: the MDP definition.
        q_table: the Q-Value table to be updated.
        transition: A (S, A, R, S') tuple representing the agent transition.
        alpha: alpha value (i.e., learning rate) for the Q-Value update.
    """
    state, action, reward, next_state = transition
    # *** BEGIN OF YOUR CODE ***
    max_val=-float("inf")
    if next_state!=mdp.terminal:
        for a in mdp.actions:
            if q_table[(next_state,a)]>max_val:
                max_val=q_table[(next_state,a)]
        q_table[(state,action)]=(1-alpha)*q_table[(state,action)]+alpha*(reward+mdp.config.gamma*max_val)
    else:
        q_table[(state,action)]=(1-alpha)*q_table[(state,action)]+alpha*reward


    


def extract_v_table(mdp: tm.TohMdp, q_table: tm.QTable) -> tm.VTable:
    """Extract the value table from the Q-Value table.

    Args:
        mdp: the MDP definition.
        q_table: the Q-Value table to extract values from.

    Returns:
        v_table: tm.VTable
            The extracted value table.
    """
    # *** BEGIN OF YOUR CODE ***
    v_table: tm.VTable={}
    for s1 in mdp.nonterminal_states:
        v_table[s1]=-float("inf")
        for a in mdp.actions:
            v_table[s1]=max(q_table[(s1,a)],v_table[s1])
    return v_table 



def choose_next_action(
        mdp: tm.TohMdp, state: tm.TohState, epsilon: float, q_table: tm.QTable,
        epsilon_greedy: Callable[[List[tm.TohAction], float], tm.TohAction]
) -> tm.TohAction:
    """Use the epsilon greedy function to pick the next action.

    You can assume that the passed in state is neither the terminal state nor
    any goal state.

    You can think of the epsilon greedy function passed in having the following
    definition:

    def epsilon_greedy(best_actions, epsilon):
        # selects one of the best actions with probability 1-epsilon,
        # selects a random action with probability epsilon
        ...

    See the concrete definition in QLearningSolver.epsilon_greedy.

    Args:
        mdp: the MDP definition.
        state: the current MDP state.
        epsilon: epsilon value in epsilon greedy.
        q_table: the current Q-value table.
        epsilon_greedy: a function that performs the epsilon

    Returns:
        action: tm.TohAction
            The chosen action.
    """
    # *** BEGIN OF YOUR CODE ***
    tm.TohAction=[]
    max_val=-float("inf")
    for a in mdp.actions:
        if q_table[(state,a)]>max_val :
            max_val=q_table[(state,a)]
            tm.TohAction.clear()
            tm.TohAction.append(a)
        elif q_table[(state,a)]==max_val:
            tm.TohAction.append(a)
    action=epsilon_greedy(tm.TohAction,epsilon)
    return action


def custom_epsilon(n_step: int) -> float:
    """Calculates the epsilon value for the nth Q learning step.

    Define a function for epsilon based on `n_step`.

    Args:
        n_step: the nth step for which the epsilon value will be used.

    Returns:
        epsilon: float
            epsilon value when choosing the nth step.
    """
    # *** BEGIN OF YOUR CODE ***
    epsilon: float=1.0
    epsilon_decay=0.9999965
    epsilon_min=0.05
    for i in(range(1,n_step+1)):
        epsilon=max(epsilon*epsilon_decay,epsilon_min)
    return epsilon


def custom_alpha(n_step: int) -> float:
    """Calculates the alpha value for the nth Q learning step.

    Define a function for alpha based on `n_step`.

    Args:
        n_step: the nth update for which the alpha value will be used.

    Returns:
        alpha: float
            alpha value when performing the nth Q update.
    """
    # *** BEGIN OF YOUR CODE ***
    
