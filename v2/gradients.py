import json

##### 







def load_ecosystem_configuration(file_path='foodweb.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['species'], data['initial_resource_levels'], data['simulation_parameters']['time_steps']

species_info, initial_resource_levels, time_steps = load_ecosystem_configuration()

def run_simulations_and_optimize(species_info, initial_resource_levels, time_steps, max_iterations=1000):
    stable_conditions_found = False
    iteration = 0
    
    while not stable_conditions_found and iteration < max_iterations:
        # Run the simulation with current species info
        results = load_and_simulate_food_web('foodweb.json', species_info, initial_resource_levels, time_steps)
        df_results = convert_results_to_df(results, species_info, initial_resource_levels)
        
        # Evaluate stability of the populations
        stability = evaluate_stability(df_results)
        print(f"Iteration {iteration}: Stability - {stability}")
        
        # Check if stability conditions are met
        if all(value == 0 for value in stability.values()):
            stable_conditions_found = True
            print("Stable conditions found.")
        else:
            # Adjust growth rates slightly to aim for stability
            species_info = tweak_species_info(species_info)  # Implement your logic to adjust growth rates based on stability
        
        iteration += 1
    
    return species_info if stable_conditions_found else None

#####

def adjust_growth_rates_for_stability(species_info, stability, learning_rate=0.01):
    """
    Adjusts species growth rates based on their stability to aim for stable populations.

    Parameters:
    - species_info: List of species information dictionaries.
    - stability: Dictionary with species names as keys and stability indicators as values.
    - learning_rate: How much to adjust the growth rates by.

    Returns:
    - Modified species_info with adjusted growth rates.
    """
    for species in species_info:
        name = species['name']
        if name in stability:
            # If the species is declining, try to increase its growth rate
            if stability[name] == -1:
                species['growth_rate'] += learning_rate
            # If the species is growing too rapidly, try to decrease its growth rate
            elif stability[name] == 1:
                species['growth_rate'] -= learning_rate
            
            # Ensure the growth rate remains within reasonable bounds
            species['growth_rate'] = max(1, species['growth_rate'])
    
    return species_info





def run_simulations_and_optimize(species_info, initial_resource_levels, time_steps, max_iterations=1000):
    for iteration in range(max_iterations):
        # Run the simulation with the current species info
        results = load_and_simulate_food_web('foodweb.json', species_info, initial_resource_levels, time_steps)
        df_results = convert_results_to_df(results, species_info, initial_resource_levels)
        
        # Evaluate the stability of populations
        stability = evaluate_stability(df_results)
        
        # Adjust growth rates based on the stability feedback
        species_info = adjust_growth_rates_for_stability(species_info, stability, learning_rate=0.01)
        
        # Optional: Add a condition to break the loop if a certain stability criterion is met
        # This could be based on the variance of population sizes, a specific stability score, etc.

    # After finishing the iterations, or finding an optimal configuration, return the modified species info
    return species_info

# Execute the optimization loop
optimized_species_info = run_simulations_and_optimize(species_info, initial_resource_levels, time_steps)




#####


optimized_species_info = run_simulations_and_optimize(species_info, initial_resource_levels, time_steps)

if optimized_species_info:
    # Save or further analyze the optimized conditions
    print("Optimized species info:", optimized_species_info)
else:
    print("Failed to find stable conditions within the given iterations.")
