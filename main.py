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

print("UE1:", round(calculMoyenne(sepUE(sepBloc(strSrc))['UE1']), 2))
print("UE2:", round(calculMoyenne(sepUE(sepBloc(strSrc))['UE2']), 2))
print("UE3:", round(calculMoyenne(sepUE(sepBloc(strSrc))['UE3']), 2))










