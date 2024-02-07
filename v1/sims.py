import numpy as np
import pandas as pd

# Simulation parameters
time_steps = 200  # Number of time steps in the simulation
initial_co2 = 150
initial_o2 = 100
initial_slime_goop = 1
initial_mushroom_pop = 1
initial_cave_beetles = 1
initial_glow_worms = 1
initial_stone_trolls = 1
initial_crystal_spiders = 1
initial_fungal_golems = 1

# Growth and interaction rates
slime_goop_max_growth_rate = 1.3
mushroom_max_growth_rate = 1.2
cave_beetle_growth_factor = 0.9
glow_worm_growth_factor = 1.1
stone_troll_impact = 0.05
crystal_spider_growth_factor = 1.05
fungal_golem_growth_factor = 0.95

# Base value for carrying capacities, to be adjusted per species
carrying_capacity_base = 100

# Initialize the simulation array
data = np.zeros((time_steps, 10))
data[0, :] = [initial_co2, initial_o2, initial_slime_goop, initial_mushroom_pop, initial_cave_beetles,
              initial_glow_worms, initial_stone_trolls, initial_crystal_spiders, initial_fungal_golems, 0]  # Last column for recording purposes

# Define the columns for the DataFrame
columns = ['CO2', 'O2', 'Slime Goop', 'Mushrooms', 'Cave Beetles', 'Glow Worms', 'Stone Trolls', 'Crystal Spiders', 'Fungal Golems', 'Recording Purpose']



# Ensure carrying capacities never drop to zero by setting a minimum threshold
min_carrying_capacity = 1  # Minimum threshold to prevent division by zero

for t in range(1, time_steps):
    co2, o2, slime_goop, mushrooms, cave_beetles, glow_worms, stone_trolls, crystal_spiders, fungal_golems, _ = data[t-1, :]
    
    # Adjust carrying capacities to ensure they never drop below the minimum threshold
    slime_goop_cc = max(carrying_capacity_base + co2, min_carrying_capacity)
    mushrooms_cc = max(carrying_capacity_base + o2, min_carrying_capacity)
    cave_beetles_cc = max(min(slime_goop, mushrooms), min_carrying_capacity)
    glow_worms_cc = max(o2, min_carrying_capacity)
    crystal_spiders_cc = max(carrying_capacity_base, min_carrying_capacity)  # Assuming a constant base for simplicity
    fungal_golems_cc = max(min(slime_goop, mushrooms), min_carrying_capacity)

    # Calculate stone_trolls_co2_absorption properly, ensuring it doesn't cause CO2 to go negative
    stone_trolls_co2_absorption = stone_trolls * stone_troll_impact * max(co2, 0)

    # Logistic growth calculations adjusted to safeguard against carrying capacity issues
    slime_goop_growth = slime_goop + (slime_goop_max_growth_rate * slime_goop * (1 - slime_goop / slime_goop_cc))
    mushrooms_growth = mushrooms + (mushroom_max_growth_rate * mushrooms * (1 - mushrooms / mushrooms_cc))
    cave_beetles_growth = cave_beetles + (cave_beetle_growth_factor * cave_beetles * (1 - cave_beetles / cave_beetles_cc))
    glow_worms_growth = glow_worms + (glow_worm_growth_factor * glow_worms * (1 - glow_worms / glow_worms_cc))
    crystal_spiders_growth = crystal_spiders + (crystal_spider_growth_factor * crystal_spiders * (1 - crystal_spiders / crystal_spiders_cc))
    fungal_golems_growth = fungal_golems + (fungal_golem_growth_factor * fungal_golems * (1 - fungal_golems / fungal_golems_cc))
    
    # Update populations ensuring no species drops below 0
    slime_goop = max(slime_goop_growth, 0)
    mushrooms = max(mushrooms_growth, 0)
    cave_beetles = max(cave_beetles_growth, 0)
    glow_worms = max(glow_worms_growth, 0)
    crystal_spiders = max(crystal_spiders_growth, 0)
    fungal_golems = max(fungal_golems_growth, 0)
    
    # Update CO2 and O2 based on life processes, ensuring no negative values
    co2 = max(co2 - stone_trolls_co2_absorption + cave_beetles_growth + fungal_golems_growth, 0)
    o2 = max(o2 + glow_worms_growth - fungal_golems_growth, 0)
    
    # Save the new state
    data[t, :] = [co2, o2, slime_goop, mushrooms, cave_beetles, glow_worms, stone_trolls, crystal_spiders, fungal_golems, 0]  # Adjust as needed for recording purposes

# Convert the data array into a DataFrame for analysis
df_simulation_corrected = pd.DataFrame(data, columns=columns)

df_simulation_corrected.head()


# Specify the filename
filename = 'simulation_data.csv'

# Save the DataFrame to a CSV file
df_simulation_corrected.to_csv(filename, index=False)

print(f"Simulation data has been saved to '{filename}'.")

