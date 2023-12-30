import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog


class ClanWarManager:
    def __init__(self):
        self.teams = {'red': [], 'blue': [], 'green': [], 'yellow': []}
        self.banned_kits = []
        self.selected_map = ""

    def parse_team_input(self, team_input):
        """
        Parses a string of IGNs separated by commas or new lines and returns a list of IGNs.
        """
        return [ign.strip() for ign in team_input.replace(',', '\n').split('\n') if ign.strip()]

    def set_team_data(self, team_name, team_input):
        """
        Sets the team members for a given team based on the input string.
        Error handling for invalid team names.
        """
        if team_name in self.teams:
            self.teams[team_name] = self.parse_team_input(team_input)
        else:
            raise ValueError(f"Invalid team name: '{team_name}'. Valid team names are 'red', 'blue', 'green', 'yellow'.")

    def set_banned_kits(self, kits_input):
        """
        Sets the list of banned kits based on the input string.
        """
        self.banned_kits = self.parse_team_input(kits_input)

    def set_map(self, map_name):
        """
        Sets the selected map.
        Error handling for empty map name.
        """
        map_name = map_name.strip()
        if map_name:
            self.selected_map = map_name
        else:
            raise ValueError("Map name cannot be empty.")

    def generate_commands(self):
        """
        Generates a list of server commands based on the current configuration.
        Error handling for missing team members or no map selection.
        """
        if not any(self.teams.values()):
            raise ValueError("No team members have been set.")
        if not self.selected_map:
            raise ValueError("No map has been selected.")

        commands = []

        commands.append("/scheduled toggle")

        for team, members in self.teams.items():
            for member in members:
                commands.append(f"/scheduled add {team} {member}")

        for kit in self.banned_kits:
            commands.append(f"/anni disablekit {kit}")

        commands.append(f"/anni forcemap {self.selected_map}")

        return commands



import tkinter as tk
from tkinter import scrolledtext, messagebox

# Include the ClanWarManager class code here

# Create the main window
root = tk.Tk()
root.title("Minecraft Clan War Manager")

# Create widgets for team inputs and store them in a dictionary
team_texts = {}
for team in ['red', 'blue', 'green', 'yellow']:
    label = tk.Label(root, text=f"{team.capitalize()} Team IGNs:")
    label.pack()
    team_texts[team] = scrolledtext.ScrolledText(root, height=5, width=40)
    team_texts[team].pack()

# Create widgets for banned kits and map name
banned_kits_label = tk.Label(root, text="Banned Kits (comma-separated or new lines):")
banned_kits_label.pack()
banned_kits_text = scrolledtext.ScrolledText(root, height=3, width=40)
banned_kits_text.pack()

map_name_label = tk.Label(root, text="Map Name:")
map_name_label.pack()
map_name_entry = tk.Entry(root, width=30)
map_name_entry.pack()

# Create an instance of ClanWarManager
manager = ClanWarManager()

def generate_commands():
    try:
        # Fetch data from the GUI
        team_inputs = {team: text.get('1.0', tk.END).strip() for team, text in team_texts.items()}
        banned_kits_input = banned_kits_text.get('1.0', tk.END).strip()
        selected_map = map_name_entry.get().strip()

        # Setting data
        for team, input_text in team_inputs.items():
            manager.set_team_data(team, input_text)
        manager.set_banned_kits(banned_kits_input)
        manager.set_map(selected_map)

        # Generating commands
        commands = manager.generate_commands()

        # Display commands in the GUI
        commands_text.delete('1.0', tk.END)
        commands_text.insert('1.0', '\n'.join(commands))

        # Save commands to a text file
        save_commands_to_file(commands)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def save_commands_to_file(commands):
    # Ask the user for a location and name to save the commands file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save commands as..."
    )
    if file_path:  # If a file path was provided
        with open(file_path, 'w') as file:
            file.write('\n'.join(commands))
        messagebox.showinfo("Success", "Commands were saved to:\n" + file_path)

# Create button to generate commands
generate_button = tk.Button(root, text="Generate Commands", command=generate_commands)
generate_button.pack()

# Create widget to display generated commands
commands_label = tk.Label(root, text="Generated Commands:")
commands_label.pack()
commands_text = scrolledtext.ScrolledText(root, height=10, width=80)
commands_text.pack()

# Run the application
root.mainloop()
