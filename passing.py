import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from main import competitions
import time

start_time = time.time()

for i in competitions:
    comp_name = i
    comp_id = competitions[i]
    print(comp_name)
    url = f'https://fbref.com/en/comps/{comp_id}/passing/{comp_name}-Stats'
    result = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", result.text), features='html.parser')

    ## soup creation
    table = soup.find('table', id='stats_passing')

    ## Table headers
    heads = table.thead.find_all('tr')
    headers = []


    ## gets the header tags and returns a list containing all the data names
    def data_headers():
        for head in heads[0]:
            name = head.text
            headers.append(name)
        for head in heads[1]:
            name2 = head.text
            headers.append(name2)
        return headers


    ## main data list
    data_headers()

    ## end of table headers
    player_data = []
    ## getting player stats
    body_tag = table.tbody.find_all('tr')

    ## getting left stats:  left stat= name, nationality, team,
    stats_left = []
    for body in body_tag:
        stat = body.find_all('td', class_='left')
        stats_left.append(stat)

    for i in range(len(stats_left)):
        individual_stats = stats_left[i]
        for pos in range(len(individual_stats)):
            individual_stat = individual_stats[pos]
            data = individual_stat.text
            player_data.append(data)

    name = player_data[::4]
    nationality = player_data[1::4]
    team = player_data[2::4]
    ### end of left stats

    ### start of right stats |
    player_right_data = []
    stats_right = []
    stats_name = ['minutes_90s', 'passes_completed', 'passes', 'passes_pct', 'passes_total_distance',
                  'passes_progressive_distance', 'passes_completed_short', 'passes_short', 'passes_pct_short',
                  ' passes_completed_medium', 'passes_medium', 'passes_pct_medium', 'passes_completed_long',
                  'passes_long',
                  'passes_pct_long', 'assists', 'xg_assist', 'pass_xa', 'xg_assist_net', 'assisted_shots',
                  'passes_into_final_third', 'passes_into_penalty_area', 'crosses_into_penalty_area',
                  'progressive_passes']
    for body in body_tag:
        right_stat = body.find_all('td', class_='right')
        stats_right.append(right_stat)

    for i in range(len(stats_right)):
        individual_stats_right = stats_right[i]
        for pos in range(len(individual_stats_right)):
            individual_stat_right = individual_stats_right[pos]
            # print(individual_stat_right.attrs['data-stat'])
            data_right = individual_stat_right.text
            player_right_data.append(data_right)
        # print("-------------------------------------------")

    # print(player_right_data)
    ### right stats
    stats_no = len(stats_name)
    print(stats_no)
    minutes_90s = player_right_data[::stats_no]
    passes_completed = player_right_data[1::stats_no]
    passes = player_right_data[2::stats_no]
    passes_pct = player_right_data[3::stats_no]
    passes_total_distance = player_right_data[4::stats_no]
    passes_progressive_distance = player_right_data[5::stats_no]
    passes_completed_short = player_right_data[6::stats_no]
    passes_short = player_right_data[7::stats_no]
    passes_pct_short = player_right_data[8::stats_no]
    passes_completed_medium = player_right_data[9::stats_no]
    passes_medium = player_right_data[10::stats_no]
    passes_pct_medium = player_right_data[11::stats_no]
    passes_completed_long = player_right_data[12::stats_no]
    passes_long = player_right_data[13::stats_no]
    passes_pct_long = player_right_data[14::stats_no]
    assists = player_right_data[15::stats_no]
    xg_assist = player_right_data[16::stats_no]
    pass_xa = player_right_data[17::stats_no]
    xg_assist_net = player_right_data[18::stats_no]
    assisted_shots = player_right_data[19::stats_no]
    passes_into_final_third = player_right_data[20::stats_no]
    passes_into_penalty_area = player_right_data[21::stats_no]
    crosses_into_penalty_area = player_right_data[22::stats_no]
    progressive_passes = player_right_data[23::stats_no]
    ### right stats end
    ### Middle stats start | pos, age, born year
    player_center_data = []
    stats_center = []

    for body in body_tag:
        middle_stat = body.find_all('td', class_='center')
        stats_center.append(middle_stat)

    for i in range(len(stats_center)):
        individual_stats_center = stats_center[i]
        # print(individual_stats_center)
        for pos in range(len(individual_stats_center)):
            individual_stat_center = individual_stats_center[pos]
            data_center = individual_stat_center.text
            player_center_data.append(data_center)

    position = player_center_data[::3]
    age = player_center_data[1::3]
    born = player_center_data[2::3]
    ### Middle stats end

    ### Making data frame from lists
    main_data = list(zip(name, nationality, team, minutes_90s, passes_completed, passes, passes_pct,
                         passes_total_distance, passes_progressive_distance, passes_completed_short, passes_short,
                         passes_pct_short, passes_completed_medium, passes_medium, passes_pct_medium,
                         passes_completed_long, passes_long, passes_pct_long, assists, xg_assist, pass_xa,
                         xg_assist_net, assisted_shots, passes_into_final_third, passes_into_penalty_area,
                         crosses_into_penalty_area, progressive_passes, position, age, born))
    print(main_data)
    stats_names = ['name', 'nationality', 'team', 'minutes_90s', 'passes_completed', 'passes', 'passes_pct',
                   'passes_total_distance',
                   'passes_progressive_distance', 'passes_completed_short', 'passes_short', 'passes_pct_short',
                   'passes_completed_medium', 'passes_medium', 'passes_pct_medium', 'passes_completed_long',
                   'passes_long', 'passes_pct_long', 'assists', 'xg_assist', 'pass_xa', 'xg_assist_net',
                   'assisted_shots', 'passes_into_final_third', 'passes_into_penalty_area', 'crosses_into_penalty_area',
                   'progressive_passes', 'position', 'age', 'born']

    player_passing = pd.DataFrame(main_data, columns=stats_names)
    # print(player_passing)
    player_passing.to_csv(f'player_passing_{comp_name}.csv')
stop_time = time.time()
execution_time = stop_time - start_time
print(f"Execution time:{execution_time} seconds")
