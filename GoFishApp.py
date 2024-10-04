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
    CSS = """
    RadioButton {
        cursor: none;
    }
    """

    def redrawCards(self):
        global player
        for i, button in enumerate(self.buttons):
            if i < len(player):
                button.display = True
                button.label = player[i]
            else:
                button.display = False

    def compose(self) -> ComposeResult:
        global player
        """The most cards you can have is 13, so we make 13 buttons"""
        self.radioSet = RadioSet(id="focus_me")
        self.buttons = []
        with self.radioSet:
            for c in ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth", "eleventh", "twelth", "thirteenth"]:
                 self.buttons.append(Button(c, id=c))
                 yield self.buttons[-1]
        with Horizontal():
                yield Label(id="index")
        self.redrawCards()

    def setParent(self,parent):
        self.parentClass = parent

    def on_button_pressed(self, event):
            selected = 0
            for i,n in enumerate(["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth", "eleventh", "twelth", "thirteenth"]):
                if event.button.id == n:
                    selected = i
                    break

            playerFetchCard(selected)
            self.parentClass.remove_cardRequest()
            self.radioSet._selected = None
    


class ConfirmDraw(Static):
    """The Button of wether you have that card or not"""

    def compose(self) -> ComposeResult:
        """You either have the card or not"""
        

    def setParent(self,parent):
        self.parentClass = parent

    def on_button_pressed(self, event):
            selected = 0
            for i,n in enumerate(["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth", "eleventh", "twelth", "thirteenth"]):
                if event.button.id == n:
                    selected = i
                    break

            playerFetchCard(selected)
            self.parentClass.remove_cardRequest()
            self.radioSet._selected = None



class GoFishApp(App):
    """An App to display the current state of the go fish game"""

    BINDINGS = [("d, D", "toggle_dark", "Toggle Dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        self.cardRequest = AskForCard()
        self.cardRequest.setParent(self)
        yield self.cardRequest

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def remove_cardRequest(self):
        self.cardRequest.redrawCards()


if __name__ == "__main__":
    app = GoFishApp()
    dealCards()
    app.run()