import random

# Constants
NUM_ATTRIBUTES = 20
MAX_ATTRIBUTE_VALUE = 5  # The maximum value an attribute can have
MAX_MONSTER_STRENGTH = 5

class Player:
    """Defines a player with health and attributes."""
    def __init__(self, health, attributes):
        self.attributes = attributes
        self.health = health

    def display_status(self):
        return f"Health: {self.health}, Attributes: {self.attributes}"

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0
     


class Monster:
    """Defines a monster with strength, attribute order, and attribute value."""
    def __init__(self, strength, attribute_order, attribute_value):
        self.strength = strength
        self.attribute_order = attribute_order
        self.attribute_value = attribute_value

    def display_status(self):
        return f"Strength: {self.strength}, Attribute Order: {self.attribute_order}, Attribute Value: {self.attribute_value}"


def create_monster():
    """Creates a monster with random strength, attribute order, and attribute value."""
    strength = random.randint(1, MAX_MONSTER_STRENGTH)
    attribute_order = random.randint(0, NUM_ATTRIBUTES - 1)
    attribute_value = random.randint(0, MAX_ATTRIBUTE_VALUE)
    return Monster(strength, attribute_order, attribute_value)


def battle(player, monster):
    """Simulates a battle between the player and the monster with variability in damage for each multiplier."""
    player_attribute_value = player.attributes[monster.attribute_order]
    damage_multiplier = (monster.attribute_value - player_attribute_value)
    
    total_damage = 0
    # Looping for each damage multiplier and calculating random damage
    for _ in range(abs(damage_multiplier)):
        damage = random.randint(1, monster.strength)
        total_damage += damage

    if total_damage > 0:
        player.take_damage(total_damage)

    return 'Player wins!' if player.is_alive() else 'Player loses!'



# Testing the game
player = Player(20, (1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
monster = Monster(5,1,10)
result = battle(player, monster)

print(f"{player.display_status()} ,\n{monster.display_status()},\n{result}")
