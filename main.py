from src.gui import GUI
from src.ui import ConsoleUI

response = ""
while response not in ["UI", "GUI"]:
    print("What type of ui do you want? (UI/GUI): ", end="")
    response = input()

ui = None
if response == "UI":
    ui = ConsoleUI()
elif response == "GUI":
    ui = GUI()

ui.play()
