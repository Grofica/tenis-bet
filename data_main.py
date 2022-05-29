import pandas as pd
import random

def replacing(list, column_name, dataset):
    for i in range(len(list)):
        dataset[column_name] = dataset[column_name].replace(str(list[i]), str(list.index(list[i])+1))
    return dataset
def delete_duplicates(first_list, second_list):
    in_first = set(first_list)
    in_second = set(second_list)

    in_second_but_not_in_first = in_second - in_first

    result = first_list + list(in_second_but_not_in_first)
    return result
def loading_data(in_data):
    #ucitavanje podataka
    data = pd.read_csv(in_data)
    df = pd.DataFrame(data)

    #biranje kolona koje su vazne za karakteristike igraca i turnira
    df_filtered = df[['draw_size','tourney_date','tourney_level','surface','winner_entry','winner_hand','winner_ht','winner_age','loser_entry','loser_hand','loser_ht','loser_age','best_of','round','winner_rank','loser_rank','winner_rank_points','loser_rank_points','winner_ioc','loser_ioc']]


    #desna ruka je 1, a leva 0
    df_filtered['winner_hand'] = df_filtered["winner_hand"].replace("R","1")
    df_filtered['winner_hand'] = df_filtered["winner_hand"].replace("L","0")
    df_filtered['loser_hand'] = df_filtered["loser_hand"].replace("R", "1")
    df_filtered['loser_hand'] = df_filtered["loser_hand"].replace("L", "0")
    df_filtered['winner_hand'] = df_filtered["winner_hand"].replace("U", "1")
    df_filtered['loser_hand'] = df_filtered["loser_hand"].replace("U", "1")

    #vrednosti su date po tome koliko koji tip turnira donosi poena na ATP listi
    df_filtered['tourney_level'] = df_filtered['tourney_level'].replace("G", "2000")
    df_filtered['tourney_level'] = df_filtered['tourney_level'].replace("M", "1000")
    df_filtered['tourney_level'] = df_filtered['tourney_level'].replace("F", "1300")
    df_filtered['tourney_level'] = df_filtered['tourney_level'].replace("A", "375")
    df_filtered['tourney_level'] = df_filtered['tourney_level'].replace("D", '250')
    df_filtered['tourney_level'] = df_filtered['tourney_level'].replace("C", "102")
    df_filtered['tourney_level'] = df_filtered['tourney_level'].replace("S", '27')


    # ovo je donete subjektivno na osnovu toga kako je igrac dosao na turnir, da li pozvan od strane organizatora,
    #srecni gubitnik ili kvalifikacijom....
    df_filtered['winner_entry'] = df_filtered['winner_entry'].replace("WC", '100')
    df_filtered['winner_entry'] = df_filtered['winner_entry'].replace("Q", '80')
    df_filtered['winner_entry'] = df_filtered['winner_entry'].replace("PR", '70')
    df_filtered['winner_entry'] = df_filtered['winner_entry'].replace("ITF", '50')
    df_filtered['winner_entry'] = df_filtered['winner_entry'].replace("LL", '30')

    df_filtered['loser_entry'] = df_filtered['loser_entry'].replace("WC", '100')
    df_filtered['loser_entry'] = df_filtered['loser_entry'].replace("Q", '80')
    df_filtered['loser_entry'] = df_filtered['loser_entry'].replace("PR", '70')
    df_filtered['loser_entry'] = df_filtered['loser_entry'].replace("ITF", '50')
    df_filtered['loser_entry'] = df_filtered['loser_entry'].replace("LL", '30')
    #ako je neko dosao na drugi nacin osim nabrojanog dodeljuje mu se 50 jer je to prosek raspona vrednosti koje su davane
    list_knowing_values = ['WC','Q','PR','ITF','LL']
    list_values_loser = df_filtered['loser_entry'].unique()
    list_values_winner = df_filtered['winner_entry'].unique()
    for x in list_values_loser:
        if x not in list_knowing_values:
            df_filtered['loser_entry'] = df_filtered['loser_entry'].replace(x, '50')
    for x in list_values_winner:
        if x not in list_knowing_values:
            df_filtered['winner_entry'] = df_filtered['winner_entry'].replace(x, '50')

    #podlogama se dodeljuju numericke vrednosti
    list_surface = df_filtered.surface.unique()
    list_surface = list(list_surface)
    df_filtered = replacing(list_surface, "surface", df_filtered)

    #nacionalnosti igraca se prvo spajaju u jednu listu pa se zamenju numerickim vrednostima
    list_winner_ioc = list(df_filtered['winner_ioc'].unique())
    list_loser_ioc = list(df_filtered['loser_ioc'].unique())
    nationality = delete_duplicates(list_winner_ioc,list_loser_ioc)
    df_filtered = replacing(nationality,"winner_ioc",df_filtered)
    df_filtered = replacing(nationality,"loser_ioc",df_filtered)

    # pretvaranje runde u numericku vrednost po tome koliko je blizu finala
    for l in range(len(df_filtered['round'])):
        rd = str(df_filtered['round'][l])
        if rd.startswith("R") and not rd.startswith("RR"):
            df_filtered['round'] = df_filtered['round'].replace(rd, int(rd[1:]))
        elif rd.startswith("Q") and not rd.startswith("QF"):
            df_filtered['round'] = df_filtered['round'].replace(rd, 2 ** (12 - int(rd[1:])))
        elif rd not in ['F', 'SF', 'QF', 'RR', 'BR']:
            df_filtered['round'] = df_filtered['round'].replace(rd, 100)

    df_filtered['round'] = df_filtered['round'].replace("F", "2")
    df_filtered['round'] = df_filtered['round'].replace("SF", "4")
    df_filtered['round'] = df_filtered['round'].replace("QF", "8")
    df_filtered['round'] = df_filtered['round'].replace("RR", "65")
    df_filtered['round'] = df_filtered['round'].replace("BR", "100")  # proveriti sta je BR sa gospodinom sa githuba

    #prati se mesec i godina, dan nije toliko bitan
    year = []
    month = []
    for x in df_filtered['tourney_date']:
        x = str(x)
        year.append(x[:4])
        month.append(x[4:6])
    df_filtered['year'] = year
    df_filtered['month'] = month

    #nove pobednik, player1, player2 kolone
    winner_list = []

    pl1_hand_list = []
    pl1_entry_list = []
    pl1_ht_list = []
    pl1_age_list = []
    pl1_rank_list = []
    pl1_rank_points_list = []
    pl1_ioc_list = []

    pl2_hand_list = []
    pl2_entry_list = []
    pl2_ht_list = []
    pl2_age_list = []
    pl2_rank_list = []
    pl2_rank_points_list = []
    pl2_ioc_list = []

    # randomizacija kolona winner i loser
    for i in range(len(df_filtered.index)):
        win_id = random.randint(1, 2)
        winner_list.append(win_id)
        if win_id == 1:
            pl1_hand_list.append(df_filtered['winner_hand'][i])
            pl1_entry_list.append(df_filtered['winner_entry'][i])
            pl1_ht_list.append(df_filtered['winner_ht'][i])
            pl1_age_list.append(df_filtered['winner_age'][i])
            pl1_rank_list.append(df_filtered['winner_rank'][i])
            pl1_rank_points_list.append(df_filtered['winner_rank_points'][i])
            pl1_ioc_list.append(df_filtered['winner_ioc'][i])

            pl2_hand_list.append(df_filtered['loser_hand'][i])
            pl2_entry_list.append(df_filtered['loser_entry'][i])
            pl2_ht_list.append(df_filtered['loser_ht'][i])
            pl2_age_list.append(df_filtered['loser_age'][i])
            pl2_rank_list.append(df_filtered['loser_rank'][i])
            pl2_rank_points_list.append(df_filtered['loser_rank_points'][i])
            pl2_ioc_list.append(df_filtered['loser_ioc'][i])

        else:
            pl1_hand_list.append(df_filtered['loser_hand'][i])
            pl1_entry_list.append(df_filtered['loser_entry'][i])
            pl1_ht_list.append(df_filtered['loser_ht'][i])
            pl1_age_list.append(df_filtered['loser_age'][i])
            pl1_rank_list.append(df_filtered['loser_rank'][i])
            pl1_rank_points_list.append(df_filtered['loser_rank_points'][i])
            pl1_ioc_list.append(df_filtered['loser_ioc'][i])

            pl2_hand_list.append(df_filtered['winner_hand'][i])
            pl2_entry_list.append(df_filtered['winner_entry'][i])
            pl2_ht_list.append(df_filtered['winner_ht'][i])
            pl2_age_list.append(df_filtered['winner_age'][i])
            pl2_rank_list.append(df_filtered['winner_rank'][i])
            pl2_rank_points_list.append(df_filtered['winner_rank_points'][i])
            pl2_ioc_list.append(df_filtered['winner_ioc'][i])

    df_filtered['1_hand'] = pl1_hand_list
    df_filtered['1_entry'] = pl1_entry_list
    df_filtered['1_ht'] = pl1_ht_list
    df_filtered['1_age'] = pl1_age_list
    df_filtered['1_rank'] = pl1_rank_list
    df_filtered['1_rank_points'] = pl1_rank_points_list
    df_filtered['1_ioc'] = pl1_ioc_list

    df_filtered['2_hand'] = pl2_hand_list
    df_filtered['2_entry'] = pl2_entry_list
    df_filtered['2_ht'] = pl2_ht_list
    df_filtered['2_age'] = pl2_age_list
    df_filtered['2_rank'] = pl2_rank_list
    df_filtered['2_rank_points'] = pl2_rank_points_list
    df_filtered['2_ioc'] = pl2_ioc_list


    df_filtered['winner'] = winner_list
    #ukloniti kolone 0_age, 0_ht...
    del df_filtered['tourney_date']
    del df_filtered['loser_hand']
    del df_filtered['loser_entry']
    del df_filtered['loser_age']
    del df_filtered['loser_ht']
    del df_filtered['loser_rank']
    del df_filtered['loser_rank_points']
    del df_filtered['loser_ioc']


    del df_filtered['winner_hand']
    del df_filtered['winner_entry']
    del df_filtered['winner_age']
    del df_filtered['winner_ht']
    del df_filtered['winner_rank']
    del df_filtered['winner_rank_points']
    del df_filtered['winner_ioc']




    # sve vrednosi float da budu
    df_filtered = df_filtered.astype('float')
    df_filtered = df_filtered.apply(pd.to_numeric, args=('coerce',))
    # popunjavanje nan vrednosti

    #'draw_size', 'tourney_level','1_entry','1_ht','1_age','1_rank','1_rank_points',
    # '2_entry','2_ht','2_age','2_rank','2_rank_points' - prosek

    prosek_draw = df['draw_size'].mean()
    prosek_level = df_filtered['tourney_level'].mean()
    prosek_1_entry = df_filtered['1_entry'].mean()
    prosek_1_ht = df_filtered['1_ht'].mean()
    prosek_1_age = df_filtered['1_age'].mean()
    prosek_2_entry = df_filtered['2_entry'].mean()
    prosek_2_ht = df_filtered['2_ht'].mean()
    prosek_2_age = df_filtered['2_age'].mean()


    df_filtered[['draw_size']] = df_filtered[['draw_size']].fillna(value=prosek_draw)
    df_filtered[['tourney_level']] = df_filtered[['tourney_level']].fillna(value=prosek_level)
    df_filtered[['1_entry']] = df_filtered[['1_entry']].fillna(value=prosek_1_entry)
    df_filtered[['1_ht']] = df_filtered[['1_ht']].fillna(value=prosek_1_ht)
    df_filtered[['1_age']] = df_filtered[['1_age']].fillna(value=df_filtered['1_age'].mean())
    df_filtered[['2_entry']] = df_filtered[['2_entry']].fillna(value=df_filtered['2_entry'].mean())
    df_filtered[['2_ht']] = df_filtered[['2_ht']].fillna(value=df_filtered['2_ht'].mean())
    df_filtered[['2_age']] = df_filtered[['2_age']].fillna(value=df_filtered['2_age'].mean())

    #rank
    df_filtered[['1_rank']] = df_filtered[['1_rank']].fillna(value="2000")
    df_filtered[['2_rank']] = df_filtered[['2_rank']].fillna(value="2000")


    #rank points
    df_filtered[['1_rank_points']] = df_filtered[['1_rank_points']].fillna(value="1")
    df_filtered[['2_rank_points']] = df_filtered[['2_rank_points']].fillna(value="1")

    # ruka desna
    df_filtered[['1_hand']] = df_filtered[['1_hand']].fillna(value="1")
    df_filtered[['1_hand']] = df_filtered[['1_hand']].fillna(value="1")

    # podloga neutralna
    df_filtered[['surface']] = df_filtered[['surface']].fillna(value="0")

    # nacionalnosti
    df_filtered[['1_ioc']] = df_filtered[['1_ioc']].fillna(value="0")
    df_filtered[['2_ioc']] = df_filtered[['2_ioc']].fillna(value="0")

    # broj setova
    df_filtered[['best_of']] = df_filtered[['best_of']].fillna(value="3")




    return df_filtered

#spajanje vise godina, vise podataka za treniranje
def years_data(location,num_next_years):
    df = pd.DataFrame()
    for year in range(num_next_years):
        previous_year = int(location[-8:-4])
        this_year = str(previous_year+year)
        this_year_location = location[:-8] + this_year + ".csv"
        df_year = loading_data(this_year_location)
        df - pd.concat([df,df_year])
    return df

df = loading_data('tennis_atp/atp_matches_2010.csv')
#df1 = loading_data('tennis_atp/atp_matches_qual_chall_2015.csv')
#df2 = loading_data('tennis_atp/atp_matches_2015.csv')
#df3 = loading_data('tennis_atp/atp_matches_1973.csv')

pd.set_option('display.max_columns', None)

print(df)