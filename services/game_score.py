import config
from model import match_model


def open_log(path_to_file):
    try:
        with open(path_to_file, 'r') as game_log:
            log = game_log.readlines()
            return log
    except IOError:
            return config.ERROR_OPEN_FILE


def create_match(log):
    if 'New match' in log[0]:
        first_line = log[0].split(' ')
        id = first_line[5]
        date = first_line[0]
        hour = first_line[1]
        new_match = match_model.Match(id,date,hour)
        return new_match
    return config.ERROR_FILE_CONFIG


def died(name, match):
    dead_player = filter(lambda player: player.name == name, match.players)[0]
    dead_player.deaths += 1
    return dead_player.deaths


def player_kill_line(line, match):
    player_name = line[3]
    dead_player = line[5]
    gun = line[-1].rstrip()
    if player_name in match.players_name:
        player = filter(lambda player: player.name == player_name, match.players)[0]
        player.kills += 1
        try:
            player.guns[gun] += 1
        except KeyError:
            player.guns[gun] = 1
    else:
        player = match.add_new_player(player_name)
        player.kills += 1
        try:
            player.guns[gun] += 1
        except KeyError:
            player.guns[gun] = 1
    if dead_player in match.players_name:
        died(dead_player,match)
    else :
        match.add_new_player(dead_player)
        died(dead_player,match)


def print_rank(ranking):
    print "Name\tKills\tDeaths"
    for player in ranking:
        if len(player.name) <= 3:
            print player.name + "    \t" + str(player.kills) + "\t\t" + str(player.deaths)
        elif len(player.name)>7:
            print player.name[:7] + "\t" + str(player.kills) + "\t\t" + str(player.deaths)
        else:
            print player.name + "\t" + str(player.kills) + "\t\t" + str(player.deaths)
    return 'Success'


def final_score(match, log):
    log.pop(0)
    for line in log:
        log_line = line.split(' ')
        if match.verify_date(log_line[0]) and match.verify_time(log_line[1]):
            if 'ended' in line and match.verify_id(log_line[4]):
                rank = sorted(match.players, key=lambda d: d.deaths)
                rank = sorted(rank, key=lambda k: k.kills, reverse=True)
                return print_rank(rank)
            elif '<WORLD>' in line:
                name = log_line[5]
                if name in match.players_name:
                    died(name,match)
                else:
                    match.add_new_player(name)
                    died(name,match)
            elif 'using' in line:
                    player_kill_line(log_line,match)
            else:
                return config.ERROR_FILE_CONFIG
        else:
            return config.ERROR_FILE_CONFIG


#if __name__ == '__main__':
#   log_file = open_log(config.FILE_PATH)
#    match_rank = create_match(log_file)
#    print final_score(match_rank,log_file)

