'''
Created on Jan 11, 2014

@author: diegob
'''
import math


def naiveBayesTrain(trainFile):
    parameter_counts = []
    for _ in xrange(11):
        parameter_counts.append(0.0)
    N = 0
    for line in trainFile:
        tokens = line.strip().split(' ')
        C = int(tokens[0])
        if C == 1:
            parameter_counts[0] += 1
            for i in xrange(1, 6):
                if int(tokens[i]) == 1:
                    parameter_counts[2*i - 1] += 1
        else:
            for i in xrange(1, 6):
                if int(tokens[i]) == 1:
                    parameter_counts[2*i] += 1
        N += 1
    probabilities = []
    for i in xrange(len(parameter_counts)):
        if i == 0:
            probabilities.append(parameter_counts[i]/N)
        elif i % 2 == 0:
            probabilities.append(parameter_counts[i]/(N - parameter_counts[0]))
        else:
            probabilities.append(parameter_counts[i]/parameter_counts[0])
    print probabilities
    return probabilities

def naiveBayesPredict(dataFile, model):
    predictedLabels = []
    realLabels = []
    for line in dataFile:
        tokens = line.strip().split(' ')
        realLabels.append(int(tokens[0]))
        probs = [1 - model[0], model[0]]
        for i in xrange(1, 6):
            if int(tokens[i]) == 1:
                probs[0] *= model[2*i]
                probs[1] *= model[2*i - 1]
            else:
                probs[0] *= (1 - model[2*i])
                probs[1] *= (1 - model[2*i - 1])
        if probs[0] > probs[1]:
            predictedLabels.append(0)
        else:
            predictedLabels.append(1)
    return predictedLabels, realLabels

def calculateError(predicted, real):
    error = 0.0
    for i in xrange(len(predicted)):
        if(predicted[i] != real[i]):
            error += 1
    print "Absolute error: %s" % error
    print "Relative misclassification: %s" % (error/len(predicted))

def buildJointTable(trainFile):
    jointTable = {}
    N = 0
    for line in trainFile:
        tokens = line.strip().split(' ')
        tokenized = tuple(int(x) for x in tokens)
        if tokenized not in jointTable:
            jointTable[tokenized] = 0.0
        jointTable[tokenized] += 1
        N += 1
    for key in jointTable:
        jointTable[key] = jointTable[key]/N
    print jointTable
    return jointTable

def jointProb(x, y,x_i, y_i, c, joint_table):
    other_variables = list(set([1,2,3,4,5]) - set([x,y]))
    prob = 0.0
    key_tuple = [c, 0,0,0,0,0]
    key_tuple[x] = x_i
    key_tuple[y] = y_i
    for z_1 in [0,1]:
        for z_2 in [0,1]:
            for z_3 in [0,1]:
                key_tuple[other_variables[0]] = z_1
                key_tuple[other_variables[1]] = z_2
                key_tuple[other_variables[2]] = z_3
                real_tuple = tuple(key_tuple)
                if real_tuple in joint_table:
                    prob += joint_table[real_tuple]
    return prob

def jointProbS(x, x_i, c, joint_table):
    other_variables = list(set([1,2,3,4,5]) - set([x]))
    prob = 0.0
    key_tuple = [c, 0,0,0,0,0]
    key_tuple[x] = x_i
    for z_1 in [0,1]:
        for z_2 in [0,1]:
            for z_3 in [0,1]:
                for z_4 in [0,1]:
                    key_tuple[other_variables[0]] = z_1
                    key_tuple[other_variables[1]] = z_2
                    key_tuple[other_variables[2]] = z_3
                    key_tuple[other_variables[3]] = z_4
                    real_tuple = tuple(key_tuple)
                    if real_tuple in joint_table:
                        prob += joint_table[real_tuple]
    return prob


