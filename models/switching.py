from dataclasses import dataclass


@dataclass
class Switching:
    main_source: str
    main_destination: str
    reserve_source : str
    reserve_destination : str

    def main_switching(self):
        return f'{self.main_source} -> {self.main_destination}'

    def reserve_switching(self):
        return f'{self.reserve_source} -> {self.reserve_destination}'