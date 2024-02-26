from pokemon import Pokemon
from move import Move
from typeGraph import TypeChart
import math

# Initialize an array
Support_Move_Roles = ['Barrier', 'Baton_Pass', 'Heal', 'Fixed_Damage', 'Burn', 'Poison', 'Badly_Poison', 'Disables_Move', 'Protect', 'Hazard', 'Disables_item'
'Prevent_Status_Effects', 'Tailwind', 'Hazard_clear', 'Barrier_break', 'Disable_healing', 'Haze', 'Defog', 'Skill Swap', 'Heal_Status_all', 'Helping_Hand',
'Taunt', 'Force_target_self', 'Torment', 'Steal_held_item', 'Swap_Defenses']
Attacker_Move_Roles = ['Attack_up_two', 'Attack_up_one', 'Attack_up_chance', 'Free_Switch']
Special_Attacker_Move_Roles = ['Special_Attack_up_three', 'Special_Attack_up_two', 'Special_Attack_up_one', 'Special_Attack_up_chance', 'Hidden_Power']
Tank_Move_Roles = ['Fixed_Damage', 'Burn', 'Poison', 'Badly_Poison', 'Self_Heal', 'Substitution', 'Heal', 'Protect', 'Hazard', 'Special_Defense_up_two', 'Defense_up_two', 
'Heals_from_damage', 'Curse', 'Paralyze_chance', 'Paralyze', 'Confusion', 'Trick_room', 'Forced_Switch', 'Pain_Split', 'Badly_Poison_chance']
Speed_Helping_Moves = ['Speed_up_one', 'Free_Switch']

