from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, RadioButton, Static, RadioSet, Button, Label
import cards 
import random


computer = []
computer_pairs = []
player =[]
player_pairs = []
deck =[]

def dealCards():
    global computer
    global computer_pairs
    global player
    global player_pairs
    global deck

    deck = cards.generateDeck()
    computer.clear()
    player.clear()
    player_pairs.clear()
    computer_pairs.clear()

    for _ in range(7):
        computer.append(deck.pop())
        player.append(deck.pop())
    
    player, pairs = cards.identify_remove_pairs(player)
    player_pairs.extend(pairs)
    computer, pairs = cards.identify_remove_pairs(computer)
    computer_pairs.extend(pairs)



def playerFetchCard(pressed):
    global computer
    global computer_pairs
    global player
    global player_pairs
    global deck

    choice = pressed
    selection = player[ int(choice) ]
    value = selection[: selection.find(" ")]
    
    found_it = False
    for n, card in enumerate(computer):
        if card.startswith(value):
            found_it = n
            break

    if isinstance(found_it, bool):
        # go fish code
        print("\nGo Fish\n")
        player.append(deck.pop())
        print(f"You drew a {player[-1]}")
        if len(deck) == 0:
            endGame()
    else:
        # swap code
        print(f"Here is your card: {computer[n]}.")
        player.append(computer.pop(n))
    
    player, pairs = cards.identify_remove_pairs(player)
    player_pairs.extend(pairs)

def endGame():
    print("GAME OVER")

class AskForCard(Static):
    """The button of what card you would like to select"""

    def compose(self) -> ComposeResult:
        """The most cards you can have is 13, so we make 13 buttons"""
        with RadioSet(id="focus_me"):
            yield RadioButton("1", id="first")
            yield RadioButton("2", id="two"  )
            yield RadioButton("3", id="three")
            yield RadioButton("4", id="four" )
            yield RadioButton("5", id="five" )
            yield RadioButton("6", id="six"  )
            yield RadioButton("7", id="seven")
            yield RadioButton("8", id="eight")
            yield RadioButton("9", id="nine" )
            yield RadioButton("10", id="ten" )
            yield RadioButton("11", id="eleven")
            yield RadioButton("12", id="twelve")
            yield RadioButton("13", id="thirteen")
        with Horizontal():
                yield Label(id="index")
    

    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        playerFetchCard(event.radio_set.pressed_index)


class GoFishApp(App):
    """An App to display the current state of the go fish game"""

    BINDINGS = [("d, D", "toggle_dark", "Toggle Dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield AskForCard()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark



if __name__ == "__main__":
    app = GoFishApp()
    print(deck)
    app.run()