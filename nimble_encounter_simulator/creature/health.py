from dataclasses import dataclass


@dataclass
class Health:
    current_hit_points: int
    max_hit_points: int
    temporary_hit_points: int
    wounds: int
    max_wounds: int

    def __post_init__(self):
        if self.current_hit_points > self.max_hit_points:
            self.current_hit_points = self.max_hit_points

    @property
    def is_alive(self):
        return self.wounds < self.max_wounds
    
    def take_damage(self, damage: int):
        # first takes damage from temporary hit points, the rest from current hit points
        if self.temporary_hit_points > 0:
            damage_taken_from_temporary = min(damage, self.temporary_hit_points)
            self.temporary_hit_points -= damage_taken_from_temporary
            damage -= damage_taken_from_temporary
        self.current_hit_points -= damage
    
    def heal(self, amount: int):
        self.current_hit_points += amount
        if self.current_hit_points > self.max_hit_points:
            self.current_hit_points = self.max_hit_points

    def add_temporary_hit_points(self, amount: int):
        self.temporary_hit_points += amount

    def set_temporary_hit_points(self, amount: int):
        self.temporary_hit_points = amount
    
    def remove_temporary_hit_points(self, amount: int):
        self.temporary_hit_points -= amount