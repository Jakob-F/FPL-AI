import pandas as pd
import os


# Player mapping for several FPL names for one player
fpl_name_mapping = {
    'Adama Traoré Diarra': 'Adama Traoré',
    'André Filipe Tavares Gomes': 'André Tavares Gomes',
    'Arnaut Danjuma Groeneveld': 'Arnaut Danjuma',
    'Benjamin Chilwell': 'Ben Chilwell',
    'Benjamin White': 'Ben White',
    'Bernardo Mota Veiga de Carvalho e Silva': 'Bernardo Veiga de Carvalho e Silva',
    'Bruno Miguel Borges Fernandes': 'Bruno Borges Fernandes',
    'Cédric Alves Soares': 'Cédric Soares',
    'David de Gea': 'David De Gea Quintana',
    'Diogo Teixeira da Silva': 'Diogo Jota',
    'Emerson Aparecido Leite de Souza Junior': 'Emerson Leite de Souza Junior',
    'Emiliano Martínez Romero': 'Emiliano Martínez',
    'Gabriel Teodoro Martinelli Silva': 'Gabriel Martinelli Silva',
    'Héctor Junior Firpo Adames': 'Junior Firpo Adames',
    'Hee-Chan Hwang': 'Hwang Hee-Chan',
    'Hwang Hee-chan': 'Hwang Hee-Chan',
    'Heung-Min Son': 'Son Heung-Min',
    'Son Heung-min': 'Son Heung-Min',
    'Jeremy Sarmiento Morante': 'Jeremy Sarmiento',
    'João Pedro Cavaco Cancelo': 'João Cancelo',
    'Joseph Gomez': 'Joe Gomez',
    'Joseph Willock': 'Joe Willock',
    'Luis Sinisterra Lucumí': 'Luis Sinisterra',
    'Lyanco Evangelista Silveira Neves Vojnovic': 'Lyanco Silveira Neves Vojnovic',
    'Marc Cucurella Saseta': 'Marc Cucurella',
    'Mateo Kovačić': 'Mateo Kovacic',
    'Matthew Cash': 'Matty Cash',
    'Miguel Almirón Rejala': 'Miguel Almirón',
    'Mohamed Naser El Sayed Elneny': 'Mohamed Elneny',
    'Moisés Caicedo Corozo': 'Moisés Caicedo',
    'Pablo Fornals Malla': 'Pablo Fornals',
    'Rayan Ait Nouri': 'Rayan Aït-Nouri',
    'Ricardo Domingos Barbosa Pereira': 'Ricardo Barbosa Pereira',
    'Rúben Diogo da Silva Neves': 'Rúben da Silva Neves',
    'Rúben Santos Gato Alves Dias': 'Rúben Gato Alves Dias',
    'Sergi Canós Tenés': 'Sergi Canós',
    'Vladimir Coufal': 'Vladimír Coufal',
}

