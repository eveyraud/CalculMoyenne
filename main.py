from objet import BlocNote
strSrc = ""
with open("src.txt", "r", encoding="UTF-8") as fichierSrc:
    for ligne in fichierSrc:
        strSrc += ligne  

def sepBloc(strSrc):
    tabSrc = strSrc.split("<tr>")
    for i in range(4):
        
        del tabSrc[0]
    del tabSrc[-1]
    return tabSrc

def sepUE(strSrc):
    UE1 = []
    UE2 = []
    UE3 = []
    UE = 1
    for i in strSrc:
        if "UE" in i:
            UE += 1
        else:
            posNote = i.find('<td class="vert text_align_center">')+35
            note = i[posNote:i.find("<", posNote)]
            if '<td colspan="3"' in i and note != "":
                if UE == 1:
                    UE1.append(BlocNote(i))
                elif UE == 2:
                    UE2.append(BlocNote(i))
                else:
                    UE3.append(BlocNote(i))
    return {'UE1': UE1, 'UE2': UE2, 'UE3': UE3}

def calculMoyenne(UE):
    coeff = 0
    notes = 0
    for i in UE:
        coeff += float(i.getCoeff())
        notes += float(i.getNote()) * float(i.getCoeff())
    return notes/coeff

def calculMoyenneClass(UE):
    coeff = 0
    notes = 0
    for i in UE:
        coeff += float(i.getCoeff())
        notes += float(i.getNoteClass()) * float(i.getCoeff())
    return notes/coeff

reponse = int(input('''1) Moyenne de toutes les UE;
2) Compétences en dessous de la moyenne;
3) Moyenne de classe.
'''))
UE1 = round(calculMoyenne(sepUE(sepBloc(strSrc))['UE1']), 2)
UE2 = round(calculMoyenne(sepUE(sepBloc(strSrc))['UE2']), 2)
UE3 = round(calculMoyenne(sepUE(sepBloc(strSrc))['UE3']), 2)
UE1Class = round(calculMoyenneClass(sepUE(sepBloc(strSrc))['UE1']), 2)
UE2Class = round(calculMoyenneClass(sepUE(sepBloc(strSrc))['UE2']), 2)
UE3Class = round(calculMoyenneClass(sepUE(sepBloc(strSrc))['UE3']), 2)
if reponse == 1:
    print("UE1:", UE1)
    print("UE2:", UE2)
    print("UE3:", UE3)
    print('moyenne generale', round((UE1 + UE2 + UE3)/3, 2))
elif reponse == 2:
    for x, y in sepUE(sepBloc(strSrc)).items():
        for i in y:
            if float(i.getNote()) < 10:
                print(x, " : ",i.getNom(), " (", i.getNote(), ")", sep="")

elif reponse == 3:
    print("UE1:", UE1Class)
    print("UE2:", UE2Class)
    print("UE3:", UE3Class)
    print('moyenne generale', round((UE1Class + UE2Class + UE3Class)/3, 2))