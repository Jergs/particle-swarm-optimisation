import numpy as np
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
import matplotlib.pyplot as plt
from pyswarms.utils.plotters.formatters import Designer
from pyswarms.utils.plotters.formatters import Mesher
from pyswarms.utils.plotters import plot_contour, plot_surface

# Set-up all the hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
# Call an instance of PSO
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=2, options=options)
# Perform the optimization
cost, pos = optimizer.optimize(fx.sphere, iters=1000)

m = Mesher(func=fx.sphere)
pos_history_3d = m.compute_history_3d(optimizer.pos_history)
d = Designer(limits=[(-1,1), (-1,1), (-0.1,1)], label=['x-axis', 'y-axis', 'z-axis'])
animation3d = plot_surface(pos_history=pos_history_3d, # The cost_history that we computed
                           mesher=m, designer=d,
                           mark=(0,0,0))               # Mark the minimum value for function.

plt.show()