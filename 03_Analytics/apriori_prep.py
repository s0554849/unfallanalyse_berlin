# Created by benjaminwuthe at 09.12.19

# Prepare categorical data for later apriori analysis in R

import pandas as pd

# load data
try:
    df_unfall = pd.read_csv(r"""../01_Source/Verkehrsunfälle_2018_clean.csv""")
except:
    df_unfall = pd.read_csv("""01_Source/Verkehrsunfälle_2018_clean.csv""")

#df_geo = pd.read_csv('01_Source/geo_information.csv', sep=';')

df_unfall.columns

cols_to_drop = ['Unnamed: 0', 'X', 'Y', 'OBJECTID_1', 'OBJECTID', 'UREGBEZ','ULAND','UKREIS', 'UGEMEINDE',
                'UJAHR','LINREFX','LINREFY']

df_unfall_clean = df_unfall.drop(cols_to_drop, axis=1)

# rename columns
df_unfall_clean.columns = ['Monat','Stunde','Wochentag',
                           'Unfallaktegorie','UnfallArt','UnfallTyp','Lichverhaeltniss','Fahrrad','PKW','Fuss',
                           'KraftRad','GueterKFZ','Sonstiges','StrassenZustand']

# Get Dummies for the DataFrame to make it categorical
df_dummies = pd.get_dummies(df_unfall_clean.astype('str'))

# For the following DFs is the value 0 not a category!
# e.g. month 1-12 but lichtverhaeltnis 0 is daylight
df_monat = df_dummies.iloc[:,0:12] # DataFrame with just months
df_stunde = df_dummies.iloc[:,12:37] # DataFrame with just the days
df_tag = df_dummies.iloc[:,36:43]

# the following DFs are with category 0


new_list = []

def iter_col(x, df):
    """
    Appends column names to new_list
    :param x:
    :return:
    """
    new_list.append(df.columns[x[:]==1])

def prep(new_list):
    """
    edit the index list from new_list
    :return:
    """
    x=[]
    for el in new_list:
        x.append(el[0])

    return x

def process_feature(df):
    global new_list
    new_list = []
    prep(new_list)
    df.transpose().apply(lambda x: iter_col(x, df), axis=0)

    return prep(new_list)


df_dummies['monat'] = process_feature(df_monat)
df_dummies['tag'] = process_feature(df_monat)
df_dummies['stunde'] = process_feature(df_tag)



df_dummies.to_csv('01_Source/apriori_data.csv')


#
#
# # new_list = new_list
#
# # Save for testing purpose
# save = df_dummies
# df_dummies = save
#
# new_list =[]
# df_monat.transpose().apply( lambda x: iter_col(x, df_monat), axis =0)
# x = prep(new_list)
# df_dummies['month'] = x
#
# new_list =[]
# x = []
#
# df_days.transpose().apply(lambda x: iter_col(x, df_days), axis =0)
# x = prep(new_list)
# df_dummies['Stunde'] = x
# print(df_dummies)
