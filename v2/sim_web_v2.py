import numpy as np
import pandas as pd
import json

def load_and_simulate_food_web(file_path):
    # Load the ecosystem configuration from a JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract simulation parameters and initial conditions
    time_steps = data['simulation_parameters']['time_steps']
    initial_resource_levels = data['initial_resource_levels']
    species_info = data['species']
    
    # Initialize populations and resource levels
    populations = {species['name']: species['initial_population'] for species in species_info}
    resource_levels = initial_resource_levels.copy()
    
    # Prepare results storage
    results = np.zeros((time_steps, len(species_info) + len(resource_levels)))
    
    for t in range(time_steps):
        # Update resource levels based on current populations
        for resource, level in resource_levels.items():
            resource_levels[resource] += sum(species['produces'].count(resource) * populations[species['name']] for species in species_info) - \
                                         sum(species['consumes'].count(resource) * populations[species['name']] for species in species_info)
        
        # Update populations based on logistic growth formula
        for i, species in enumerate(species_info):
            N = populations[species['name']]
            r = species['growth_rate']
            
            # Determine carrying capacity (K) based on resource and prey availability
            K_resource = min(resource_levels[resource] for resource in species['consumes'] if resource in resource_levels) if species['consumes'] else np.inf
            K_prey = min(populations[prey] for prey in species['prey']) if species['prey'] else np.inf
            K = min(K_resource, K_prey, np.inf)
            
            # Logistic growth formula
            populations[species['name']] = N + r * N * ((K - N) / K) if K != 0 else N
            
            # Store results
            results[t, i] = populations[species['name']]
        
        # Store resource levels in results
        results[t, len(species_info):] = list(resource_levels.values())
    
    
    # Convert the NumPy results array to a pandas DataFrame
    columns = [species['name'] for species in species_info] + list(initial_resource_levels.keys())
    df_results = pd.DataFrame(results, columns=columns)
    
    # Print the first and last 10 rows
    print("First 10 rows of results:")
    print(df_results.head(10))
    print("\nLast 10 rows of results:")
    print(df_results.tail(10))
    
    # Write the results to a CSV file
    output_file_path = 'web_simulation_results.csv'
    df_results.to_csv(output_file_path, index=False)
    print(f"\nResults written to {output_file_path}")


    # Convert results to a more readable format (e.g., DataFrame) if necessary
    return results

# Example usage
file_path = 'foodweb.json'
results = load_and_simulate_food_web(file_path)



import copy
import random

def tweak_species_info(species_info, growth_rate_delta=0.1, population_delta=10):
    """
    Creates a copy of the species info and tweaks growth rates and initial populations.
    
    Parameters:
    - species_info: List of dictionaries, each containing species data.
    - growth_rate_delta: Maximum change to apply to the growth rate.
    - population_delta: Maximum change to apply to the initial population.
    
    Returns:
    - A new list of species info with tweaked values.
    """
    tweaked_species_info = copy.deepcopy(species_info)  # Make a deep copy to avoid altering the original list
    
    for species in tweaked_species_info:
        # Apply a random adjustment within +/- the delta for the growth rate
        growth_rate_adjustment = random.uniform(-growth_rate_delta, growth_rate_delta)
        species['growth_rate'] = max(1, species['growth_rate'] + growth_rate_adjustment)  # Ensure growth rate stays at least 1
        
        # Apply a random adjustment within +/- the delta for the initial population
        population_adjustment = random.randint(-population_delta, population_delta)
        species['initial_population'] = max(1, species['initial_population'] + population_adjustment)  # Ensure population stays positive
    
    return tweaked_species_info

def evaluate_stability(species_populations):
    """
    Evaluates the stability of species populations.

    Parameters:
    - species_populations: DataFrame containing population data for each species over time.

    Returns:
    - Dictionary with species as keys and stability indicators (-1, 0, 1) as values.
      1 indicates increasing, -1 indicates decreasing, and 0 indicates stable.
    """
    stability = {}
    for species in species_populations.columns:
        # Calculate the average change in population over the last 10% of time steps
        changes = species_populations[species].diff().iloc[-int(len(species_populations) * 0.1):].mean()
        if changes > 0:
            stability[species] = 1  # Population is increasing
        elif changes < 0:
            stability[species] = -1  # Population is decreasing
        else:
            stability[species] = 0  # Population is stable
    return stability

import pandas as pd

def convert_results_to_df(results, species_info, initial_resource_levels):
    """
    Converts simulation results into a pandas DataFrame for easier analysis.

    Parameters:
    - results: The simulation results, assumed to be a NumPy array where each row represents a time step,
               and each column represents the population of a species or the level of a resource.
    - species_info: List of dictionaries with information about each species, including their names.
    - initial_resource_levels: Dictionary with the names and initial levels of resources (e.g., CO2, O2).

    Returns:
    - A pandas DataFrame with one column per species and resource, indexed by time step.
    """
    # Combine species names and resource names to form column labels
    column_labels = [species['name'] for species in species_info] + list(initial_resource_levels.keys())
    
    # Create the DataFrame
    df = pd.DataFrame(results, columns=column_labels)
    
    return df


def optimize_growth_rates(species_info, initial_resource_levels, iterations=100, learning_rate=0.01):
    """
    Optimizes species growth rates to achieve stable populations using gradient descent.

    Parameters:
    - species_info: List of species information dictionaries.
    - initial_resource_levels: Dictionary with initial levels of resources.
    - iterations: Number of iterations for the gradient descent process.
    - learning_rate: Learning rate for the gradient descent updates.

    Returns:
    - Optimized species_info with adjusted growth rates.
    """
    for iteration in range(iterations):
        # Run the simulation
        tweaked_species_info = tweak_species_info(species_info)
        results = load_and_simulate_food_web('foodweb.json', tweaked_species_info, initial_resource_levels)
        df_results = convert_results_to_df(results, species_info, initial_resource_levels)

        # Evaluate stability of the current populations
        stability = evaluate_stability(df_results)

        # Adjust growth rates based on stability
        for species in species_info:
            if stability[species['name']] == 1:  # If population is increasing, decrease growth rate
                species['growth_rate'] -= learning_rate
            elif stability[species['name']] == -1:  # If population is decreasing, increase growth rate
                species['growth_rate'] += learning_rate

            # Ensure growth rate stays within bounds
            species['growth_rate'] = max(1, min(species['growth_rate'], 2))  # Assuming max growth rate of 2 for example

    return species_info
