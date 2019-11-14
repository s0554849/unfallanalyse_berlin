# Created by benjaminwuthe at 14.11.19

# Datacleaning for Projekt Wissensmanagement

# imports
import pandas as pd
import utm # package to generate lat long from given data -
import geopandas as gpd
"""Grafische Koordinate 1 und
Grafische Koordinate 2
LINREFX und LINREFY
bilden die Koordinate des
auf dem Straßenabschnitt
liegenden Unfallortes
(UTM
-Koordinate des
Referenzsystems ETRS89,
Zone 32N)"""

#Files and path
root_path = '/Users/benjaminwuthe/Google Drive/Wissensmngt. Projekt/src/'
f_join_old = "U_VM_A_L_BRW.geojson"
f_join = "U_VM_A_L_BRW_edit.geojson"
f_districts = "Einwohner.csv"



def get_lat_long():
    df = pd.read_csv('Unfallorte2018.txt', sep=';')
    df.info()
    df['LINREFX'] = df['LINREFX'].apply(lambda x : x.replace(',','.'))
    df['LINREFY'] = df['LINREFY'].apply(lambda x: x.replace(',', '.'))
    df.shape
    df.loc[0, ['LINREFX', 'LINREFY']]
    coords = utm.to_latlon( float(df.loc[0, ['LINREFX']]),  float(df.loc[0, ['LINREFY']]), zone_letter='N', zone_number=32)
    print(coords)

def clean_unfaelle(path = None):
    """
    :param path: path to original file
    :return:
    """
    import pandas as pd
    if path ==None:
        path = '/Users/benjaminwuthe/Google Drive/Wissensmngt. Projekt/src/Verkehrsunfälle_2018.csv'#/Users/benjaminwuthe/Downloads/Verkehrsunfälle_2018.csv'
    df2 = pd.read_csv(path, sep=",")
    df2.shape
    df2 = df2[df2['ULAND']==11] # ULAND 11 = Berlin
    df2.to_csv('/Users/benjaminwuthe/Google Drive/Wissensmngt. Projekt/src/Verkehrsunfälle_2018_clean.csv')

# clean_unfaelle()

# get_lat_long()


def beleuchtung_clean(path_source, path_desti):
    import matplotlib.pyplot as plt
    import geopandas as gpd

    path = '/Users/benjaminwuthe/Google Drive/Wissensmngt. Projekt/src/U_VM_A_L_BRW.geojson'
    geo_df = gpd.read_file(path)

    geo_df.columns
    # geo_df = geo_df[geo_df['WERT_VES']<200]

    geo_new =  geo_df.geometry[0:20]

    geo_df = geo_df.to_crs(epsg=4326)
    # geo_df.plot()
    geo_df.shape

    # geo_wrong = geo_df.geometry

    # print(geo_df.get('North'))
    geo_df.to_file("/Users/benjaminwuthe/Desktop/U_VM_A_L_BRW_.geojson", driver='GeoJSON')



def get_einwohner():
    """
    Get inhabitans of berlins districts and export as csv.
    """
    import pandas as pd

    df_wiki = pd.read_html(
        'https://de.wikipedia.org/wiki/Liste_der_Bezirke_und_Ortsteile_Berlins'
    )
    df_wiki[1].to_csv(root_path + 'Einwohner.csv')
    return df_wiki[1]


def clear_joshis_file (df = None):
    """
    Wrong geo-format. Change it and save
    :return: geopandas df
    """

    if df == None :
        geo_df = gpd.read_file(root_path+f_join_old) #original file
    else:
        geo_df = df

    print(geo_df.crs)  # {'init': 'epsg:5555'} <-- this is the wron format
    crs = {'init': 'epsg:5555'} # Desitnation format
    geo_df.crs = crs
    export_df = geo_df.to_crs(epsg=4326)
    export_df.to_file("/Users/benjaminwuthe/Desktop/U_VM_A_L_BRW_edit.geojson", driver='GeoJSON')
    return export_df

def id_switcher(left_df, right_df):
    """

    :param left_df: main df
    :param right_df: merger df, col 1 = merger column; col 2 corresponding value
    :return: dataframe
    """
    on_column = right_df.columns[0]
    left_df[on_column] = left_df.merge(right_df, on = on_column)['Value']
    return left_df

# id_switcher()



def prepare_data():



    # switch cols with id with corresponding value

    # load data
    df = gpd.read_file(root_path+f_join)

    # Unfallart
    uart_df = pd.DataFrame({'UART' : [1,2,3,4,5,6,7,8,9,0], 'Value':["Zusammenstoß mit anfahrendem / anhaltendem / ruhendem Fahrzeug",
                "Zusammenstoß mit vorausfahrendem / wartendem Fahrzeug",
                "Zusammenstoß mit seitlich in gleicher Richtung fahrendem Fahrzeug",
                "Zusammenstoß mit entgegenkommendem Fahrzeug",
                "Zusammenstoß mit einbiegendem / kreuzendem Fahrzeug",
                "Zusammenstoß zwischen Fahrzeug und Fußgänger",
                "Aufprall auf Fahrbahnhindernis",
                "Abkommen von Fahrbahn nach rechts",
                "Abkommen von Fahrbahn nach links",
                "Unfall anderer Art"]})

    df = id_switcher(df, uart_df)

    # Wochentag
    wochentag_df = pd.DataFrame({'UWOCHENTAG':[1,2,3,4,5,6,7],
                                 'Value':['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag']})
    df = id_switcher(df, wochentag_df)

    # Unfallkategorie
    ukategorie_df = pd.DataFrame({'UKATEGORIE':[1,2,3], 'Value':['Unfall mit Getöteten', 'Unfall mit Schwerverletzten', 'Unfall mit Leichtverletzten']})
    df = id_switcher(df, ukategorie_df)

    return df

fial_df = prepare_data()

# x = id_switcher(df, wochentag_df)

def kpi_analyzer():
    """
    Take several open data sources, combine them and compute kpis
    :return: pandas DataFrame
    """


    df_join =  gpd.read_file(root_path + f_join)
    df_districts = pd.read_csv(root_path + f_districts, sep = ';')

    df_kombined =  df_join.merge(df_districts, on='Bezirk')
    df_join.columns

def read_from_google():
    # https: // drive.google.com / open?id = 1

    googleSheetId = 'gBvP1niNLFG8fjvtutTbx20gdA5tacLu'
    worksheetName = 'Einwohner'
    URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
        googleSheetId,
        worksheetName
    )

    df = pandas.read_csv(URL)
    print(df)
