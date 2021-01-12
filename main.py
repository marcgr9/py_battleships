from src.ui.gui import GUI
from src.ui.console_ui import ConsoleUI

response = ""
while response not in ["CONSOLE", "GUI"]:
    print("What type of ui do you want? (CONSOLE/GUI): ", end="")
    response = input()

ui = None
if response == "CONSOLE":
    ui = ConsoleUI()
elif response == "GUI":
    ui = GUI()

ui.play()
