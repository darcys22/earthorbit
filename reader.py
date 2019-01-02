import numpy as np
import glob

# numpy_vars = {}
numpy_vars = []
for np_name in glob.glob('./games/*.np[yz]'):
        numpy_vars.append(np.load(np_name))

print(numpy_vars[0][0])
