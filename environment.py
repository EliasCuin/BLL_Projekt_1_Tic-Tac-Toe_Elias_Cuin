import random
from datetime import datetime

# Überprüft, ob ein bestimmter Spieler 'x' oder 'o' gewonnen hat.
def checkwinForPlayer(field, player):

  # Vertikale Gewinnbedingung.
  field = [field[0:3], field[3:6], field[6:9]]
  for i in range(3):
    middle = field[i][1]
    if (not middle == "") and field[i][0] == middle and middle == field[i][2]:
      return middle==player

  # Horizontale Gewinnbedingung.
  for i in range(3):
    middle = field[1][i]
    if (not middle == "") and field[0][i] == middle and middle == field[2][i]:
      return field[0][i]==player
  middle = field[1][1]

  # Diagonale Gewinnbedingung.
  if not middle == "":
    if field[0][0] == middle and middle == field[2][2]:
      return middle==player
    if field[2][0] == middle and middle == field[0][2]:
      return middle==player

  return False

# Prüft, ob alle Felder des Spielfelds belegt sind.
def gameOver(inputMatrix):
  return len(list(filter(lambda x: x=="" , inputMatrix))) == 0

# Funktion getScoreForSet:
# "set" ist die ID auf der Matrix, von wo ein X bzw ein O gesetzt wird
# "tiefe" damit den weiteren Wins weniger Wichtigkeit zugeführt wird.

# Protagonist = Gegner des Minimax Algorithmuses.
# Bei protagonist gleich "x" ist in minimax der Spieler "o".
# Bei protagonist gleich "o" ist in minimax der Spieler "x".

# Berechnet den Minimax-Wert eines Feldes 'set' auf dem Spielfeld, basierend auf möglichen zukünftigen Spielzuständen.
# Für das Reward-System des "Agent" später von Wichtigkeit.
def getScoreForSet(inputMatrix, set,tiefe=0, playersTurn=False, protagonist = "x"):
  if(tiefe == 0):
    if(protagonist == "o"):
        inputMatrix = ["x" if cell == "o" else "o" if cell == "x" else cell for cell in inputMatrix]
        protagonist = "x"

  inputMatrix = inputMatrix.copy()
  if(inputMatrix == ["" for _ in range(9)]):
    return 0

  matrix = inputMatrix.copy()
  matrix[set] = protagonist if not playersTurn else "o"
  scores = []

  tiefe +=1

  if(checkwinForPlayer(matrix, "x")):

      return 10 - tiefe
  elif (checkwinForPlayer(matrix, "o")):
      return tiefe - 10

  if(gameOver(matrix)):
    return 0

  # Rekursiver Aufruf des getScoreForSet
  for i in range(len(matrix)):
    if(matrix[i] == ""):
      scores.append(getScoreForSet(matrix, i, tiefe=tiefe, playersTurn=not playersTurn))

  if(playersTurn):
    return max(scores)
  else:
    return min(scores)

# Bewertet die MiniMax Value Qualität eines Spielzugs (actionIndex (0-8)) im Vergleich zum besten möglichen Zug in einem gegebenen Tic-Tac-Toe-Spielstand (inputMatrix).
# Anderes gesagt: Wandelt den MiniMax Score eines Moves in einem Feld in einem aussagekräftigen Reward um.
def getRewardForMove(field,actionIndex,player="x" ):
  reward = 0
  scores = []
  for i in range(len(field)):
      scores.append(getScoreForSet(field, i, protagonist=player))

  maxScore = max(list(filter(lambda x: x != "" and x != "x" and x != "o",scores)))
  minScore = min(list(filter(lambda x: x != "" and x != "x" and x != "o",scores)))

  choosenSet = scores[actionIndex]

  if(len(list(set(scores))) == 1):
    return 0.5

  middle = (maxScore+minScore)/2

  # Berechnung des Rewards des Zugs, indem der Mittelwert zwischen dem maxScore und dem minScore verwendet wird.
  if(choosenSet > middle):
    reward = abs(choosenSet - middle) / abs(maxScore - middle)
  elif(choosenSet == middle):
    reward = 0
  elif(choosenSet < middle):
    reward = -abs(choosenSet - middle) / abs(minScore - middle)

  return reward

