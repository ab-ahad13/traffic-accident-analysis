import pandas as pd

# raw = pd.read_csv("raw_accident_data.csv")

# df['Location'] = df['Location'].str.extract(r'\((.+)\)')
# df['Location'] = df['Location'].apply(lambda x: ', '.join([str(round(float(i), 3)) for i in x.split(',')]) if pd.notna(x) else x)

# df = df.drop(columns=['Latitude', 'Longitude'])

# df.to_csv("cleaned_crash.csv", index=False)


df = pd.read_csv("cleaned_vehicles_binary.csv")


# df = df.drop(columns=['Local Case Number','Off-Road Description','Municipality','Related Non-Motorist','Non-Motorist Substance Abuse','Vehicle First Impact Location','Vehicle Second Impact Location','Driverless Vehicle'])
# df = df.drop(columns=['Equipment Problems'])
# df = df.drop(columns=['Cross-Street Type'])

# df = df.dropna(subset=['Vehicle Body Type', 'Vehicle Continuing Dir', 'Vehicle Going Dir'])
# df = df.dropna(subset=['Vehicle Model','Vehicle Make'])
# df = df.dropna(subset=['Weather'])
# df = df.dropna(subset=['Weather', 'Surface Condition'])
# df = df.dropna(subset=['Vehicle Movement'])
# df = df.dropna(subset=['Vehicle Damage Extent'])
# df = df.dropna(subset=['Collision Type'])
# df = df[df['Driver Substance Abuse'].notna()]
# df = df[df['Route Type'].notna()]


# df['Light'] = df['Light'].fillna('UNKNOWN')
# df['Light'] = df['Light'].replace('OTHER', 'UNKNOWN')
# top_states = df['Drivers License State'].value_counts()[lambda x: x >= 1000].index
# df['Drivers License State'] = df['Drivers License State'].apply(lambda x: x if x in top_states else 'OTHER')
# df['Traffic Control'] = df['Traffic Control'].fillna('NO CONTROLS')
# df = df[df['Traffic Control'] != 'UNKNOWN']
# df = df[df['Traffic Control'] != 'SCHOOL ZONE SIGN DEVICE']


# upper case fix (agar needed ho)
# df['Weather'] = df['Weather'].str.upper()

# # similar categories merge
# df['Weather'] = df['Weather'].replace({
#     'CLEAR': 'CLEAR',
#     'CLOUDY': 'CLOUDY',
#     'RAINING': 'RAIN',
#     'FOGGY': 'FOG',
#     'SNOW': 'SNOW',
#     'SLEET': 'SNOW',
#     'WINTRY MIX': 'SNOW',
#     'BLOWING SNOW': 'SNOW',
#     'SEVERE WINDS': 'OTHER',
#     'OTHER': 'OTHER',
#     'UNKNOWN': None ,
#     'BLOWING SAND, SOIL, DIRT': 'OTHER'
# })

# df['Surface Condition'] = df['Surface Condition'].replace({
#     'WATER(STANDING/MOVING)': 'WET',
#     'SLUSH': 'SNOW',
#     'ICE': 'SNOW',
#     'SNOW': 'SNOW',
#     'MUD, DIRT, GRAVEL': 'OTHER',
#     'OIL': 'OTHER',
#     'SAND': 'OTHER',
#     'OTHER': 'OTHER',
#     'UNKNOWN': None
# })

# def fill_surface(row):
#     if pd.isna(row['Surface Condition']):
#         if row['Weather'] == 'RAIN':
#             return 'WET'
#         elif row['Weather'] == 'SNOW':
#             return 'SNOW'
#         elif row['Weather'] == 'FOG':
#             return 'WET'
#         elif row['Weather'] == 'CLEAR':
#             return 'DRY'
#         elif row['Weather'] == 'CLOUDY':
#             return 'DRY'
#         else:
#             return None
#     return row['Surface Condition']

# df['Surface Condition'] = df.apply(fill_surface, axis=1)




# -----------------------------
# STEP 2: restore Vehicle Movement (correct alignment)
# -----------------------------
# df['Vehicle Movement'] = raw.loc[df.index, 'Vehicle Movement']

# df['Vehicle Movement'] = df['Vehicle Movement'].str.strip().str.upper()

# def group_movement(x):
#     if x in ['MOVING CONSTANT SPEED', 'ACCELERATING']:
#         return 'Moving'
    
#     elif x in ['SLOWING OR STOPPING', 'STOPPED IN TRAFFIC LANE']:
#         return 'Stopping'
    
#     elif x in ['MAKING LEFT TURN', 'MAKING RIGHT TURN', 'MAKING U TURN', 'RIGHT TURN ON RED']:
#         return 'Turning'
    
#     elif x in ['CHANGING LANES', 'ENTERING TRAFFIC LANE', 'LEAVING TRAFFIC LANE']:
#         return 'Lane Change'
    
#     elif x in ['STARTING FROM LANE', 'STARTING FROM PARKED', 'PARKING']:
#         return 'Starting/Parking'
    
#     elif x == 'BACKING':
#         return 'Reversing'
    
#     elif x in ['SKIDDING', 'NEGOTIATING A CURVE']:
#         return 'Loss of Control'
    
#     elif x in ['PASSING', 'OTHER', 'DRIVERLESS MOVING VEH.']:
#         return 'Other'
    
#     else:
#         return x   # important (data lose nahi hoga)

# df['Vehicle Movement'] = df['Vehicle Movement'].apply(group_movement)


# df['Vehicle Damage Extent'] = df['Vehicle Damage Extent'].str.strip().str.upper()

# def group_damage(x):
#     if x == 'NO DAMAGE':
#         return 'No Damage'
    
#     elif x == 'SUPERFICIAL':
#         return 'Minor'
    
#     elif x == 'FUNCTIONAL':
#         return 'Moderate'
    
#     elif x in ['DISABLING', 'DESTROYED']:
#         return 'Severe'
    
#     else:
#         return 'Other'

# df['Vehicle Damage Extent'] = df['Vehicle Damage Extent'].apply(group_damage)



# Step 1: clean text (VERY IMPORTANT)
# df['Collision Type'] = df['Collision Type'].astype(str).str.strip().str.upper()

# # Step 2: mapping
# collision_map = {
#     # ---- TURN REAR GROUP ----
#     'SAME DIR REND LEFT TURN': 'TURN REAR',
#     'SAME DIR REND RIGHT TURN': 'TURN REAR',
#     'SAME DIR BOTH LEFT TURN': 'TURN REAR',

#     # ---- ANGLE TURN GROUP ----
#     'ANGLE MEETS LEFT TURN': 'ANGLE TURN',
#     'ANGLE MEETS RIGHT TURN': 'ANGLE TURN',

#     # ---- FORCE TO OTHER ----
#     'ANGLE MEETS LEFT HEAD ON': 'OTHER',
#     'UNKNOWN': 'OTHER',
#     'OPPOSITE DIR BOTH LEFT TURN': 'OTHER'
# }

# # Step 3: apply mapping safely
# df['Collision Type'] = df['Collision Type'].replace(collision_map)




# df['Circumstance'] = df['Circumstance'].astype(str).str.upper().str.strip()

# def group_circumstance(x):
#     if pd.isna(x):
#         return 'Other'
    
#     if any(w in x for w in ['RAIN', 'WET']):
#         return 'Rainy Weather'
    
#     elif any(w in x for w in ['SNOW', 'ICE', 'SLEET', 'FREEZ']):
#         return 'Snow/Ice'
    
#     elif any(w in x for w in ['CROSSWINDS', 'BLOWING', 'SAND', 'DIRT']):
#         return 'Wind/Dust'
    
#     elif any(w in x for w in ['SMOG', 'SMOKE', 'FOG', 'VISION']):
#         return 'Visibility'
    
#     elif any(w in x for w in ['RUTS', 'BUMPS']):
#         return 'Road Damage'
    
#     elif any(w in x for w in ['WORN', 'SLIPPERY']):
#         return 'Road Wear'
    
#     elif any(w in x for w in ['CONSTRUCTION', 'WORK']):
#         return 'Construction'
    
