from nimble_encounter_simulator.action.attack import MeleeAttack
from nimble_encounter_simulator.action.rage import Rage
from nimble_encounter_simulator.creature.berserker import Berserker
from nimble_encounter_simulator.creature.goblin import get_melee_goblin
from nimble_encounter_simulator.creature.monster import Monster
from nimble_encounter_simulator.encounter.monster_handler import MonsterHandler
from nimble_encounter_simulator.effect.intensifying_fury import IntensifyingFury
from nimble_encounter_simulator.encounter.encounter import Encounter
from nimble_encounter_simulator.encounter.party import Party
from nimble_encounter_simulator.encounter.player import Player
import nimble_encounter_simulator.items.weapon as weapons
from nimble_encounter_simulator.creature.strategy.strategy import RageBeforeAttack
from nimble_encounter_simulator.creature.strategy.monster_strategy import MonsterAlwaysMeleeAttack
import statistics
import plotly
from nimble_encounter_simulator.logging_setup import get_named_console_logger
logger = get_named_console_logger(__name__)

def main():
    runs = 1_000
    rounds=10
    plot_results = []
    weapon = weapons.get_longsword()
    for rage_threshold in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        damage_results = [run_simple_combat(rage_threshold=rage_threshold, weapon=weapon)/rounds for _ in range(runs)]

        # store results for plotting in a dict
        results = {
            "rage_threshold": rage_threshold,
            "damage_results": (statistics.mean(damage_results), statistics.stdev(damage_results))
        }
        plot_results.append(results)

    # print damage statistics
    # plot results
    rage_thresholds = [result["rage_threshold"] for result in plot_results]
    damage_means = [result["damage_results"][0] for result in plot_results]
    damage_stds = [result["damage_results"][1] for result in plot_results]

    plotly_fig = plotly.graph_objs.Figure()
    plotly_fig.add_trace(
        plotly.graph_objs.Scatter(
            x=rage_thresholds,
            y=damage_means,
            error_y=dict(type="data", array=damage_stds),
            mode="markers"
        )
    )
    # set the title and axes titles
    plotly_fig.update_layout(
        title=f"Damage per round vs Rage Threshold, Berserker, {weapon.name}",
        xaxis_title="Rage Threshold",
        yaxis_title="Damage"
    )

    plotly_fig.show()

def run_simple_combat(rage_threshold: float = 0.5, weapon=weapons.unarmed_attack()) -> int:
    party = Party()

    karru = Berserker.new(
        name="Karru Mossfist",
        strength=3,
        dexterity=1,
        intelligence=-1,
        willpower=0,
        ancestry="Beastkin(Gorilla)"
        )
    karru.weapon = weapon
    player_1 = Player(creature=karru, strategy=RageBeforeAttack(character=karru, party=party, rage_threshold=rage_threshold))
    player_1.register_action(action=MeleeAttack())
    player_1.register_action(action=Rage())
    party.players.append(player_1)

    karru.level = 2
    karru.register_feature(feature=IntensifyingFury(character=karru))
    # print("Berserker:")
    # print(karru)

    # enemies
    goblin = get_melee_goblin(name="Goblin")
    goblin.health.current_hit_points = 1000
    goblin.health.max_hit_points = 1000
    goblin_strategy = MonsterAlwaysMeleeAttack(monster=goblin, available_actions=[MeleeAttack()])
    goblin_handler = MonsterHandler(monster=goblin, strategy=goblin_strategy)
    enemies : list[MonsterHandler] = [
        goblin_handler,
    ]

    encounter = Encounter(party=party, enemies=enemies)
    encounter.run()

    return goblin.health.max_hit_points - goblin.health.current_hit_points
    

if __name__ == "__main__":
    main()
