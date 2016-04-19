import matplotlib.pyplot as plt



def plot_grid(draw, initialize=lambda f,a,p: None, dims=(1,1), include=[]):
 
    f, axes = plt.subplots(dims[0], dims[1],figsize=(20,20))
    initialize(f, axes, plt)
    for i in xrange(dims[0]):
        for j in xrange(dims[1]):
            if  not (i,j) in include: 
                axes[i][j].axis('off')
            else:
                draw((i,j), axes, f, plt)   

    return f, axes
