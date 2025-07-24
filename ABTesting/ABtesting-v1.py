'''
Design service for AB testing.

'''

from collections import defaultdict
from itertools import count
import random

experiment_id_gen = count(start=1)

class Variant:
    def __init__(self, name: str):
        self.name = name
        self.events = defaultdict(int)  # event_name -> count

    def record_event(self, event_name: str):
        self.events[event_name] += 1

class Experiment:
    def __init__(self, name: str):
        self.id = next(experiment_id_gen)
        self.name = name
        self.variants: dict[str, Variant] = {}
        self.user_to_variant: dict[str, str] = {}

    def add_variant(self, variant_name: str):
        if variant_name not in self.variants:
            self.variants[variant_name] = Variant(variant_name)

    def assign_user(self, user_id: str) -> str:
        if user_id in self.user_to_variant:
            return self.user_to_variant[user_id]
        if not self.variants:
            raise Exception("No variants available in experiment.")
        variant_name = random.choice(list(self.variants.keys()))
        self.user_to_variant[user_id] = variant_name
        return variant_name

    def record_event(self, user_id: str, event_name: str):
        if user_id not in self.user_to_variant:
            raise Exception("User not assigned to any variant.")
        variant_name = self.user_to_variant[user_id]
        self.variants[variant_name].record_event(event_name)

    def get_results(self):
        result = {}
        for name, variant in self.variants.items():
            result[name] = dict(variant.events)
        return result


class ABTestingService:
    def __init__(self):
        self.experiments: dict[int, Experiment] = {}

    def create_experiment(self, name: str) -> int:
        exp = Experiment(name)
        self.experiments[exp.id] = exp
        print(f"Created experiment '{name}' with ID: {exp.id}")
        return exp.id

    def add_variant(self, experiment_id: int, variant_name: str):
        self._validate_exp(experiment_id)
        self.experiments[experiment_id].add_variant(variant_name)
        print(f"Added variant '{variant_name}' to experiment {experiment_id}")

    def assign_user(self, experiment_id: int, user_id: str) -> str:
        self._validate_exp(experiment_id)
        variant = self.experiments[experiment_id].assign_user(user_id)
        print(f"User '{user_id}' assigned to variant '{variant}'")
        return variant

    def record_event(self, experiment_id: int, user_id: str, event_name: str):
        self._validate_exp(experiment_id)
        self.experiments[experiment_id].record_event(user_id, event_name)
        print(f"Event '{event_name}' recorded for user '{user_id}'")

    def get_results(self, experiment_id: int):
        self._validate_exp(experiment_id)
        print(f"Results for experiment {experiment_id}:")
        results = self.experiments[experiment_id].get_results()
        for variant, events in results.items():
            print(f"  Variant: {variant}")
            for event, count in events.items():
                print(f"    {event}: {count}")
        return results

    def _validate_exp(self, experiment_id: int):
        if experiment_id not in self.experiments:
            raise Exception("Experiment not found.")


if __name__ == "__main__":
    ab = ABTestingService()

    exp_id = ab.create_experiment("New Button Color")
    ab.add_variant(exp_id, "Red")
    ab.add_variant(exp_id, "Green")
    ab.add_variant(exp_id, "Blue")

    # Assign users
    ab.assign_user(exp_id, "user1")
    ab.assign_user(exp_id, "user2")
    ab.assign_user(exp_id, "user3")

    # Record events
    ab.record_event(exp_id, "user1", "click")
    ab.record_event(exp_id, "user2", "click")
    ab.record_event(exp_id, "user1", "purchase")

    # Get results
    ab.get_results(exp_id)
