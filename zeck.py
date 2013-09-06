#!/usr/bin/python

import matplotlib.pyplot as plt
import sys

#nth fibonacci number
#using fib0 == 1, fib1 == 2
def fibo(n):
    fib0 = 1
    fib1 = 2
    for _ in range(n):
        fib0, fib1 = fib1, fib0 + fib1
    return fib0

#get product of terms in ar
def prod(ar):
    p = 1
    for i in ar:
        p *= i
    return p

#n choose k
def choose(n, k):
    k = max(k, n - k)
    p = prod(range(k+1, n+1))
    return p / prod(range(1, n - k + 1))

#return x where fibo(x) <= n, maximise x
def fibindex(n):
    fib0 = 1
    fib1 = 2
    count = 0
    while True:
        if fib0 > n:
            return count - 1
        fib0, fib1 = fib1, fib0 + fib1
        count += 1

#modified project euler solution to problem 115
#think of zeckendorf representations as red tiles
def tiles2(length, additional, ar):
    n = length
    k = length
    tiles = additional
    while k >= 0:
        ar[tiles] += choose(n, k)
        n -= 1
        k -= 2
        tiles += 1
    return ar

#get rid of all trailing zeros except one
def trim(ar):
    while ar[-1] == 0:
        ar.pop(-1)
    return ar + [0]

#get the count of how many representations have n terms
def getar(maxx):
    index = fibindex(maxx)
    used = 0
    ar = (index/2 + 3)*[0]

    #index walks through the terms in the zeckendorf representation of maxx
    #the last used number of terms in zeckendorf representation of maxx have been used
    while index >= 0:
        ar = tiles2(index + 1, used, ar)
        maxx = maxx - fibo(index)
        index = fibindex(maxx)
        used += 1

    ar = trim(ar)
    #note: ar[0] == 1
    #I am considering the Zeckendorf representation of 0 contains 0 terms
    return ar

#get ar / sum(ar)
def getfreq(ar): 
    freq = []
    for i in range(len(ar)):
        freq += [float(ar[i])/sum(ar)]
    return freq

#plot the frequency of terms in given array
def plotfreq(ar):
    plt.plot(range(len(ar)), ar, color="black")

#plot the distribution where x < maxx
def singledist(maxx):
    plotfreq(getfreq(getar(maxx)))

#get all distributions from 10**1 to 10**(maxx - 1)
def multdist(maxx):
    for i in range(1, maxx):
        singledist(10**i + 1)

    plt.title(u"Zeckendorf Representation Distributions\n for 0 \u2264 x \u2264 10\u207f, where 1 \u2264 n \u2264 {}".format(maxx - 1))
    plt.xlabel("Number of Terms in Zeckendorf Representation of x")
    plt.ylabel("Frequency")
    plt.savefig("zeck.pdf")

try:
    maxx = int(sys.argv[1]) 
except:
    maxx = 100
multdist(maxx + 1)