#     elif 'ANIMAL' in x:
#         return 'Animal'
    
#     elif any(w in x for w in ['DEBRIS', 'OBSTRUCTION']):
#         return 'Obstruction'
    
#     elif any(w in x for w in ['BACKUP', 'CONGESTION']):
#         return 'Traffic'
    
#     elif 'PRIOR CRASH' in x:
#         return 'Prior Crash'
    
#     else:
#         return 'Other'

# df['Circumstance'] = df['Circumstance'].apply(group_circumstance)






# make_mapping = {

#     # TOYOTA
#     'TOYT': 'TOYOTA', 'TOYTA': 'TOYOTA', 'TOYOT': 'TOYOTA', 'TOYOYA': 'TOYOTA',
#     'TOYTOTA': 'TOYOTA', 'TOYTOA': 'TOYOTA', 'TOYOTS': 'TOYOTA', 'TOYOYTA': 'TOYOTA',
#     'TOY0TA': 'TOYOTA', 'TOY': 'TOYOTA', 'TOTOTA': 'TOYOTA', 'TOYO': 'TOYOTA',
#     'TOYOA': 'TOYOTA', 'TOYOAT': 'TOYOTA', 'T0YOTA': 'TOYOTA', 'T0Y0TA': 'TOYOTA',
#     'TIYOTA': 'TOYOTA', 'TYOTA': 'TOYOTA', 'TYOYOTA': 'TOYOTA', 'TOOYOTA': 'TOYOTA',
#     'TOYIOTA': 'TOYOTA', 'TOYITA': 'TOYOTA', 'TOYOOTA': 'TOYOTA', 'TOYORA': 'TOYOTA',
#     'TOYATO': 'TOYOTA', 'TOYOTOA': 'TOYOTA', 'TOYOTTO': 'TOYOTA', 'TOYOVA': 'TOYOTA',
#     'TOTOYTA': 'TOYOTA', 'TOTYOTA': 'TOYOTA', 'TOTOYA': 'TOYOTA', 'TOYOATA': 'TOYOTA',
#     'TOOTA': 'TOYOTA', 'TOTY': 'TOYOTA', 'TOTYOTA': 'TOYOTA', 'TOT': 'TOYOTA',
#     'POYOTA': 'TOYOTA', 'TPYPTA': 'TOYOTA', 'TPYT': 'TOYOTA', 'YOYOTA': 'TOYOTA',
#     'YTOYOTA': 'TOYOTA', 'TOYOVAL2002': 'TOYOTA', 'TOYOVAL2006': 'TOYOTA',
#     'TOYOVAL2011': 'TOYOTA', 'TOYOTA SCION': 'TOYOTA', 'TOYOTA/SCION': 'TOYOTA',
#     'TOYOTA4': 'TOYOTA', 'TOYOTA4D': 'TOYOTA', 'TOYOTAC': 'TOYOTA',
#     'TOYOTACE': 'TOYOTA', 'TOYOTAT': 'TOYOTA', 'TOYOTAY': 'TOYOTA',
#     'TOYOTO': 'TOYOTA', 'TOYOTTA': 'TOYOTA', 'TOYYOTA': 'TOYOTA',
#     'TOOYOTA': 'TOYOTA', 'TOYR': 'TOYOTA', 'TIYOTA': 'TOYOTA',
#     'TOYOTA C': 'TOYOTA',

#     # HONDA
#     'HOND': 'HONDA', 'HINDA': 'HONDA', 'HODNA': 'HONDA', 'HONA': 'HONDA',
#     'HODA': 'HONDA', 'HONAD': 'HONDA', 'HONADA': 'HONDA', 'HNDA': 'HONDA',
#     'HIONDA': 'HONDA', 'HHONDA': 'HONDA', 'HOMDA': 'HONDA', 'HON': 'HONDA',
#     'HO': 'HONDA', 'HONDM': 'HONDA', 'HONDRA': 'HONDA', 'HONDVA': 'HONDA',
#     'HONDDA': 'HONDA', 'HOONDA': 'HONDA', 'HPNDA': 'HONDA', 'JONDA': 'HONDA',
#     'IHON': 'HONDA', 'ONDA': 'HONDA', 'HON DA': 'HONDA', 'HONDQ': 'HONDA',
#     'HONDAQ': 'HONDA', 'HONDAT': 'HONDA', "HONDA`": 'HONDA',
#     'HONDVAL1992': 'HONDA', 'HONDVAL2000': 'HONDA', 'HONDVAL2006': 'HONDA',

#     # FORD
#     'FOED': 'FORD', 'FOORD': 'FORD', 'FORDD': 'FORD', 'FORDE': 'FORD',
#     'FORDQ': 'FORD', 'FOR': 'FORD', 'FRD': 'FORD', 'FORD BUS': 'FORD',
#     'FORD TK': 'FORD', 'FORD UTILIMASTER': 'FORD', 'FORD/GOSHEN': 'FORD',
#     'FORD/UTILIMASTER': 'FORD', 'FORE': 'FORD', 'FORF': 'FORD',
#     'FORDVAL2007': 'FORD', 'FORDVAL2012': 'FORD', 'FORDVAL2013': 'FORD',

#     # CHEVROLET
#     'CHEV': 'CHEVROLET', 'CHEVY': 'CHEVROLET', 'CHEVEROLET': 'CHEVROLET',
#     'CHEVORLET': 'CHEVROLET', 'CHEVERLOT': 'CHEVROLET', 'CHEVROLETE': 'CHEVROLET',
#     'CHEVOLET': 'CHEVROLET', 'CHERVOLET': 'CHEVROLET', 'CHERVEROLET': 'CHEVROLET',
#     'CHEVRO': 'CHEVROLET', 'CHEVROLE': 'CHEVROLET', 'CHEVROLEET': 'CHEVROLET',
#     'CHEVROLT': 'CHEVROLET', 'CHEVROLTE': 'CHEVROLET', 'CHEVRLOET': 'CHEVROLET',
#     'CHEVROELT': 'CHEVROLET', 'CHEVROET': 'CHEVROLET', 'CHEVERLET': 'CHEVROLET',
#     'CHECROLET': 'CHEVROLET', 'CEHVORLET': 'CHEVROLET', 'CHAVROLET': 'CHEVROLET',
#     'CHERVEOLET': 'CHEVROLET', 'CHERVERLET': 'CHEVROLET', 'CHVROLET': 'CHEVROLET',
#     'CHRVROLET': 'CHEVROLET', 'CHEVYROLET': 'CHEVROLET', 'CVEVROLET': 'CHEVROLET',
#     'CEHVY': 'CHEVROLET', 'CHECY': 'CHEVROLET', 'CHEV.': 'CHEVROLET',
#     'CHEVELOT': 'CHEVROLET', 'CHEVEY': 'CHEVROLET', 'CHEVUY': 'CHEVROLET',
#     'CHEVVAL1995': 'CHEVROLET', 'CHEVVAL2013': 'CHEVROLET',
#     'CHEY': 'CHEVROLET', 'CHEYV': 'CHEVROLET', 'CHEVE': 'CHEVROLET',
#     'CHE VY': 'CHEVROLET', 'CHVY': 'CHEVROLET', 'CHE': 'CHEVROLET',
#     'CEV': 'CHEVROLET', 'CEVROLET': 'CHEVROLET', 'CEVY': 'CHEVROLET',
#     'CHEVROLETT': 'CHEVROLET', 'CHEVROLETTE': 'CHEVROLET',
#     'CHEVROLEY': 'CHEVROLET', 'CHEVEROLRT': 'CHEVROLET',
#     'CHEVVAL2013': 'CHEVROLET',

