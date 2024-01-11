import agent
import environment
import HumanVSAi

#_____________________________________
# Modusauswahl:

MODELPATH = "model.h5" # Pfad zum Speichern oder Laden des KI-Modells (Modelle haben das Format .h5).
MODE = "PLAY"
# MODE = "TRAIN" steht für das Tranieren einer KI, dabei wird das KI-Modell in "MODELPATH" (z. 8) gespeichert.
# MODE = "PLAY": aktiviert das Spielen gegen eine KI, geladen aus MODELPATH.

#_____________________________________

# Funktion zum Spielen gegen die KI.
def play():
  global agent
  global environment
  global HumanVSAi

  # Initialisieren des "Agent" und Starten des Environment.
  agent = agent.agent(environment.Environement, modelName=MODELPATH)
  game = HumanVSAi.GameAgainstAI(agent)

  # Abfrage für wer das Spiel beginnt.
  whoStarts = int(input("Wer soll anfangen? \nKünstliche Intelligenz: 1\nDu: 2\nEingabe:"))
  if(whoStarts == 1):
    game.ai_plays()

  # Innere Funktion zum Überprüfen des Spielende.
  def checkWins():
    if(game.gameFinished()):
      if(game.checkwinForPlayer("x")):
        print("Du hast verloren!")
      elif(game.checkwinForPlayer("o")):
        print("Du hast gewonnen!")
      else:
        print("Das Spiel ist unentschieden!")
      return True
    return False

  # Spielablaufschleife.
  while True:
    print(game)
    spielzug = int(input("Dein Spielzug:"))

    if(not game.human_plays(spielzug)):
      print("Dieses Feld ist schon besetzt!")
      break

    if(checkWins()): break
    game.ai_plays()
    print("Ai_reward:", environment)
    if(checkWins()): break

# Startet das Spielen gegen KI bzw. Trainieren basierend auf dem eingestellten Modus.
if(MODE == "PLAY"):
  play()
else:
  agent = agent.agent(environment.Environement, modelName=MODELPATH)
  agent.train()