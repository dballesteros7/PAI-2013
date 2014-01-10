'''
Created on Jan 10, 2014

@author: diegob
'''
import copy
import random
import numpy as np

P_B = [0.1,0.9]
P_M = [0.9,0.1]
P_I = {(0,0) : [0.9,0.1],
       (0,1) : [0.5,0.5],
       (1,0) : [0.5,0.5],
       (1,1) : [0.1,0.9]} # P(I | B,M)
P_G = {(0,0,0) : [1.0,0.0],
       (0,0,1) : [1.0,0.0],
       (0,1,0) : [0.9,0.1],
       (0,1,1) : [0.8,0.2],
       (1,0,0) : [1.0,0.0],
       (1,0,1) : [1.0,0.0],
       (1,1,0) : [0.2,0.8],
       (1,1,1) : [0.1,0.9]
       } # P(G | B,I,M)
P_J = {0 : [1.0,0.0],
       1 : [0.1,0.9]} # P(J | G)

P_B_g_i_m = {}
P_M_g_i_b = {}
P_I_g_b_m = {}
P_G_i_b_m_j = {}

def coin_flip(p):
    x = random.random()
    if x < p:
        return 1
    else:
        return 0

def get_P_B_g_i_m(current_state):
    others = (current_state['G'], current_state['I'], current_state['M'])
    if others not in P_B_g_i_m:
        P_0_g_i_m = P_G[(0, current_state['I'], current_state['M'])][current_state['G']]*P_I[(0, current_state['M'])][current_state['I']]*P_B[0]
        P_1_g_i_m = P_G[(1, current_state['I'], current_state['M'])][current_state['G']]*P_I[(1, current_state['M'])][current_state['I']]*P_B[1]
        P_B_g_i_m[others] = P_1_g_i_m/(P_0_g_i_m + P_1_g_i_m)
    return P_B_g_i_m[others]

def get_M_g_i_b(current_state):
    others = (current_state['G'], current_state['I'], current_state['B'])
    if others not in P_M_g_i_b:
        P_0_g_i_b = P_G[(current_state['B'], current_state['I'], 0)][current_state['G']]*P_I[(current_state['B'], 0)][current_state['I']]*P_M[0]
        P_1_g_i_b = P_G[(current_state['B'], current_state['I'], 1)][current_state['G']]*P_I[(current_state['B'], 1)][current_state['I']]*P_M[1]
        P_M_g_i_b[others] = P_1_g_i_b/(P_0_g_i_b + P_1_g_i_b)
    return P_M_g_i_b[others]

def get_I_g_b_m(current_state):
    others = (current_state['G'], current_state['B'], current_state['M'])
    if others not in P_I_g_b_m:
        P_0_g_b_m = P_G[(current_state['B'], 0, current_state['M'])][current_state['G']]*P_I[(current_state['B'],current_state['M'])][0]
        P_1_g_b_m = P_G[(current_state['B'], 1, current_state['M'])][current_state['G']]*P_I[(current_state['B'],current_state['M'])][1]
        P_I_g_b_m[others] = P_1_g_b_m/(P_1_g_b_m + P_0_g_b_m)
    return P_I_g_b_m[others]

def get_G_i_b_m_j(current_state):
    others = (current_state['I'], current_state['B'], current_state['M'], current_state['J'])
    if others not in P_G_i_b_m_j:
        P_0_i_b_m_j = P_J[0][current_state['J']]*P_G[(current_state['B'], current_state['I'], current_state['M'])][0]
        P_1_i_b_m_j = P_J[1][current_state['J']]*P_G[(current_state['B'], current_state['I'], current_state['M'])][1]
        P_G_i_b_m_j[others] = P_1_i_b_m_j/(P_0_i_b_m_j + P_1_i_b_m_j)
    return P_G_i_b_m_j[others]

def produce_new_sample(current_state, variable):
    if variable == 'B':
        # P(B | g, i, m) = (1/Z)P(g | i,m,B)P(i | m,B)P(B)
        p = get_P_B_g_i_m(current_state)
    elif variable == 'M':
        # P(M | g, i, b) = (1/Z)P(g | i,m,B)P(i | M,b)P(M)
        p = get_M_g_i_b(current_state)
    elif variable == 'I':
        # P(I | g, b, m) = (1/Z)P(g | I,m,b)P(I | m,b)
        p = get_I_g_b_m(current_state)
    elif variable == 'G':
        # P(G | i, b, m, j) = (1/Z)P(j | G)P(G | i,m,b)
        p = get_G_i_b_m_j(current_state)
    new_state_value = coin_flip(p)
    new_state = copy.copy(current_state)
    new_state[variable] = new_state_value
    return new_state


def main():
    R = 10
    values = []
    for _ in xrange(R):
        N = 100000
        Count_B = 0.0
        state = {'B' : 0, 'M' : 0, 'I' : 0, 'G' : 0, 'J' : 0}
        for _ in xrange(N):
            for x in ['B', 'M', 'I', 'G']:
                state = produce_new_sample(state, x)
                if state['B'] == 1:
                    Count_B += 1
        values.append(Count_B/(4*N))
    print np.mean(values)
    print np.std(values)

if __name__ == '__main__':
    main()