#     # NISSAN
#     'NISS': 'NISSAN', 'NISSIAN': 'NISSAN', 'NISAN': 'NISSAN',
#     'NISAAN': 'NISSAN', 'NIISAN': 'NISSAN', 'NISSON': 'NISSAN',
#     'NISSSAN': 'NISSAN', 'NISSAM': 'NISSAN', 'NISSAB': 'NISSAN',
#     'MISSAN': 'NISSAN', 'NSSAN': 'NISSAN', 'NISSA': 'NISSAN',
#     'NISSA N': 'NISSAN', 'NIS': 'NISSAN', 'NISSN': 'NISSAN',
#     'NISSVAL2007': 'NISSAN', 'NISSVAL2008': 'NISSAN', 'NSSAN': 'NISSAN',
#     'NUSS': 'NISSAN', 'NSS': 'NISSAN', 'NISSAN DIESEL': 'NISSAN',
#     'NISSAN 4S': 'NISSAN', 'NISSAN320': 'NISSAN',

#     # DODGE
#     'DODG': 'DODGE', 'DODGE RAM': 'DODGE', 'DAODGE': 'DODGE',
#     'DDOGE': 'DODGE', 'DOAGE': 'DODGE', 'DOD': 'DODGE', 'DODDGE': 'DODGE',
#     'DODE': 'DODGE', 'DODGDE': 'DODGE', 'DODOGE': 'DODGE', 'DODGEQ': 'DODGE',
#     "DODGE`": 'DODGE', 'DODGVAL2013': 'DODGE', 'DOGDE': 'DODGE',
#     'DOGDGE': 'DODGE', 'DOGE': 'DODGE', 'DOIDGE': 'DODGE', 'DOSGE': 'DODGE',
#     'DIDGE': 'DODGE', 'DODGE SUV': 'DODGE',

#     # HYUNDAI
#     'HYUN': 'HYUNDAI', 'HYUNDIA': 'HYUNDAI', 'HYUND': 'HYUNDAI',
#     'HYUNDA': 'HYUNDAI', 'HYUNDAY': 'HYUNDAI', 'HYUNDI': 'HYUNDAI',
#     'HYUDAI': 'HYUNDAI', 'HUNDAI': 'HYUNDAI', 'HYNDAI': 'HYUNDAI',
#     'HUYNDAI': 'HYUNDAI', 'HYUANDAI': 'HYUNDAI', 'HYUANDI': 'HYUNDAI',
#     'HYANDAI': 'HYUNDAI', 'HYAUNDAI': 'HYUNDAI', 'HUYANDAI': 'HYUNDAI',
#     'HUYANDI': 'HYUNDAI', 'HUYNDA': 'HYUNDAI', 'HHYUNDIA': 'HYUNDAI',
#     'HIUNDAY': 'HYUNDAI', 'HUNDA': 'HYUNDAI', 'HUNDI': 'HYUNDAI',
#     'HUNYDAI': 'HYUNDAI', 'HUUNDAI': 'HYUNDAI', 'HUYUNDAI': 'HYUNDAI',
#     'HY8UNDAI': 'HYUNDAI', 'HYDUNAI': 'HYUNDAI', 'HYINDAI': 'HYUNDAI',
#     'HYND': 'HYUNDAI', 'HYN': 'HYUNDAI', 'HUY': 'HYUNDAI', 'HUYN': 'HYUNDAI',
#     'NYUNDAI': 'HYUNDAI', 'HDAIYUN': 'HYUNDAI', 'HYUNUNDAI': 'HYUNDAI',
#     'HYUNADAI': 'HYUNDAI', 'HYUNADI': 'HYUNDAI', 'HYUNAI': 'HYUNDAI',
#     'HYUNDAU': 'HYUNDAI', 'HYUNDAUI': 'HYUNDAI', 'HYUNDY': 'HYUNDAI',
#     'HYUNDYA': 'HYUNDAI', 'HYUNVAL1999': 'HYUNDAI', 'HYUNVAL2008': 'HYUNDAI',
#     'HYUN/HON': 'HYUNDAI', 'HHYUNDIA': 'HYUNDAI',

#     # BMW
#     'BWM': 'BMW', 'BMMW': 'BMW', 'BMV': 'BMW', 'BM': 'BMW', 'BW': 'BMW',
#     'BMW 4S': 'BMW',

#     # JEEP
#     'JEEB': 'JEEP', 'JEEEP': 'JEEP', 'JEEF': 'JEEP', 'JEEO': 'JEEP',
#     'HEEP': 'JEEP', 'JEEPVAL2013': 'JEEP',

#     # LEXUS
#     'LEXS': 'LEXUS', 'LEXU': 'LEXUS', 'LEXSUS': 'LEXUS', 'LEXAS': 'LEXUS',
#     'LEXES': 'LEXUS', 'LEXIS': 'LEXUS', 'LECUS': 'LEXUS', 'LESUX': 'LEXUS',
#     'LUXUS': 'LEXUS', 'LEXUIS': 'LEXUS', 'LEZUS': 'LEXUS', 'LEXUSS': 'LEXUS',
#     'LEXUSZ': 'LEXUS', 'LEXUUS': 'LEXUS', 'LEXUW': 'LEXUS', 'LEXUX': 'LEXUS',
#     'LEXI': 'LEXUS', 'LEX': 'LEXUS', 'LEXUVAL2012': 'LEXUS',

#     # ACURA
#     'ACUR': 'ACURA', 'ACCURA': 'ACURA', 'ACUA': 'ACURA', 'ACRUA': 'ACURA',
#     'ACARA': 'ACURA', 'ACRA': 'ACURA', 'ACUAR': 'ACURA',
#     'ACURA STATEFARM': 'ACURA', 'ACURAMDX': 'ACURA', 'ACURARDX': 'ACURA',
#     'ACURAT': 'ACURA', 'ACRUA': 'ACURA', 'CURA': 'ACURA',
#     'ACURAR': 'ACURA', 'ACCU': 'ACURA',

#     # SUBARU
#     'SUBA': 'SUBARU', 'SUBURU': 'SUBARU', 'SUBU': 'SUBARU',
#     'SUBURA': 'SUBARU', 'SUBURAU': 'SUBARU', 'SUBARRU': 'SUBARU',
#     'SUBARY': 'SUBARU', 'SUBARO': 'SUBARU', 'SUBARBU': 'SUBARU',
#     'SABSRU': 'SUBARU', 'SABURU': 'SUBARU', 'DUBARU': 'SUBARU',
#     'SSUBARU': 'SUBARU', 'SUNARU': 'SUBARU', 'SURARU': 'SUBARU',
#     'SUBUARU': 'SUBARU', 'SUBBARU': 'SUBARU', 'SUBR': 'SUBARU',
#     'SUBRA': 'SUBARU', 'SUBRARU': 'SUBARU', 'SUBRU': 'SUBARU',
#     'SUBAR': 'SUBARU', 'SUBARA': 'SUBARU', 'SUB': 'SUBARU',
#     'SUBAVAL1997': 'SUBARU', 'SUBUREU': 'SUBARU', 'SABARU': 'SUBARU',

#     # MAZDA
#     'MAZD': 'MAZDA', 'MAZADA': 'MAZDA', 'MADZA': 'MAZDA', 'MAZA': 'MAZDA',
#     'MAZ': 'MAZDA', 'MAXDA': 'MAZDA', 'NAZDA': 'MAZDA', 'MAZDZ': 'MAZDA',
#     'MAZFA': 'MAZDA', 'MADZ': 'MAZDA',

#     # GMC
#     'GM': 'GMC', 'GENERAL MOTORS': 'GMC', 'GMC/CHEVY': 'GMC',
#     'GMV': 'GMC', 'GENERAL MOTORS CORPO': 'GMC',

#     # AUDI
#     'ADUI': 'AUDI', 'AUFI': 'AUDI', 'AUDIVAL2007': 'AUDI',

