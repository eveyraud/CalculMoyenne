class BlocNote: 
    def __init__(self, bloc):
        def recupNoteCoeffNom(bloc):
            posCoeff = bloc.find('<td class="text_align_center">')+30
            coeff = bloc[posCoeff:bloc.find("<", posCoeff)]
            
            posNote = bloc.find('<td class="vert text_align_center">')+35
            note = bloc[posNote:bloc.find("<", posNote)]
            
            posNom = bloc.find('<td colspan="3" class="vert">')+29
            nom = bloc[posNom:bloc.find("<", posNom)]
            
            posMoyClass = bloc.find('<th class="text_align_center">')+30
            noteClass = bloc[posMoyClass:bloc.find("<", posMoyClass)]
            
            return(note, coeff, nom.strip("\\"), noteClass)
        
        self.bloc = bloc
        self.noteCoeffNom = recupNoteCoeffNom(bloc)
        
    def getNote(self):
        return self.noteCoeffNom[0]
    
    def getCoeff(self):
        return self.noteCoeffNom[1]
    
    def getNom(self):
        return self.noteCoeffNom[2]
    
    def getNoteClass(self):
        return self.noteCoeffNom[3]