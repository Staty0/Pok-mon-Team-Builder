import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import threading
from teamBuilder import PokemonTeamBuilder

class GUI:
    def update_output_text(self, text):
        #output text to the field, call from processing to update user
        self.output_text.insert(tk.END, text + '\n')
        self.output_text.see(tk.END)

    def clear_left_panel(self):
        # Clear all text input slots and reset role dropdowns to default
        for entry in self.input_entries:
            entry.delete(0, tk.END)

        for role_var in self.role_vars:
            role_var.set(self.role_options[0]) 

    def on_generate_button_click(self):
        try:
            teamBuilder = PokemonTeamBuilder()

            # Get the user inputs from text entry slots
            pokemon_names = [entry.get() for entry in self.input_entries]

            # Get the selected values from dropdown menus
            selected_generation = self.generation_var.get()
            selected_smogon_format = self.smogon_format_var.get()
            selected_strategy = self.strategy_var.get()
            selected_monotype = self.monotype_var.get()
            selected_offrole = self.offrole_var.get()
            selected_roles = [self.role_var.get() for role_var in self.role_vars]

            # Get the value from the variance slider
            selected_variance = self.variance_slider.get()


            processing_thread = threading.Thread(target=teamBuilder.build_team, args=(pokemon_names, selected_generation, 
            selected_smogon_format, selected_strategy, selected_monotype, round(selected_variance), selected_roles, selected_offrole, self))
            processing_thread.start()
            

        except Exception as e:
            # Handle the exception, for example, display an error message in the output text field
            self.update_output_text(f"An error occurred: {str(e)}")

    def set_pokemon(self, pokemons):
        print(pokemons)
        for i, (pokemon, role) in enumerate(pokemons):
            # Set the returned Pokémon names
            self.input_entries[i].delete(0, tk.END)  # Clear existing text
            self.input_entries[i].insert(tk.END, pokemon)

            # Set Pokémon role if it's a valid role
            if role in self.role_options:
                self.role_vars[i].set(role)
            else:
                self.role_vars[i].set(role_options[0])

    def show_popup_warning(self, message):
          return messagebox.askyesno("Warning", message)            

    def __init__(self, master):
        self.master = master            

        # Create the left frame for text input slots
        self.left_frame = ttk.Frame(root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create text input slots on the left side
        self.input_entries = []
        self.role_vars = []
        self.role_options = ['', 'Support', 'Physical_Attacker', 'Special_Attacker', 'Mixed_Attacker',
            'Physical_Brawler', 'Special_Brawler', 'Physical_Tank', 'Special_Tank', 'Mixed_Tank']


        for i in range(6):
            self.label = ttk.Label(self.left_frame, text=f'Pokemon {i+1}: ')
            self.label.grid(row=i, column=0, padx=5, pady=5)
            
            self.entry = ttk.Entry(self.left_frame, width=15)
            self.entry.grid(row=i, column=1, padx=5, pady=5)
            self.input_entries.append(self.entry)

            # Pokémon role dropdown
            self.role_label = ttk.Label(self.left_frame, text='Role:')
            self.role_label.grid(row=i, column=2, padx=5, pady=5) 
            self.role_var = tk.StringVar(value=self.role_options[0])
            self.role_dropdown = ttk.Combobox(self.left_frame, values=self.role_options, textvariable=self.role_var)
            self.role_dropdown.grid(row=i, column=3, padx=5, pady=5)
            self.role_vars.append(self.role_var) 

            
        # Create the right frame for filter dropdowns
        self.right_frame = ttk.Frame(root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

        # Define filter options
        self.generation_options = ['Generation 1', 'Generation 2', 'Generation 3', 'Generation 4', 'Generation 5', 'Generation 6', 'Generation 7', 'Generation 8', 'Generation 9']
        self.smogon_format_options = ['','OU', 'UU', 'RU', 'NU', 'PU']
        self.strategy_options = ['Balanced', 'Offensive', 'Defensive', 'Overly Defensive', 'Overly Offensive']
        self.monotype_options = ['','Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Dark', 'Fairy', 'Dragon', 'Steel', 'Ice', 'Ghost', 'Rock', 'Ground', 'Flying', 'Bug', 'Poison', 'Normal', 'Fighting']
        self.offrole_options = ['Full Random', 'Best Only', 'Worst in Logic', 'Off Selections Allowed', 'All Off Role', 'Some Off Role Allowed', 'Some Off Role Forced', 'All Off Role Lite', 'Funny']

        # Create filter dropdowns on the right side
        self.generation_var = tk.StringVar(value=self.generation_options[0])
        self.generation_label = ttk.Label(self.right_frame, text='Generation: ')
        self.generation_label.grid(row=0, column=0, padx=5, pady=5)
        self.generation_dropdown = ttk.Combobox(self.right_frame, values=self.generation_options, textvariable=self.generation_var)
        self.generation_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self.smogon_format_var = tk.StringVar(value=self.smogon_format_options[0])
        self.smogon_format_label = ttk.Label(self.right_frame, text='Smogon Format: ')
        self.smogon_format_label.grid(row=1, column=0, padx=5, pady=5)
        self.smogon_format_dropdown = ttk.Combobox(self.right_frame, values=self.smogon_format_options, textvariable=self.smogon_format_var)
        self.smogon_format_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.strategy_var = tk.StringVar(value=self.strategy_options[0])
        self.strategy_label = ttk.Label(self.right_frame, text='Strategy: ')
        self.strategy_label.grid(row=2, column=0, padx=5, pady=5)
        self.strategy_dropdown = ttk.Combobox(self.right_frame, values=self.strategy_options, textvariable=self.strategy_var)
        self.strategy_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.monotype_var = tk.StringVar(value=self.monotype_options[0])
        self.monotype_label = ttk.Label(self.right_frame, text='MonoType Team: ')
        self.monotype_label.grid(row=3, column=0, padx=5, pady=5)
        self.monotype_dropdown = ttk.Combobox(self.right_frame, values=self.monotype_options, textvariable=self.monotype_var)
        self.monotype_dropdown.grid(row=3, column=1, padx=5, pady=5)
        
        self.offrole_var = tk.StringVar(value=self.offrole_options[0])
        self.offrole_label = ttk.Label(self.right_frame, text='Role Selection Logic: ')
        self.offrole_label.grid(row=4, column=0, padx=5, pady=5)
        self.offrole_dropdown = ttk.Combobox(self.right_frame, values=self.offrole_options, textvariable=self.offrole_var)
        self.offrole_dropdown.grid(row=4, column=1, padx=5, pady=5)

        # Create the bottom frame for variance slider, generate button, and status bar
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Create slider for strength and randomness
        self.variance_slider = ttk.Scale(self.bottom_frame, from_=0, to=100, length=200, orient=tk.HORIZONTAL)
        self.variance_slider.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.variance_slider.set(50)  # Set initial value to the middle

        self.strength_label = ttk.Label(self.bottom_frame, text='Strength')
        self.strength_label.grid(row=0, column=0, padx=5, pady=5)

        self.randomness_label = ttk.Label(self.bottom_frame, text='Randomness')
        self.randomness_label.grid(row=0, column=2, padx=5, pady=5)

        # Create the 'Generate' button
        self.generate_button = ttk.Button(self.bottom_frame, text='Generate Team', command=self.on_generate_button_click)
        self.generate_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        # Create a clear button
        self.clear_button = ttk.Button(self.bottom_frame, text='Clear Pokemon Selections', command=self.clear_left_panel)
        self.clear_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Create the status bar
        self.output_text = tk.Text(self.bottom_frame, height=10, width=80, wrap=tk.WORD)
        self.output_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)


root = tk.Tk()
root.title('Data Generator')
app = GUI(root)
root.mainloop()
