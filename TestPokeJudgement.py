from pokemon import Pokemon
from jsonPokemonAdapter import JSONAdapter
from pokemonJudgment import Judgement

def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip().split() for line in lines]

def write_output(filename, output):
    with open(filename, 'a') as file:
        file.write(output)

pokemon_manager = JSONAdapter()
pokeJudgment = Judgement()

# Read input values from the file
input_values = read_input('input.txt')

for region, pokemon_name in input_values:
    pokemon = pokemon_manager.get_Single_Pokemon(region, pokemon_name)

    if pokemon:
        pokeJudgment.assign_roles(pokemon)

        # Print the pokemon.roles value to another file
        output_text = f"{pokemon.name} region: {region} roles: {pokemon.roles}\n"
        write_output('output.txt', output_text)
