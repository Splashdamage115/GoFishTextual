from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Button, Label, LoadingIndicator
from textual.timer import Timer
import cards 
import random
import asyncio


computer = []
computer_pairs = []
player =[]
player_pairs = []
deck =[]
computerRequest = ""
secondaryText = False

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



def checkHandLength():
    global player, player_pairs, computer, computer_pairs, deck
    player, pairs = cards.identify_remove_pairs(player)
    player_pairs.extend(pairs)

    computer, pairs = cards.identify_remove_pairs(computer)
    computer_pairs.extend(pairs)

    if len(deck) == 0:
        endGame()
    elif len(computer) == 0:
        print("The game is over. The computer Won!")
        endGame()
    elif len(player) == 0:
        print("The game is over. The player Won!")
        endGame()



def playerFetchCard(pressed):
    global computer
    global computer_pairs
    global player
    global player_pairs
    global deck

    choice = pressed
    selection = player[ int(choice) ]
    value = selection[: selection.find(" ")]
    text = ""

    found_it = False
    for n, card in enumerate(computer):
        if card.startswith(value):
            found_it = n
            break
    
    global secondaryText 

    if isinstance(found_it, bool):
        # go fish code
        text = "\nGo Fish\n"
        player.append(deck.pop())
        secondaryText = f"You drew a {player[-1]}"
        if len(deck) == 0:
            endGame()
    else:
        # swap code
        text = f"Here is your card: {computer[n]}."
        player.append(computer.pop(n))

    checkHandLength()
    return text



def ComputerChoseCard():
    global computerRequest
    global computer
    computerRequest = random.choice(computer)



def CheckRequstCardComputer():
    global computerRequest
    global computer
    global player

    value = computerRequest[: computerRequest.find(" ")]
    # swap code
    for n, card in enumerate(player):
        if card.startswith(value):
            break
    
    computer.append(player.pop(n))

    checkHandLength()



def ComputerGoFish():
    global computer
    global deck

    computer.append(deck.pop())
    
    checkHandLength()


def endGame():
    print("GAME OVER")

class AskForCard(Static):
    """The button of what card you would like to select"""

    def redrawCards(self):
        global player
        #player = ["Ace", "King", "Queen", "Jack", "2", "3", "4" ,"5", "6", "7", "8", "9", "10"]
        for i, button in enumerate(self.buttons):
            if i < len(player):
                button.display = True
                button.label = player[i]
            else:
                button.display = False

    def compose(self) -> ComposeResult:
        global player
        """The most cards you can have is 13, so we make 13 buttons"""
        text = Label("What card will you ask for?", id="Text")
        text.styles.align = ("center","middle")
        yield text
        container = Container(id="box")
        self.buttons = []
        yield container


    def on_mount(self):
        box = self.query_one("#box")
        box.styles.layout = "grid"
        box.styles.grid_size_columns = 4
        box.styles.grid_size_rows = 5
        box.styles.align = ("center", "middle")


        for c in ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth", "eleventh", "twelth", "thirteenth"]:
                 self.buttons.append(Button(c, id=c))
                 self.buttons[-1].styles.align = ("center", "middle")
                 box.mount(self.buttons[-1])

        self.redrawCards()

    def setParent(self,parent):
        self.parentClass = parent

    def on_button_pressed(self, event):
            selected = 0
            for i,n in enumerate(["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth", "eleventh", "twelth", "thirteenth"]):
                if event.button.id == n:
                    selected = i
                    break
            
            text = playerFetchCard(selected)

            self.parentClass.moveToNext(self.parentClass.remove_cardRequest, text)
    


class ConfirmDraw(Static):
    """The Button of wether you have that card or not"""

    def ChangeText(self):
        global computerRequest
        name = computerRequest[: computerRequest.find(" ")]
        # this is used to turn a to an for aces, added all vowels just in case
        append = ""
        if name[0] in "a e i o u A E I O U".split():
            append = "n"
        self.request.update(f"Do you have a{append} {name} ?")
        self.DisplayHand()
    
    def DisplayHand(self):
        global player
        hand = ""
        skipLineCounter = 0
        for i in player:
            hand += f"{i}, "
            skipLineCounter += 1
            if skipLineCounter > 6:
                hand += "\n"
                skipLineCounter = 0
        hand = hand.removesuffix(", ")
        self.hand.update(f"Your Hand : \n {hand}")

    def compose(self) -> ComposeResult:
        """You either have the card or not"""
        self.buttons = []
        container = Container(id="button_container")
        yield container

        container = Container(id="deck_container")
        yield container
        

    def setParent(self,parent):
        self.parentClass = parent

    def on_button_pressed(self, event):
        global computerRequest
        text = ""
        if event.button.id == "Yes":
            CheckRequstCardComputer()
            text = f"Recieves {computerRequest}"
        else:
            ComputerGoFish()
            text = "FISHING!"
        self.parentClass.moveToNext(self.parentClass.remove_cardConfirm, text)

    def on_mount(self):
        deckContainer = self.query_one("#deck_container")
        deckContainer.styles.align = ("center", "middle")

        deckContainer.styles.justify_content = "center"
        deckContainer.styles.align_items = "center"

        self.hand = Label("HAND")
        deckContainer.mount(self.hand)
        
        buttonContainer = self.query_one("#button_container")
        buttonContainer.styles.align = ("center", "middle")
        buttonContainer.styles.justify_content = "center"
        buttonContainer.styles.align_items = "center"

        self.request = Label("RequestCard")
        buttonContainer.mount(self.request)

        self.buttons.append(Button(label="Yes", id="Yes", variant="success"))
        buttonContainer.mount(self.buttons[-1])

        self.buttons.append(Button(label="No", variant="error"))
        buttonContainer.mount(self.buttons[-1])

