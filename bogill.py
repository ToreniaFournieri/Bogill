
###To intall stereamlit:
#pip install streamlit
#
###To Play game:
#streamlit run bogill.py
#

import streamlit as st
import random
import pandas as pd
import time

# Constants
NUM_ATTRIBUTES = 6
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

    enemy_level = st.slider("Select Enemy Level:", 1, 100)

    # Adjust monsters based on the selected enemy level
    # (This is a basic scaling mechanism; you can adjust this based on your desired difficulty curve)
    def adjust_monster_attributes(monster):
        adjusted_strength = monster.strength + (enemy_level // 7)
        adjusted_attribute_value = monster.attribute_value + (enemy_level // 5)
        return Monster(adjusted_strength, monster.attribute_order, adjusted_attribute_value)


    # Sample base monsters for demonstration
    base_monsters = [
        Monster(5, 1, 3),
        Monster(4, 2, 2),
        Monster(3, 3, 4),
        Monster(6, 0, 1)
    ]

    # Adjust monsters' attributes based on enemy level
    adjusted_monsters = [adjust_monster_attributes(monster) for monster in base_monsters]

    # Display a table of adjusted monsters
    st.subheader("Available Monsters:")
    monster_data = {
        'Monster Number': [f"Monster {i+1}" for i in range(len(adjusted_monsters))],
        'Strength': [monster.strength for monster in adjusted_monsters],
        'Attribute Order': [monster.attribute_order for monster in adjusted_monsters],
        'Attribute Value': [monster.attribute_value for monster in adjusted_monsters]
    }
    df_monsters = pd.DataFrame(monster_data)
    st.table(df_monsters)

    # Let user select a monster
    monster_names = [f"Monster {i+1}" for i in range(len(adjusted_monsters))]
    selected_monster_name = st.selectbox("Select a Monster:", monster_names)

    # Take action based on the selected monster
    selected_monster = adjusted_monsters[monster_names.index(selected_monster_name)]
    st.subheader("Selected Monster's Status:")
    st.text(selected_monster.display_status())


# This is just the function definition. You can call this function in the main() of the Streamlit app
# or integrate it as part of your existing app.

# Sample code to demonstrate st.multiselect with the monster game

def equipment_selection_app(player):
    st.title("Equipment Selection")
    # Save the player's current attributes before any equipment effects
    initial_attributes = player.attributes
    
    option = st.radio("Choose an option", ["Option A", "Option B", "Option C"])
    user_input = st.text_input("Enter your name", "Type here...")
    number = st.number_input("Enter a number", min_value=0, max_value=100, step=1)
    #uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
    if st.checkbox("Show/Hide"):
        st.text("Showing or hiding widget...")
    with st.expander("ステータス詳細"):
        st.text("各種詳細ステータスがこちらに\n 改行")
        st.write("write を使った2行目の内容")
        st.write("3行め")

    if st.button("Show Notification"):
        st.toast("This is a notification!")

    # Define an inventory of equipment items
    inventory = [
        Equipment("ショートソード", (1, 0, 0, 0, 0, 0)),
        Equipment("臭いショートシールド", (0, 0, 1, 1, 0, 0)),
        Equipment("臭いアーマー", (1, 0, 1, 1, 0, 0)),
        Equipment("臭いナイトシールド", (0, 0, 1, 1, 1, 0)),
        Equipment("臭いガンレット", (0, 0, 1, 0, 0, 0)),
        Equipment("臭いガンレット", (0, 0, 1, 0, 0, 0)),
        Equipment("臭いガンレット", (0, 0, 1, 0, 0, 0)),
        Equipment("臭い日本刀", (1, 0, 0, 0, 0, 0)),
        Equipment("臭い木刀", (0, 0, 0, 0, 0, 0)),
        Equipment("臭い長刀物干竿", (2, 0, 0, 0, 0, 0)),
        Equipment("臭い名刀コテツ", (2, 0, 0, 0, 0, 0)),
        # ... Add more equipment items as needed ...
    ]
    # Store the player's base attributes in the session state if not already done
    if 'base_attributes' not in st.session_state:
        st.session_state.base_attributes = player.attributes

    # Display the multiselect widget and limit to 4 selections
    equipment_names = [item.name for item in inventory]
    selected_equipment_names = st.multiselect(f"Select up to 4 Equipment:", equipment_names, max_selections=4)

    # Start with player's base attributes and apply the equipment attribute modifiers
    updated_attributes = list(st.session_state.base_attributes)
    for name in selected_equipment_names:
        equipment = next(item for item in inventory if item.name == name)
        updated_attributes = [base + modifier for base, modifier in zip(updated_attributes, equipment.attribute_modifiers)]

    # Update player's attributes with the modified values
    player.attributes = tuple(updated_attributes)

    # Display player's current attributes after the selection
    st.subheader("Player's Current Attributes:")
    st.text(player.display_status())

    # After applying the equipment effects, compare the new attributes
    changes = [(new - old) for old, new in zip(initial_attributes, player.attributes)]
    if any(change != 0 for change in changes):
        st.toast(f"Attributes changed: {initial_attributes} -> {player.attributes}")


def main():
    st.title("戦闘ブラウザゲーム")
    
    # Check if 'player' is already in the session state:
    if 'player' not in st.session_state:
        loaded_player = load_progress()
        if loaded_player:
            st.session_state.player = loaded_player
        else:
            st.session_state.player = Player(80, (0, 0, 0, 0, 0, 0))

    player = st.session_state.player

    st.subheader("主人公 ステータス:")
    equipment_selection_app(player)

    if player.is_alive():
        monster_selection_app()
        
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
            st.session_state.player = Player(80, (0, 0, 0, 0, 0, 0))
            save_progress(st.session_state.player)

if __name__ == "__main__":
    main()

