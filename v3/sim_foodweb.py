import numpy as np
import pandas as pd
import json

def load_food_web_json(file_path):
    # Load the ecosystem configuration from a JSON file
    with open(file_path, 'r') as file:
        food_web = json.load(file)
    return food_web

def load_simulation_from_food_web(food_web):
    species_data = food_web['species']
    initial_resource_levels = food_web['initial_resource_levels']
    simulation_parameters = food_web['simulation_parameters']
    return species_data, initial_resource_levels, simulation_parameters

def calculate_resource_consumption_and_production(population_levels, species_data, resource):
    total_consumption = 0
    total_production = 0
    # Iterate over each species in the food_web
    for species in species_data:
        # Get the current population of the species
        population = population_levels.get(species['name'], 0)

        # Check if the species consumes the specified resource
        if resource in species['consumes']:
            total_consumption += population * species['breathe_rate']
        if resource in species['produces']:
            total_production += population * species['breathe_rate']

    return total_production - total_consumption

def calculate_predation_effects(population_levels, species_data):
    # Initialize a dictionary to keep track of how much each species eats and is eaten
    consumption = {species['name']: 0 for species in species_data}
    
    # Iterate over each species to calculate consumption based on predation
    for predator in species_data:
        predator_name = predator['name']
        predator_population = population_levels[predator_name]
        num_prey = len(predator['prey'])
        
        # Only proceed if the predator has prey
        if num_prey > 0:
            # Calculate the amount of prey eaten per prey species by this predator
            prey_consumed_per_species = predator_population / num_prey
            
            for prey_name in predator['prey']:
                # Update the 'eaten' count for the prey
                consumption[prey_name] += prey_consumed_per_species
    
    return consumption

## function: apply logistic growth to population
def apply_logistic_growth(k, N, r):
    return "A VERY LARGE NUMBER, BUT NOT TOO LARGE"


## function: run 1 simulation on food web from initial parameters, return all data
def run_one_simulation(species_data, initial_resource_levels, simulation_parameters):
    # Initialize simulation parameters
    time_steps = simulation_parameters['time_steps']

    # Initialize populations and resource levels
    population_levels = {species['name']: species['initial_population'] for species in species_data}
    growth_rates = {species['name']: species['growth_rate'] for species in species_data}
    resource_levels = initial_resource_levels.copy()
    print(resource_levels)

    # Prepare results storage
    column_count = len(population_levels) + len(resource_levels)
    results = np.zeros((time_steps, column_count))
    
    for current_time_step in range(time_steps):
        ## everyone breathes: update gas / resource levels
        for resource_name in resource_levels.items():
            # calculate change in resource (+ produced, - consumed)
            resource_levels[resource_name] += calculate_resource_consumption_and_production(population_levels, species_data, resource_name)
        
        consumption = calculate_predation_effects(population_levels, species_data)
        
        ## everyone eats & reproduces: update population levels
        for species_name in species_data:
            population_levels[species_name] -= consumption[species_name]
            ## eat other species

            ## calculate carrying capacity
            ## recalculate growth rate

            ## reproduce

### utility function: judgment of outcomes based on initial simulation parameters
    #### check & score every step -> crash after 10 turns > crash after 5



############################################################
############################################################
############################################################

    ### BELOW = FROM CHATGPT, FIX THIS ####
def uncalled_function(time_steps, resource_levels, populations, species_info, results, initial_resource_levels):
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

    #### ABOVE = FROM CHATGPT, FIX THIS ####


############################################################
############################################################
############################################################

## TEST STATEMENTS WHEN I CALL THIS SCRIPT FROM COMMAND LINE

food_web = load_food_web_json('food_web.json')
species_data, initial_resource_levels, simulation_parameters = load_simulation_from_food_web(food_web)
run_one_simulation(species_data, initial_resource_levels, simulation_parameters)


############################################################
############################################################
############################################################





#
#
#
#To use these functions together to run many simulations and find good initial conditions that create stability in your ecosystem, you'll need to create a workflow that integrates the simulation execution, the tweaking of growth rates, and the evaluation of population stability. The goal is to iteratively adjust the growth rates based on the outcomes of each simulation until you find conditions that lead to stable populations. Here's a high-level approach to accomplish this:
#1. Load Initial Configuration
#
#First, load your ecosystem configuration from the foodweb.json file to get the initial species information and resource levels.
#
#python
#
#import json
#
#def load_ecosystem_configuration(file_path='foodweb.json'):
#    with open(file_path, 'r') as file:
#        data = json.load(file)
#    return data['species'], data['initial_resource_levels'], data['simulation_parameters']['time_steps']
#
#species_info, initial_resource_levels, time_steps = load_ecosystem_configuration()
#
#2. Define the Main Simulation Loop
#
#Create a main loop that runs simulations, evaluates stability, and adjusts growth rates. This loop will keep running simulations until you've found satisfactory stable conditions or reached a maximum number of iterations.
#
#python
#
#def run_simulations_and_optimize(species_info, initial_resource_levels, time_steps, max_iterations=1000):
#    stable_conditions_found = False
#    iteration = 0
#    
#    while not stable_conditions_found and iteration < max_iterations:
#        # Run the simulation with current species info
#        results = load_and_simulate_food_web('foodweb.json', species_info, initial_resource_levels, time_steps)
#        df_results = convert_results_to_df(results, species_info, initial_resource_levels)
#        
#        # Evaluate stability of the populations
#        stability = evaluate_stability(df_results)
#        print(f"Iteration {iteration}: Stability - {stability}")
#        
#        # Check if stability conditions are met
#        if all(value == 0 for value in stability.values()):
#            stable_conditions_found = True
#            print("Stable conditions found.")
#        else:
#            # Adjust growth rates slightly to aim for stability
#            species_info = tweak_species_info(species_info)  # Implement your logic to adjust growth rates based on stability
#        
#        iteration += 1
#    
#    return species_info if stable_conditions_found else None
#
#3. Adjust Growth Rates Based on Stability
#
#Incorporate logic to adjust growth rates based on the evaluation of stability. This could be a separate function or integrated into your main loop. The tweak_species_info function provided earlier randomizes this process, but for optimizing towards stability, you'd implement a more directed adjustment:
#
#    Increase growth rates slightly for species declining towards extinction.
#    Decrease growth rates for species growing uncontrollably.
#
#This targeted adjustment requires modifying tweak_species_info or creating a new function to specifically adjust growth rates based on stability feedback.
#4. Execute the Workflow
#
#Finally, call your main simulation loop with the loaded or defined initial conditions.
#
#python
#
#optimized_species_info = run_simulations_and_optimize(species_info, initial_resource_levels, time_steps)
#
#if optimized_species_info:
#    # Save or further analyze the optimized conditions
#    print("Optimized species info:", optimized_species_info)
#else:
#    print("Failed to find stable conditions within the given iterations.")
#
#Note:
#
#This approach assumes an iterative process of slight adjustments and reevaluation, aiming to converge on a set of growth rates that yield stable ecosystems. Realistically, achieving true stability in complex, dynamic systems may require sophisticated models and understanding of ecological interactions. The methods described here provide a starting point, but real-world applications may necessitate more detailed and nuanced approaches, potentially involving machine learning techniques for optimization.