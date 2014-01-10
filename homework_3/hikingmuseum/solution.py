'''
Created on Jan 10, 2014

@author: diegob
'''

# Sunny is 1, Rain is 0
P_X0 = [0.4, 0.6]
# Hike is 1, Museum is 0
# P_X1_C_X0 = P(X1 = 1 | X0 = x0)
P_X1_C_X0 = [[0.8, 0.2], [0.2, 0.8]]
# Uri is 0, Zurich is 1, Bern is 2, Valais is 3, Genf is 4, Lucerne is 5
# P_X2_C_X1 = P(X2 = i | X1 = x1)
P_X2_C_X1 = [[0, 0.3, 0.2, 0, 0.3, 0.2], [0.3, 0.2, 0.4, 0.1, 0, 0]]

def computeJointDistribution():
    joint_table = {}
    print "X0 (Sunny = 1, Rain = 0) | X1 (Hike = 1, Museum = 0) | X2 (Uri = 0, Zurich = 1, Bern = 2, Valais = 3, Genf = 4, Lucerne = 5) | P(X0, X1, X2)"
    for x0 in [0, 1]:
        for x1 in [0, 1]:
            for x2 in [0, 1, 2, 3, 4, 5]:
                joint_table[(x0, x1, x2)] = P_X2_C_X1[x1][x2]*P_X1_C_X0[x0][x1]*P_X0[x0]
                print "%s                        | %s                         | %s                                                                     | %s" % (x0, x1, x2, joint_table[(x0, x1, x2)])
    return joint_table

def marginalProb(joint_dist, x2 = 1):
    marginal = 0.0
    for x0 in [0, 1]:
        for x1 in [0, 1]:
            marginal += joint_dist[(x0, x1, x2)]
    return marginal

def conditionQuery(joint_dist, notZurich):
    marginal = 1.0 - notZurich
    condProb = 0.0
    for x1 in [0,1]:
        for x2 in [0, 2, 3, 4, 5]:
            condProb += joint_dist[(0, x1, x2)]
    return condProb/marginal
def main():
    joint_table = computeJointDistribution()
    print "Probability of being in Zurich: %s" % marginalProb(joint_table, x2 = 1)
    print "Probability of rain given not being in Zurich: %s" % conditionQuery(joint_table, 0.244)
if __name__ == '__main__':
    main()