# Player mapping season 2023-24
player_mapping_23 = {
    'Aleksandar Mitrovic': 'Aleksandar Mitrović',
    'Álex Moreno': 'Alexandre Moreno Lopera',
    'Alisson': 'Alisson Ramses Becker',
    'Amad Diallo Traore': 'Amad Diallo',
    'Amari&#039;i Bell': "Amari'i Bell",
    'Ameen Al Dakhil': 'Ameen Al-Dakhil',
    'Andreas Pereira': 'Andreas Hoelgebaum Pereira',
    'André Gomes': 'André Tavares Gomes',
    'Anel Ahmedhodzic': 'Anel Ahmedhodžić',
    'Anis Ben Slimane': 'Anis Slimane',
    'Anssumane Fati': 'Anssumane Fati Vieira',
    'Antony': 'Antony Matheus dos Santos',
    'Ben Brereton Díaz': 'Ben Brereton',
    'Ben White': 'Benjamin White',
    'Benoit Badiashile Mukinayi': 'Benoît Badiashile',
    'Benson Manuel': 'Manuel Benson Hedilazio',
    'Bernardo Silva': 'Bernardo Veiga de Carvalho e Silva',
    'Beto': 'Norberto Bercique Gomes Betuncal',
    'Bobby Reid': 'Bobby De Cordova-Reid',
    'Boubacar Traore': 'Boubacar Traoré',
    'Brandon Aguilera': 'Brandon Aguilera Zamora',
    'Bruno Fernandes': 'Bruno Borges Fernandes',
    'Bruno Guimarães': 'Bruno Guimarães Rodriguez Moura',
    'Carlos Vinicius': 'Carlos Vinícius Alves Morais',
    'Casemiro': 'Carlos Henrique Casimiro',
    'Cheick Oumar Doucoure': 'Cheick Doucouré',
    'Chimuanya Ugochukwu': 'Lesley Ugochukwu',
    'Clement Lenglet': 'Clément Lenglet',
    'Cédric Soares': 'Cédric Alves Soares',
    'Danilo': 'Danilo dos Santos de Oliveira',
    'Dara O\'Shea': 'Dara O\'Shea',
    'Dara O&#039;Shea': "Dara O'Shea",
    'Darwin Núñez': 'Darwin Núñez Ribeiro',
    'David Raya': 'David Raya Martin',
    'Deivid Washington': 'Deivid Washington de Souza Eugênio',
    'Destiny Udogie': 'Iyenoma Destiny Udogie',
    'Diego Carlos': 'Diego Carlos Santos Silva',
    'Diogo Dalot': 'Diogo Dalot Teixeira',
    'Diogo Jota': 'Diogo Teixeira da Silva',
    'Douglas Luiz': 'Douglas Luiz Soares de Paulo',
    'Ederson': 'Ederson Santana de Moraes',
    'Edson Álvarez': 'Edson Álvarez Velázquez',
    'Emiliano Martinez': 'Emiliano Martínez Romero',
    'Emile Smith-Rowe': 'Emile Smith Rowe',
    'Estupiñán': 'Pervis Estupiñán',
    'Fabio Silva': 'Fábio Silva',
    'Fábio Vieira': 'Fábio Ferreira Vieira',
    'Facundo Pellistri': 'Facundo Pellistri Rebollo',
    'Felipe': 'Felipe Augusto de Almeida Monteiro',
    'Fode Toure': 'Fodé Ballo-Touré',
    'Gabriel': 'Gabriel dos Santos Magalhães',
    'Gabriel Jesus': 'Gabriel Fernando de Jesus',
    'Gabriel Martinelli': 'Gabriel Martinelli Silva',
    'Hee-Chan Hwang': 'Hwang Hee-chan',
    'Hugo Bueno': 'Hugo Bueno López',
    'Ibrahim Sangare': 'Ibrahim Sangaré',
    'Igor Julio': 'Igor Julio dos Santos de Paulo',
    'Ionut Radu': 'Ionuț Radu',
    'Issa Kabore': 'Issa Kaboré',
    'Ivan Perisic': 'Ivan Perišić',
    'Iyenoma Destiny Udogie': 'Destiny Udogie',
    'Jack Colback': 'Jack Colback',
    'Jefferson Lerma': 'Jefferson Lerma Solís',
    'Jéremy Doku': 'Jérémy Doku',
    'João Gomes': 'João Victor Gomes da Silva',
    'João Palhinha': 'João Palhinha Gonçalves',
    'João Pedro': 'João Pedro Junqueira de Jesus',
    'Joelinton': 'Joelinton Cássio Apolinário de Lira',
    'Johann Berg Gudmundsson': 'Jóhann Berg Gudmundsson',
    'José Sá': 'José Malheiro de Sá',
    'Josko Gvardiol': 'Joško Gvardiol',
    'Jorginho': 'Jorge Luiz Frello Filho',
    'Joseph Gomez': 'Joe Gomez',
    'Kaine Hayden': 'Kaine Kesler-Hayden',
    'Louis Beyer': 'Jordan Beyer',
    'Lucas Paquetá': 'Lucas Tolentino Coelho de Lima',
    'Mads Andersen': 'Mads Juel Andersen',
    'Mads Roerslev': 'Mads Roerslev Rasmussen',
    'Marc Cucurella': 'Marc Cucurella Saseta',
    'Marc Guehi': 'Marc Guéhi',
    'Martin Odegaard': 'Martin Ødegaard',
    'Mateo Kovacic': 'Mateo Kovačić',
    'Matheus Cunha': 'Matheus Santos Carneiro Da Cunha',
    'Matheus França': 'Matheus França de Oliveira',
    'Matheus Nunes': 'Matheus Luiz Nunes',
    'Matthew Cash': 'Matty Cash',
    'Maxime Estève': 'Maxime Esteve',
    'Miguel Almirón': 'Miguel Almirón Rejala',
    'Moisés Caicedo': 'Moisés Caicedo Corozo',
    'Moussa Niakhate': 'Moussa Niakhaté',
    'Murillo': 'Murillo Santiago Costa dos Santos',
    'Naif Aguerd': 'Nayef Aguerd',
    'Nélson Semedo': 'Nélson Cabral Semedo',
    'Neto': 'Norberto Murara Neto',
    'Nicolo Zaniolo': 'Nicolò Zaniolo',
    'Nuno Tavares': 'Nuno Varela Tavares',
    'Odysseas Vlachodimos': 'Odysseas Vlachodimos',
    'Odisseas Vlachodimos': 'Odysseas Vlachodimos',
    'Ola Aina': 'Olu Aina',
    'Pablo Fornals': 'Pablo Fornals Malla',
    'Pape Sarr': 'Pape Matar Sarr',
    'Pedro Neto': 'Pedro Lomba Neto',
    'Philippe Coutinho': 'Philippe Coutinho Correia',
    'Raphael Varane': 'Raphaël Varane',
    'Rayan Ait Nouri': 'Rayan Aït-Nouri',
    'Richarlison': 'Richarlison de Andrade',
    'Rodri': 'Rodrigo Hernandez',
    'Rodrigo Muniz': 'Rodrigo Muniz Carvalho',
    'Romeo Lavia': 'Roméo Lavia',
    'Rúben Dias': 'Rúben Gato Alves Dias',
    'Ryan John Giles': 'Ryan Giles',
    'Said Benrahma': 'Saïd Benrahma',
    'Sasa Lukic': 'Saša Lukić',
    'Son Heung-Min': 'Son Heung-min',
    'Thiago Alcántara': 'Thiago Alcántara do Nascimento',
    'Thiago Silva': 'Thiago Emiliano da Silva',
    'Tomas Soucek': 'Tomáš Souček',
    'Toti': 'Toti António Gomes',
    'Valentino Livramento': 'Tino Livramento',
    'Vinicius Souza': 'Vini de Souza Costa',
    'Vitinho': 'Victor da Silva',
    'Vladimir Coufal': 'Vladimír Coufal',
    'Wilfred Ndidi': 'Wilfred Ndidi',
    'Willian': 'Willian Borges da Silva',
    'Yehor Yarmolyuk': 'Yegor Yarmoliuk',
    'Youssef Chermiti': 'Youssef Ramalho Chermiti',
    'Zanka': 'Mathias Jorgensen'
}


