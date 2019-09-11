class HeroFactory:
    @classmethod  # создаёт героя с заданным именем
    def create_hero(Class, name):
        return Class.Hero(name)

    @classmethod  # создаёт оружие
    def create_weapon(Class):
        return Class.Weapon()

    @classmethod  # создаёт заклинание
    def create_spell(Class):
        return Class.Spell()


class WarriorFactory(HeroFactory):
    class Hero:  # класс войнов
        def __init__(self, name):
            self.name = name
            self.weapon = None
            self.armor = None
            self.spell = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):  # удар оружием
            print(f"W. {self.name} uses {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):  # использование заклинания
            print(f"W. {self.name} casts {self.spell.cast()}")
            self.spell.cast()

    class Weapon:
        def hit(self):
            return "Claymore"

    class Spell:
        def cast(self):
            return "Power"


class MageFactory(HeroFactory):
    class Hero:
        def __init__(self, name):
            self.name = name
            self.weapon = None
            self.armor = None
            self.spell = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):
            print(f"M. {self.name} uses {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"M. {self.name} casts {self.spell.cast()}")
            self.spell.cast()

    class Weapon:
        def hit(self):
            return "Staff"

    class Spell:
        def cast(self):
            return "Fireball"


class AssassinFactory(HeroFactory):
    class Hero:
        def __init__(self, name):
            self.name = name
            self.weapon = None
            self.armor = None
            self.spell = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):
            print(f"A. {self.name} uses {self.weapon.hit()}")
            self.weapon.hit()

        def cast(self):
            print(f"A. {self.name} casts {self.spell.cast()}")

    class Weapon:
        def hit(self):
            return "Dagger"

    class Spell:
        def cast(self):
            return "Invisibility"


def create_hero(factory):
    hero = factory.create_hero("Nagibator")
    weapon = factory.create_weapon()
    ability = factory.create_spell()
    hero.add_weapon(weapon)
    hero.add_spell(ability)
    return hero


factory = AssassinFactory()
player = create_hero(factory)
player.cast()
player.hit()
