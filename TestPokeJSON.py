from pokemon import Pokemon
from jsonPokemonAdapter import JSONAdapter

pokemon_manager = JSONAdapter()
pokemons = pokemon_manager.gen_to_class("rb")

if pokemons:
    for pokemon in pokemons:
        moves = pokemon.movepool
        print(f"{pokemon.name}") 
        print("Type:", pokemon.types)
        print(f"Base Stats - HP: {pokemon.hp}, Attack: {pokemon.attack}, Defense: {pokemon.defense}")
        print(f"Speed: {pokemon.speed}, Special Attack: {pokemon.special_attack}, Special Defense: {pokemon.special_defense}")
        print("------")