#     # MERCEDES-BENZ
#     'MERZ': 'MERCEDES-BENZ', 'MERC': 'MERCEDES-BENZ',
#     'MERCEDES BENZ': 'MERCEDES-BENZ', 'MERCEDEZ': 'MERCEDES-BENZ',
#     'MERCEDES': 'MERCEDES-BENZ', 'MERCEDEZ BENZ': 'MERCEDES-BENZ',
#     'MB': 'MERCEDES-BENZ', 'MBENZ': 'MERCEDES-BENZ', 'M BENZ': 'MERCEDES-BENZ',
#     'MER': 'MERCEDES-BENZ', 'MECEDES BENZ': 'MERCEDES-BENZ',
#     'MECEDEZ': 'MERCEDES-BENZ', 'MERCE': 'MERCEDES-BENZ',
#     'MERCED': 'MERCEDES-BENZ', 'MERCEDEES': 'MERCEDES-BENZ',
#     'MERCEDES BENS': 'MERCEDES-BENZ', 'MERCADES': 'MERCEDES-BENZ',
#     'MERCDES': 'MERCEDES-BENZ', 'MERCEDS': 'MERCEDES-BENZ',
#     'MERCEDS BENZ': 'MERCEDES-BENZ', 'MERCEES': 'MERCEDES-BENZ',
#     'MERCENDES': 'MERCEDES-BENZ', 'MERCERDEZ': 'MERCEDES-BENZ',
#     'MERCERY': 'MERCEDES-BENZ', 'MERCEZ': 'MERCEDES-BENZ',
#     'MERDECES': 'MERCEDES-BENZ', 'MERDEDES': 'MERCEDES-BENZ',
#     'MERECEDES': 'MERCEDES-BENZ', 'MERS-BENZ': 'MERCEDES-BENZ',
#     'MERZEDES': 'MERCEDES-BENZ', 'MERZEDEZ': 'MERCEDES-BENZ',
#     'MERZ BENZ': 'MERCEDES-BENZ', 'MRCEDES': 'MERCEDES-BENZ',
#     'MRECEDES': 'MERCEDES-BENZ', 'MRRZ': 'MERCEDES-BENZ',
#     'BENZ': 'MERCEDES-BENZ', 'BENS': 'MERCEDES-BENZ',
#     'MER-BENZ': 'MERCEDES-BENZ', 'MERC EDES': 'MERCEDES-BENZ',
#     'MEZ': 'MERCEDES-BENZ', 'MEDZ': 'MERCEDES-BENZ',
#     'MERCEDES-BENZ': 'MERCEDES-BENZ', 'MERCEDES ZBENZ': 'MERCEDES-BENZ',
#     'MERCEDEZ-BENZ': 'MERCEDES-BENZ', 'MECURY': 'MERCEDES-BENZ',
#     'MERZ 4S': 'MERCEDES-BENZ', 'MERZEDES BENZ': 'MERCEDES-BENZ',
#     'MERCEDEZ BENS': 'MERCEDES-BENZ', 'MECREDES': 'MERCEDES-BENZ',

#     # VOLKSWAGEN
#     'VOLK': 'VOLKSWAGEN', 'VOLKSWAGON': 'VOLKSWAGEN', 'VOLKS': 'VOLKSWAGEN',
#     'VW': 'VOLKSWAGEN', 'VOLKS WAGON': 'VOLKSWAGEN', 'VOLKWAGON': 'VOLKSWAGEN',
#     'VOLKWAGEN': 'VOLKSWAGEN', 'VOLSWAGON': 'VOLKSWAGEN',
#     'VOKSWAGEN': 'VOLKSWAGEN', 'VOKSWAGON': 'VOLKSWAGEN',
#     'VOLKSAWAGON': 'VOLKSWAGEN', 'VOLKSWAG': 'VOLKSWAGEN',
#     'VOLKSWAGAN': 'VOLKSWAGEN', 'VOLKSWAGEB': 'VOLKSWAGEN',
#     'VOLKSWAGEM': 'VOLKSWAGEN', 'VOLKSWAGGON': 'VOLKSWAGEN',
#     'VOLKSWAGKON': 'VOLKSWAGEN', 'VOLKSWAGN': 'VOLKSWAGEN',
#     'VOLKSWGEN': 'VOLKSWAGEN', 'VOLKSWGN': 'VOLKSWAGEN',
#     'VOLKSWGONA': 'VOLKSWAGEN', 'VOLKWAGGON': 'VOLKSWAGEN',
#     'VOLKWASGEN': 'VOLKSWAGEN', 'VOLSWAGAN': 'VOLKSWAGEN',
#     'VOLSWAGEN': 'VOLKSWAGEN', 'VOLSKWAGON': 'VOLKSWAGEN',
#     'VOLTSWAGON': 'VOLKSWAGEN', 'VOIK': 'VOLKSWAGEN', 'VOKS': 'VOLKSWAGEN',
#     'VOLK SWAGON': 'VOLKSWAGEN', 'VOLKD': 'VOLKSWAGEN', 'VOLKK': 'VOLKSWAGEN',
#     'VOLKKWAGON': 'VOLKSWAGEN', 'WOLK': 'VOLKSWAGEN',
#     'WOLKSWAGON': 'VOLKSWAGEN', 'VOLKS WAGEN': 'VOLKSWAGEN',

#     # BUICK
#     'BUIC': 'BUICK', 'BUICL': 'BUICK', 'BUICCK': 'BUICK',
#     'BUICKE': 'BUICK', 'BUIK': 'BUICK', 'BUCK': 'BUICK',

#     # INFINITI
#     'INFI': 'INFINITI', 'INFINITY': 'INFINITI', 'INFINTI': 'INFINITI',
#     'INFIN': 'INFINITI', 'INFINI': 'INFINITI', 'INFINIT': 'INFINITI',
#     'INFINITE': 'INFINITI', 'INFINITIG': 'INFINITI', 'INFINITU': 'INFINITI',
#     'INFINTY': 'INFINITI', 'INFITY': 'INFINITI', 'INF': 'INFINITI',
#     'INIF': 'INFINITI', 'INIFINIT': 'INFINITI', 'INIFINITI': 'INFINITI',
#     'INIFINITY': 'INFINITI', 'INFIVAL2014': 'INFINITI', 'INFIINITY': 'INFINITI',

#     # CADILLAC
#     'CADI': 'CADILLAC', 'CADILAC': 'CADILLAC', 'CAD': 'CADILLAC',
#     'CADALLAC': 'CADILLAC', 'CADALLIC': 'CADILLAC', 'CADDILAC': 'CADILLAC',
#     'CADILACC': 'CADILLAC', 'CADILLA': 'CADILLAC', 'CADILLIAC': 'CADILLAC',
#     'CADILLIC': 'CADILLAC',

#     # CHRYSLER
#     'CHRY': 'CHRYSLER', 'CHRYS': 'CHRYSLER', 'CHRYSTLER': 'CHRYSLER',
#     'CRYSLER': 'CHRYSLER', 'CHRYLSER': 'CHRYSLER', 'CHRSLER': 'CHRYSLER',
#     'CHYSLER': 'CHRYSLER', 'CHYRSLER': 'CHRYSLER', 'CHRYLSLER': 'CHRYSLER',
#     'CHRSYLER': 'CHRYSLER', 'CHRYSELEY': 'CHRYSLER', 'CHRYSLR': 'CHRYSLER',
#     'CHRYST': 'CHRYSLER', 'CHRISLER': 'CHRYSLER', 'CHRYSELER': 'CHRYSLER',
#     'CHRYSLEY': 'CHRYSLER', 'CGHRUSYLER': 'CHRYSLER', 'CHRYVAL2008': 'CHRYSLER',
#     'CHRYLS': 'CHRYSLER', 'CHY': 'CHRYSLER', 'CHYR': 'CHRYSLER',
#     'CRY': 'CHRYSLER', 'CRYS': 'CHRYSLER', 'CHHRY': 'CHRYSLER',
#     'CHTYS': 'CHRYSLER', 'CHTY': 'CHRYSLER', 'CHRV': 'CHRYSLER',

