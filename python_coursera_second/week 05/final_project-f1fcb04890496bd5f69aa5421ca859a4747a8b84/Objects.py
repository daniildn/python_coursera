from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    """Функция загружает изображение, прорисовывают его на поверхности и
    возвращают эту поверхность, наверное это функция нужна просто для
    дебага"""
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):
    """Абстрактный базовый класс для классов Creature и Ally, от Creature
    в свою очередь наследуются классы Hero и Enemy, от Hero по сути своей
    наследуют все эффекты"""
    @abstractmethod
    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position

    def draw(self, display):
        pixels = self.position[0]*60, self.position[1]*60
        display.blit(self.sprite, pixels)


class Interactive(ABC):
    """Абстрактный класс для Ally и Enemy"""
    @abstractmethod
    def interact(self, engine, hero):
        pass


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        super().__init__(icon, stats, position)
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        """Метод рассчитывает максимальное здоровье объекта, при этом
        данным объектом может быть как герой, так и враг"""
        self.max_hp = 5 + self.stats["endurance"] * 2


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        super().__init__(icon, {}, position)
        self.action = action

    def interact(self, engine, hero):
        """Союзник применяет определенные действия относительно героя"""
        self.action(engine, hero)


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.xp = xp

    def interact(self, engine, hero):
        hero.hp -= self.stats['strength']
        if hero.hp <= 0:
            exit()
        engine.hero.exp += self.xp
        levels = hero.level_up()
        for message in levels:
            engine.notify(message)


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        """Метод генератор суть которого заключается в том, что при достижении
        определенного количество опыта(зависящего от уровня), возвращается
        строка "level up!" и его работа приостанавливается, при возобновлении
        работы метода у гегоя увеоичивается уровень на 1, сила на 2,
        выносливость на 2, высчитывается максимальное количество здоровья и
        оно восстанавливается полностью"""
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        """Стоит обратить внимание на то, что объекты данного класса применяют
        apply_effect, это в принципе из-за того, что наследниками данного
        класса являются эффекты и за счет вызова этого метода не нужно
        явно вызывать данный метод, так как он вызван уже при инициализации"""
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 7
        self.stats['endurance'] += 7
        self.stats['luck'] += 7
        self.max_hp += 50
        self.stats['intelligence'] -= 3


class Blessing(Effect):
    def apply_effect(self):
        self.stats['strength'] += 2
        self.stats['endurance'] += 2
        self.stats['intelligence'] += 2
        self.stats['luck'] += 2


class Weakness(Effect):
    def apply_effect(self):
        self.stats['strength'] -= 4
        self.stats['endurance'] -= 4