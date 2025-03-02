from dataclasses import dataclass


@dataclass
class Product:
    name: str
    quantity: int
    unit_weight: float

    @property
    def total_weight(self):
        return self.quantity * self.unit_weight