class Judgement:
    def assign_roles(self, pokemon):
        # Initialize counters
        Support = 0
        Physical_Attacker = 0
        Special_Attacker = 0
        Mixed_Attacker = 0
        Physical_Brawler = 0
        Special_Brawler = 0
        Physical_Tank = 0
        Special_Tank = 0
        Mixed_Tank = 0

        Support += math.floor((pokemon.defense / 20) + (pokemon.special_defense / 20) + (pokemon.hp / 10) + (pokemon.speed / 20))
        Physical_Attacker += math.floor((pokemon.attack / 10) + (pokemon.defense / 60) + (pokemon.special_defense / 60) + (pokemon.hp / 40) + (pokemon.speed / 10))
        Special_Attacker += math.floor((pokemon.special_attack / 10) + (pokemon.defense / 60) + (pokemon.special_defense / 60) + (pokemon.hp / 40) + (pokemon.speed / 10))
        Mixed_Attacker = math.floor((pokemon.special_attack / 20) + (pokemon.attack / 20) + (pokemon.defense / 80) + (pokemon.special_defense / 80) + (pokemon.hp / 40) + (pokemon.speed / 10))  
        Physical_Brawler += math.floor((pokemon.attack / 10) + (pokemon.defense / 20) + (pokemon.special_defense / 20) + (pokemon.hp / 20) + (pokemon.speed / 60))
        Special_Brawler += math.floor((pokemon.special_attack / 10) + (pokemon.defense / 20) + (pokemon.special_defense / 20) + (pokemon.hp / 20) + (pokemon.speed / 60))
        Physical_Tank += math.floor((pokemon.attack / 30) + (pokemon.special_attack / 30) + (pokemon.defense / 10) + (pokemon.special_defense / 30) + (pokemon.hp / 10))
        Special_Tank += math.floor((pokemon.attack / 30) + (pokemon.special_attack / 30) + (pokemon.defense / 30) + (pokemon.special_defense / 10) + (pokemon.hp / 10))
        Mixed_Tank += math.floor((pokemon.attack / 50) + (pokemon.special_attack / 50) + (pokemon.defense / 20) + (pokemon.special_defense / 20) + (pokemon.hp / 10))

        # Stat checks
        if pokemon.speed * 1.3 > pokemon.hp:
            Physical_Attacker += 10
            Special_Attacker += 10
            Mixed_Attacker += 10
            if pokemon.speed * 1.05 > pokemon.hp:
                Physical_Attacker += 15
                Special_Attacker += 15
                Mixed_Attacker += 15

        if pokemon.speed * 1.3 < pokemon.hp:
            Physical_Brawler += 10
            Special_Brawler += 10
            Physical_Tank += 10
            Special_Tank += 10
            Mixed_Tank += 10
            if pokemon.speed * 1.05 < pokemon.hp:
                Physical_Brawler += 15
                Special_Brawler += 15
                Physical_Tank += 15
                Special_Tank += 15
                Mixed_Tank += 15      

        if pokemon.special_attack > pokemon.attack * 1.1:
            Special_Attacker += 20
            Special_Brawler += 20
        elif pokemon.attack > pokemon.special_attack * 1.1:   
            Physical_Attacker += 20
            Physical_Brawler += 20
        else:
            Mixed_Attacker += 20
            Physical_Attacker += 5
            Physical_Brawler += 5
            Special_Attacker += 5
            Special_Brawler += 5

        if (pokemon.special_attack + pokemon.attack) < (pokemon.special_defense + pokemon.defense):
            if pokemon.special_defense > pokemon.defense * 1.1:
                Special_Tank += 20
                Mixed_Tank += 5
            elif pokemon.pokemon.defense > pokemon.special_defense * 1.1:      
                Physical_Tank += 20
                Mixed_Tank += 5
            else:
                Mixed_Tank += 20
        elif (pokemon.special_attack + pokemon.attack) >= (pokemon.special_defense + pokemon.defense):
            if pokemon.special_attack > pokemon.attack * 1.1:
                Special_Attacker += 20
                Special_Brawler += 20
            elif pokemon.attack > pokemon.special_attack * 1.1:      
                Physical_Attacker += 20
                Physical_Brawler += 20
            else:
                Mixed_Attacker += 20
                Special_Attacker += 10
                Special_Brawler += 5
                Physical_Attacker += 10
                Physical_Brawler += 5

        if pokemon.speed > (pokemon.special_defense + pokemon.defense) / 2:
            if pokemon.special_attack > pokemon.attack * 1.1:
                Special_Attacker += 10
            elif pokemon.attack > pokemon.special_attack  * 1.1:
                Physical_Attacker += 10
            else:
                Mixed_Attacker += 10
        
            if pokemon.speed > (pokemon.special_defense + pokemon.defense) / 1.5:
                if pokemon.special_attack > pokemon.attack * 1.1:
                    Special_Attacker += 10
                elif pokemon.attack > pokemon.special_attack  * 1.1:
                    Physical_Attacker += 10
                else:
                    Mixed_Attacker += 10

        if pokemon.speed < (pokemon.special_defense + pokemon.defense) / 2:
            if pokemon.special_defense > pokemon.defense * 1.1:
                Special_Tank += 10
            elif pokemon.defense > pokemon.special_defense * 1.1:
                Physical_Tank += 10
            else:
                Mixed_Tank += 10

            Physical_Brawler += 10
            Special_Brawler += 10
        
            if pokemon.speed < (pokemon.special_defense + pokemon.defense) / 1.5:
                if pokemon.special_defense > pokemon.defense * 1.1:
                    Special_Tank += 10
                elif pokemon.defense > pokemon.special_defense * 1.1:
                    Physical_Tank += 10
                else:
                    Mixed_Tank += 10

                Physical_Brawler += 10
                Special_Brawler += 10

        # Check the move pool for moves that fit roles or have status
        type_chart = TypeChart()

        super_coverage_physical = []
        super_coverage_special = []
        normal_coverage_physical = []
        normal_coverage_special = [] 

        for move in pokemon.movepool:
            if move.power is not None:
                incoming_type_arrays = type_chart.attacking_effective_types(move.type.capitalize())
                if move.split == 'physical':
                    super_coverage_physical = list(set(super_coverage_physical + incoming_type_arrays[0]))
                    normal_coverage_physical = list(set(normal_coverage_physical + incoming_type_arrays[1]))
                elif move.split == 'special':
                    super_coverage_special = list(set(super_coverage_special + incoming_type_arrays[0]))
                    normal_coverage_special = list(set(normal_coverage_special + incoming_type_arrays[1]))

                if move.power > 70:
                    if move.split == 'physical':
                        Physical_Attacker += 4
                        Physical_Brawler += 4
                        Mixed_Attacker += 2
                        Physical_Tank += 1
                        Special_Tank += 1
                        Mixed_Tank += 1
                    elif move.split == 'special':
                        Special_Attacker += 4
                        Special_Brawler += 4
                        Mixed_Attacker += 2
                        Physical_Tank += 1
                        Special_Tank += 1
                        Mixed_Tank += 1
                if move.power > 110:
                    if move.split == 'physical':
                        Physical_Attacker += 7
                        Physical_Brawler += 7
                        Mixed_Attacker += 4
                        Physical_Tank += 2
                        Special_Tank += 2
                        Mixed_Tank += 2
                        Support += 1
                    elif move.split == 'special':
                        Special_Attacker += 7
                        Special_Brawler += 7
                        Mixed_Attacker += 4
                        Physical_Tank += 2
                        Special_Tank += 2
                        Mixed_Tank += 2
                        Support += 1

            for role in move.role:
                if role in Attacker_Move_Roles:
                    Physical_Attacker += 2
                    Physical_Brawler += 2
                if role in Special_Attacker_Move_Roles:
                    Special_Attacker += 2
                    Special_Brawler += 2
                if role in Tank_Move_Roles:
                    Physical_Tank += 4
                    Special_Tank += 4
                    Mixed_Tank += 4
                    Support += 2
                if role in Speed_Helping_Moves:
                    Physical_Attacker += 2
                    Special_Attacker += 2
                if role in Support_Move_Roles:
                    Support += 10
                    Physical_Tank += 4
                    Special_Tank += 4
                    Mixed_Tank += 4
                if role in Speed_Helping_Moves:
                    Physical_Attacker += 3
                    Special_Attacker += 3   

        # Check overall defensive advantage
        average_effectiveness = type_chart.count_defending_effectiveness(pokemon.types)

        if average_effectiveness > 1:
                Physical_Brawler -= round(average_effectiveness * 5)
                Special_Brawler -= round(average_effectiveness * 5)
                Physical_Tank -= round(average_effectiveness * 5)
                Special_Tank -= round(average_effectiveness * 5)
                Mixed_Tank -= round(average_effectiveness * 5)     
        elif average_effectiveness < 0:
                Physical_Brawler -= round(average_effectiveness * 10)
                Special_Brawler -= round(average_effectiveness * 10)
                Physical_Tank -= round(average_effectiveness * 10)
                Special_Tank -= round(average_effectiveness * 10)
                Mixed_Tank -= round(average_effectiveness * 10)

        # Check move coverage
        if len(normal_coverage_physical) == 18:
            Physical_Attacker += 2
            Mixed_Attacker += 1
            Physical_Brawler += 2
        
        if len(normal_coverage_special) == 18:
            Special_Attacker += 2
            Mixed_Attacker += 1
            Special_Brawler += 2  

        Physical_Attacker += len(super_coverage_physical)
        Special_Attacker += len(super_coverage_special)
        Mixed_Attacker += (len(super_coverage_physical) + len(super_coverage_special)) / 2
        Physical_Brawler += len(super_coverage_physical)
        Special_Brawler += len(super_coverage_special) 

        # Create a dictionary with variable names as keys and values as values
        variables_dict = {
        'Support': Support,
        'Physical_Attacker': Physical_Attacker,
        'Special_Attacker': Special_Attacker,
        'Mixed_Attacker': Mixed_Attacker,
        'Physical_Brawler': Physical_Brawler,
        'Special_Brawler': Special_Brawler,
        'Physical_Tank': Physical_Tank,
        'Special_Tank': Special_Tank,
        'Mixed_Tank': Mixed_Tank
        }

        # Sort the dictionary based on values in descending order
        sorted_variables = sorted(variables_dict.items(), key=lambda x: x[1], reverse=True)

        # Get the top 3 variable names
        top_3_roles = [item[0] for item in sorted_variables[:3]]
        roles_with_scores = {role: variables_dict[role] for role in top_3_roles}
        pokemon.roles = list(roles_with_scores.items())
