"""=================================================== Assignment 6 ===================================================

Some instructions:
    * You can write seperate function for gradient and hessian computations.
    * You can also write any extra function as per need.
    * Use in-build functions for the computation of inverse, norm, etc.

"""

""" Import the required libraries"""


# Start your code here
import numpy as np
import math
# End your code here

def func(x_input):
    """
    --------------------------------------------------------
    Write your logic to evaluate the function value.

    Input parameters:
        x: input column vector (a numpy array of n x 1 dimension)

    Returns:
        y : Value of the function given in the problem at x.

    --------------------------------------------------------
    """

    # Start your code here
    # y = -0.0001*(abs(np.sin(x_input[0]) * np.sin(x_input[1])*np.exp(abs(100 - (np.sqrt(x_input[0]**2 + x_input[1]**2))/math.pi)))**0.1)
    y = x_input[0]**2 + x_input[1]**2 + (0.5*x_input[0] + x_input[1])**2 + (0.5*x_input[0] + x_input[1])**4
    # y = abs(x_input[0])**2 + abs(x_input[1])**3
    # End your code here

    return y


def gradient(func, x_input):
    """
    --------------------------------------------------------------------------------------------------
    Write your logic for gradient computation in this function. Use the code from assignment 2.

    Input parameters:
      func : function to be evaluated
      x_input: input column vector (numpy array of n dimension)

    Returns:
      delF : gradient as a column vector (numpy array)
    --------------------------------------------------------------------------------------------------
    """
    # Start your code here
    # Use the code from assignment 2
    h = 0.001
    grad_f = np.array([])
    for i in range(len(x_input)):
        e = np.array([np.zeros(len(x_input), dtype=int)]).T
        e[i][0] = 1
        del_f = (func(x_input + (h * e)) - func(x_input - (h * e))) / (2 * h)
        grad_f = np.append(grad_f, del_f)
    delF = np.array([grad_f]).T


    # End your code here

    return delF


def hessian(func, x_input):
    """
    --------------------------------------------------------------------------------------------------
    Write your logic for hessian computation in this function. Use the code from assignment 2.

    Input parameters:
      func : function to be evaluated
      x_input: input column vector (numpy array)

    Returns:
      del2F : hessian as a 2-D numpy array
    --------------------------------------------------------------------------------------------------
    """
    # Start your code here
    # Use the code from assignment 2
    n = len(x_input)
    del_x = np.full(shape=n, fill_value=0.001)
    del2F = np.array([]).reshape(0, n)
    for i in range(n):
        hess_f = np.array([])
        del_i = np.array([np.zeros(n)]).T
        del_i[i][0] = del_x[i]
        for j in range(n):
            del_j = np.array([np.zeros(n)]).T
            del_j[j][0] = del_x[j]
            if (i == j):
                a = x_input + del_i
                b = x_input - del_j
                value = (func(a) - (2 * func(x_input)) + func(b)) / (del_x[i] ** 2)
                hess_f = np.append(hess_f, value)
            else:
                a = x_input + del_i + del_j
                b = x_input - del_i - del_j
                c = x_input - del_i + del_j
                d = x_input + del_i - del_j
                value = (func(a) + func(b) - func(c) - func(d)) / (4 * del_x[i] * del_x[j])
                hess_f = np.append(hess_f, value)
        del2F = np.vstack([del2F, hess_f])


    # End your code here

    return del2F

def PDM(R , x):
    p_newton = -np.linalg.inv(hessian(func, x)) @ gradient(func, x)
    b = hessian(func, x)
    if ((gradient(func, x).T) @ b) @ gradient(func, x) > 0:
        p_cauchy = -((gradient(func, x).T @ gradient(func, x)) / (
                ((gradient(func, x).T) @ b) @ gradient(func, x))) * gradient(func, x)
    else:
        p_cauchy = (-R / (np.sqrt(gradient(func, x).T @ gradient(func, x)))) * gradient(func, x)
    theta = (-1 * ((p_newton - p_cauchy).T) @ p_cauchy + np.sqrt(
        (((p_newton - p_cauchy).T) @ p_cauchy) ** 2 + (R ** 2 - (p_cauchy.T @ p_cauchy)) * (
                    (p_newton - p_cauchy).T @ (p_newton - p_cauchy)))) / (
                        (p_newton - p_cauchy).T @ (p_newton - p_cauchy))
    p_other = theta * p_newton + (1 - theta) * p_cauchy
    if np.sqrt(p_newton.T@p_newton) <= R:
        return p_newton
    elif np.sqrt(p_cauchy.T@p_cauchy) >=R:
        return ((R/np.sqrt(p_cauchy.T@p_cauchy))*p_cauchy)
    else:
        return p_other

def M(func ,x,p):
    l = func(x) + gradient(func,x).T@p + 0.5*((p.T@hessian(func,x))@p)
    return l


def TRPD(func, x_initial):
    """
    -----------------------------------------------------------------------------------------------------------------------------
    Write your logic for Trust Region - Powell Dogleg Method.

    Input parameters:
        func : input function to be evaluated
        x_initial: initial value of x, a column vector (numpy array)

    Returns:
        x_output : converged x value, a column vector (numpy array)
        f_output : value of f at x_output
        grad_output : value of gradient at x_output, a column vector(numpy array)
    -----------------------------------------------------------------------------------------------------------------------------
    """

    # Start your code here
    d1 = 1
    d2 = 0.5
    n = 0.2
    R = d2
    N = 15000
    e = 0.000001
    x = x_initial
    k = np.array([[0,0]]).T
    i = 0
    x_k = 0
    while i<=N :
        i += 1
        p = PDM(R,x)
        pho = (func(x) - func(x + p ))/(M(func,x,k) - M(func,x,p))
        if pho < 0.25:
            R = 0.25*np.sqrt(p.T@p)
        else:
            if pho >0.75 and np.sqrt(p.T@p) == R :
                R = min(2*R , d1)
            else:
                R = R
        x_k = x
        if pho > n:
            x = x + p
        else:
            x =x
        if np.sqrt(gradient(func,x).T@gradient(func,x)) < e:
            break

    x_output = x_k
    f_output = func(x_output)
    grad_output = gradient(func , x_output)


    # End your code here

    return x_output, f_output, grad_output


"""--------------- Main code: Below code is used to test the correctness of your code ---------------

    func : function to evaluate the function value. 
    x_initial: initial value of x, a column vector, numpy array

"""

x_initial = np.array([[1.5, 1.5]]).T

x_output, f_output, grad_output = TRPD(func, x_initial)

print("\n\nTrust Region - Powell Dogleg Method:")
print("-" * 40)
print("\nFunction converged at x = \n", x_output)
print("\nFunction value at converged point = \n", f_output)
print("\nGradient value at converged point = \n", grad_output)