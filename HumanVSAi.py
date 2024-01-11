import numpy as np

# Diese Klasse ermöglicht es, die KI nach dem Training im Terminal zu testen.
# Es handelt sich um eine Art zweites Environment, in dem die KI gegen einen Menschen spielt und nicht gegen den MiniMax-Algorithmus.
# So handelt es sich um eine Klasse mit Hilfsfunktionen, die das Spielen gegen KI erleichtern.

class GameAgainstAI():
  def __init__(self,agent):
    # Initialisierung der KI (Agent) und des Spielfelds.
    self.agent = agent
    self.currentField = ["" for _ in range(9)]

    # Konvertierungstabelle für Spielfeldelemente: Mensch='o', KI='x', Leeres Feld=''."
    self.statesBins = {
      "": 0,
      "x": 1,
      "o": -1
    }

  # Setzt das Spielfeld zurück.
  def resetGame(self):
    self.currentField = ["" for _ in range(9)]

  # Ermöglicht dem menschlichen Spieler einen Zug zu machen.
  # step_number: Zahl zwischen 0 und 8, die beschreibt, wo der menschliche Spieler einen Zug absolvieren soll.
  # Gibt zurück, ob der eingegebene Zug gültig ist.
  def human_plays(self,step_number):
    if(step_number < 0 or step_number > 8):
      raise Exception("Die eingegebene Nummer mus zwischen 0 und 8 sein, ist aber", step_number, ".")

    if(self.currentField[step_number] != ""):
      return False # Zug ungültig, wenn Feld bereits belegt.

    self.currentField[step_number] = "o"
    return True

   # Konvertiert Spielfeld in ein Format, das die KI verarbeiten kann.
  def covertStateToAIFormat(self):
    state = []
    for cur in self.currentField:
      state.append(self.statesBins[cur])
    return state

  # Lässt die KI einen Zug machen.
  def ai_plays(self):
    converted_state = self.covertStateToAIFormat()
    prediction = self.agent.vanilla_prediction(converted_state)

    minValue = np.min(prediction)
    step_number = np.argmax(prediction)
    print(step_number)

    # Prüft ob der Zug gültig ist, und wählt gegebenfalls einen anderen.
    while(self.currentField[step_number] != ""):
      prediction[step_number] = minValue - 1
      step_number = np.argmax(prediction)

    # Setzt das Zeichen der KI auf dem Spielfeld.
    self.currentField[step_number] = "x"

  # Überprüft ob ein Spieler das Spiel gewonnen hat.
  def checkwinForPlayer(self,player):
    # Vertikale Gewinnbedingung.
    field = self.currentField
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

    # Diagonale Gewinnbedingung.
    middle = field[1][1]
    if not middle == "":
      if field[0][0] == middle and middle == field[2][2]:
        return middle==player
      if field[2][0] == middle and middle == field[0][2]:
        return middle==player

    return False

  # Überprüft, ob das Spiel beendet ist.
  def gameFinished(self):
    return self.isGameFull() or self.checkwinForPlayer("o") or self.checkwinForPlayer("x")

  # Prüft, ob das Spielfeld voll ist.
  def isGameFull(self):
    return len(list(filter(lambda x: x=="" , self.currentField))) == 0

  # Gibt das Spielfeld aus, im Falle, dass eine Instanz dieser Klasse geprintet wird.
  def __repr__(self):
      return str(self.currentField[0:3]) + "\n" + str(self.currentField[3:6]) + "\n" + str(self.currentField[6:9])
