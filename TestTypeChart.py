from typeGraph import TypeChart

attack_type = 'Steel'
defense_type = 'Fairy'

type_chart = TypeChart()
effectiveness = type_chart.count_defending_effectiveness([defense_type])
effectiveness2 = type_chart.attacking_effective_types(attack_type)
print(f"test: {effectiveness}")
print(f"test: {effectiveness2}")