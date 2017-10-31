import config
from datetime import datetime
from model import player_model


class Match:

    def __init__(self,id, date,start_hour):
        self.id = id
        self.date = datetime.strptime(date,config.DATE_PATTERN)
        self.start_time = datetime.strptime(start_hour, config.TIME_PATTERN)
        self.end_time = ''
        self.players_name =[]
        self.players = []
        self.guns = []

    def date_equals(self,date):
        if datetime.strptime(date,config.DATE_PATTERN) == self.date:
            return True
        return False

    def hour_equals(self,hour,witchHour):
        if witchHour == 'start':
            if datetime.strptime(hour, config.TIME_PATTERN) == self.start_time:
                return True
        elif witchHour == 'end':
            if datetime.strptime(hour, config.TIME_PATTERN) == self.end_time:
                return True
        return False

    def set_end_hour(self,hour):
        self.end_time = datetime.strptime(hour, config.TIME_PATTERN)

    def verify_date(self,date_to_check):
        date_to_check = datetime.strptime(date_to_check,config.DATE_PATTERN)
        if date_to_check == self.date:
            return True
        else:
            return False

    def verify_time(self,hour_to_check):
        hour_to_check = datetime.strptime(hour_to_check,config.TIME_PATTERN)
        if hour_to_check >= self.start_time:
            return True
        else:
            return False

    def verify_id(self, id):
        if id == self.id:
            return True
        else:
            return False

    def add_new_player(self,name):
        player = player_model.Player(name)
        self.players.append(player)
        self.players_name.append(name)
        return player