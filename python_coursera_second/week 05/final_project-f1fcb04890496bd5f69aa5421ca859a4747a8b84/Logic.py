import Service


class GameEngine:
    """Класс игрового движка, который представлен в виде паттерна
       наблюдатель"""
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False

    def subscribe(self, obj):
        """Метод добавляет подписчика"""
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        """Метод удаляет подписчика"""
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        """Метод уведовляет всех подписчиков, что нужно обновить свое
           состояние"""
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        """Метод устанавливает героя в движке"""
        self.hero = hero

    def interact(self):
        """Взаимодействие объекта с героем - если позиция объекта и героя
           совпадают, то объект удаляется из списка объектов движка и
           вызывается метод объекта interact, использующий игровой движок и
           героя"""
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # MOVEMENT
    def move_up(self):
        """Если над героем нет стены, то он двигается вверх и взаимодействует с
           всеми объектами"""
        self.score -= 0.02
        if self.map[self.hero.position[1] - 1][self.hero.position[0]] == \
                Service.wall:
            return
        self.hero.position[1] -= 1
        self.interact()

    def move_down(self):
        """Если под героем нет стены, то он двигается вниз и взаимодействует со
           всеми объектами"""
        self.score -= 0.02
        if self.map[self.hero.position[1] + 1][self.hero.position[0]] ==\
                Service.wall:
            return
        self.hero.position[1] += 1
        self.interact()

    def move_left(self):
        """Если слева нет стены, то герой двигается налево и взаимодействует со
           всеми объектами"""
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] - 1] ==\
                Service.wall:
            return
        self.hero.position[0] -= 1
        self.interact()

    def move_right(self):
        """Если справа от героя не стены, то он идет направо и взаимодействует
           со всеми объектами"""
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] + 1] ==\
                Service.wall:
            return
        self.hero.position[0] += 1
        self.interact()

    # MAP
    def load_map(self, game_map):
        """Устанавливается карта"""
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        """Добавляется один объект"""
        self.objects.append(obj)

    def add_objects(self, objects):
        """Добавляется несколько объектов"""
        self.objects.extend(objects)

    def delete_object(self, obj):
        """Удаляется один объект"""
        self.objects.remove(obj)