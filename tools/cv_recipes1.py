# (héros, décor, ambiance, accessoires)  -- une entrée par épisode, dans l'ordre
def R(h, bg='nu', m='standard', acc=(), **k): 
    d = dict(h=h, bg=bg, m=m, acc=list(acc)); d.update(k); return d
REC = {
 'pt01': [R('child_stage','scene'), R('balance','pellicule'), R(('arc_ciel',{}),'etoiles','standard',[('souliers',100,252,.42)]), R('tramway','ville_aube'), R('porte_valise','stores','cendre'),
          R(('enseigne',{'t':'PALLADIUM'}),'rayons'), R('salle','nu','or'), R('cle_hotel','pluie','nuit'), R('bougies','ville_nuit','nuit')],
 'pt02': [R(('maison_num',{'t':'2300'}),'ville_aube','aube'), R('chaise_ceinture','brique','cendre'), R(('vinyle',{'t':''}),'spot'), R('miroir_gant','etoiles'), R('pyro','nu','alerte'),
          R('veste','diag','nuit'), R(('papier_stylo',{'t':'RÈGLEMENT'}),'presse'), R('balance_justice','marbre'), R(('compteur',{'t':'50'}),'scene','or')],
 'pt03': [R('palais','ville_aube'), R('casiers','nu'), R('objectifs','trame','alerte'), R('tondeuse','carreaux'), R('cage','brume','cendre'), R(('pancarte',{'t':'#FREE'}),'balayage','jour'), R('chaine_brisee','rayons','aube')],
}