#     # FREIGHTLINER
#     'FRHT': 'FREIGHTLINER', 'FREIGHT': 'FREIGHTLINER', 'FRT': 'FREIGHTLINER',
#     'FREIGHLINER': 'FREIGHTLINER', 'FRIEGHTLINER': 'FREIGHTLINER',
#     'FREIGHT LINER': 'FREIGHTLINER', 'FREIGHTLINE': 'FREIGHTLINER',
#     'FREIGHTL': 'FREIGHTLINER', 'FREIGHTLNR': 'FREIGHTLINER',
#     'FRIEGHT': 'FREIGHTLINER', 'FRIEGHT LINER': 'FREIGHTLINER',
#     'FRIGHTLINER': 'FREIGHTLINER', 'FRAIGHT LINER': 'FREIGHTLINER',
#     'FRAIGHT': 'FREIGHTLINER', 'FREIGHTLINR': 'FREIGHTLINER',
#     'FREIGHTLNER': 'FREIGHTLINER', 'FREITLINER': 'FREIGHTLINER',
#     'FRGT': 'FREIGHTLINER', 'FRGHT': 'FREIGHTLINER',
#     'GREIGHTLINER': 'FREIGHTLINER', 'FRG': 'FREIGHTLINER',
#     'FRLI': 'FREIGHTLINER', 'FRNT': 'FREIGHTLINER',
#     'FRONTLINER': 'FREIGHTLINER', 'FRTL': 'FREIGHTLINER',
#     'FTL': 'FREIGHTLINER', 'FREIGHTLINER BUS': 'FREIGHTLINER',
#     'FRHT AM': 'FREIGHTLINER', 'FRHT LINER': 'FREIGHTLINER',
#     'FRHT LNR': 'FREIGHTLINER', 'FRHTLINER': 'FREIGHTLINER',
#     'FRH': 'FREIGHTLINER', 'FRHT TK': 'FREIGHTLINER',
#     'FRHT-THOMAS': 'FREIGHTLINER', 'FREI': 'FREIGHTLINER',
#     'FREIG': 'FREIGHTLINER', 'FREI TK': 'FREIGHTLINER',
#     'FREIGHT BUS': 'FREIGHTLINER', 'FREIGHT LINNER': 'FREIGHTLINER',
#     'FREIGHT TRK': 'FREIGHTLINER', 'FREIGHTLINERS': 'FREIGHTLINER',
#     'FRE': 'FREIGHTLINER', 'FREGHT': 'FREIGHTLINER',
#     'FRIGHT': 'FREIGHTLINER', 'FRIG': 'FREIGHTLINER',
#     'FRT LINER': 'FREIGHTLINER', 'FRTH': 'FREIGHTLINER',
#     'FTHT': 'FREIGHTLINER', 'FREDI': 'FREIGHTLINER',

#     # LINCOLN
#     'LINC': 'LINCOLN', 'LICOLN': 'LINCOLN', 'LINCON': 'LINCOLN',
#     'LINCCOLN': 'LINCOLN', 'LINCILN': 'LINCOLN', 'LINCLN': 'LINCOLN',
#     'LINOLM': 'LINCOLN', 'LIN': 'LINCOLN',

#     # VOLVO
#     'VOLV': 'VOLVO', 'VOVLO': 'VOLVO', 'VOLV0': 'VOLVO', 'VOLVA': 'VOLVO',
#     'VOVL': 'VOLVO', 'COLVO': 'VOLVO', 'AUVOLVO': 'VOLVO',
#     'VOLVO SAB': 'VOLVO', 'VOLO': 'VOLVO', 'VOLS': 'VOLVO',

#     # MACK
#     'MAC': 'MACK', 'MACH': 'MACK', 'MACJ': 'MACK', 'MACL': 'MACK',
#     'MACK TK': 'MACK', 'MACK 600': 'MACK', 'MACK TRUCKS INC': 'MACK',

#     # MITSUBISHI
#     'MITS': 'MITSUBISHI', 'MITZ': 'MITSUBISHI', 'MITSU': 'MITSUBISHI',
#     'MISTUBISHI': 'MITSUBISHI', 'MITSIBISHI': 'MITSUBISHI',
#     'MITSIBUSHI': 'MITSUBISHI', 'MITSHUBISHI': 'MITSUBISHI',
#     'MITSUBHISHI': 'MITSUBISHI', 'MITSUBICHI': 'MITSUBISHI',
#     'MITSUBISH': 'MITSUBISHI', 'MITSUBISI': 'MITSUBISHI',
#     'MITSUBISSHI': 'MITSUBISHI', 'MITSUBSCHI': 'MITSUBISHI',
#     'MITSUBSHI': 'MITSUBISHI', 'MITSUBUSHI': 'MITSUBISHI',
#     'MITSUNSHI': 'MITSUBISHI', 'MITTS': 'MITSUBISHI',
#     'MITUBISHI': 'MITSUBISHI', 'MITUS': 'MITSUBISHI',
#     'MITUSBISHI': 'MITSUBISHI', 'MITZUBISHI': 'MITSUBISHI',
#     'MITBISHI': 'MITSUBISHI', 'MITBUSHI': 'MITSUBISHI',
#     'MITH=SHUBISHI': 'MITSUBISHI', 'MITIS': 'MITSUBISHI',
#     'MITISHIBI': 'MITSUBISHI', 'MITISUBISHI': 'MITSUBISHI',
#     'MISTISBUSH': 'MITSUBISHI', 'MISTSUBISHI': 'MITSUBISHI',
#     'MTSUBISHI': 'MITSUBISHI', 'MIT SUBISHI': 'MITSUBISHI',
#     'MIT': 'MITSUBISHI', 'MITSUB': 'MITSUBISHI', 'MITSUBI': 'MITSUBISHI',
#     'MITSIBUISHI': 'MITSUBISHI', 'MIST': 'MITSUBISHI',

#     # PONTIAC
#     'PONT': 'PONTIAC', 'PONTAIC': 'PONTIAC', 'PANTIAC': 'PONTIAC',
#     'PONTIC': 'PONTIAC', 'POTIAC': 'PONTIAC', 'PONT.': 'PONTIAC',

#     # NEW FLYER
#     'NFLY': 'NEW FLYER', 'NWFL': 'NEW FLYER', 'NEW': 'NEW FLYER',
#     'NEW FLYE': 'NEW FLYER', 'NEW FYLER': 'NEW FLYER',
#     'NEW FLER': 'NEW FLYER', 'NEW FLIER': 'NEW FLYER',
#     'NEY FLYER': 'NEW FLYER', 'NEW LYER': 'NEW FLYER',
#     'NEWFLYER': 'NEW FLYER', 'NFWL': 'NEW FLYER',
#     'NEW GLYER': 'NEW FLYER', 'NEW FLYER BUS': 'NEW FLYER',
#     'NEW FLYER IND.': 'NEW FLYER', 'NEW FLYER OF AMERICA': 'NEW FLYER',
#     'NEW FLYER TRANSIT': 'NEW FLYER', 'NEW F': 'NEW FLYER',
#     'HYBRID NEW FLYER': 'NEW FLYER',

#     # KENWORTH
#     'KW': 'KENWORTH', 'KENW': 'KENWORTH', 'KENILWORTH': 'KENWORTH',
#     'KENWOOD': 'KENWORTH', 'KENEWORTH': 'KENWORTH',
#     'KENILWOTH': 'KENWORTH', 'KENNWORTH': 'KENWORTH',
#     'KENOWORTH': 'KENWORTH', 'KENTWORTH': 'KENWORTH',
#     'KENWTH': 'KENWORTH', 'K.W.': 'KENWORTH', 'KENT': 'KENWORTH',
#     'KEN': 'KENWORTH', 'KWNW': 'KENWORTH',

#     # JAGUAR
#     'JAGU': 'JAGUAR', 'JAG': 'JAGUAR', 'JAGAUR': 'JAGUAR',
#     'JAGUARS': 'JAGUAR', 'JAJUAR': 'JAGUAR',

#     # PORSCHE
#     'PORS': 'PORSCHE', 'PORCHE': 'PORSCHE', 'PORSCH': 'PORSCHE',
#     'PORSCE': 'PORSCHE', 'PORSE': 'PORSCHE', 'PORSH': 'PORSCHE',
#     'PORSHCE': 'PORSCHE', 'PORSHE': 'PORSCHE',

