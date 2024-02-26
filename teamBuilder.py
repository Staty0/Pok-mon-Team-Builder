from pokemon import Pokemon
from jsonPokemonAdapter import JSONAdapter

import random
import os
import math
import pickle


class PokemonTeamBuilder:
    strategy_arrays = {
        'Offensive': ['Physical_Attacker', 'Physical_Attacker', 'Special_Attacker', 'Special_Attacker', 'Mixed_Attacker', 'Physical_Brawler', 'Special_Brawler', 'Support', 'Mixed_Tank'],
        'Defensive': ['Mixed_Tank', 'Mixed_Tank', 'Mixed_Tank', 'Special_Tank', 'Physical_Tank', 'Special_Brawler', 'Physical_Brawler', 'Support', 'Mixed_Attacker'],
        'Balanced': ['Physical_Attacker', 'Special_Attacker', 'Mixed_Attacker', 'Special_Brawler', 'Physical_Brawler', 'Support', 'Mixed_Tank', 'Special_Tank', 'Physical_Tank',],
        'Overly Defensive': ['Mixed_Tank', 'Mixed_Tank', 'Mixed_Tank', 'Mixed_Tank', 'Special_Tank', 'Special_Tank', 'Physical_Tank', 'Physical_Tank'],
        'Overly Offensive': ['Physical_Attacker', 'Physical_Attacker', 'Physical_Attacker', 'Special_Attacker', 'Special_Attacker', 'Special_Attacker', 'Mixed_Attacker', 'Mixed_Attacker'],
    }
   
    generation_translations = {
        'Generation 1': 'rb', 
        'Generation 2': 'gs', 
        'Generation 3': 'rs', 
        'Generation 4': 'dp', 
        'Generation 5': 'bw', 
        'Generation 6': 'xy', 
        'Generation 7': 'sm', 
        'Generation 8': 'ss', 
        'Generation 9': 'sv'
    }

    off_role_arrays = {
        'Full Random': [[0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3]],
        'Best Only': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]],
        'Worst in Logic': [[2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3]],
        'Off Selections Allowed': [[0, 2], [0, 2], [0, 2], [0, 2], [0, 2], [0, 2]],
        'All Off Role': [[1, 3], [1, 3], [1, 3], [1, 3], [1, 3], [1, 3]],
        'Some Off Role Allowed': [[0, 1], [0, 1], [0, 1], [0, 2], [0, 2], [0, 3]],
        'Some Off Role Forced': [[0, 1], [0, 1], [0, 2], [0, 2], [1, 2], [1, 3]],
        'All Off Role Lite': [[1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2]],
        'Funny': [[0, 1], [2, 3], [1, 2], [0, 3], [1, 3], [0, 2]],
    }


    def fetch_pokemon_info(self, generation, gui):

        # Check if the file exists
        if os.path.exists(generation):
            # File exists, load the data
            with open(generation, 'rb') as file:
                pokemons = pickle.load(file)
            gui.update_output_text("Data loaded from existing file.")
        else:
            # File not found, show a popup warning
            warning_message = (
            "No Pokémon data for this generation was found.\n"
            "Would you like to create a new one?\n"
            "Warning: Creating a new file will take some time."
            )
            user_wants_to_continue = gui.show_popup_warning(warning_message)

            if not user_wants_to_continue:
                gui.update_output_text("Operation canceled by user.")
                return None

            pokemon_manager = JSONAdapter()
            gen_code = self.generation_translations.get(generation)
            pokemons = pokemon_manager.gen_to_class(gen_code, gui)

            with open(generation, 'wb') as file:
                pickle.dump(pokemons, file)
        
        return pokemons

    def build_team(self, set_pokemon_names, generation, smogon_format, strategy, monotype, variance, role_filter, off_role, gui):
        pokemons = self.fetch_pokemon_info(generation, gui)

        if pokemons is None:
            return None

        roles_needed = []
        required_pokemon = []
        team = []
        
        if smogon_format != '':
             # Filter all pokemon to only ones with the format filtered
            filtered_pokemons = []
            for pokemon in pokemons:
                if pokemon.formats == smogon_format:
                    filtered_pokemons.append(pokemon)
            pokemons = filtered_pokemons

        if monotype != '':
            # Filter all pokemon to only ones with the type filter
            filtered_pokemons = []
            for pokemon in pokemons:
                for type in pokemon.types:
                    if type == monotype:
                        filtered_pokemons.append(pokemon)
            pokemons = filtered_pokemons

        for role in role_filter:
            # Add requested roles
            if role != '':
                roles_needed.append(role)
            
        
        # Get a weighted role list and off role allowance 
        strategy_array = self.strategy_arrays.get(strategy)[:]
        off_role_array = self.off_role_arrays.get(off_role)[:]

        # Calculate the number of additional roles needed
        additional_roles_needed = max(0, 6 - len(strategy_array))

        # Draw additional random strings to fill out to 6
        additional_roles = random.sample(strategy_array, min(additional_roles_needed, len(strategy_array)))

        # Extend the selected_strings list with the additional strings
        roles_needed.extend(additional_roles)

        for name in set_pokemon_names:
            if name != '':
                required_pokemon.append(name)

        percent = int(len(pokemons) * (variance / 100)) + 12

        def sort_key(pokemon):
            return sum(score for _, score in pokemon.roles)

        # Sort the Pokemon objects based on the sum of scores
        sorted_pokemons = sorted(pokemons, key=sort_key, reverse=True)
        
        # Get the top percent pokemon
        top_pokemon = sorted_pokemons[:percent]

        selected_names = []  # List to keep track of selected Pokémon names

        for pokemon in pokemons:
            for r_pokemon in required_pokemon:
                if r_pokemon == pokemon.name:
                    for role, score in pokemon.roles():
                        if role in roles_needed:
                            strategy_array.remove(role)
                            team.append([pokemon.name, role])
                            selected_names.append(pokemon.name)
                        else:
                            team.append([pokemon.name, pokemon.roles[0]])
                            selected_names.append(pokemon.name)
                else:
                    gui.update_output_text(f"Could not find {r_pokemon}")       

        for pokemon in top_pokemon:
            pokemon.roles.sort(key=lambda x: x[1], reverse=True)

        loopcheckmax = 6
        while len(team) < 6 and top_pokemon:
            pokemon = random.choice(top_pokemon)
            loopcheck = 0
            pokemon_selected = False

            while loopcheck < loopcheckmax:
                min_value, max_value = off_role_array[loopcheck]
                role_subset = [role[0] for role in pokemon.roles[min_value:max_value]]
                for role in role_subset:
                    if pokemon.name not in selected_names and role in strategy_array:
                        selected_names.append(pokemon.name)  # Add the selected name to the list
                        strategy_array.remove(role)
                        off_role_array.pop(loopcheck)
                        loopcheckmax -= 1
                        team.append([pokemon.name, role])
                        pokemon_selected = True
                        break
                
                if pokemon_selected:
                    break

                loopcheck += 1
            top_pokemon.remove(pokemon)

        if len(team) == 6:
            gui.set_pokemon(team)
        else:
            gui.update_output_text('Error: Not enough Pokémon found matching filters to build a team, try lowering strength')

