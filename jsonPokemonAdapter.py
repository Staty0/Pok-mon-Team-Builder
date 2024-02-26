from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from smogonApiAccess import ApiAccess
from pokeApiAccess import PokeApiAccess
from pokemon import Pokemon
from move import Move
from pokemonJudgment import Judgement
from moveRoleAssign import MoveRoleFind 

api = ApiAccess()
pokeapi = PokeApiAccess()

class JSONAdapter:
    def __init__(self):
        self.checked_moves = Queue()

    def process_pokemon_data(self, pokemon_data, gen, gui=None):
        try:
            if pokemon_data.get("oob").get("dex_number") < 0:
                return None

            name = pokemon_data.get("name")
            types = pokemon_data.get("types")
            abilities = pokemon_data.get("abilities")
            formats = pokemon_data.get("formats")
            hp = pokemon_data.get("hp")
            attack = pokemon_data.get("atk")
            defense = pokemon_data.get("def")
            special_attack = pokemon_data.get("spa")
            special_defense = pokemon_data.get("spd")
            speed = pokemon_data.get("spe")

            pokemon = Pokemon(
                name=name,
                types=types,
                abilities=abilities,
                formats=formats,
                hp=hp,
                attack=attack,
                defense=defense,
                speed=speed,
                special_attack=special_attack,
                special_defense=special_defense
            )

            pokeAPIgap = api.get_pokemon_data(gen, name.lower())
            if gui is not None:
                gui.update_output_text(f"Finished processing stats for {pokemon.name}")
            moves = pokeAPIgap.get('learnset')

            for move_data in moves:
                for checked_move in list(self.checked_moves.queue):
                    if move_data.lower().replace(" ", "-") == checked_move.name:
                        pokemon.add_move(checked_move)
                        break

                moveAPI = pokeapi.get_pokemon_move(move_data.lower().replace(" ", "-"))
                name = move_data.lower().replace(" ", "-").replace("'", "")
                PP = moveAPI.get("pp")
                split = moveAPI.get("damage_class").get("name")
                power = moveAPI.get("power")
                type = moveAPI.get("type").get("name")
                accuracy = moveAPI.get("accuracy")
                priority = moveAPI.get("priority")
                try:
                    effectDesc = moveAPI.get("effect_entries")[0].get("effect")
                except IndexError:
                    effectDesc = "Empty"

                move = Move(
                    name=name,
                    PP=PP,
                    split=split,
                    power=power,
                    type=type,
                    accuracy=accuracy,
                    effectDesc=effectDesc,
                    priority=priority
                )

                MoveRoleFind(move)
                pokemon.add_move(move)
                self.checked_moves.put(move)
            
            if gui is not None:
                gui.update_output_text(f"Finished processing moves for {pokemon.name}")

            pokeJudgment = Judgement()
            pokeJudgment.assign_roles(pokemon)
            return pokemon
        except Exception as e:
            print(f"Error processing Pokemon data: {e}")
            return None        

    def gen_to_class(self, gen_id, gui):
        gui.update_output_text('Starting API retrieval')
        pokemon_data = api.get_pokemon_by_gen(gen_id)
    

        if pokemon_data:
            # Create Pokemon instances for each Pokemon in the generation
            pokemon_list = []

            # Define a partial function to pass only the relevant argument to process_pokemon_data
            partial_process_pokemon_data = lambda x: self.process_pokemon_data(x, gen_id, gui)

            # Mutiple threads to speed up pulling from API
            with ThreadPoolExecutor(max_workers=25) as executor:
                pokemon_list = list(executor.map(partial_process_pokemon_data, pokemon_data))

            return pokemon_list
        
        else:
            print(f"Failed to get Pokemon data for generation {gen_id}")
            return None

    def get_Single_Pokemon(self, gen_id, pokemon_name):
        pokemon_data = api.get_pokemon_by_gen(gen_id)

        for pokemons in pokemon_data:
            print(pokemons.get("name"))
            if pokemons.get("name") == pokemon_name:
                pokemon = self.process_pokemon_data(pokemons, gen_id)
                return pokemon

        else:
            print(f"No Pokemon found for {gen_id} , {pokemon_name}")
            return None