#     # LAND ROVER
#     'LANDROVER': 'LAND ROVER', 'LNDR': 'LAND ROVER',
#     'LANDOVER': 'LAND ROVER', 'L ROVER': 'LAND ROVER',
#     'LNDROVER': 'LAND ROVER', 'LLR': 'LAND ROVER',
#     'LAND': 'LAND ROVER', 'ROV': 'LAND ROVER', 'ROVER': 'LAND ROVER',

#     # SATURN
#     'SATU': 'SATURN', 'SATR': 'SATURN', 'SATRN': 'SATURN',
#     'SATUR': 'SATURN', 'SAATURN': 'SATURN', 'SATURNN': 'SATURN',

#     # ISUZU
#     'ISU': 'ISUZU', 'ISUZ': 'ISUZU', 'IZUZU': 'ISUZU',
#     'ISUSU': 'ISUZU', 'ISUZI': 'ISUZU', 'ISUZIU': 'ISUZU',

#     # HARLEY-DAVIDSON
#     'HARLEY': 'HARLEY-DAVIDSON', 'HD': 'HARLEY-DAVIDSON',
#     'HARL': 'HARLEY-DAVIDSON', 'HARLEY D': 'HARLEY-DAVIDSON',
#     'HARLEY DAV': 'HARLEY-DAVIDSON', 'HARLEY DA': 'HARLEY-DAVIDSON',
#     'HAR DAVIDSON': 'HARLEY-DAVIDSON', 'HARDLEY DAVIDSON': 'HARLEY-DAVIDSON',
#     'HARLE DAVIDSON': 'HARLEY-DAVIDSON', 'HARLY DAVIDSON': 'HARLEY-DAVIDSON',
#     'HARLEY DAVISON': 'HARLEY-DAVIDSON', 'HARLEYDAVIDSON': 'HARLEY-DAVIDSON',
#     'HARL D': 'HARLEY-DAVIDSON', 'HARLEY DAVIDSON': 'HARLEY-DAVIDSON',

#     # HUMMER
#     'HUMM': 'HUMMER',

#     # KAWASAKI
#     'KAWK': 'KAWASAKI', 'KAWA': 'KAWASAKI', 'KAWAZAKI': 'KAWASAKI',
#     'KAWKISKI': 'KAWASAKI', 'KAWALSKI': 'KAWASAKI', 'KWAK': 'KAWASAKI',

#     # SUZUKI
#     'SUZI': 'SUZUKI', 'SUZU': 'SUZUKI', 'SUZIKI': 'SUZUKI',
#     'SUSUKI': 'SUZUKI', 'SUZ': 'SUZUKI', 'SUZAKI': 'SUZUKI',
#     'SUZKI': 'SUZUKI', 'SUZUK': 'SUZUKI', 'SUUKI': 'SUZUKI',
#     'ZUZUKI': 'SUZUKI', 'SZUSU': 'SUZUKI',

#     # PETERBILT
#     'PTRB': 'PETERBILT', 'PETERBUILT': 'PETERBILT', 'PETE': 'PETERBILT',
#     'PETER': 'PETERBILT', 'PETER BUILT': 'PETERBILT', 'PETERBLT': 'PETERBILT',
#     'PETERBIL': 'PETERBILT', 'PETEBUILT': 'PETERBILT',
#     'PERTERBUILT': 'PETERBILT', 'PTB': 'PETERBILT', 'PTR': 'PETERBILT',
#     'PETERB': 'PETERBILT', 'PBUILT': 'PETERBILT',
#     'PETERBUILT 389': 'PETERBILT',

#     # SPARTAN
#     'SPAR': 'SPARTAN', 'SPART': 'SPARTAN', 'SPARTIN': 'SPARTAN',
#     'SPTN': 'SPARTAN', 'SPRM': 'SPARTAN',

#     # PIERCE
#     'PIER': 'PIERCE', 'PIRC': 'PIERCE', 'PIRCE': 'PIERCE', 'PIERS': 'PIERCE',
#     'PRCE': 'PIERCE',

#     # MASERATI
#     'MASE': 'MASERATI', 'MASERATTI': 'MASERATI', 'MASERTI': 'MASERATI',
#     'MAZZERATI': 'MASERATI',

#     # SMART
#     'SMRT': 'SMART', 'SMART CAR': 'SMART',

#     # TRIUMPH
#     'TRIU': 'TRIUMPH', 'TRIUMP': 'TRIUMPH', 'TRIMUPH': 'TRIUMPH',
#     'TRIM': 'TRIUMPH',

#     # GENESIS (Hyundai brand)
#     'GENISIS': 'GENESIS', 'GENSIS': 'GENESIS', 'GENS': 'GENESIS',
#     'GENU': 'GENESIS',

#     # SCION
#     'SCIO': 'SCION', 'SCIONE': 'SCION',

#     # TESLA
#     'TESL': 'TESLA', 'TELSA': 'TESLA', 'TSLA': 'TESLA', 'TESTLA': 'TESLA',

#     # MINI
#     'MINNI': 'MINI', 'MINI COOP': 'MINI', 'MINICOOPER': 'MINI',
#     'MINI COOPER': 'MINI', 'MNI': 'MINI', 'MNNI': 'MINI',

#     # THOMAS (Bus manufacturer)
#     'THOM': 'THOMAS', 'THMS': 'THOMAS', 'THOMAS BUILT': 'THOMAS',
#     'THOMP': 'THOMAS', 'THOMA': 'THOMAS', 'THOMASS': 'THOMAS',
#     'THOMMAS': 'THOMAS', 'THOMS': 'THOMAS', 'THAOMAS': 'THOMAS',
#     'THIMAS': 'THOMAS', 'THMS BU': 'THOMAS', 'THOM BU': 'THOMAS',
#     'THOM BUS': 'THOMAS', 'THOMAS BLUE BIRD': 'THOMAS',
#     'THOMAS BUILT BUS': 'THOMAS', 'THOMAS BUILT BUSES': 'THOMAS',
#     'THOMAS BUS': 'THOMAS', 'THOMAS BUS CO': 'THOMAS',
#     'THOMAS-BUILT': 'THOMAS', 'THOMSON': 'THOMAS',

#     # GILLIG (Bus manufacturer)
#     'GILL': 'GILLIG', 'GILG': 'GILLIG', 'GILIG': 'GILLIG',
#     'GIL': 'GILLIG', 'GILLIC': 'GILLIG', 'GILLIAN': 'GILLIG',
#     'GILLIS': 'GILLIG', 'GILLAG': 'GILLIG', 'GILLG': 'GILLIG',
#     'GILLIAM': 'GILLIG', 'GILLIA': 'GILLIG', 'GILLIB': 'GILLIG',
#     'GILLIE': 'GILLIG', 'GILLIGAN': 'GILLIG', 'GILLARD': 'GILLIG',
#     'GILLEM': 'GILLIG', 'GILLAM': 'GILLIG', 'GILLAN': 'GILLIG',
#     'GILLILAND': 'GILLIG', 'GILLILG': 'GILLIG', 'GILLLIG': 'GILLIG',
#     'GILLIT': 'GILLIG', 'GILLMAN': 'GILLIG', 'GILLS': 'GILLIG',
#     'GILLY': 'GILLIG', 'GIUIG': 'GILLIG', 'GGILLIG': 'GILLIG',
#     'GIILIG': 'GILLIG', 'GILILG': 'GILLIG', 'GILIQBUS': 'GILLIG',
#     'GLLIG': 'GILLIG', 'GUILLIG': 'GILLIG', 'GILB': 'GILLIG',
#     'GILG BU': 'GILLIG', 'GILGIN': 'GILLIG', 'GILL BU': 'GILLIG',
#     'GILL BUS': 'GILLIG', 'GILL.': 'GILLIG', 'GILLIGE': 'GILLIG',
#     'GILLLIG BU': 'GILLIG', 'GILLIG BUS': 'GILLIG', 'GILLIG LLC': 'GILLIG',
#     'GIILIG': 'GILLIG', 'GIILIAM': 'GILLIG',

#     # ALFA ROMEO
#     'ALFA': 'ALFA ROMEO', 'ALFA ROMERO': 'ALFA ROMEO',

