"""
Conosci il gioco Master Mind?
Consiste nel cercare di dedurre per tentativi un codice segreto.
Ecco qualche indicazione per realizzare il gioco:
    ad ogni partita bisogna scoprire un codice segreto che consiste in una sequenza di tre cifre nel range 0-9
    ad ogni turno il giocatore fa un tentativo proponendo una sequenza di tre cifre
    se la sequenza proposta ad un turno è corrisponde al codice segreto allora il giocatore ha vinto
    altrimenti il giocatore ottiene un suggerimento che consiste di due informazioni:
    il numero di cifre presenti nel codice segreto ma collocate in una posizione errata della sequenza (aka “cifra giusta al posto sbagliato”)
    il numero di cifre presenti nel codice segreto e che sono anche nel posto giusto della sequenza (aka “cifra giusta al posto giusto”)
    in qualsiasi momento il giocatore si può arrendere e in quel caso gli viene rivelata la combinazione segreta
Ulteriori sviluppi (facoltativi)
Se hai del tempo da impiegare e vuoi arricchire il programma con altre funzionalità, considera i seguenti desiderata che potrei avere come utente:
    duello: due giocatori si sfidano, ciascuno stabilisce un codice segreto e cerca di indovinare il codice segreto dell’altro, alternandosi a turno nei tentativi
    configurazione: potrei voler regolare la difficoltà del gioco stabilendo di quante cifre consiste la sequenza del codice segreto, oppure ampliando o restringendo il numero di simboli ammessi
    top ten: ad ogni partita il gioco potrebbe darmi un punteggio per la risoluzione, basato sul tempo che ci metto a scoprire una combinazione o sul numero di tentativi che ho a disposizione. Come giocatore vorrei che il programma mi desse la top ten dei giocatori migliori.
"""

# TODO aggiungere impostazione per configurare quanti simboli sono ammessi
# TODO aggiungere impostazione per configurare modalita duello fra due player contemporaneamente
# TODO modificare menu iniziale per selezione multipla delle opzioni



import random
import os
import json
import time

file_path = "top_ten.json"
points = 0
username = ""


def guide():
    print("***** Guida *****")
    print("Il gioco consiste nel tentare di indovinare un codice segreto di 3 cifre.")
    print("Ogni volta che si prova a indovinare il codice, il gioco fornisce due indizi:")
    print(
        "1) Il numero di cifre presenti nel codice ma collocate in una posizione errata (cifra giusta al posto sbagliato)")
    print("2) Il numero di cifre presenti nel codice e che sono anche nel posto giusto (cifra giusta al posto giusto)")
    print("Buona fortuna!")
    print("******************")
    print("")


def generate_code(size):
    code = []
    for i in range(size):
        code.append(random.randint(0, 9))
    return code


def get_user_attempt(size):
    attempt = []
    input_string = input("Inserisci il codice: ")
    if (len(input_string) != size or not input_string.isnumeric()) and input_string != "q":
        print("Input non valido. Riprova.")
        return [], "error"
    elif input_string == "q":
        return [], "quit"
    for i in range(size):
        attempt.append(int(input_string[i]))
    return attempt, ""


def analyze_attempt(size, code, attempt):
    right_place = 0
    wrong_place = 0
    for i in range(size):
        if attempt[i] == code[i]:
            right_place += 1
        elif attempt[i] in code:
            wrong_place += 1
    print("Cifre giuste al posto giusto: ", right_place)
    print("Cifre giuste al posto sbagliato: ", wrong_place)


def check_attempt(size, code, attempt):
    if code == attempt:
        return True
    else:
        analyze_attempt(size, code, attempt)
        return False


def save_time():
    global time
    global username
    global file_path

    if os.path.exists(file_path):
        # Se esiste, carica i dati esistenti dal file
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                # Se il file è vuoto o non contiene dati JSON validi,
                # impostiamo existing_data come una lista vuota.
                existing_data = []
    else:
        # Se il file non esiste, crea una lista vuota come existing_data
        existing_data = []

    data = [{"username": username, "time": time}]

    # Unisce i dati esistenti con i nuovi dati
    merged_data = existing_data + data

    # Ordina i dati in base al tempo
    merged_data.sort(key=lambda x: x["time"])

    # Salva i dati nel file
    with open(file_path, 'w') as file:
        json.dump(merged_data, file)


def start_game(size):
    global time
    code = generate_code(size)
    start_time = time.time()
    while True:
        attempt, err = get_user_attempt(size)
        if err == "error":
            continue
        elif err == "quit":
            print(username + " hai deciso di arrenderti. Il codice era: ", code)
            exit()
        elif check_attempt(size, code, attempt):
            print("Hai indovinato il codice! Bravo " + username + "!")
            end_time = time.time()  # Registra l'istante di fine del gioco
            time = end_time - start_time
            print("Tempo impiegato: {:.2f} secondi".format(time))
            save_time()
            exit()
        else:
            print("Non hai indovinato il codice.")


def config_game():
    global username
    username = input("Inserisci il tuo nome: ")
    level = input("Scegli il livello di difficolta (1, 2, 3): ")
    if level == "1":
        print("Hai scelto il livello 1, dovrai indovinare un codice di 3 cifre. Per arrenderti premi q.")
        size = 3
        start_game(size)
    elif level == "2":
        print("Hai scelto il livello 2, dovrai indovinare un codice di 4 cifre. Per arrenderti premi q.")
        size = 4
        start_game(size)
    elif level == "3":
        print("Hai scelto il livello 3, dovrai indovinare un codice di 5 cifre. Per arrenderti premi q.")
        size = 5
        start_game(size)
    else:
        print("Input non valido. Riavvia il programma e riprova.")
        exit()


def print_top_ten():
    global file_path
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    if len(existing_data) == 0:
        print("Non ci sono ancora giocatori nella top ten.")
    else:
        print("***** Top Ten *****")
        for i in range(len(existing_data)):
            print(str(i + 1) + ") " + existing_data[i]["username"] + " - " + str(existing_data[i]["time"]) + " secondi")
        print("******************")


if __name__ == "__main__":
    print("***** Master Mind *****")

    print("Menu:")
    print("1) Inizia a giocare")
    print("2) Leggi le istruzioni")
    print("3) Vedi la top ten")
    print("4) Esci")
    choice = input("Cosa vuoi fare? ")
    if choice == "1":
        config_game()
    elif choice == "2":
        guide()
        understood_game = input("Sei pronto per iniziare? - Premi Y per iniziare o q per uscire: ")
        if understood_game == "Y":
            config_game()
        elif understood_game == "q":
            print("Alla prossima!")
            exit()
        else:
            print("Input non valido. Riavvia il programma e riprova.")
            exit()
    elif choice == "3":
        print_top_ten()
    elif choice == "4":
        print("Alla prossima!")
        exit()
    else:
        print("Input non valido. Riavvia il programma e riprova.")
        exit()