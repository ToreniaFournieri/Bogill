import streamlit as st
import random

# Constants
NUM_ATTRIBUTES = 20
MAX_ATTRIBUTE_VALUE = 5  # The maximum value an attribute can have
MAX_MONSTER_STRENGTH = 9

# Define a path for the progress file
PROGRESS_FILE = "battle_progress.txt"


class Player:
    """Defines a player with health and attributes."""
    def __init__(self, health, attributes):
        self.attributes = attributes
        self.health = health

    def display_status(self):
        return f"HP: {self.health}, \n性能: {self.attributes}"

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
        return f"力: {self.strength}, \n性能: {self.attribute_order}, \n性能値: {self.attribute_value}"


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

    return '勝利' if player.is_alive() else '敗北'

def save_progress(player):
    """Save the player's progress to a file."""
    with open(PROGRESS_FILE, 'w') as file:
        file.write(str(player.health) + '\n')
        file.write(','.join(map(str, player.attributes)))

def load_progress():
    """Load the player's progress from a file."""
    try:
        with open(PROGRESS_FILE, 'r') as file:
            health_line = file.readline().strip()
            attributes_line = file.readline().strip()

            # Check if the lines are not empty and can be processed
            if not health_line or not attributes_line:
                return None

            health = int(health_line)
            attributes = tuple(map(int, attributes_line.split(',')))

            # Check if the loaded attributes match the expected number of attributes
            if len(attributes) != NUM_ATTRIBUTES:
                return None

            return Player(health, attributes)
    except (FileNotFoundError, ValueError):
        # Handle file not found or value conversion errors
        return None

def main():
    st.title("戦闘ブラウザゲーム")
    
    # Check if 'player' is already in the session state:
    if 'player' not in st.session_state:
        loaded_player = load_progress()
        if loaded_player:
            st.session_state.player = loaded_player
        else:
            st.session_state.player = Player(80, (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    player = st.session_state.player

    st.subheader("主人公 ステータス:")
    st.text(player.display_status())

    if player.is_alive():
        if st.button("敵と戦う"):
            # Create a monster
            #monster = Monster(5,1,10)
            monster = create_monster()

            st.subheader("敵ステータス:")
            st.text(monster.display_status())

            # Battle
            result = battle(player, monster)
            st.subheader("戦闘結果:")
            st.write(result)

            st.text(player.display_status())
            # Save progress after battle
            save_progress(player)
    else:
        st.subheader("Player has been defeated!")
        if st.button("Restart Game"):
            # Reset the player's status
            st.session_state.player = Player(80, (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            save_progress(st.session_state.player)

if __name__ == "__main__":
    main()

