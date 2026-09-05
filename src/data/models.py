from dataclasses import dataclass


@dataclass
class Stint:
    driver: str
    stint_number: int
    compound: str
    start_lap: int
    end_lap: int

    @property
    def length(self) -> int:
        return self.end_lap - self.start_lap + 1


@dataclass
class PitStop:
    driver: str
    lap: int
    duration_s: float
