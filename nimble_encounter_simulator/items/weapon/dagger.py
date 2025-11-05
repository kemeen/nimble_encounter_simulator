from nimble_encounter_simulator.items.item import ItemTier
from nimble_encounter_simulator.items.weapon.weapon import DamageType, Weapon, WeaponBonusStat, WeaponProperties
from nimble_encounter_simulator.roll.die import Die


def simple_dagger() -> Weapon:
    return Weapon(
        name="Simple Dagger",
        description="A simple dagger.",
        value=3,
        size=1,
        stack_size=10,
        tier=ItemTier.COMMON,
        properties=WeaponProperties(
            two_handed=False,
            load=False,
            reach=1,
            range=4,
            thrown=True,
            vicious=False,
            light=True,
        ),
        bonus_stat=WeaponBonusStat.DEX,
        damage_dice=[Die(sides=4, is_primary=True)],
        damage_types=[DamageType.SLASHING],
        requirements=[],
    )