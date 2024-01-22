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
    UE4 = []
    UE5 = []
    UE = 1
    for i in strSrc:
        if "UE" in i:
            UE += 1
        else:
            posNote = i.find('<td class="vert text_align_center">') + 35
            note = i[posNote:i.find("<", posNote)]
            if '<td colspan="3"' in i and note != "":
                if UE == 1:
                    UE1.append(BlocNote(i))
                elif UE == 2:
                    UE2.append(BlocNote(i))
                elif UE == 3:
                    UE3.append(BlocNote(i))
                elif UE == 4:
                    UE4.append(BlocNote(i))
                elif UE == 5:
                    UE5.append(BlocNote(i))
    return {'UE1': UE1, 'UE2': UE2, 'UE3': UE3, 'UE4': UE4, 'UE5': UE5}

def calculMoyenne(UE):
    coeff = 0
    notes = 0
    for i in UE:
        coeff += float(i.getCoeff())
        notes += float(i.getNote()) * float(i.getCoeff())
    return round(notes / coeff, 2)

def calculMoyenneClass(UE):
    coeff = 0
    notes = 0
    for i in UE:
        coeff += float(i.getCoeff())
        notes += float(i.getNoteClass()) * float(i.getCoeff())
    return round(notes / coeff, 2)

# Calcul des moyennes
UE1 = calculMoyenne(sepUE(sepBloc(strSrc))['UE1'])
UE2 = calculMoyenne(sepUE(sepBloc(strSrc))['UE2'])
UE3 = calculMoyenne(sepUE(sepBloc(strSrc))['UE3'])
UE4 = calculMoyenne(sepUE(sepBloc(strSrc))['UE4'])
UE5 = calculMoyenne(sepUE(sepBloc(strSrc))['UE5'])

UE1Class = calculMoyenneClass(sepUE(sepBloc(strSrc))['UE1'])
UE2Class = calculMoyenneClass(sepUE(sepBloc(strSrc))['UE2'])
UE3Class = calculMoyenneClass(sepUE(sepBloc(strSrc))['UE3'])
UE4Class = calculMoyenneClass(sepUE(sepBloc(strSrc))['UE4'])
UE5Class = calculMoyenneClass(sepUE(sepBloc(strSrc))['UE5'])

# Affichage des résultats
print("")
print("UE1: ", UE1, " (", UE1Class, ")", " /!\\ " if UE1 < UE1Class else "", sep="")
print("UE2: ", UE2, " (", UE2Class, ")", " /!\\ " if UE2 < UE2Class else "", sep="")
print("UE3: ", UE3, " (", UE3Class, ")", " /!\\ " if UE3 < UE3Class else "", sep="")
print("UE4: ", UE4, " (", UE4Class, ")", " /!\\ " if UE4 < UE4Class else "", sep="")
print("UE5: ", UE5, " (", UE5Class, ")", " /!\\ " if UE5 < UE5Class else "", sep="")
print("")
print('Moyenne générale: ', round((UE1 + UE2 + UE3 + UE4 + UE5) / 5, 2), " (", round((UE1Class + UE2Class + UE3Class + UE4Class + UE5Class) / 5, 2), ")", sep="")


###############
## Optionnel ##
###############

print("")
print("--------------------------")
print("")
print("Matières en dessous de la moyenne :")
print("")
# Matières en dessous de la moyenne
for x, y in sepUE(sepBloc(strSrc)).items():
    for i in y:
        if float(i.getNote()) < 10:
            print(f"{x} : {i.getNom()} ({i.getNote()}) coeff: {i.getCoeff()}")
print("")

print("Matières importantes :")
print("")
# Matières en dessous de la moyenne
for x, y in sepUE(sepBloc(strSrc)).items():
    for i in y:
        if float(i.getCoeff()) >= 5:
            print(f"{x} : {i.getNom()} ({i.getNote()}) coeff: {i.getCoeff()}")
print("")
