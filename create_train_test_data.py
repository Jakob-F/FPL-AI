import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import pickle

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

def one_hot_encode_team(team_id, num_teams):
    # Create a zero array of length num_teams
    one_hot = np.zeros(num_teams)
    
    # Set the correct index to 1 (team_id - 1 because team_id starts from 1)
    one_hot[team_id - 1] = 1

    return one_hot


def select_features(df_all):
    # Select only numeric columns
    numeric_df = df_all.select_dtypes(include='number')

    # List of columns to drop
    columns_to_drop = [
        'element', 'fixture', 'round', 'GW', 'id',
        'season', 'roster_id', 'player_id', 'team_id', 'opp_team_id',
        'pos_id', 'time',
        'h_goals', 'a_goals', 'team_a_score', 'team_h_score',
        ]
    numeric_df = numeric_df.drop(columns=columns_to_drop)

    # Choose which features to use for data
    keys_to_select = list(numeric_df.columns)

    return keys_to_select

def plot_correlation_matrix(df_filtered):
    # Save correlation matrix of features
    correlation_matrix = df_filtered.corr()
    plt.figure(figsize=(50, 40))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.savefig('figures/correlation_matrix_heatmap.png')


def create_training_data(df_all, keys_to_select):
    X = []
    y = []
    played = []

    for player in df_all.name.unique():
        df_temp = df_all[df_all.name == player].copy()
        if len(df_temp) < 4:
            continue
        
        for i in range(3, len(df_temp)):
            
            # Select row for next game
            next_game = df_temp.iloc[i]
            
            if next_game['minutes']+df_temp.iloc[i-1]['minutes']+df_temp.iloc[i-2]['minutes']+df_temp.iloc[i-3]['minutes']==0:
                played.append(0)
            else:
                played.append(1)
            
            # Get one-hot encoding for players team, opp team, home/away and position
            player_team = one_hot_encode_team(next_game['team_id'], 27)
            opponent_team = one_hot_encode_team(next_game['opp_team_id'], 27)
            home_away = one_hot_encode_team(next_game['was_home'], 2)
            position = one_hot_encode_team(next_game['pos_id'], 4)
            
            # Combine into one vector
            combined_stats = np.concatenate([player_team, opponent_team, home_away, position])
            
            # Get points scored (y value)
            points = next_game['total_points']
            
            # Get player stats from previous games
            for j in range(1,4):
                row_temp = df_temp.iloc[i-j]
                
                # Get home/away encoding
                home_away = one_hot_encode_team(row_temp['was_home'], 2)
                
                # Add player team goals and opponent team goals
                if row_temp.was_home:
                    score = np.array(row_temp[['team_h_score', 'team_a_score']].astype(float).values)
                else:
                    score = np.array(row_temp[['team_a_score','team_h_score']].astype(float).values)
                
                # Select the wanted stats and convert to float numpy array
                selected_stats = np.array(row_temp[keys_to_select].astype(float).values) 
                    
                # Combine into one vector
                combined_stats = np.concatenate([combined_stats, home_away, score, selected_stats])
                
            # Append combined stats to X and points (y value) to y
            X.append(combined_stats)
            y.append(points)

    # Convert lists to numpy arrays for training/testing
    X = np.array(X)
    y = np.array(y)
    played = np.array(played)

    np.save('data/xgboost/X_train.npy', X)
    np.save('data/xgboost/y_train.npy', y)
    np.save('data/xgboost/played_train.npy', played)

    print("Training data (X):", X.shape)
    print("Target values (y):", y.shape)
    print("Played values (y):", played.shape)

def load_player_data():
    # Make an HTTP GET request to fetch the overall fpl data
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)

    # If successful, save the data to a file
    if response.status_code == 200:
        overall_data = response.json()
        with open("data/overall_data.json", "w") as f:
            json.dump(overall_data, f)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    # Extract the player data and convert to dictionary
    players = overall_data['elements']
    player_overall_stats = {}
    for player in players:
        player_id = str(player['id'])
        player_overall_stats[player_id] = player


    # Get all fixtures from the FPL API
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the fixture data
        fixtures = response.json()
        fixtures_data = {str(element['id']): element for element in fixtures}

        # Save the data to a file
        with open("data/fixture_data.json", "w") as f:
            json.dump(fixtures_data, f)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


    # Add every fixture to player stats
    player_stats = {}
    for player_id in player_overall_stats.keys():

        url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Get player stats for played gameweeks
            player_history = response.json()['history']
            for i in range(len(player_history)):
                player_fixture = fixtures_data[str(player_history[i]['fixture'])]
                if player_history[i]['was_home'] == True:
                    player_history[i]['player_team'] = player_fixture['team_h']
                    player_history[i]['team_goals'] = player_fixture['team_h_score']
                else:
                    player_history[i]['player_team'] = player_fixture['team_a']
                    player_history[i]['team_goals'] = player_fixture['team_a_score']
            player_history = {str(element['round']): element for element in player_history}
            
            # Get player upcoming fixtures
            player_fixtures = response.json()['fixtures']
            player_fixtures = {str(element['event']): element for element in player_fixtures}
            
            # Add to overall player stats dictionary
            player_stats[player_id] = {'fixtures': player_fixtures, 'history': player_history}
        
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
        
    # Save the data to a file
    with open("data/player_data.json", "w") as f:
        json.dump(player_stats, f)


