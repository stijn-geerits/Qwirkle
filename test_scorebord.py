import scorebord

spelers = ["Stijn", "Laël", "Stan"]
bord = scorebord.Scorebord(spelers)
print("Begin score: "+str(bord.get_score()))

# ronde1
bord.change_score("Stijn", 100)
bord.change_score("Laël", 200)
bord.change_score("Stan", 150)
print("Score na ronde 1: "+str(bord.get_score()))

# ronde2
bord.change_score("Stijn", 135)
bord.change_score("Laël", 115)
bord.change_score("Stan", 125)
print("Score na ronde 2: "+str(bord.get_score()))

# ronde3
bord.change_score("Stijn", 145)
bord.change_score("Laël", 105)
bord.change_score("Stan", 225)
print("Score na ronde 3: "+str(bord.get_score()))