#     # GRUMMAN
#     'GRUMAN': 'GRUMMAN', 'GRUMIN': 'GRUMMAN', 'GRUMMAN ALLIED': 'GRUMMAN',
#     'GRUMMAN OLSEN': 'GRUMMAN', 'GRUMMAN/GMC': 'GRUMMAN',
#     'GRUMMLV': 'GRUMMAN', 'GRUMMON OLSEN': 'GRUMMAN',
#     'GRUMMUN': 'GRUMMAN', 'GRUNM': 'GRUMMAN', 'GRUNMAN': 'GRUMMAN',

#     # DUCATI
#     'DUCA': 'DUCATI',

#     # SAAB
#     'SAA': 'SAAB', 'SABB': 'SAAB',

#     # MERCURY
#     'MECURY': 'MERCURY', 'MUCURY': 'MERCURY', 'MURCERY': 'MERCURY',
#     'MURCURY': 'MERCURY', 'MERCRY': 'MERCURY', 'MERCZ': 'MERCURY',

#     # OLDSMOBILE
#     'OLDS': 'OLDSMOBILE',

#     # PLYMOUTH
#     'PLYM': 'PLYMOUTH', 'PLYMOTH': 'PLYMOUTH',

#     # DAIMLER
#     'DAIM': 'DAIMLER',

#     # INTERNATIONAL (Truck)
#     'INTL': 'INTERNATIONAL', 'INTE': 'INTERNATIONAL', 'INT': 'INTERNATIONAL',
#     'INTER': 'INTERNATIONAL', 'INTERN': 'INTERNATIONAL',
#     'INTERNAIONAL': 'INTERNATIONAL', 'INTERNATINAL': 'INTERNATIONAL',
#     'INTERNATINOAL': 'INTERNATIONAL', 'INTERNATIOAL': 'INTERNATIONAL',
#     'INTERNATION': 'INTERNATIONAL', 'INTL TK': 'INTERNATIONAL',
#     'INTL TRUCK': 'INTERNATIONAL', 'INTERNATIONAL HRVST': 'INTERNATIONAL',

#     # STERLING
#     'STERL': 'STERLING', 'STLG': 'STERLING', 'STRN': 'STERLING',
#     'STRG': 'STERLING', 'STELING': 'STERLING', 'STIRLING': 'STERLING',
#     'STER': 'STERLING',

#     # ORION (Bus)
#     'ORIO': 'ORION', 'ORIN': 'ORION', 'ORI': 'ORION',
#     'ORIAN': 'ORION', 'ORIAN BLUE': 'ORION',

#     # NOVA BUS
#     'NOVB': 'NOVA BUS', 'NOVABUS': 'NOVA BUS', 'NOVA': 'NOVA BUS',

#     # IC BUS
#     'IC': 'IC BUS', 'IC CORP': 'IC BUS', 'IC CORPORA': 'IC BUS',
#     'IC INTERNATIONAL': 'IC BUS', 'ICBUS': 'IC BUS', 'ICRB': 'IC BUS',
#     'ICRP': 'IC BUS',

#     # MCI (Bus)
#     'MCIN': 'MCI',

#     # VAN HOOL (Bus)
#     'VANH': 'VAN HOOL', 'VANHOOL': 'VAN HOOL', 'VNHL': 'VAN HOOL',

#     # BENTLEY
#     'BENT': 'BENTLEY',

#     # FERRARI
#     'FERR': 'FERRARI',

#     # LAMBORGHINI
#     'LAMO': 'LAMBORGHINI', 'LAMBOURGHINI': 'LAMBORGHINI',

#     # UNKNOWN
#     'UNK': 'UNKNOWN', 'UNKN': 'UNKNOWN', 'UNKNOW': 'UNKNOWN',
#     'UNKOWN': 'UNKNOWN',

#     # GENERAL ELECTRIC
#     'GENE': 'GENERAL ELECTRIC',

#     # WORKHORSE
#     'WRKH': 'WORKHORSE', 'WRKHS': 'WORKHORSE',

#     # WESTERN STAR
#     'WSTR': 'WESTERN STAR', 'WSTRG': 'WESTERN STAR',
#     'WEST STAR': 'WESTERN STAR', 'WESTERN': 'WESTERN STAR',

#     # THOMPSON
#     'THOMP': 'THOMPSON',

#     # SEAGRAVE
#     'SEAG': 'SEAGRAVE',

#     # AUTOCAR
#     'AUTOCART': 'AUTOCAR',

#     # BLUE BIRD
#     'BLUEBIRD': 'BLUE BIRD',

#     # CRIMSON FIRE
#     'CRIMSON': 'CRIMSON FIRE', 'CHRIMSON': 'CRIMSON FIRE',
#     'RIMSON': 'CRIMSON FIRE',

#     # KTM
#     'KTM AG': 'KTM',

#     # ROYAL ENFIELD
#     'ROYALENFIELD': 'ROYAL ENFIELD',

#     # APRILIA
#     'APRILLA': 'APRILIA',

#     # PREVOST
#     'PREVO': 'PREVOST',

#     # STARCRAFT
#     'STACRAFT': 'STARCRAFT',
# }

# # ============================================================
# # VEHICLE MODEL - Standardization Mapping
# # ============================================================
# model_mapping = {

#     # CAMRY
#     'CAMRY': 'CAMRY',

#     # COROLLA
#     'COROLLA': 'COROLLA',

#     # CIVIC
#     'CIVIC': 'CIVIC',

#     # CRV -> CR-V
#     'CRV': 'CR-V',

#     # ALTIMA
#     'ALTIMA': 'ALTIMA',

#     # ELANTRA
#     'ELANTRA': 'ELANTRA',

#     # SONATA
#     'SONATA': 'SONATA',

#     # PRIUS
#     'PRIUS': 'PRIUS',

#     # JETTA
#     'JETTA': 'JETTA',

#     # FORESTER
#     'FORESTER': 'FORESTER',

#     # CHEROKEE
#     'CHEROKEE': 'CHEROKEE',

#     # TAHOE
#     'TAHOE': 'TAHOE',

#     # MAXIMA
#     'MAXIMA': 'MAXIMA',

#     # MUSTANG
#     'MUSTANG': 'MUSTANG',

#     # ACCENT
#     'ACCENT': 'ACCENT',

#     # FORTE
#     'FORTE': 'FORTE',

#     # VERSA
#     'VERSA': 'VERSA',

#     # OUTLANDER
#     'OUTLANDER': 'OUTLANDER',

#     # GOLF
#     'GOLF': 'GOLF',

#     # RANGE ROVER (model)
#     'RANG ROVER': 'RANGE ROVER', 'RANGER ROVER': 'RANGE ROVER',
#     'RNG RVR': 'RANGE ROVER', 'RANGROV': 'RANGE ROVER',
#     'RANG': 'RANGE ROVER', 'RANGE': 'RANGE ROVER',

#     # GENESIS (model)
#     'GENISIS': 'GENESIS', 'GENSIS': 'GENESIS', 'GENS': 'GENESIS',

#     # ECONOLINE
#     'ECONOLINE': 'ECONOLINE',

#     # F-150
#     'F150': 'F-150',

#     # F-250
#     'F250': 'F-250',

#     # E-250
#     'E250': 'E-250',

#     # YUKON
#     'YUKON': 'YUKON',

#     # ECLIPSE
#     'ECLIPSE': 'ECLIPSE',

#     # ION
#     'ION': 'ION',

#     # SPARK
#     'SPARK': 'SPARK',

#     # SPRINTER
#     'SPRINTER': 'SPRINTER',

#     # LEAF
#     'LEAF': 'LEAF',

#     # SUBURBAN
#     'SUBURBAN': 'SUBURBAN',

#     # SANTA FE
#     'SANTA FE': 'SANTA FE',

#     # BRONCO
#     'BRONCO': 'BRONCO',

#     # CORVETTE
#     'CORVETTE': 'CORVETTE',

#     # C-HR
#     'C-HR': 'C-HR',