def create_test_data(df_all, keys_to_select, next_gameweek):
    
    # Load the overall fpl data
    with open("data/overall_data.json", "r") as f:
        overall_data = json.load(f)

    # Extract the player data and convert to dictionary
    players = overall_data['elements']
    player_overall_stats = {}
    for player in players:
        player_id = str(player['id'])
        player_overall_stats[player_id] = player

    # Load the player stats for each gameweek
    with open("data/player_data.json", "r") as f:
        player_stats = json.load(f)

    # Dictionaries to keep track of player name and id
    id_dict = {}
    name_to_id = {}
    df_player_id = pd.read_csv('data/2024-25/player_idlist.csv')
    for row in df_player_id.iloc:
        name = row['first_name'] + ' ' + row['second_name']
        mapped_name = fpl_name_mapping.get(name, name)
        id_dict[str(row['id'])] = mapped_name
        name_to_id[mapped_name] = str(row['id'])


    
    # Create test data
    X_test_games = []
    eP_games = []
    player_names_games = []

    # From next gameweek until GW38
    for i in range(next_gameweek,39):
        X_test = []
        eP = []
        player_names = []
            
        for player_id in id_dict.keys():
            df_temp = df_all[df_all.name == id_dict[player_id]]
            
            # If player does not have at least 3 previous games then skip
            if len(df_temp) < 3:
                continue
                
            # If playerID is not in player_stats
            if not player_id in player_stats.keys():
                continue

            # Get player's next game
            next_game = player_stats[player_id]['fixtures'][str(i)]
            
            # Get one-hot encoding for players team, opp team and home/away
            if next_game['is_home']:
                player_team = one_hot_encode_team(next_game['team_h'], 27)
                opponent_team = one_hot_encode_team(next_game['team_a'], 27)
                home_away = one_hot_encode_team(1, 2)
            else:
                player_team = one_hot_encode_team(next_game['team_a'], 27)
                opponent_team = one_hot_encode_team(next_game['team_h'], 27)
                home_away = one_hot_encode_team(0, 2)
                
            # Get position information of player
            position = one_hot_encode_team(df_temp.iloc[-1]['pos_id'], 4)
            
            # Combine next game stats
            combined_stats = np.concatenate([player_team, opponent_team, home_away, position])
            
            # Get expected points (y value)
            expected_points = float(player_overall_stats[player_id]['ep_next'])
            
            # Get player stats from his previous 3 games
            for j in range(1,4):
                row_temp = df_temp.iloc[-j]
                
                # Get home/away encoding
                home_away = one_hot_encode_team(row_temp['was_home'], 2)
                
                # Add player team goals and opponent team goals
                if row_temp.was_home:
                    score = np.array(row_temp[['team_h_score', 'team_a_score']].astype(float).values)
                else:
                    score = np.array(row_temp[['team_a_score','team_h_score']].astype(float).values)
                
                # Select the wanted stats and convert to float numpy array
                selected_stats = np.array(row_temp[keys_to_select].astype(float).values) 
                    
                # Combine into one vector
                combined_stats = np.concatenate([combined_stats, home_away, score, selected_stats])
                
            # Append combined stats to X and points (y value) to y
            X_test.append(combined_stats)
            eP.append(expected_points)
            player_names.append(id_dict[player_id])
            
        # Convert to numpy arrays
        X_test = np.array(X_test)
        eP = np.array(eP)
        
        # Append to overall list
        X_test_games.append(X_test)
        eP_games.append(eP)
        player_names_games.append(player_names)
    
    # Save to a pickle file
    with open('data/xgboost/X_test.pkl', 'wb') as f:
        pickle.dump(X_test_games, f)
    with open('data/xgboost/xP_test.pkl', 'wb') as f:
        pickle.dump(eP_games, f)
    with open('data/xgboost/names_test.pkl', 'wb') as f:
        pickle.dump(player_names_games, f)
    with open('data/xgboost/id_dict.pkl', 'wb') as f:
        pickle.dump(id_dict, f)
    with open('data/xgboost/name_to_id.pkl', 'wb') as f:
        pickle.dump(name_to_id, f)


def main():
    # Load dataframe
    df_all = pd.read_csv('data/all_seasons_merged.csv')

    # Select features to use for model
    keys_to_select = select_features(df_all)

    # Plot correlation matrix of features
    plot_correlation_matrix(df_all[keys_to_select])

    # Create training data
    create_training_data(df_all, keys_to_select)

    # # API calls to load player data (Do once before each gameweek)
    # load_player_data()

    # Create test data
    next_gameweek = 13
    create_test_data(df_all, keys_to_select, next_gameweek)



if __name__ == '__main__':
    main()