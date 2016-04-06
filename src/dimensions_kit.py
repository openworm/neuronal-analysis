"""
This is a small toolkit for mapping 
one dimensional positive integers over a
closed interval onto a two dimensional
space. 

So you can run a loop in one dimensions 
and plot sequential points in two dimensions. 

The universal solution for determining dimensionality
is sqrt[n](x), i.e. the nth root of x, and actually transforming
a point is the exact same procedure folded over n dimensions

You can also start playing around with things by setting scaling
preferences, axes ordering, etc. but I like this ad hoc solution
because it solves my problem and I don't need to think about it anymore
"""

# Returns a 2-tuple 
def dimensions(n):
    # Minimizes the dimensions of a grid (xy) to plot n elements
    import math
    s = math.sqrt(float(n))
    x = int(math.ceil(s))
    y = int(math.floor(s))
    return (x,y)

def transform(dims, n):
    x,y = dims
    a = n/y
    b = n%(y)
    return (a,b)