#     # SCION (model name used)
#     'SCIO': 'SCION',

#     # SCHOOL BUS
#     'SCHOOL': 'SCHOOL BUS', 'SCHOOL BUS': 'SCHOOL BUS',

#     # FIRE TRUCK
#     'FIRETRUCK': 'FIRE TRUCK', 'FIRE': 'FIRE TRUCK',

#     # POSTAL / MAIL
#     'POSTAL TRUCK': 'POSTAL TRUCK', 'POST OFFICE': 'POSTAL TRUCK',
#     'US POSTAL': 'POSTAL TRUCK', 'POSTAL': 'POSTAL TRUCK',

#     # UNKNOWN
#     'UNK': 'UNKNOWN', 'UNKN': 'UNKNOWN', 'UNKNOW': 'UNKNOWN',
#     'UNKOWN': 'UNKNOWN',

#     # PRIUS
#     'PRIUS': 'PRIUS',

#     # RAM
#     'RAM': 'RAM',

#     # SEDAN (body type used as model)
#     'SEDAN': 'SEDAN',

#     # SUV (body type used as model)
#     'SUV': 'SUV',

#     # VAN
#     'VAN': 'VAN',

#     # TRUCK
#     'TRUCK': 'TRUCK',

#     # BUS
#     'BUS': 'BUS', 'BU': 'BUS',

#     # TK (Truck abbreviation)
#     'TK': 'TRUCK',

#     # TBU (Transit Bus)
#     'TBU': 'TRANSIT BUS', 'TUBU': 'TRANSIT BUS',

#     # TRANSIT
#     'TRANSIT': 'TRANSIT',

#     # DUMP (Dump Truck)
#     'DUMP': 'DUMP TRUCK',

#     # UTILIMASTER
#     'UTILIMASTER': 'UTILIMASTER',

#     # MAZDA 3
#     'MAZDA 3': 'MAZDA3',

#     # RDX
#     'RDX': 'RDX',

#     # TL
#     'TL': 'TL',

#     # 4S (trim/body style)
#     '4S': '4S',

#     # 4D (4 door)
#     '4D': '4D',

#     # 2D (2 door)
#     '2D': '2D',
# }

# def standardize_column(df, column_name, mapping_dict):
#     """
#     Replace variations with standardized names.
#     Strips whitespace and converts to uppercase before matching.
#     """
#     df[column_name] = (
#         df[column_name]
#         .astype(str)
#         .str.strip()
#         .str.upper()
#         .replace(mapping_dict)
#     )
#     return df

# df = standardize_column(df, 'Vehicle Make', make_mapping)
# df = standardize_column(df, 'Vehicle Model', model_mapping)

# # ============================================================
# # STEP 3: Save cleaned file
# # ============================================================
# df.to_csv('cleaned_vehicles.csv', index=False)





# df['Crash Date/Time'] = pd.to_datetime(df['Crash Date/Time'])

# df['Crash Date'] = df['Crash Date/Time'].dt.date
# df['Crash Time'] = df['Crash Date/Time'].dt.strftime('%I:%M:%S %p')

# df.drop(columns=['Crash Date/Time'], inplace=True)





# # ACRS Report Type ki position dhundho
# acrs_index = df.columns.get_loc('ACRS Report Type')

# # Crash Date aur Crash Time ko end se hatao
# crash_date_col = df.pop('Crash Date')
# crash_time_col = df.pop('Crash Time')

# # ACRS Report Type se PEHLE insert karo
# df.insert(acrs_index,     'Crash Date',  crash_date_col)
# df.insert(acrs_index + 1, 'Crash Time',  crash_time_col)

# # Save
# df.to_csv('cleaned_vehicles_loc.csv', index=False)

# print("✅ Done! Crash Date aur Crash Time ab ACRS Report Type se pehle hain.")
# print(f"Columns order check:\n{list(df.columns)}")





# df['Driver At Fault'] = df['Driver At Fault'].astype(str).str.strip().str.upper()

# df = df[df['Driver At Fault'] != 'UNKNOWN']

# df['Driver At Fault'] = df['Driver At Fault'].map({
#     'YES': 1,
#     'NO': 0
# })





# bike_makes = {
#     'HARLEY-DAVIDSON', 'KAWASAKI', 'YAMAHA', 'SUZUKI', 'DUCATI',
#     'KTM', 'TRIUMPH', 'APRILIA', 'INDIAN', 'VICTORY', 'ROYAL ENFIELD',
#     'MOTO GUZZI', 'VESPA', 'PIAGGIO', 'ZERO', 'CANNONDALE', 'TREK',
#     'SCHWINN', 'CERVELO',
# }

# bike_models = {
#     'MOTORCYCLE', 'BIKE', 'SCOOTER', 'MOPED',
# }

# bus_truck_makes = {
#     'FREIGHTLINER', 'MACK', 'PETERBILT', 'KENWORTH', 'VOLVO',
#     'INTERNATIONAL', 'STERLING', 'WESTERN STAR', 'AUTOCAR',
#     'THOMAS', 'GILLIG', 'NEW FLYER', 'ORION', 'NOVA BUS',
#     'IC BUS', 'NABI', 'MCI', 'VAN HOOL', 'BLUE BIRD',
#     'HINO', 'ISUZU', 'UD', 'NAVISTAR', 'SPARTAN', 'PIERCE',
#     'SEAGRAVE', 'CRIMSON FIRE', 'GRUMMAN', 'UTILIMASTER',
#     'WORKHORSE', 'FLYER', 'STARCRAFT', 'GOSHEN',
# }

# bus_truck_models = {
#     'BUS', 'TRANSIT BUS', 'SCHOOL BUS', 'FIRE TRUCK', 'DUMP TRUCK',
#     'TRUCK', 'POSTAL TRUCK', 'TRANSIT', 'SEMI',
# }

# # ============================================================
# # STEP 3: Classification Function
# # ============================================================

# def classify_vehicle(make, model):
#     make  = str(make).strip().upper()
#     model = str(model).strip().upper()

#     # Bike check
#     is_bike = 0
#     if make in bike_makes and model in bike_models:
#         is_bike = 1
#     elif make in bike_makes:
#         is_bike = 1
#     elif model in bike_models:
#         is_bike = 1

#     # Bus/Truck check
#     is_bus_truck = 0
#     if make in bus_truck_makes:
#         is_bus_truck = 1
#     elif model in bus_truck_models:
#         is_bus_truck = 1

#     # Car check (agar bike ya bus/truck nahi)
#     is_car = 0
#     if is_bike == 0 and is_bus_truck == 0:
#         is_car = 1

#     return is_bike, is_car, is_bus_truck

# # ============================================================
# # STEP 4: Apply & Insert after 'Vehicle Model'
# # ============================================================

# df[['Is_Bike', 'Is_Car', 'Is_Bus_Truck']] = df.apply(
#     lambda row: classify_vehicle(row['Vehicle Make'], row['Vehicle Model']),
#     axis=1,
#     result_type='expand'
# )


# model_col_index  = df.columns.get_loc('Vehicle Model')
# is_bike_col      = df.pop('Is_Bike')
# is_car_col       = df.pop('Is_Car')
# is_bus_truck_col = df.pop('Is_Bus_Truck')

# df.insert(model_col_index + 1, 'Is_Bike',      is_bike_col)
# df.insert(model_col_index + 2, 'Is_Car',       is_car_col)
# df.insert(model_col_index + 3, 'Is_Bus_Truck', is_bus_truck_col)

# # ============================================================
# # STEP 5: Save
# # ============================================================
# df.to_csv('cleaned_vehicles_binary.csv', index=False)







# print(df['Vehicle Make'].unique())
# print(df['Vehicle Make'].value_counts())

# print({v: list(df['Vehicle Make']).count(v) for v in sorted(set(df['Vehicle Make'].dropna()))})
# print("============================================================")
# print({v: list(df['Vehicle Model']).count(v) for v in sorted(set(df['Vehicle Make'].dropna()))})

# df.to_csv("cleaned_vehicles.csv", index=False)
# print(df.isnull().sum())



