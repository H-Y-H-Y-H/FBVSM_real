import numpy as np

def balance_steps(data):
    # Calculate the cumulative distances for the data
    diffs = np.diff(data, axis=0)
    distances = np.linalg.norm(diffs, axis=1)
    cumulative_distances = np.insert(np.cumsum(distances), 0, 0)

    # Create a linearly spaced set of values based on the start and end points of the cumulative distances
    balanced_cumulative_distances = np.linspace(0, cumulative_distances[-1], len(cumulative_distances))

    # Interpolate to get balanced steps
    balanced_data = np.zeros(data.shape)
    for i in range(data.shape[1]):
        balanced_data[:,i] = np.interp(balanced_cumulative_distances, cumulative_distances, data[:,i])
    
    return balanced_data

# Sample data
data = np.loadtxt('spiral_cmds.csv')
balanced_data = balance_steps(data)
print(balanced_data)
np.savetxt('spiral_cmds_balance.csv',balanced_data)
