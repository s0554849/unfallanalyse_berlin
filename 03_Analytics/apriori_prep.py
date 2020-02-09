# Created by benjaminwuthe at 09.12.19

# Prepare categorical data for later apriori analysis in R

import pandas as pd

# load data
try:
    df_unfall = pd.read_csv(r"""../01_Source/Verkehrsunfälle_2018_clean.csv""")
except:
    df_unfall = pd.read_csv("""01_Source/Verkehrsunfälle_2018_clean.csv""")

#df_geo = pd.read_csv('01_Source/geo_information.csv', sep=';')

#df_unfall.columns

cols_to_drop = ['Unnamed: 0', 'X', 'Y', 'OBJECTID_1', 'OBJECTID', 'UREGBEZ','ULAND','UKREIS', 'UGEMEINDE',
                'UJAHR','LINREFX','LINREFY']

df_unfall_clean = df_unfall.drop(cols_to_drop, axis=1)

# rename columns
df_unfall_clean.columns = ['Monat','Stunde','Wochentag',
                           'Unfallaktegorie','UnfallArt','UnfallTyp','Lichverhaeltniss','Fahrrad','PKW','Fuss',
                           'KraftRad','GueterKFZ','Sonstiges','StrassenZustand']

# Get Dummies for the DataFrame to make it categorical
df_dummies = pd.get_dummies(df_unfall_clean.astype('str'))

# drop columns where 0 is no category - like fahrrad 0 --> not involved unnessesary
# lichtverhältnis 0 --> normal --> nessesary
dummy_desription = df_dummies.describe()
cols_to_drop_dummies = ['Fahrrad_0', 'PKW_0', 'Fuss_0','KraftRad_0','GueterKFZ_0', 'Sonstiges_0']
df_dummies = df_dummies.drop(cols_to_drop_dummies, axis = 1)

columns_rename = ['Januar','Oktober','November','Dezember','Februar','März','April','Mai','Juni','Juli','Augus',
                  'September','0 Uhr','1 Uhr','10 Uhr','11 Uhr','12 Uhr','13 Uhr','14 Uhr','15 Uhr','16 Uhr',
                  '17 Uhr','18 Uhr','19 Uhr','2 Uhr','20 Uhr','21 Uhr','22 Uhr','23 Uhr','3 Uhr','4 Uhr','5 Uhr',
                  '6 Uhr','7 Uhr','8 Uhr','9 Uhr','Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag',
                  'Samstag','Unfallkategorie: getötet','Unfallkategorie: schwer verletzt',
                  'Unfallkategorie: leicht verletzt',
                  'Unfallart: Unfall anderer Art',
                  'Unfallart: Zusammenstoß mit anfahrendem/ anhaltendem/ruhendem Fahrzeug',
                  'Unfallart: Zusammenstoß mit vorausfahrendem / wartendem Fahrzeug',
                  'Unfallart: Zusammenstoß mit seitlich in gleicher Richtung fahrendem Fahrzeug',
                  'Unfallart: Zusammenstoß mit entgegenkommendem Fahrzeug',
                  'Unfallart: Zusammenstoß mit einbiegendem / kreuzendem Fahrzeug',
                  'Unfallart: Zusammenstoß zwischen Fahrzeug und Fußgänger',
                  'Unfallart: Aufprall auf Fahrbahnhindernis',
                  'Unfallart:Abkommen von Fahrbahn nach rechts',
                  'Unfallart: Abkommen von Fahrbahn nach links',
                  'Unfalltyp: Fahrunfall',
                  'Unfalltyp: Abbiegeunfall',
                  'Unfalltyp: Einbiegen / Kreuzen-Unfall',
                  'Unfalltyp: Überschreiten-Unfall',
                  'Unfalltyp: Unfall durch ruhenden Verkehr',
                  'Unfalltyp: Unfall im Längsverkehr',
                  'Unfalltyp: sonstiger Unfall',
                  'Lichtverhältnis: Tageslicht',
                  'Lichtverhältnis: Dämmerung',
                  'Lichtverhältnis: Dunkelheit','Fahrrad', 'PKW', 'Fussgänger', 'KraftRad', 'Güter KFZ',
                  'Sonstiger Verkehrsteilnehmener',
                  'Straßenzustand: trocken',
                  'Straßenzustand: nass/feucht/schlüpfrig',
                  'Straßenzustand: winterglatt']
df_dummies.columns = columns_rename

tst_df = df_dummies.applymap(lambda x : True if x==1 else False) # change 0 and 1 to false and true

all_unf = [] #stores all accidents

#iterate over all accidents
for rows, cols in df_dummies.iterrows():
    colind = 0
    tep_unf =[] # current accident
    for col in cols:
        if col ==1:
            tep_unf.append(df_dummies.columns[colind])

        colind += 1
    all_unf.append(tep_unf)

df_all[3].unique()

df_all = pd.DataFrame(all_unf)
df_all.to_csv('01_Source/apriori_data2.csv')
df_dummies.to_csv('01_Source/apriori_data_final.csv')

"""THE FOLLOWING CODE IS DEPRECATED"""
        # # For the following DFs is the value 0 not a category!
        # # e.g. month 1-12 but lichtverhaeltnis 0 is daylight
        # df_monat = df_dummies.iloc[:,0:12] # DataFrame with just months
        # df_stunde = df_dummies.iloc[:,12:37] # DataFrame with just the days
        # df_tag = df_dummies.iloc[:,36:43]
        #
        # # the following DFs are with category 0
        #
        #
        # new_list = []
        #
        # def iter_col(x, df):
        #     """
        #     Appends column names to new_list
        #     :param x:
        #     :return:
        #     """
        #     new_list.append(df.columns[x[:]==1])
        #
        # def prep(new_list):
        #     """
        #     edit the index list from new_list
        #     :return:
        #     """
        #     x=[]
        #     for el in new_list:
        #         x.append(el[0])
        #
        #     return x
        #
        # def process_feature(df):
        #     global new_list
        #     new_list = []
        #     prep(new_list)
        #     df.transpose().apply(lambda x: iter_col(x, df), axis=0)
        #
        #     return prep(new_list)
        #
        #
        # df_dummies['monat'] = process_feature(df_monat)
        # df_dummies['tag'] = process_feature(df_monat)
        # df_dummies['stunde'] = process_feature(df_tag)
        #
        #
        #
        #
        #
        # df_dummies.to_csv('01_Source/apriori_data.csv')
        #
        #
        # #
        # #
        # # # new_list = new_list
        # #
        # # # Save for testing purpose
        # # save = df_dummies
        # # df_dummies = save
        # #
        # # new_list =[]
        # # df_monat.transpose().apply( lambda x: iter_col(x, df_monat), axis =0)
        # # x = prep(new_list)
        # # df_dummies['month'] = x
        # #
        # # new_list =[]
        # # x = []
        # #
        # # df_days.transpose().apply(lambda x: iter_col(x, df_days), axis =0)
        # # x = prep(new_list)
        # # df_dummies['Stunde'] = x
        # # print(df_dummies)




