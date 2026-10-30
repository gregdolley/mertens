import numpy as np
import mpmath as mp
#import math

mp.mp.dps = 100

def lll(basis, n, delta = 3/4):
    # input a list of lists (representing vectors in a basis), outputs lll reduced basis
    gs_basis = gram_schmidt(basis)
    k = 1
    while k < n:
        print(k)
        for j in range(k-1,-1,-1):
            mu_kj = gram_coeffs(gs_basis[j],basis[k])
            if abs(mu_kj) > 1/2:
                basis[k] = basis[k] - mp.nint(mu_kj)*basis[j]
                gs_basis = gram_schmidt(basis)
        mu = gram_coeffs(gs_basis[k-1],basis[k])
        if (np.dot(gs_basis[k],gs_basis[k])) >= ((delta - mu**2) * np.dot(gs_basis[k-1], gs_basis[k-1])):
            k = k + 1
        else:
            temp1 = np.copy(basis[k])
            temp2 = np.copy(basis[k-1])
            basis[k] = temp2
            basis[k-1] = temp1
            gs_basis = gram_schmidt(basis)
            k = max(k-1, 1)
    return basis

def gram_schmidt(basis):
    # input a list of lists (representing vectors in a basis), outputs gram schmidt basis
    b0 = basis[0]
    gs_basis = np.array([b0])
    for vec_index in range(1,len(basis)):
        b = basis[vec_index]
        newb = np.copy(b)
        for i in range(0,vec_index):
            newb = newb - proj(gs_basis[i],b)
        gs_basis = np.vstack([gs_basis,newb])
    return gs_basis

def proj(u,v):
    # calculates proj_u(v) (v projects onto u)
    return (np.dot(u,v) / np.dot(u,u)) * u

def gram_coeffs(u,v):
    # calculate coefficients of gram schmidt
    return np.dot(u,v) / np.dot(u,u)