# Player mapping season 2022-23
player_mapping_22 = {}

# Load player mapping dict
df_player_mapping_22 = pd.read_csv('data/2022-23/id_dict.csv')
for row in df_player_mapping_22.iloc:
    if row['Understat_Name'] != row['FPL_Name']:
        player_mapping_22[row['Understat_Name']] = row['FPL_Name']
        
# Manually add mistakes
player_mapping_22['Lewis O&#039;Brien'] = "Lewis O'Brien"
player_mapping_22['Son Heung-Min'] = 'Son Heung-min'
player_mapping_22['Diogo Jota'] = 'Diogo Teixeira da Silva'


# Player mapping season 2021-22
player_mapping_21 = {}

# Load player mapping dict
df_player_mapping_21 = pd.read_csv('data/2021-22/id_dict.csv')
for row in df_player_mapping_21.iloc:
    if row[' Understat_Name'] != row[' FPL_Name']:
        player_mapping_21[row[' Understat_Name']] = row[' FPL_Name']
        
# Manually add mistakes
player_mapping_21['Emerson Leite de Souza Junior'] = 'Emerson Aparecido Leite de Souza Junior'


# Player mapping for 2020-21 season
player_mapping_20 = {
    'Ahmed Elmohamady': 'Ahmed El Mohamady',
    'Aleksandar Mitrovic': 'Aleksandar Mitrović',
    'Alex Telles': 'Alex Nicolao Telles',
    'Alisson': 'Alisson Ramses Becker',
    'Allan': 'Allan Marques Loureiro',
    'André Gomes': 'André Filipe Tavares Gomes',
    'Ben Chilwell': 'Benjamin Chilwell',
    'Bernard': 'Bernard Anício Caldeira Duarte',
    'Bernardo Silva': 'Bernardo Mota Veiga de Carvalho e Silva',
    'Bobby Reid': 'Bobby Decordova-Reid',
    'Bruno Fernandes': 'Bruno Miguel Borges Fernandes',
    'Caglar Söyüncü': 'Çaglar Söyüncü',
    'Carlos Vinicius': 'Carlos Vinicius Alves Morais',
    'Dani Ceballos': 'Daniel Ceballos Fernández',
    'Daniel Podence': 'Daniel Castelo Podence',
    'David Luiz': 'David Luiz Moreira Marinho',
    'Dele Alli': 'Bamidele Alli',
    'Douglas Luiz': 'Douglas Luiz Soares de Paulo',
    'Ederson': 'Ederson Santana de Moraes',
    'Eddie Nketiah': 'Edward Nketiah',
    'Emile Smith-Rowe': 'Emile Smith Rowe',
    'Emiliano Martinez': 'Emiliano Martínez',
    'Fabinho': 'Fabio Henrique Tavares',
    'Fernandinho': 'Fernando Luiz Rosa',
    'Ferrán Torres': 'Ferran Torres',
    'Franck Zambo': 'André-Frank Zambo Anguissa',
    'Fred': 'Frederico Rodrigues de Paula Santos',
    'Gabriel Jesus': 'Gabriel Fernando de Jesus',
    'Gabriel Martinelli': 'Gabriel Teodoro Martinelli Silva',
    'Hélder Costa': 'Hélder Wander Sousa de Azevedo e Costa',
    'Ian Poveda-Ocampo': 'Ian Carlo Poveda-Ocampo',
    'Ivan Cavaleiro': 'Ivan Ricardo Neves Abreu Cavaleiro',
    'Joelinton': 'Joelinton Cássio Apolinário de Lira',
    'Jonny': 'Jonathan Castro Otto',
    'Jorginho': 'Jorge Luiz Frello Filho',
    'Joe Willock': 'Joseph Willock',
    'João Moutinho': 'João Filipe Iria Santos Moutinho',
    'João Cancelo': 'João Pedro Cavaco Cancelo',
    'Kepa': 'Kepa Arrizabalaga',
    'Lucas Moura': 'Lucas Rodrigues Moura da Silva',
    'Martin Odegaard': 'Martin Ødegaard',
    'Mat Ryan': 'Mathew Ryan',
    'Mohamed Elneny': 'Mohamed Naser El Sayed Elneny',
    'Nicolas Pepe': 'Nicolas Pépé',
    'Nélson Semedo': 'Nélson Cabral Semedo',
    'Semi Ajayi': 'Oluwasemilogo Adesewo Ibidapo Ajayi',
    'Oriol Romeu': 'Oriol Romeu Vidal',
    'Pablo Hernández': 'Pablo Hernández Domínguez',
    'Pedro Neto': 'Pedro Lomba Neto',
    'Raphinha': 'Raphael Dias Belloli',
    'Ricardo Pereira': 'Ricardo Domingos Barbosa Pereira',
    'Richarlison': 'Richarlison de Andrade',
    'Rodri': 'Rodrigo Hernandez',
    'Rodrigo': 'Rodrigo Moreno',
    'Romain Saiss': 'Romain Saïss',
    'Rui Patrício': 'Rui Pedro dos Santos Patrício',
    'Rúben Neves': 'Rúben Diogo da Silva Neves',
    'Rúben Dias': 'Rúben Santos Gato Alves Dias',
    'Said Benrahma': 'Saïd Benrahma',
    'Solly March': 'Solomon March',
    'Son Heung-Min': 'Heung-Min Son',
    'Tanguy NDombele Alvaro': 'Tanguy Ndombele',
    'Thiago Alcántara': 'Thiago Alcántara do Nascimento',
    'Vitinha': 'Vitor Ferreira',
    'Willian': 'Willian Borges Da Silva',
    'Willian José': 'Willian José Da Silva',
    'Daniel N&#039;Lundulu': "Daniel N'Lundulu",
    'Dara O&#039;Shea': "Dara O'Shea",
    'Gabriel': 'Gabriel Magalhães',
    'Trézéguet': 'Mahmoud Ahmed Ibrahim Hassan',
    'N&#039;Golo Kanté': "N'Golo Kanté",
    'Thiago Silva': 'Thiago Thiago'
}


