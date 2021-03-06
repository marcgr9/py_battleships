# ui_abc.py
# marc, marc@gruita.ro
from abc import ABC, abstractmethod

from src.utils.utils import ShipType, ShotResult, Player


class UI(ABC):
    ship_names = {
        ShipType.CARRIER: "Aircraft Carrier",
        ShipType.BATTLESHIP: "Battleship",
        ShipType.DESTROYER: "Destroyer",
        ShipType.SUBMARINE: "Submarine",
        ShipType.PATROL_BOAT: "Patrol Boat"
    }

    shot_responses = {
        ShotResult.MISS: "Miss",
        ShotResult.HIT: "Hit",
        ShotResult.ALREADY_HIT: "Area already hit"
    }

    players = {
        Player.AI: "AI",
        Player.HUMAN: "You"
    }

    @abstractmethod
    def play(self):
        pass
