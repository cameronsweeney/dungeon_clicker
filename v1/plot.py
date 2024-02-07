import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load your DataFrame here, assuming it's already loaded as df
df = pd.read_csv('batch_simulation_data.csv')

# Assuming 'simulation_id' is a column used to distinguish between different simulations
simulation_ids = df['simulation_id'].unique()

# Select 3 random simulations to visualize
selected_ids = np.random.choice(simulation_ids, size=3, replace=False)

plt.figure(figsize=(14, 8))

for i, sim_id in enumerate(selected_ids, start=1):
    sim_data = df[df['simulation_id'] == sim_id]
    
    # Ensuring we're plotting using DataFrame index correctly
    plt.subplot(3, 1, i)
    plt.plot(sim_data.index.to_numpy(), sim_data['CO2'].to_numpy(), label='CO2', color='gray')
    plt.plot(sim_data.index.to_numpy(), sim_data['O2'].to_numpy(), label='O2', color='blue')
    plt.plot(sim_data.index.to_numpy(), sim_data['slime_goop'].to_numpy(), label='Slime Goop', color='green')
    plt.plot(sim_data.index.to_numpy(), sim_data['mushrooms'].to_numpy(), label='Mushrooms', color='red')
    plt.plot(sim_data.index.to_numpy(), sim_data['cave_beetles'].to_numpy(), label='Cave Beetles', color='brown')
    
    plt.title(f'Simulation {sim_id}: Population and Environment Dynamics')
    plt.xlabel('Time Steps')
    plt.ylabel('Population / Gas Concentration')
    plt.legend()

plt.tight_layout()
plt.show()
