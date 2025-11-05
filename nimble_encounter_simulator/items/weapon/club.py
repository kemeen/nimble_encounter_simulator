from nimble_encounter_simulator.items.item import ItemTier
from nimble_encounter_simulator.items.weapon.weapon import DamageType, Weapon, WeaponBonusStat, WeaponProperties
from nimble_encounter_simulator.roll.die import Die


def get_great_club() -> Weapon:
    return Weapon(
        name="Great Club",
        description="A large club.",
        value=60,
        size=1,
        stack_size=1,
        tier=ItemTier.COMMON,
        properties=WeaponProperties(
            two_handed=True,
            load=False,
            reach=1,
            range=0,
            thrown=False,
            vicious=False,
            light=False,
        ),
        bonus_stat=WeaponBonusStat.STR,
        damage_dice=[Die(sides=10, is_primary=True)],
        damage_types=[DamageType.BLUDGE],
        requirements=[(WeaponBonusStat.STR, 2)],
        )

def get_great_maul() -> Weapon:
    return Weapon(
        name="Great Maul",
        description="A very large maul.",
        value=120,
        size=1,
        stack_size=1,
        tier=ItemTier.COMMON,
        properties=WeaponProperties(
            two_handed=True,
            load=False,
            reach=1,
            range=0,
            thrown=False,
            vicious=False,
            light=False,
        ),
        bonus_stat=WeaponBonusStat.STR,
        damage_dice=[Die(sides=12, is_primary=True)],
        damage_types=[DamageType.BLUDGE],
        requirements=[(WeaponBonusStat.STR, 2)],
        )