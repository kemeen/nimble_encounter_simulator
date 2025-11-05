from nimble_encounter_simulator.items.item import ItemTier
from nimble_encounter_simulator.items.weapon.weapon import DamageType, Weapon, WeaponBonusStat, WeaponProperties
from nimble_encounter_simulator.roll.die import Die


def get_longsword() -> "Weapon":
    return Weapon(
        name="Longsword",
        description="A long sword.",
        value=60,
        size=1,
        stack_size=1,
        tier=ItemTier.COMMON,
        properties=WeaponProperties(
            two_handed=False,
            load=False,
            reach=1,
            range=4,
            thrown=False,
            vicious=False,
            light=False,
        ),
        bonus_stat=WeaponBonusStat.STR,
        damage_dice=[Die(sides=8, is_primary=True)],
        damage_types=[DamageType.SLASHING],
        requirements=[(WeaponBonusStat.STR, 2)],
    )

def get_greatsword() -> "Weapon":
    return Weapon(
        name="Greatsword",
        description="A very large sword.",
        value=120,
        size=1,
        stack_size=1,
        tier=ItemTier.COMMON,
        properties=WeaponProperties(
            two_handed=True,
            load=False,
            reach=2,
            range=0,
            thrown=False,
            vicious=False,
            light=False,
        ),
        bonus_stat=WeaponBonusStat.STR,
        damage_dice=[Die(sides=4, is_primary=True), Die(sides=4, is_primary=False), Die(sides=4, is_primary=False)],
        damage_types=[DamageType.SLASHING],
        requirements=[(WeaponBonusStat.STR, 2)],
    )