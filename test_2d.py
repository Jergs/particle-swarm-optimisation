# Import modules
# Import PySwarms
import pyswarms as ps
from IPython.display import Image
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import plot_contour
from pyswarms.utils.plotters.formatters import Mesher

options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
optimizer = ps.single.GlobalBestPSO(n_particles=50, dimensions=2, options=options)
cost, pos = optimizer.optimize(fx.sphere, iters=100)

# Initialize mesher with sphere function
m = Mesher(func=fx.sphere)

# Make animation
animation = plot_contour(pos_history=optimizer.pos_history,
                         mesher=m,
                         mark=(0, 0))

# Enables us to view it in a Jupyter notebook
animation.save('plot0.gif', writer='imagemagick', fps=10)
Image(url='plot0.gif')