class Environement:
  def __init__(self, gameReset = True, randomPreparedField=True):
    self.currentField = ["","","","","","","","",""]
    # Konvertierungstabelle von TicTacToe Zeichen in Werten
    self.statesBins = {
      "": 0,
      "x": 1,
      "o": -1
    }

    # Legt fest, ob zusätzliche Schwachstelle in Spiel vorliegen soll. (siehe Seite 16 BLL: "Zugefügte Schwächen gegenüber dem Trainingsgegner").
    self.randomPreparedField = randomPreparedField

    # Bestimmt die Wahrscheinlichkeit, mit der hierbei immer ein zufälliger Zug anstelle des besten Minimax-Zugs gewählt wird.
    self.epsilonMinimax = 0.3

    # Belohnungen:

    # Sieg der KI:
    self.gewinn = 15

    # Niederlage der KI:
    self.verloren = -15

    # Belohnung für die Ausführung eines ungültigen Zuges:
    self.invaliderZug = -50

    # Belohnung für ein unentschiedenes Spiel:
    self.unentschieden = 8

    # Im Falle dass das Spielfeld beim Initialisieren nochmal zurückgesetzt werden soll.
    if(gameReset):
      self.resetGame()

  # Gibt an, ob Spiel beendet ist.
  def gameFinished(self):
    return gameOver(self.currentField) or checkwinForPlayer(self.currentField, "o") or checkwinForPlayer(self.currentField, "x")

  # Gibt das aktuelle Spielfeld in einer KI bzw. Menschen lesbaren Form zurück (humanReadable).
  def getState(self, humanReadable = False):
    if(humanReadable):
      return self.currentField
    state = []
    for cur in self.currentField:
      state.append(self.statesBins[cur])
    return state

  # Zurücksetzen des Spiels
  def resetGame(self):
    # Wenn Funktion: "randomPreparedField" aus ist, dann wird das Spielfeld resettet
    self.currentField = ["","","","","","","","",""]
    if(not self.randomPreparedField):
      return

    # Wenn nicht, wird durch einen Algorithmus ein angefangenes Spielfeld generiert:
    players = ["o", "x"]
    currentPlayer = random.randint(0,1)

    # Hier wird berechnet, wie viele Spielzüge auf dem neuen Spielfeld gespielt werden sollen.
    # Dabei wird zufällig ausgerechnet, ob die KI oder der KI Gegner beginnen soll.
    if(currentPlayer == 1):
      # Am Ende muss immer die KI gespielt haben
      alreadyPlayedMoves = [0,2,4][random.randint(0,2)]
    # Wenn MiniMax-Algorithmus beginnt
    elif(currentPlayer == 0):
      alreadyPlayedMoves = [1,3][random.randint(0,1)]

    # Gibt einen zufälligen Index zurück, von einem leeren Feld auf dem Spielfeld.
    def randomIndexNotOnField():
      while True:
        r = random.randint(0,8)
        if(self.currentField[r] == ""):
          return r

    # Hier werden Spielzüge generiert, um das Spielfeld um "alreadyPlayedMoves"-Züge zufällig zu generieren.
    for _ in range(alreadyPlayedMoves):
        r = randomIndexNotOnField()
        # Spieler aktualisieren
        self.currentField[r] = players[currentPlayer]
        # Auf nächsten Spieler wechseln
        currentPlayer = 0 if currentPlayer == 1 else 1

  # Teilt mit, wie gut ein bestimmter Schritt von KI war -> gibt anschließend die Belohnung zurück.
  # Der Input ist ein Array mit 9 Nullen, außer einer 1, dessen Index angibt, wo auf dem Spielfeld gespielt werden soll.
  def step(self,action):

    # Was passiert hier?
    # - 1. Wenn die action ungültig ist, wird die dafür bestimmte Belohnung zurückgegeben.
    # - 2. Ein Reward bezüglich der Richtigkeit des Zuges wird in variable "reward" gespeichert.
    # - 3. Die Action wird auf dem Spielfeld aktualisiert.
    # - 4. Wenn man verloren/gewonnen hat: Zurückgeben von entsprechenden Reward.
    # - 5. Wenn das Spielfeld voll ist, Belohnung: X.
    # - 6. MiniMax oder ein zufälliger Zug wird für den nächsten Zug gespielt
    # - 7. Wenn MiniMax gewonnen hat, +X Punkte.
    # - 8. Wenn das Spielfeld voll ist, Re: 0
    # - 9. "reward" wird zurückgegeben.

    actionCase = action.index(1)

    #region - Schritt 1.
    if(self.currentField[actionCase] != ""):
      return self.invaliderZug
    #endregion

    #region - Schritt 2.
    reward = getRewardForMove(self.currentField.copy(), actionCase ,player="x") * 0
    #endregion

    #region - Schritt 3.
    self.currentField[actionCase] = "x"
    #endregion

    #region -  Schritt 4.
    if(checkwinForPlayer(self.currentField, "x")):
      return self.gewinn
    if(checkwinForPlayer(self.currentField, "o")):
        return self.verloren
    #endregion

    #region -  Schritt 5.
    if(len(list(filter(lambda x: x=="x" or x == "o", self.currentField))) == 9):
      return self.unentschieden
    #endregion

    #region -  Schritt 6.
    scores = []
    for i in range(len(self.currentField)):
      if(self.currentField[i] != ""):
        scores.append("-")
      else:
        scores.append(getScoreForSet(self.currentField.copy(), i, protagonist="o"))


    # Entfernen von allen "-" in scoreNotSorted
    scoresNotSorted = list(filter(lambda x: x != "-",scores))

    # Returnt ein Spielfeldindex, der den besten Move für den KI-Gegner repräsentiert. Epsilon gibt dabei an, wie zufällig dieser Move dabei sein soll.
    def getMaxNumberFromMinimax_BecauseOfRandom(epsilon):
      scoresNotSortedEditor = list(set(scoresNotSorted.copy()))
      if(random.random() < epsilon):
        maxNumber = max(scoresNotSortedEditor)
        # Entferne überall diese Max Number, damit später, beim Generieren der neuen Zufallszahl, nicht dieselbe rauskommt.
        scoresNotSortedEditor.pop(scoresNotSortedEditor.index(maxNumber))
        # Falls alle Zahlen gleich waren:
        if(len(scoresNotSortedEditor) == 0):
          return maxNumber
        return scoresNotSortedEditor[random.randint(0, len(scoresNotSortedEditor)-1)]
      else:
        return max(scoresNotSortedEditor)

    self.currentField[scores.index(getMaxNumberFromMinimax_BecauseOfRandom(self.epsilonMinimax))] = "o"

    #endregion

    #region - Schritt 7.
    if(checkwinForPlayer(self.currentField, "x")):
      return self.gewinn
    if(checkwinForPlayer(self.currentField, "o")):
      return self.verloren
    #endregion

    #region - Schritt 8.
    if(len(list(filter(lambda x: x=="x" or x == "o", self.currentField))) == 9):
      return self.unentschieden
    #endregion

    #region - Schritt 9.
    return reward
      #endregion

  # Liefert ob das aktuelle Spielfeld leer ist.
  def isFieldEmpty(self):
    return self.currentField == ["","","","","","","","",""]