class RestartScreen(Static):
    def changeText(self):
        global player_pairs, computer_pairs
        if len(player_pairs) == len(computer_pairs):
            self.winnerText.update("Draw! You both Suck")
        elif len(player_pairs) > len(computer_pairs):
            self.winnerText.update("You Won, but barely")
        else:
            self.winnerText.update("The Computer has proven it is superior\nby Winning")

    def compose(self) -> ComposeResult:
        self.buttons = []
        container = Container(id="button_container")
        yield container

    def on_mount(self):
        buttonContainer = self.query_one("#button_container")
        buttonContainer.styles.align = ("center", "middle")
        buttonContainer.styles.justify_content = "center"
        buttonContainer.styles.align_items = "center"

        self.winnerText = Label("WinnerText")
        buttonContainer.mount(self.winnerText)

        self.request = Label("Do you Want To Restart?")
        buttonContainer.mount(self.request)

        self.buttons.append(Button(label="Yes", id="Yes", variant="success"))
        buttonContainer.mount(self.buttons[-1])

        self.buttons.append(Button(label="No", variant="error"))
        buttonContainer.mount(self.buttons[-1])

    def setParent(self,parent):
        self.parentClass = parent

    def on_button_pressed(self, event):
        if event.button.id == "Yes":
            dealCards()
            self.parentClass.remove_cardConfirm()
        else:
            exit()

class LoadScreen(Static):
    def compose(self) -> ComposeResult:
        self.container = Container(id="textContainer")
        yield self.container
        self.LoadContainer = Container(id="LoadContainer")
        yield self.LoadContainer
        self.container.display = False

    def displayText(self):
        self.loader.display = False
        self.container.display = True
    
    
    def moveOn(self):
        self.loader.display = True
        self.container.display = False
        self.callBack()

    def secondaryText(self):
        self.setString(self.secondText)

    async def startWaitForLoad(self):
        global secondaryText 
        self.secondText = secondaryText
        secondaryText = False
        await asyncio.sleep(1)
        self.displayText()
        await asyncio.sleep(1)
        if self.secondText:
            self.secondaryText()
            await asyncio.sleep(1)
        self.moveOn()

    def setParent(self, parent):
        self.parentClass = parent
    
    def callBackFunction(self, func):
        self.callBack = func
    
    def setString(self, displayString):
        self.disp.update(displayString)


    def on_mount(self):
        bound = self.query_one("#textContainer")
        bound.styles.align = ("center", "middle")
        self.disp = Label("HIDE")
        bound.mount(self.disp)
        
        self.loader = LoadingIndicator()
        self.LoadContainer.mount(self.loader)
        self.LoadContainer.styles.align = ("center", "middle")

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
        self.confirmDraw = ConfirmDraw()
        self.confirmDraw.setParent(self)
        self.confirmDraw.display = False
        yield self.confirmDraw
        self.restartScreen = RestartScreen()
        self.restartScreen.setParent(self)
        self.restartScreen.display = False
        yield self.restartScreen
        self.loadScreen = LoadScreen()
        self.loadScreen.display = False
        yield self.loadScreen


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
    
    def endScreeen(self):
        self.restartScreen.changeText()
        self.restartScreen.display = True
        self.cardRequest.display = False
        self.confirmDraw.display = False

    def moveToNext(self, funcToMoveTo, word):
        self.loadScreen.callBackFunction(funcToMoveTo)
        self.loadScreen.setString(word)
        self.loadScreen.display = True
        self.cardRequest.display = False
        self.confirmDraw.display = False
        asyncio.create_task(self.loadScreen.startWaitForLoad())


    def remove_cardRequest(self):
        self.loadScreen.display = False

        if len(deck) <= 0 or len(player) <= 0 or len(computer) <= 0:
            self.endScreeen()
            return

        ComputerChoseCard()
        self.confirmDraw.ChangeText()
        self.cardRequest.display = False
        self.confirmDraw.display = True

    def remove_cardConfirm(self):
        self.loadScreen.display = False

        if len(deck) <= 0 or len(player) <= 0 or len(computer) <= 0:
            self.endScreeen()
            return
        
        self.cardRequest.redrawCards()
        self.cardRequest.display = True
        self.confirmDraw.display = False
        self.restartScreen.display = False


if __name__ == "__main__":
    app = GoFishApp()
    dealCards()
    app.run()