def calculateMutualInfo(x, y, joint_table, P_C):
    mutual_info = 0.0
    for c in [0,1]:
        for x_i in [0, 1]:
            for y_i in [0, 1]:
                P_D_x_y_c = jointProb(x,y, x_i, y_i, c, joint_table)
                P_D_x_c = jointProbS(x, x_i, c, joint_table)
                P_D_y_c = jointProbS(y, y_i, c, joint_table)
                if c == 0:
                    p = 1 - P_C
                else:
                    p = P_C
                term = P_D_x_y_c*math.log(P_D_x_y_c*p/(P_D_x_c*P_D_y_c))
                mutual_info += term
    return mutual_info

def TANBayesTrain(trainFile):
    # Parameter 0: P(C)
    # Parameter 1: P(A2 | C)
    # Parameter 2: P(A1 | A2, C)
    # Parameter 3: P(A3 | A2, C)
    # Parameter 4: P(A4 | A2, C)
    # Parameter 5: P(A5 | A4, C)
    parameter_counts = []
    parameter_counts.append([0.0, 0.0])
    parameter_counts.append([[0.0, 0.0], [0.0, 0.0]])
    parameter_counts.append([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    parameter_counts.append([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    parameter_counts.append([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    parameter_counts.append([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    for line in trainFile:
        tokens = line.strip().split(' ')
        C = int(tokens[0])
        A1 = int(tokens[1])
        A2 = int(tokens[2])
        A3 = int(tokens[3])
        A4 = int(tokens[4])
        A5 = int(tokens[5])
        parameter_counts[0][C] += 1
        parameter_counts[1][C][A2] += 1
        parameter_counts[2][C*2 + A2][A1] += 1
        parameter_counts[3][C*2 + A2][A3] += 1
        parameter_counts[4][C*2 + A2][A4] += 1
        parameter_counts[5][C*2 + A4][A5] += 1
    model = []
    model.append([parameter_counts[0][0]/sum(parameter_counts[0]),parameter_counts[0][1]/sum(parameter_counts[0])])
    model.append([[parameter_counts[1][0][0]/sum(parameter_counts[1][0]), parameter_counts[1][0][1]/sum(parameter_counts[1][0])], [parameter_counts[1][1][0]/sum(parameter_counts[1][1]), parameter_counts[1][1][1]/sum(parameter_counts[1][1])]])
    for i in xrange(2, 6):
        model.append([])
        for j in xrange(0, 4):
            model[i].append([parameter_counts[i][j][0]/sum(parameter_counts[i][j]), parameter_counts[i][j][1]/sum(parameter_counts[i][j])])
    return model

def TANBayesPredict(dataFile, model):
    predictedLabels = []
    realLabels = []
    for line in dataFile:
        tokens = line.strip().split(' ')
        realLabels.append(int(tokens[0]))
        A1 = int(tokens[1])
        A2 = int(tokens[2])
        A3 = int(tokens[3])
        A4 = int(tokens[4])
        A5 = int(tokens[5])
        probs = [0.0,0.0]
        for C in [0,1]:
            probs[C] = model[0][C]*model[1][C][A2]*model[2][C*2 + A2][A1]*model[3][C*2 + A2][A3]*model[4][C*2 + A2][A4]*model[5][C*2 + A4][A5]
        if probs[0] > probs[1]:
            predictedLabels.append(0)
        else:
            predictedLabels.append(1)
    return predictedLabels, realLabels
def main():
    # Naive Bayes approach
    trainFileHandle = open('trainingData.txt', 'r')
    model = naiveBayesTrain(trainFileHandle)
    trainFileHandle.seek(0)
    testFileHandle = open('testingData.txt', 'r')
    pL, rL = naiveBayesPredict(testFileHandle, model)
    calculateError(pL, rL)
    testFileHandle.seek(0)
    # TAN approach
    #joint_dist = buildJointTable(trainFileHandle)
    #for i in xrange(1, 6):
    #    for j in xrange(i + 1, 6):
    #        pass
    #        print "%s,%s : %s" % (i, j, calculateMutualInfo(i, j, joint_dist, model[0]))
    trainFileHandle.seek(0)
    model = TANBayesTrain(trainFileHandle)
    pL, rL = TANBayesPredict(testFileHandle, model)
    calculateError(pL, rL)
    trainFileHandle.close()
    testFileHandle.close()

if __name__ == '__main__':
    main()