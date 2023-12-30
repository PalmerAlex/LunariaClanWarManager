import pyautogui
import time
import keyboard
from tkinter import Tk, filedialog

# WARNING: Use such scripts responsibly and in compliance with server rules and policies.

def send_command(command):
    # Simulate pressing 't', typing the command, and pressing 'Enter'
    pyautogui.press('t')
    time.sleep(0.1)
    pyautogui.typewrite(command)
    pyautogui.press('enter')

def get_commands_from_file():
    # Function to open a file dialog and read commands from the selected file
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select command file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    root.destroy()
    if file_path:
        with open(file_path, 'r') as file:
            commands = file.readlines()
        return commands
    return []

# Hotkey setup
select_file_hotkey = 'f7'
start_stop_hotkey = 'f8'
exitkey = 'esc'
toggle = False  # This variable keeps track of whether the auto-typing is active
commands = []  # This will hold the commands read from the file

print(f"Press {select_file_hotkey} to select the command file.")
print(f"Press {start_stop_hotkey} to start/stop sending the messages.")
print(f"Press {exitkey} to exit.")

while True:
    try:
        if keyboard.is_pressed(select_file_hotkey):
            # If F7 is pressed, prompt the user to select the file
            commands = get_commands_from_file()
            print(f"{len(commands)} commands loaded." if commands else "No commands loaded.")
            time.sleep(1)  # Sleep to prevent bouncing

        if keyboard.is_pressed(start_stop_hotkey):
            toggle = not toggle
            print("Auto-typing started." if toggle else "Auto-typing stopped.")
            time.sleep(1)  # Sleep to prevent bouncing

        if keyboard.is_pressed(exitkey):
            # If ESC is pressed, exit the script
            print("Script exited by user.")
            break

        # If toggle is active, send commands
        while toggle and commands:
            for command in commands:
                if toggle:  # Check if toggle is still on
                    send_command(command.strip())
                    time.sleep(0.4)  # Wait before sending the next command
                else:
                    break  # If toggled off, stop sending commands
            # After all commands are sent, stop the typing
            toggle = False
            print("All commands executed. Auto-typing stopped.")
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break  # Break the loop if an error occurs

    time.sleep(0.1)  # Small delay to prevent high CPU usage
