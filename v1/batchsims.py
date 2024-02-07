import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_simulation(time_steps, initial_conditions, growth_rates, carrying_capacities):
    """
    Runs a single simulation with specified parameters.
    
    Parameters:
    - time_steps: Number of steps in the simulation.
    - initial_conditions: Dictionary with initial populations and environmental conditions.
    - growth_rates: Dictionary with growth rates for each population.
    - carrying_capacities: Dictionary with carrying capacity adjustments.
    
    Returns:
    - A DataFrame with the simulation results.
    """
    # Initialize data array
    data = np.zeros((time_steps, len(initial_conditions)))
    data[0, :] = [initial_conditions[key] for key in sorted(initial_conditions.keys())]
    
    columns = sorted(initial_conditions.keys())
    
    for t in range(1, time_steps):
        for i, key in enumerate(columns):
            if "growth_rate" in key or "capacity" in key:
                continue  # Skip non-population parameters
            growth_rate_key = f"{key}_growth_rate"
            growth_rate = growth_rates.get(growth_rate_key, 0)
            capacity_key = f"{key}_capacity"
            carrying_capacity = carrying_capacities.get(capacity_key, np.inf)
            pop = data[t-1, i]
            pop_growth = pop + growth_rate * pop * (1 - pop / carrying_capacity)
            data[t, i] = max(pop_growth, 0)  # Ensure population doesn't go negative
    
    return pd.DataFrame(data, columns=columns)


def run_simulation_with_gas_exchange(time_steps, initial_conditions, growth_rates):
    """
    Runs a simulation with specified parameters, including dynamic CO2 and O2 levels
    based on species' breathing and production.
    
    Parameters:
    - time_steps: Number of steps in the simulation.
    - initial_conditions: Dictionary with initial populations and environmental conditions.
    - growth_rates: Dictionary with growth rates for each population.
    - simulation_id: Identifier for the simulation run.
    
    Returns:
    - A DataFrame with the simulation results.
    """
    # Initialize the simulation array
    data = np.zeros((time_steps, len(initial_conditions)))
    data[0, :] = [initial_conditions[key] for key in sorted(initial_conditions.keys())]
    #initial_values = [initial_conditions[key] for key in sorted(initial_conditions.keys())]
    #data[0, :-1] = initial_values  # Exclude the last column (simulation_id)
    


    columns = sorted(initial_conditions.keys())
    
    for t in range(1, time_steps):
        co2, o2 = data[t-1, columns.index('CO2')], data[t-1, columns.index('O2')]
        
        for i, key in enumerate(columns):
            if key in ['CO2', 'O2']:  # Skip direct updates to CO2 and O2
                continue
            
            growth_rate = growth_rates.get(f"{key}_growth_rate", 0)
            pop = data[t-1, i]
            carrying_capacity = initial_conditions.get(f"{key}_capacity", np.inf)
            
            # Apply logistic growth formula
            pop_growth = pop + growth_rate * pop * (1 - pop / carrying_capacity)
            data[t, i] = max(pop_growth, 0)  # Ensure population doesn't go negative
        
        # Update CO2 and O2 based on species interactions
        # Assuming Slime Goop consumes CO2 and produces O2, Mushrooms and Cave Beetles do the opposite
        co2 += -0.1 * data[t, columns.index('slime_goop')] + 0.05 * (data[t, columns.index('mushrooms')] + data[t, columns.index('cave_beetles')])
        o2 += 0.1 * data[t, columns.index('slime_goop')] - 0.05 * (data[t, columns.index('mushrooms')] + data[t, columns.index('cave_beetles')])
        
        data[t, columns.index('CO2')] = max(co2, 0)
        data[t, columns.index('O2')] = max(o2, 0)
    
    return pd.DataFrame(data, columns=columns)



# Define ranges for initial populations and growth rates
initial_populations_range = range(1, 11)
growth_rates_range = np.arange(1.0, 2.6, 0.2)

# Define a fixed carrying capacity for simplicity
carrying_capacity_base = 100

# Placeholder for simulation results
simulation_results = []

simulation_id = 1

# Iterate over all combinations of initial conditions and growth rates
for slime_goop_initial in initial_populations_range:
    for mushrooms_initial in initial_populations_range:
        for cave_beetles_initial in initial_populations_range:
            for growth_rate in growth_rates_range:
                # Define initial conditions and growth rates for this simulation
                initial_conditions = {
                    'slime_goop': slime_goop_initial,
                    'mushrooms': mushrooms_initial,
                    'cave_beetles': cave_beetles_initial,
                    'CO2': 100,
                    'O2': 100,
                    'simulation_id': simulation_id
                }
                growth_rates = {
                    'slime_goop_growth_rate': growth_rate,
                    'mushrooms_growth_rate': growth_rate,
                    'cave_beetles_growth_rate': growth_rate
                }
                carrying_capacities = {
                    'slime_goop_capacity': carrying_capacity_base,
                    'mushrooms_capacity': carrying_capacity_base,
                    'cave_beetles_capacity': carrying_capacity_base
                }
                
                # Run the simulation
                df_result = run_simulation_with_gas_exchange(
                    100,
                    initial_conditions,
                    growth_rates
                )

                simulation_id += 1
                
                # Record the results
                final_population = df_result.iloc[-1].to_dict()
                final_population.update({
                    'slime_goop_initial': slime_goop_initial,
                    'mushrooms_initial': mushrooms_initial,
                    'cave_beetles_initial': cave_beetles_initial,
                    'growth_rate': growth_rate
                })
                simulation_results.append(final_population)

# Convert results to DataFrame for analysis
df_simulation_results = pd.DataFrame(simulation_results)

# Specify the filename
filename = 'batch_simulation_data.csv'

# Save the DataFrame to a CSV file
df_simulation_results.to_csv(filename, index=False)

print(f"Simulation data has been saved to '{filename}'.")




import matplotlib.pyplot as plt
import seaborn as sns

# Example scatter plot for slime goop final population vs initial population
plt.figure(figsize=(10, 6))
sns.scatterplot(x='slime_goop_initial', y='slime_goop', hue='growth_rate', data=df_simulation_results, palette='viridis')
plt.title('Final Slime Goop Population vs Initial Population')
plt.xlabel('Initial Slime Goop Population')
plt.ylabel('Final Slime Goop Population')
plt.legend(title='Growth Rate', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

