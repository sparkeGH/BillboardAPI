#some imports
import random
import requests

#function for randomly selecting songs; returns diff random ints 0-99 in nums list
def getIndices(diff):
    nums = []
    nums.append(random.randint(0, 99))
    trial = random.randint(0, 99)
    for i in range(diff-1):
        while (nums.count(trial) > 0):
            trial = random.randint(0, 99)
        nums.append(trial)
    return nums

#get request for song dictionary from backend
r = requests.get("http://127.0.0.1:5000/songs")
songList = r.json()

#establish some score-tracking variables
rounds = 0
points = 0
difficulty = 0

#print statements for beginning of game
print("""
                Welcome to Billboard Shuffle!

  The rules are simple: select your difficulty, then rank the
 songs shown in each round based on where you think they fall
in the Billboard Hot 100. Score 1 point for each correct guess!     \n\n""")

print("""
    Select your difficulty: enter a number between 3 and 5.
         You will receive this many songs each round.                   """)

#accept input until valid difficulty provided
difficulty = input()
while (difficulty != "3" and difficulty != "4" and difficulty != "5"):
    print("Invalid difficulty. Please type '3','4', or '5' and press enter.")
    difficulty = input()
difficulty = int(difficulty)

#Print for in-round instructions
print(f"""
\nEnter your guesses for the order of the songs below as
{difficulty} distinct numbers, 1 through {difficulty}.
Ex: if you think the third song appears first, type 3 first, then hit
enter. (Or, enter 'q' to quit and view your stats.)                     """)

#enter game loop
inStr = "default"
while (inStr != "q"):

    #print the randomly selected songs
    print("\n")
    indices = getIndices(difficulty)
    for i in range(difficulty):
        print( str(i+1) + ".) " + songList[indices[i]]["title"] + " by " + songList[indices[i]]["artist"])

    #accept user inputs until 'q' received or all rankings provided
    userGuess = []
    ii = 0
    inStr = "default"
    while (inStr != "q" and ii < difficulty):
        inStr = input()
        while(inStr != 'q' and (len(inStr) > 1 or inStr < "1" or inStr > str(difficulty))):
            print("Invalid input. Please type a number or 'q'.")
            inStr = input()
        if (inStr != "q"):
            ind = int(inStr)
            userGuess.append(indices[ind-1])
            ii += 1

    #if not quitting, sort the selected songs and give a point for correct rankings
    if (inStr != "q"):
        rounds += 1
        roundScore = 0
        indices.sort()
        for i in range(difficulty):
            if (userGuess[i] == indices[i]):
                roundScore += 1
                points += 1
        print(str(roundScore) + " points scored this round!\n")
        #print the correct order of the songs
        print("Correct rankings:")
        for i in range(difficulty):
            print( str(i+1) + ".) " + songList[indices[i]]["title"] + " by " + songList[indices[i]]["artist"])

#if the game was played at least once, yield statistics
if (rounds>0):
    average = points/rounds
    accuracy = (points/(rounds*difficulty))*100
    print(f"You played {rounds} rounds and scored {points} points.")
    print(f"""With a difficulty of {difficulty}, that means you averaged
    {average} points per round, with {accuracy}% accuracy.""")
#ending message
print("Play again sometime!")
