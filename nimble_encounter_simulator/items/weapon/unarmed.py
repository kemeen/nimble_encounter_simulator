from nimble_encounter_simulator.items.item import ItemTier
from nimble_encounter_simulator.items.weapon.weapon import DamageType, Weapon, WeaponBonusStat, WeaponProperties
from nimble_encounter_simulator.roll.die import Die


def unarmed_attack() -> Weapon:
    return Weapon(
        name="Unarmed Strike",
        description="A unarmed strike.",
        value=0,
        size=0,
        stack_size=1,
        tier=ItemTier.COMMON,
        properties=WeaponProperties(
            two_handed=False,
            load=False,
            reach=1,
            range=0,
            thrown=False,
            vicious=False,
            light=True,
        ),
        bonus_stat=WeaponBonusStat.STR,
        damage_dice=[Die(sides=4, is_primary=True)],
        damage_types=[DamageType.BLUDGE],
        requirements=[],
    )