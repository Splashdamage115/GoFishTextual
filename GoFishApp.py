from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Button, Label, LoadingIndicator
import cards 
import random
import asyncio


# Initialising global variables to store the games information
computer = []
computer_pairs = []
player =[]
player_pairs = []
deck =[]
computerRequest = "" # card that the computer wants, this is used for printing to the screen
secondaryText = False # this is for the  "GoFish" followed by "Card type" text displayed on screen


def dealCards():
    """
    This deals cards to the player and computer, and reshuffles a new deck for the game
    """
    # call in global variables
    global computer
    global computer_pairs
    global player
    global player_pairs
    global deck

    # create new deck and clear all arrays
    deck = cards.generateDeck()
    computer.clear()
    player.clear()
    player_pairs.clear()
    computer_pairs.clear()

    # deal out 7 cards
    for _ in range(7):
        computer.append(deck.pop())
        player.append(deck.pop())
    
    #this clears the hands of pairs and adds them to the correct pile
    checkHandLength()



def checkHandLength():
    """
    Moves pairs from hands to pair decks
    """
    global player, player_pairs, computer, computer_pairs, deck
    player, pairs = cards.identify_remove_pairs(player)
    player_pairs.extend(pairs)

    computer, pairs = cards.identify_remove_pairs(computer)
    computer_pairs.extend(pairs)



def playerFetchCard(pressed):
    """
    upon request from player, this does the go fish or swap card logic
    """
    global computer
    global computer_pairs
    global player
    global player_pairs
    global deck
    global secondaryText 

    # figure out the players choice of card, and remove the suit
    choice = pressed
    selection = player[ int(choice) ]
    value = selection[: selection.find(" ")]
    text = ""

    # check if the computer has it
    found_it = False
    for n, card in enumerate(computer):
        if card.startswith(value):
            found_it = n
            break

    if isinstance(found_it, bool):
        # go fish code
        text = "Go Fish\n"
        player.append(deck.pop())
        secondaryText = f"You drew a {player[-1]}"
    else:
        # swap code
        text = f"Here is your card: {computer[n]}."
        player.append(computer.pop(n))

    checkHandLength()
    return text



def ComputerChoseCard():
    """
    computer randomly selects a card to request
    """
    global computerRequest
    global computer
    computerRequest = random.choice(computer)



def CheckRequstCardComputer():
    """
    remove the selected card from the player hand and place it into the computers hand
    """
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
    """
    make the computer draw a card from the deck
    """
    global computer
    global deck

    computer.append(deck.pop())
    
    checkHandLength()

def checkPlayerHasCard():
    """
    check if the player has the card requested
    """
    value = computerRequest[: computerRequest.find(" ")]
    # swap code
    for n, card in enumerate(player):
        if card.startswith(value):
            return True
    return False

