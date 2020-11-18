from dataclasses import dataclass


@dataclass
class Furniture:
    weight_kg: float
    height_mm: int
    width_mm: int
    material: str = 'wood'


fw = Furniture(5, 100, 500)
fa = Furniture(25, 500, 500, 'aluminium')

if __name__ == '__main__':
    print(fa)

