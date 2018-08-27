import re
import csv
import json
import os

###################################
# Podatki, ki nas bodo zanimali.

polja = ['uvrstitev', 'startna_st', 'name', 'state',
         'velocity_1', 'distance_1',
         'SLO_1', 'GER_1', 'AUT_1', 'POL_1', 'JPN_1', 'NOR_1',
         'FIN_1', 'CAN_1', 'KAZ_1', 'ITA_1', 'FRA_1', 'RUS_1',
         'CZE_1', 'SUI_1', 'ROU_1', 'USA_1', 'KOR_1', 'SWE_1',
         'gate_1', 'tocke_1', 'mesto_1',
         'velocity_2', 'distance_2',
         'SLO_2', 'GER_2', 'AUT_2', 'POL_2', 'JPN_2', 'NOR_2',
         'FIN_2', 'CAN_2', 'KAZ_2', 'ITA_2', 'FRA_2', 'RUS_2',
         'CZE_2', 'SUI_2', 'ROU_2', 'USA_2', 'KOR_2', 'SWE_2',
         'gate_2', 'tocke_2', 'mesto_2',
         'tocke', 'hill_size', 'k_point'
         ]

####################################
# S tem regularnim izrazom bomo prebrali podatke o sodnikih, ki so sodili tekmo.

iskanje_sodnikov = re.compile(
    '<div style="position:absolute;left:\d+?.\d+?px;top:\d+?.\d+?px" class="cls_\d+?"><span class="cls_\d+?">A    (.+?)'
    '(?P<sodnik_A>[A-Z]{3})'
    '\)<\/span><\/div>'
    '.*?'
    '<.*?>B</span></div>\n'
    '<.*?>.*?'
    '(?P<sodnik_B>[A-Z]{3})'
    '\)<\/span><\/div>'
    '.*?'
    '<.*?>C</span></div>\n'
    '<.*?>.*?'
    '(?P<sodnik_C>[A-Z]{3})'
    '\)<\/span><\/div>'
    '.*?'
    '<.*?>D</span></div>\n'
    '<.*?>.*?'
    '(?P<sodnik_D>[A-Z]{3})'
    '\)<\/span><\/div>'
    '.*?'
    '<.*?>E</span></div>\n'
    '<.*?>.*?'
    '(?P<sodnik_E>[A-Z]{3})'
    '\)<\/span><\/div>',
    flags=re.DOTALL
    )
####################################
# S tem regularnim izrazon preberemo podatke o velikosti skakalnice.

velikost_skakalnice = re.compile(
    r'<.*?>HILL SIZE \(?HS\)?( / \(95%\))?</span></div>\n'
    r'<.*?>'
    r'(?P<hill_size>\d+?\.?\d)'
    r' ?m.*?</span></div>\n'
    r'<.+?>\n'
    r'<.+?>\n'
    r'<.+?>\n'
    r'<.+?>\n'
    r'<.*?>K-POINT</span></div>\n'
    r'<.*?>'
    r'(?P<k_point>\d+?)'
    r' ?m.*?</span></div>'
    ,
    flags = re.IGNORECASE
    )

################################################
# Spodnji programi izpišejo podatke iz prebranih html datotek v csv-je.
def zapisi_json(podatki, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        json.dump(podatki, datoteka, indent=2)

def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)

