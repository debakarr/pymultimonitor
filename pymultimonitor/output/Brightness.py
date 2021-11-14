from dataclasses import dataclass


@dataclass
class Brightness:
    minimum: int
    current: int
    maximum: int
