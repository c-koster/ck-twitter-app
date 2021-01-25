"""
hold some machinery to make my weather predictions:
1 join on timestamp to pair the weather table and the examples table (use class method like get_y)
2 create a key based upon the top 50? most commonly used emojis


i need to re-write this entire thing using the numpy vectorizer
"""
import numpy as np

from models import *



def get_examples():
    """
    Get examples from models.py as a of json objects. I use a method create_json_with_weather
    """
    examples = Example.query.all()
    examples_json = []
    for i in examples:
        examples_json.append(i.create_json_with_weather())
    return examples_json


def create_index(data,num_features):
    """
    create a key based upon the top (50?) most commonly used emojis. This works as a guide
    for where to put the counts in the matrices.
    """
    p = {}
    count = 1


    for example in data:
        for emoji in example["contents"]:
            if emoji not in p:
                p[emoji] = count
                count += 1
            if count > num_features:
                return p
    # for now I'm returning the first num_featurs emojis that appear, not the most used ones
    return p


def build_matrices(data,index):
    """
    Return a numpy matrix to hold my examples. Friendly reminder that I want to initialize
     each row as [1 * * * *] so I've got a bias/coefficient variable.
    Also return temperature in imperial as a vector.
    """
    m = len(data)# number of rows
    n = len(index) + 1# number of columns/features
    print(f"creating matrix of size {m}x{n}")
    array = np.zeros((m,n),int)
    y = np.zeros(m,float)
    for i in range(m):
        array[i] = create_row(data[i],index) # helper function returns list of size n
        y[i] = data[i]['weather']['temperature']

    # return the training set and its labels. For LR/NN's,
    return array,y

def create_row(example,index):
    """
    hello I am a helper function for the row above. For cleanup, make me work using dictionary.items()
    """
    L = [1]
    for i in range(len(index)):
        L.append(0) # placeholder
    for e in example["contents"]:
        if e in index:
            L[index[e]]= example["contents"][e]
    return L


def create_model(A,b):
    """
    First try to do this using the algebraic method. This returns least-squares theta
    """
    A_transpose = A.T
    mult = np.dot(A_transpose,A) # A-transpose * A
    mult_inv = np.linalg.inv(mult) # (A-transpose * A)^-1
    # this is wrong... mult * inv doesn't return I_n
    #print(np.dot(mult,mult_inv))
    A_T_b = np.dot(A_transpose,b)
    theta = np.dot(mult_inv,A_T_b) # inverted term left multiplied to (a-transpose*b)
    return theta


def create_model_grad(A,b,a=.01,num_iter=100000):
    """
    Using gradient descent for linear regression.

    """
    n = len(A.T)
    m = len(b)
    theta = np.ones(n)# initialize theta
    c = a*(1/m) # and constant

    for iteration in range(num_iter+1):
        h = A.dot(theta)
        errors = h - b # total error
        # compute cost
        #print("Mean squared error for iteration " +str(iteration)+ ":")
        #print(compute_cost(A,b,theta))
        update_theta = c*(A.T.dot(errors))
        theta = (theta - update_theta)

    return theta


def compute_cost(A,b,theta):
    """
    Compute mean squared error for given theta
    """
    h = A.dot(theta)
    error = (h - y);
    error_squared = np.dot(error,error);
    J = error_squared/(2*len(h))
    return J


if __name__ == '__main__':

    print("-"*12)

    # 1 pair the weather table and the examples table and import them
    examples_json = get_examples()

    # 2 create an index to help me build the matrix
    index = create_index(examples_json,num_features = 50)
    # this is where you get to decidee how wide your training set shall be (num_features + 1)x(num_examples).


    # 3 create a matrix with these guys
    training_set,y = build_matrices(data=examples_json,index=index)

    # 4 get theta--iterative or algebraic method
    theta = create_model(A=training_set,b=y)
    test = training_set[2]
    theta2 = create_model_grad(A=training_set,b=y)

    print(theta)
    print("final cost for theta (lin): " + str(compute_cost(training_set,y,theta)))

    print(theta2)
    print("final cost for theta2 (grad): " + str(compute_cost(training_set,y,theta2)))
