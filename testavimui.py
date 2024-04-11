def high_score(SCORE):
    with open('high_score.txt','r+') as file:
        high_score=file.read()
        if int(high_score)<SCORE:
            file.seek(0)
            file.truncate()
            file.write(str(SCORE))
        file.close()

high_score(30)
