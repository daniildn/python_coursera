from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
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
    def get_stats(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_stats(self):
        pass

    def get_positive_effects(self):
        return self.base.get_positive_effects() + [self.__class__.__name__]


class Berserk(AbstractPositive):
    def get_stats(self):
        res = self.base.get_stats()
        res["Strength"] += 7
        res["Endurance"] += 7
        res["Agility"] += 7
        res["Luck"] += 7

        res["HP"] += 50

        res["Perception"] -= 3
        res["Charisma"] -= 3
        res["Intelligence"] -= 3
        return res


class Blessing(AbstractPositive):
    def get_stats(self):
        res = self.base.get_stats()
        res["Strength"] += 2
        res["Endurance"] += 2
        res["Agility"] += 2
        res["Luck"] += 2
        res["Perception"] += 2
        res["Charisma"] += 2
        res["Intelligence"] += 2
        return res


class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_stats(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]


class Weakness(AbstractNegative):
    def get_stats(self):
        res = self.base.get_stats()
        res["Strength"] -= 4
        res["Endurance"] -= 4
        res["Agility"] -= 4
        return res


class EvilEye(AbstractNegative):
    def get_stats(self):
        res = self.base.get_stats()
        res["Luck"] -= 10
        return res


class Curse(AbstractNegative):
    def get_stats(self):
        res = self.base.get_stats()
        res["Strength"] -= 2
        res["Endurance"] -= 2
        res["Agility"] -= 2
        res["Luck"] -= 2
        res["Perception"] -= 2
        res["Charisma"] -= 2
        res["Intelligence"] -= 2
        return res

# >>> from deco import *
# >>> # создаем героя
# >>> hero = Hero()
# >>> hero.get_stats()
# {'HP': 128, 'MP': 42, 'SP': 100, 'Strength': 15, 'Perception': 4, 'Endurance': 8, 'Charisma': 2, 'Intelligence': 3, 'Agility': 8, 'Luck': 1}
# >>> hero.stats
# {'HP': 128, 'MP': 42, 'SP': 100, 'Strength': 15, 'Perception': 4, 'Endurance': 8, 'Charisma': 2, 'Intelligence': 3, 'Agility': 8, 'Luck': 1}
# >>> hero.get_negative_effects()
# [ ]
# >>> hero.get_positive_effects()
# [ ]

# >>> # накладываем эффект
# >>> brs1 = Berserk(hero)
# >>> brs1.get_stats()
# {'HP': 178, 'MP': 42, 'SP': 100, 'Strength': 22, 'Perception': 1, 'Endurance': 15, 'Charisma': -1, 'Intelligence': 0, 'Agility': 15, 'Luck': 8}
# >>> brs1.get_negative_effects()
# [ ]
# >>> brs1.get_positive_effects()
# ['Berserk']
# >>> # накладываем эффекты
# >>> brs2 = Berserk(brs1)
# >>> cur1 = Curse(brs2)
# >>> cur1.get_stats()
# {'HP': 228, 'MP': 42, 'SP': 100, 'Strength': 27, 'Perception': -4, 'Endurance': 20, 'Charisma': -6, 'Intelligence': -5, 'Agility': 20, 'Luck': 13}
# >>> cur1.get_positive_effects()
# ['Berserk', 'Berserk']
# >>> cur1.get_negative_effects()
# ['Curse']
# >>> # снимаем эффект Berserk
# >>> cur1.base = brs1
# >>> cur1.get_stats()
# {'HP': 178, 'MP': 42, 'SP': 100, 'Strength': 20, 'Perception': -1, 'Endurance': 13, 'Charisma': -3, 'Intelligence': -2, 'Agility': 13, 'Luck': 6}
# >>> cur1.get_positive_effects()
# ['Berserk']
# >>> cur1.get_negative_effects()
# ['Curse']
# hero = Hero()
#
# print(hero.get_stats())
# print(hero.stats)
# print(hero.get_negative_effects())
# print(hero.get_positive_effects())
#
# brs1 = Berserk(hero)
#
# print(brs1.get_stats())
# print(brs1.get_positive_effects())
# print(brs1.get_negative_effects())
#
# brs2 = Berserk(brs1)
# cur1 = Curse(brs2)
#
# print(cur1.get_stats())
# print(cur1.get_positive_effects())
# print(cur1.get_negative_effects())
#
# cur1.base = brs1
# print(cur1.get_positive_effects())
# print(cur1.get_negative_effects())
# print(cur1.get_stats())