class AskForCard(Static):
    """The button of what card you would like to select"""

    def redrawCards(self):
        """
        reset the texts of all of the cards
        """
        global player
        #player = ["Ace", "King", "Queen", "Jack", "2", "3", "4" ,"5", "6", "7", "8", "9", "10"]
        for i, button in enumerate(self.buttons):
            if i < len(player):
                button.display = True
                button.label = player[i]
            else:
                button.display = False

    def compose(self) -> ComposeResult:
        """
        set up the container and text on the 
        """
        global player
        text = Label("What card will you ask for?", id="Text")
        text.styles.align = ("center","middle")
        yield text
        container = Container(id="box")
        self.buttons = []
        yield container


    def on_mount(self):
        """
        set up the 13 buttons and place them into the aligned container box
        """
        box = self.query_one("#box")
        box.styles.layout = "grid"
        box.styles.grid_size_columns = 4
        box.styles.grid_size_rows = 5
        box.styles.align = ("center", "middle")

        # assign ids based off the button
        for c in ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth", "eleventh", "twelth", "thirteenth"]:
                 self.buttons.append(Button(c, id=c))
                 self.buttons[-1].styles.align = ("center", "middle")
                 box.mount(self.buttons[-1])

        self.redrawCards()

    def setParent(self,parent):
        "set the parent class of this object"
        self.parentClass = parent

    def on_button_pressed(self, event):
        """
        check which button was pressed and move to the load and display text screen
        """
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
        """
        change the requested card text on the game screen
        """
        global computerRequest
        name = computerRequest[: computerRequest.find(" ")]
        # this is used to turn a to an for aces, added all vowels just in case
        append = ""
        if name[0] in "a e i o u A E I O U".split():
            append = "n"
        self.request.update(f"Do you have a{append} {name} ?")
        self.DisplayHand()
    
    def DisplayHand(self):
        """
        show the players hand at the bottom of the screen
        """
        global player
        hand = ""
        skipLineCounter = 0
        for i in player:
            hand += f"{i}, "
            skipLineCounter += 1
            # every 6 items we move to the next line
            if skipLineCounter >= 6:
                hand += "\n"
                skipLineCounter = 0
        # remove the new line, getting ready for the  ", "
        hand = hand.removesuffix("\n")
        # remove the last ", " so that it is shown correctly
        hand = hand.removesuffix(", ")
        self.hand.update(f"Your Hand : \n {hand}")

    def compose(self) -> ComposeResult:
        """initialise the 2 containers for the "yes/no" and for the hand"""
        self.buttons = []
        container = Container(id="button_container")
        yield container

        container = Container(id="deck_container")
        yield container
        

    def setParent(self,parent):
        "Set the parent class of the object"
        self.parentClass = parent

    def on_button_pressed(self, event):
        """
        Check which button has been pressed by the player
        """
        global computerRequest
        text = ""
        # if pressed yes
        if event.button.id == "Yes":
            if checkPlayerHasCard():
                CheckRequstCardComputer()
                text = f"Recieves {computerRequest}"
            else:
                self.request.update(f"Liar!")
                return
        # if didnt press yes then it was "no"
        else:
            if checkPlayerHasCard():
                self.request.update(f"Liar!")
                return
            else:
                ComputerGoFish()
                text = "FISHING!"
        self.parentClass.moveToNext(self.parentClass.remove_cardConfirm, text)

    def on_mount(self):
        """
        after initialising the widgets mount them to the containers
        """
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
    """
    Restart the game screen
    """
    def changeText(self):
        # set the text displayed on the end screen, winner, loser or draw
        global player_pairs, computer_pairs, deck, player, computer
        if len(deck) <= 0:
            self.InfoText.update("The Deck is empty!")
        elif len(player) <= 0:
            self.InfoText.update("You Emptied your hand!")
        elif len(computer) <= 0:
            self.InfoText.update("the computer has an empty Hand!")
        else:
            self.InfoText.update("")
        
        if len(player_pairs) == len(computer_pairs):
            self.winnerText.update("Draw! You both Suck")
        elif len(player_pairs) > len(computer_pairs):
            self.winnerText.update(f"You Won! with {len(player_pairs)/2} pairs.")
        else:
            self.winnerText.update(f"The Computer has proven it is superior\nby Winning\nThe computer had {len(computer_pairs)/2} pairs")

    def compose(self) -> ComposeResult:
        # initialise the button container
        self.buttons = []
        container = Container(id="button_container")
        yield container

    def on_mount(self):
        # mount the buttons to the container after it is initialised
        buttonContainer = self.query_one("#button_container")
        buttonContainer.styles.align = ("center", "middle")
        buttonContainer.styles.justify_content = "center"
        buttonContainer.styles.align_items = "center"

        self.InfoText = Label("Info")
        buttonContainer.mount(self.InfoText)

        self.winnerText = Label("WinnerText")
        buttonContainer.mount(self.winnerText)

        self.request = Label("Do you Want To Restart?")
        buttonContainer.mount(self.request)

        self.buttons.append(Button(label="Yes", id="Yes", variant="success"))
        buttonContainer.mount(self.buttons[-1])

        self.buttons.append(Button(label="No", variant="error"))
        buttonContainer.mount(self.buttons[-1])

    def setParent(self,parent):
        # set the parent class
        self.parentClass = parent

    def on_button_pressed(self, event):
        # restart the game or close the game
        if event.button.id == "Yes":
            dealCards()
            self.parentClass.remove_cardConfirm()
        else:
            exit()

