import numpy as np
import matplotlib.pyplot as plt
########################################################
def fixedpt(f,x0,tol,Nmax):

    ''' x0 = initial guess''' 
    ''' Nmax = max number of iterations'''
    ''' tol = stopping tolerance'''

    count = 0
    # make an array of zeros of length Nmax
    x = np.zeros((Nmax,1))
    # save the initial guess
    x[0] = x0
    while (count < Nmax):
       count = count +1
       x1 = f(x0)
       # save the current iterate
       x[count] = x1
       if (abs(x1-x0) <tol):
          xstar = x1
          ier = 0
          # truncate the array to have only count entries
          x = x[0:count]
          return [xstar,x,ier,count]
       x0 = x1

    xstar = x1
    x = x[0:count]
    ier = 1
    return [xstar,x,ier,count]

def compute_order(x,xstar):
# p_{n+1}-p (from the second index to the end)
  diff1 = np.abs(x[1::]-xstar)
  # p_n-p (from the first index to the second to last)
  diff2 = np.abs(x[0:-1]-xstar)
  # linear fit to log of differences
  fit = np.polyfit(np.log(diff2.flatten()),np.log(diff1.flatten()),1)
  print('the order equation is')
  print('log(|p_{n+1}-p|) = log(lambda) + alpha*log(|p_n-p|) where')
  print('lambda = ' + str(np.exp(fit[1])))
  print('alpha = ' + str(fit[0]))
  return [fit,diff1,diff2]

def aitkens(x,xstar,tol):
  count = len(x)
  hat_x = np.zeros((count-2,1))
  for n in range(0,count-2):
    # compute new iterates using aitkens formula
    hat_x[n] = x[n] - (x[n+1]-x[n])**2/(x[n+2]-2*x[n+1]+x[n])  
    # return if we're less than tol
    if np.abs(hat_x[n]-xstar) < tol:
      return hat_x[0:n+1]
  return hat_x  

########################################################

# define fixed point iteration functions
f1 = lambda x: x * (1 + (7 - x**5)/x**2)**3
f2 = lambda x: x - (x**5 - 7)/x**2
f3 = lambda x: x - (x**5 - 7)/(5*x**4)
f4 = lambda x: x - (x**5 - 7)/12
fcts = [f1,f2,f3,f4]

for fct in fcts:
  [xstar,x,ier,count] = fixedpt(fct,1,1e-10,3)
  # compute the convergence rate and constant
  [fit,diff1,diff2] = compute_order(x,xstar)