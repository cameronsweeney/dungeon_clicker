import numpy as np

def simulate_food_web(time_steps, species_info, initial_gas_levels):
    # Initialize populations and gas levels
    populations = {species['name']: species['initial_population'] for species in species_info}
    gas_levels = initial_gas_levels.copy()
    
    # Prepare results storage
    results = np.zeros((time_steps, len(species_info) + len(gas_levels)))
    
    for t in range(time_steps):
        # Update gas levels based on current populations
        for gas, level in gas_levels.items():
            gas_levels[gas] += sum(species['produces'].count(gas) * populations[species['name']] for species in species_info) - \
                               sum(species['consumes'].count(gas) * populations[species['name']] for species in species_info)
        
        # Update populations based on logistic growth formula
        for i, species in enumerate(species_info):
            N = populations[species['name']]
            r = species['growth_rate']
            
            # Determine carrying capacity (K) based on gas and prey availability
            K_gas = min(gas_levels[gas] for gas in species['consumes'] if gas in gas_levels) if species['consumes'] else np.inf
            K_prey = min(populations[prey] for prey in species['prey']) if species['prey'] else np.inf
            K = min(K_gas, K_prey, species.get('carrying_capacity', np.inf))
            
            # Logistic growth formula
            populations[species['name']] = N + r * N * ((K - N) / K)
            
            # Store results
            results[t, i] = populations[species['name']]
        
        # Store gas levels in results
        results[t, len(species_info):] = list(gas_levels.values())
    
    # Convert results to a more readable format (e.g., DataFrame) if necessary
    return results

# Example usage
species_info = [
    {"name": "Algae", "consumes": ["CO2"], "produces": ["O2"], "prey": [], "predators": [], "initial_population": 10, "growth_rate": 1.5},
    # Add other species details here...
]
initial_gas_levels = {"CO2": 1000, "O2": 1000}

# Run the simulation
results = simulate_food_web(100, species_info, initial_gas_levels)