class LoadScreen(Static):
    """
    Loading screen shown between picks, this is used to provide a more realistic look to the game
    """
    def compose(self) -> ComposeResult:
        # initialise the text box and the load icon
        self.container = Container(id="textContainer")
        yield self.container
        self.LoadContainer = Container(id="LoadContainer")
        yield self.LoadContainer
        self.container.display = False

    def displayText(self):
        # show the normal text, hide loader
        self.loader.display = False
        self.container.display = True
    
    
    def moveOn(self):
        # set up for next call and move to the callBack
        self.loader.display = True
        self.container.display = False
        self.callBack()

    def secondaryText(self):
        # change the displayed text
        self.setString(self.secondText)

    async def startWaitForLoad(self):
        # async function to do the countdown for the screen reset to next
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
        # set parent class
        self.parentClass = parent
    
    def callBackFunction(self, func):
        # set the function we will move back to
        self.callBack = func
    
    def setString(self, displayString):
        # set the string which will be displayed on screen
        self.disp.update(displayString)


    def on_mount(self):
        # put the label and loader into containers for centering
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
        """make all the scrreens for the game"""
        self.text = Header()
        yield self.text
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
        self.updateCardCounts()

    def action_toggle_dark(self) -> None:
        #change to dark mode
        self.dark = not self.dark
    
    def updateCardCounts(self):
        global deck, computer
        self.title = "Card Amounts"
        self.sub_title = f"Deck: {len(deck)} - Computer: {len(computer)}"

    def endScreeen(self):
        # move to the restart screen, hide other screens
        self.restartScreen.changeText()
        self.updateCardCounts()
        self.restartScreen.display = True
        self.cardRequest.display = False
        self.confirmDraw.display = False

    def moveToNext(self, funcToMoveTo, word):
        """ 
        move to the next screen, this calls the load screen and assigns the passed in function
        that we will move to after the loading is complete, and the word to be displayed to the screen
        """
        self.loadScreen.callBackFunction(funcToMoveTo)
        self.loadScreen.setString(word)
        self.loadScreen.display = True
        self.cardRequest.display = False
        self.confirmDraw.display = False
        asyncio.create_task(self.loadScreen.startWaitForLoad()) # start the asynchryonous task


    def remove_cardRequest(self):
        """move out of the card request screen"""
        self.loadScreen.display = False # hide the load screen

        # check if the game is over, and move to the end screen if it is
        if len(deck) <= 0 or len(player) <= 0 or len(computer) <= 0:
            self.endScreeen()
            return
        self.updateCardCounts()

        # make the computer chose a card (for the confirm screen)
        ComputerChoseCard()
        # set up the screenm, and show it
        self.confirmDraw.ChangeText()
        self.cardRequest.display = False
        self.confirmDraw.display = True

    def remove_cardConfirm(self):
        """close the card confirm screen and move to the card request screen for the player"""
        self.loadScreen.display = False # hide the load screen

        # check if the game is over, and move to the end screen if it is
        if len(deck) <= 0 or len(player) <= 0 or len(computer) <= 0:
            self.endScreeen()
            return
        
        self.updateCardCounts()
        
        # set up the screenm, and show it
        self.cardRequest.redrawCards()
        self.cardRequest.display = True
        self.confirmDraw.display = False
        self.restartScreen.display = False

# run the main game
if __name__ == "__main__":
    app = GoFishApp()
    dealCards() # deal out cards before the game starts
    app.run()