# Player mapping for season 2019-20
player_mapping_19 = {
    'Adrián': 'Adrián San Miguel del Castillo',
    'Ahmed Elmohamady': 'Ahmed El Mohamady',
    'Alisson': 'Alisson Ramses Becker',
    'André Gomes': 'André Filipe Tavares Gomes',
    'Ben Chilwell': 'Benjamin Chilwell',
    'Bernard': 'Bernard Anício Caldeira Duarte',
    'Bernardo': 'Bernardo Fernandes da Silva Junior',
    'Bernardo Silva': 'Bernardo Mota Veiga de Carvalho e Silva',
    'Björn Engels': 'Bjorn Engels',
    'Bruno Fernandes': 'Bruno Miguel Borges Fernandes',
    'Caglar Söyüncü': 'Çaglar Söyüncü',
    'Dani Ceballos': 'Daniel Ceballos Fernández',
    'Daniel Podence': 'Daniel Castelo Podence',
    'David Luiz': 'David Luiz Moreira Marinho',
    'Dele Alli': 'Bamidele Alli',
    'Djibril Sidibe': 'Djibril Sidibé',
    'Douglas Luiz': 'Douglas Luiz Soares de Paulo',
    'Eddie Nketiah': 'Edward Nketiah',
    'Ederson': 'Ederson Santana de Moraes',
    'Emiliano Martinez': 'Emiliano Martínez',
    'Felipe Anderson': 'Felipe Anderson Pereira Gomes',
    'Fernandinho': 'Fernando Luiz Rosa',
    'Fred': 'Frederico Rodrigues de Paula Santos',
    'Frederic Guilbert': 'Frédéric Guilbert',
    'Gabriel Jesus': 'Gabriel Fernando de Jesus',
    'Gabriel Martinelli': 'Gabriel Teodoro Martinelli Silva',
    'Gedson Fernandes': 'Gedson Carvalho Fernandes',
    'Ismaila Sarr': 'Ismaïla Sarr',
    'Jack O&#039;Connell': "Jack O'Connell",
    'Jean-Philippe Gbamin': 'Jean-Philippe Gbamin',
    'Joe Willock': 'Joseph Willock',
    'Joelinton': 'Joelinton Cássio Apolinário de Lira',
    'Jorginho': 'Jorge Luiz Frello Filho',
    'João Cancelo': 'João Pedro Cavaco Cancelo',
    'João Moutinho': 'João Filipe Iria Santos Moutinho',
    'Kepa': 'Kepa Arrizabalaga',
    'Kiko Femenía': 'Francisco Femenía Far',
    'Lucas Moura': 'Lucas Rodrigues Moura da Silva',
    'Mat Ryan': 'Mathew Ryan',
    'Max Aarons': 'Maximillian Aarons',
    'Muhamed Besic': 'Muhamed Bešić',
    'N&#039;Golo Kanté': 'N&#039;Golo Kanté',
    'Nicolas Pepe': 'Nicolas Pépé',
    'Oriol Romeu': 'Oriol Romeu Vidal',
    'Pedro': 'Pedro Rodríguez Ledesma',
    'Pedro Neto': 'Pedro Lomba Neto',
    'Ricardo Pereira': 'Ricardo Domingos Barbosa Pereira',
    'Richarlison': 'Richarlison de Andrade',
    'Roberto Jiménez': 'Roberto Jimenez Gago',
    'Rodri': 'Rodrigo Hernandez',
    'Romain Saiss': 'Romain Saïss',
    'Rui Patrício': 'Rui Pedro dos Santos Patrício',
    'Rúben Neves': 'Rúben Diogo da Silva Neves',
    'Rúben Vinagre': 'Rúben Gonçalo Silva Nascimento Vinagre',
    'Sokratis': 'Sokratis Papastathopoulos',
    'Solly March': 'Solomon March',
    'Son Heung-Min': 'Heung-Min Son',
    'Tanguy NDombele Alvaro': 'Tanguy Ndombele',
    'Trézéguet': 'Trézéguet',
    'Wesley': 'Wesley Moraes',
    'Willian': 'Willian Borges Da Silva',
    'Willy Caballero': 'Willy Caballero',
    'Fabinho': 'Fabio Henrique Tavares',
    'Jonny': 'Jonathan Castro Otto',
    "N&#039;Golo Kanté": "N'Golo Kanté",
    'Jota': 'José Ignacio Peleteiro Romallo',
    'Angelino': 'José Ángel Esmorís Tasende',
    'Trézéguet': 'Mahmoud Ahmed Ibrahim Hassan'
}


