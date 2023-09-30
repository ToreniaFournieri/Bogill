
###To intall stereamlit:
#pip install streamlit
#
###To Play game:
#streamlit run bogill.py
#

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
     
# Equipment class definition
class Equipment:
    def __init__(self, name, attribute_modifiers):
        """Creates an equipment item.
        
        Args:
        - name (str): The name of the equipment.
        - attribute_modifiers (tuple): Modifiers that are added to the player's attributes.
        """
        self.name = name
        self.attribute_modifiers = attribute_modifiers

    def display(self):
        return f"{self.name} ({self.attribute_modifiers})"



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

# Sample code for Streamlit selectable list table
def monster_selection_app():
    st.title("Monster Selection")

    # Sample monsters for demonstration
    monsters = [
        Monster(5, 1, 3),
        Monster(4, 2, 2),
        Monster(3, 3, 4),
        Monster(6, 0, 1)
    ]

    # Display a table of monsters
    st.subheader("Available Monsters:")
    monster_data = [(monster.strength, monster.attribute_order, monster.attribute_value) for monster in monsters]
    st.table(monster_data)

    # Let user select a monster
    monster_names = [f"Monster {i+1}" for i in range(len(monsters))]
    selected_monster_name = st.selectbox("Select a Monster:", monster_names)

    # Take action based on the selected monster
    selected_monster = monsters[monster_names.index(selected_monster_name)]
    st.subheader("Selected Monster's Status:")
    st.text(selected_monster.display_status())

# This is just the function definition. You can call this function in the main() of the Streamlit app
# or integrate it as part of your existing app.

# Sample code to demonstrate st.multiselect with the monster game

def equipment_selection_app(player):
    st.title("Equipment Selection")

    # Define an inventory of equipment items
    inventory = [
        Equipment("Sword", (2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
        Equipment("Shield", (0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
        Equipment("Helmet", (1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
        # ... Add more equipment items as needed ...
    ]

    # Display available equipment in the inventory
    st.subheader("Available Equipment:")
    for item in inventory:
        st.text(item.display())

    # Allow the player to select up to 4 equipment items
    equipment_names = [item.name for item in inventory]
    selected_equipment_names = st.multiselect("Select up to 4 Equipment:", equipment_names)

    # Apply the equipment attribute modifiers to the player's attributes
    base_attributes = player.attributes
    for name in selected_equipment_names:
        equipment = next(item for item in inventory if item.name == name)
        base_attributes = tuple(base + modifier for base, modifier in zip(base_attributes, equipment.attribute_modifiers))

    # Update player's attributes with the modified values
    player.attributes = base_attributes

    st.subheader("Player's Updated Attributes:")
    st.text(player.display_status())

# You can call this function in the main() of the Streamlit app or integrate it as part of your existing app.
# Note: Ensure the player is initialized before calling this function.


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
        monster_selection_app()
        equipment_selection_app(player)
        
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

