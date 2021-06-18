from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def _change_effects(self):
        pass

    @abstractmethod
    def _change_stats(self):
        pass

    def get_stats(self):
        self.stats = self.base.get_stats().copy()
        self._change_stats()
        return self.stats.copy()


class AbstractPositive(AbstractEffect, ABC):
    def get_positive_effects(self):
        self.positive_effects = self.base.get_positive_effects().copy()
        self._change_effects()
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect, ABC):
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects().copy()
        self._change_effects()
        return self.negative_effects.copy()


class Berserk(AbstractPositive):
    def _change_effects(self):
        self.positive_effects.append('Berserk')

    def _change_stats(self):
        self.stats['HP'] += 50
        for stat in ['Strength', 'Endurance', 'Agility', 'Luck']:
            self.stats[stat] += 7
        for stat in ['Perception', 'Charisma', 'Intelligence']:
            self.stats[stat] -= 3


class Blessing(AbstractPositive):
    def _change_effects(self):
        self.positive_effects.append('Blessing')

    def _change_stats(self):
        for stat in ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]:
            self.stats[stat] += 2


class Weakness(AbstractNegative):
    def _change_effects(self):
        self.negative_effects.append('Weakness')

    def _change_stats(self):
        for stat in ['Strength', 'Endurance', 'Agility']:
            self.stats[stat] -= 4


class EvilEye(AbstractNegative):
    def _change_effects(self):
        self.negative_effects.append('EvilEye')

    def _change_stats(self):
        self.stats['Luck'] -= 10


class Curse(AbstractNegative):
    def _change_effects(self):
        self.negative_effects.append('Curse')

    def _change_stats(self):
        for stat in ["Strength", "Perception", "Endurance", "Charisma", "Intelligence", "Agility", "Luck"]:
            self.stats[stat] -= 2