def merge_season(season, player_mapping):

    # Create team mapping
    df_teams = pd.read_csv(f"data/{season}/teams.csv")
    team_dict = {}
    for row in df_teams.iloc:
        team_dict[row['id']] = row['name']

    # Load FPL data
    df_fpl = pd.read_csv(f"data/{season}/gws/merged_gw.csv")
    df_fpl['kickoff_date'] = pd.to_datetime(df_fpl['kickoff_time']).dt.date
    if season == '2023-24':
        df_fpl['name'] = df_fpl['name'].map({'Đorđe Petrović': 'Djordje Petrovic'}).fillna(df_fpl['name'])
    df_fpl['opponent_team'] = df_fpl['opponent_team'].map(team_dict).fillna(df_fpl['opponent_team'])
    if season == '2019-20':
        df_fpl['name'] = df_fpl['name'].str.replace('_', ' ').str.replace(r' \d+$', '', regex=True)

    # Load Understat data
    folder_path = f'data/{season}/understat'
    dataframes = []
    teams = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):

            # Skip teams and understat_player
            if filename.split('_')[0].lower() == 'understat':
                team_file_name = filename[:-4]
                team_name = (' ').join(team_file_name.split('_')[1:])
                if team_name != 'player':
                    teams.append(team_name)
                continue

            # Create the full file path
            file_path = os.path.join(folder_path, filename)
            
            # Read the CSV into a dataframe
            df = pd.read_csv(file_path)
            
            # Extract the player name from the filename (remove .csv)
            player_file_name = filename[:-4]
            
            # Add a new column 'Player' with the player's name
            player_name = (' ').join(player_file_name.split('_')[:-1])
            player_id = player_file_name.split('_')[-1]
            df['name'] = player_name
            df['player_id'] = player_id
            
            # Hardcode for the two Emersons
            if player_name == 'Emerson':
                if player_id == '1245':
                    df['name'] = 'Emerson Palmieri dos Santos'
                elif player_id == '7430':
                    df['name'] = 'Emerson Leite de Souza Junior'
            
            # Append the dataframe to the list
            dataframes.append(df)

    # Combine all the dataframes into one large dataframe
    df_understat = pd.concat(dataframes, ignore_index=True)
    df_understat = df_understat[df_understat.h_team.isin(teams)]
    df_understat = df_understat.drop(['position'], axis=1)
    df_understat['date'] = pd.to_datetime(df_understat['date']).dt.date
    df_understat['name'] = df_understat['name'].map(player_mapping).fillna(df_understat['name'])

    # Merge FPL and Understat data
    df_merged = pd.merge(df_fpl, df_understat, how='left', left_on=['name', 'kickoff_date'], right_on=['name', 'date'])

    # Remove players who play no minutes all season
    for player in sorted(df_merged.name.unique()):
        total_games = len(df_merged[df_merged.name==player])
        games_not_played = sum(df_merged[df_merged.name==player].minutes == 0)
        mins_played = sum(df_merged[df_merged.name==player].minutes)
        nans = sum(df_merged[df_merged.name==player].goals.isna())
        if mins_played == 0:
            df_merged = df_merged[df_merged.name != player]
        # if total_games - games_not_played < 6:
        #     df_merged = df_merged[df_merged.name != player]

    return df_merged


def main():
    # Merge FPL and Understat data for each past season
    df_23 = merge_season('2023-24', player_mapping_23)
    df_22 = merge_season('2022-23', player_mapping_22)
    df_21 = merge_season('2021-22', player_mapping_21)
    df_20 = merge_season('2020-21', player_mapping_20)
    df_19 = merge_season('2020-21', player_mapping_19)

    # Combine all seasons
    df_all = pd.concat([df_19, df_20, df_21, df_22, df_23], ignore_index=True)
    df_all.reset_index(drop=True, inplace=True)
    df_all['name'] = df_all['name'].map(fpl_name_mapping).fillna(df_all['name'])

    # Save to flle
    df_all.to_csv("data/prev_seasons_merged.csv", index=False)


if __name__ == '__main__':
    main()