jump_data = {"hill_size" : 0, "k_point" : 0}
def podatki_tekem(imenik, ime_csvja):
    global jump_data
    podatki = []
    st_tekem = 0
    for tekma in os.listdir(imenik):
        st_tekem += 1
        #podatki = []
        #ime_csvja = tekma[:-4] + 'csv'
        #ime_csvja = "vse_tekme.csv"
        polna_pot_datoteke = os.path.join(imenik, tekma)
        with open(polna_pot_datoteke) as datoteka:
            vsebina_datoteke = datoteka.read()
            ######## s to zanko preberemo kateri sodniki so ocenjevali skakalce
            for ujemanje in re.finditer(iskanje_sodnikov, vsebina_datoteke): 
                sodniki = ujemanje.groupdict()
                #print(sodniki)
            blok_tekme = re.compile(
               '<div style="position:absolute;left:\d+?.\d+?px;top:\d+?.\d+?px" class="cls_\d+?"><span class="cls_\d+?">'
                '(?P<name>[A-Z]{3,} ?-?\w+ ?\w*)' #Ime tekmovalca
                '<\/span><\/div>\n'
                '<div style="position:absolute;left:\d+?.\d+?px;top:\d+?.\d+?px" class="cls_\d+?"><span class="cls_\d+?">'
                '(?P<state>[A-Z]{3})' #Narodnost tekmovalca
                '<\/span><\/div>\n'
                '<div style="position:absolute;left:\d+?.\d+?px;top:\d+?.\d+?px" class="cls_\d+?"><span class="cls_\d+?">'
                '(?P<velocity_1>\d+?.\d)' #Hitrost ob skoku
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<distance_1>\d.*?)' #dolžina skoka
                '<\/span><\/div>\n'
                '<.+?>\n' +
                ('<.+?>'
                '(?P<{}_1>\d.*?)' #Ocena sodnika A v prvi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_1>\d.*?)' #Ocena sodnika B v prvi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_1>\d.*?)' #Ocena sodnika C v prvi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_1>\d.*?)' #Ocena sodnika D v prvi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_1>\d.*?)' #Ocena sodnika E v prvi seriji
                '<\/span><\/div>\n').format(
                    sodniki["sodnik_A"],
                    sodniki["sodnik_B"],
                    sodniki["sodnik_C"],
                    sodniki["sodnik_D"],
                    sodniki["sodnik_E"]) +
                '<.+?>\n'
                '<.+?>©?0?'
                '(?P<gate_1>\d.*?)' #Zaletno mesto v prvi seriji
                '<\/span><\/div>\n'
                '(?:<div style="position:absolute;left:4(?:2|3)\d.\d\dpx;top:\d*?.\d*?px" class="cls_\d*?"><span class="cls_\d*?">.*?</span></div>\n)?'
                '<.+?>\n'
                '<.+?>\n'
                '<.+?>'
                '(?P<tocke_1>\d.*?)' #Točke v prvi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<mesto_1>\d.*?)' #Uvrstitev v prvi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<uvrstitev>\d.*?)' #Končna uvrstitev
                '<\/span><\/div>\n'
                '<.+?>\*?'
                '(?P<startna_st>\d.*?)' #Štartna številka
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<tocke>\d.*?)' #Dosežene točke
                '<\/span><\/div>\n'
                '<.+?>\n'
                '<.+?>\n'
                '<.+?>'
                '(?P<velocity_2>\d+?.\d)' #Hitrost pri drugem skoku 
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<distance_2>\d.*?)' #Dolžina drugega skoka
                '<\/span><\/div>\n'
                '<.+?>\n' +
                ('<.+?>'
                '(?P<{}_2>\d.*?)' #Ocena sodnika A v drugi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_2>\d.*?)' #Ocena sodnika B v drugi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_2>\d.*?)' #Ocena sodnika C v drugi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_2>\d.*?)' #Ocena sodnika D v drugi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<{}_2>\d.*?)' #Ocena sodnika E v drugi seriji
                '<\/span><\/div>\n').format(
                    sodniki["sodnik_A"],
                    sodniki["sodnik_B"],
                    sodniki["sodnik_C"],
                    sodniki["sodnik_D"],
                    sodniki["sodnik_E"]) +
                '<.+?>\n'
                '<.+?>©?0?'
                '(?P<gate_2>\d.*?)' #Zaletno mesto v drugi seriji
                '<\/span><\/div>\n'
                '(?:<div style="position:absolute;left:4(?:2|3)\d.\d*?px;top:\d*?.\d*?px" class="cls_\d*?"><span class="cls_\d*?">.*?</span></div>\n)?'
                '<.+?>\n'
                '<.+?>\n'
                '<.+?>'
                '(?P<tocke_2>\d.*?)' #Točke v drugi seriji
                '<\/span><\/div>\n'
                '<.+?>'
                '(?P<mesto_2>\d.*?)' #Uvrstitev v drugi seriji
                '<\/span><\/div>\n'
                )
            for ujemanje in re.finditer(velikost_skakalnice, vsebina_datoteke):
                global jump_data
                jump_data = ujemanje.groupdict()
            for ujemanje in re.finditer(blok_tekme,vsebina_datoteke):
                tekmovalec = ujemanje.groupdict()
                tekmovalec['hill_size'] = jump_data['hill_size']
                tekmovalec['k_point'] = jump_data['k_point']
                podatki.append(tekmovalec)
        zapisi_csv(podatki, polja, ime_csvja)
    print(st_tekem)
    print(jump_data)
    
        
#################################################################################################

        





