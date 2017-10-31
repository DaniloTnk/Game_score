from __future__ import absolute_import

import unittest

import config
from model import player_model
from services import game_score


class GameScoreTests(unittest.TestCase):
    def create_match(self):
        log = game_score.open_log('test.log')
        match = game_score.create_match(log)
        return match

    def test_open_log(self):
        log = game_score.open_log('test.log')
        self.assertEqual(type(log),list)

    def test_error_open_log(self):
        log = game_score.open_log('x' + 'test.log')
        self.assertEqual(log, config.ERROR_OPEN_FILE)

    def create_player(self):
        player = player_model.Player(config.PLAYER_NAME)
        return player

    def test_create_player(self):
        player = self.create_player()
        self.assertEqual(config.PLAYER_NAME,player.name)

    def test_player_attributes(self):
        player = self.create_player()
        score = 2
        player.deaths = score
        player.kills = score
        player.is_alive = False
        player.guns = config.PLAYER_GUNS
        self.assertEqual(score,player.deaths)
        self.assertEqual(score, player.kills)
        self.assertFalse(player.is_alive)
        self.assertEqual(config.PLAYER_GUNS,player.guns)

    def test_create_match(self):
        match = self.create_match()
        self.assertEqual(config.MATCH_ID,match.id)
        self.assertTrue(match.date_equals(config.MATH_DATE))
        self.assertTrue(match.hour_equals(config.MATCH_START_HOUR,'start'))

    def test_date_not_equals(self):
        match = self.create_match()
        self.assertFalse(match.date_equals('23/04/2014'))

    def test_match_attributes(self):
        match = self.create_match()
        match.set_end_hour(config.MATCH_START_HOUR)
        match.players_name.append(config.PLAYER_TEST['name'])
        match.players.append(config.PLAYER_TEST)
        for gun in config.GUNS_LIST:
            match.guns.append(gun)
        self.assertTrue(match.hour_equals(config.MATCH_START_HOUR,'end'))
        self.assertEqual(match.players[0], config.PLAYER_TEST)
        self.assertEqual(match.guns, config.GUNS_LIST)

    def test_hour_not_equals(self):
        match = self.create_match()
        match.set_end_hour(config.MATCH_START_HOUR)
        self.assertFalse(match.hour_equals('08:34:22', 'end'))


    def test_create_match_from_game_score(self):
        log = game_score.open_log('test.log')
        match = game_score.create_match(log)
        id = log[0].split(' ')[5]
        self.assertEqual(id,match.id)

    def test_create_match_error(self):
        log = game_score.open_log('test.log')
        log = log[1:]
        match = game_score.create_match(log)
        self.assertEqual(match,config.ERROR_FILE_CONFIG)

    def test_final_score_error_on_log(self):
        log = game_score.open_log('log_with_error.log')
        match = game_score.create_match(log)
        result = game_score.final_score(match,log)
        self.assertEqual(result,config.ERROR_FILE_CONFIG)

    def test_verify_date(self):
        match = self.create_match()
        self.assertTrue(match.verify_date('23/04/2013'))
        self.assertFalse(match.verify_date('23/04/2014'))

    def test_verify_time(self):
        match = self.create_match()
        self.assertTrue(match.verify_time('15:34:33'))
        self.assertFalse(match.verify_time('15:32:33'))

    def test_new_player(self):
        name = 'Player1'
        match = self.create_match()
        player = match.add_new_player(name)
        self.assertEqual(player,match.players[0])

    def test_player_death(self):
        match = self.create_match()
        name = 'Player1'
        match.add_new_player(name)
        game_score.died(name,match)
        player = filter(lambda player: player.name == name, match.players)[0]
        self.assertEqual(player.deaths,1)

    def test_player_kill(self):
        match = self.create_match()
        line = '23/04/2014 15:36:04 - Player1 killed Player2 using GUN'
        line = line.split(' ')
        game_score.player_kill_line(line,match)
        player1 = filter(lambda player: player.name == 'Player1', match.players)[0]
        player2 = filter(lambda player: player.name == 'Player2', match.players)[0]
        self.assertEqual(player1.kills,1)
        self.assertEqual(player1.guns['GUN'],1)
        self.assertEqual(player2.deaths,1)
        line2 = '23/04/2014 15:37:04 - Player1 killed Player2 using GUN2'
        game_score.player_kill_line(line,match)
        self.assertEqual(player1.guns['GUN'],2)

    def test_final_score(self):
        log = game_score.open_log('complete_match.log')
        match = game_score.create_match(log)
        result = game_score.final_score(match,log)
        self.assertEqual(result,'Success')

    def test_final_score_error(self):
        log = game_score.open_log('log_with_error.log')
        match = game_score.create_match(log)
        result = game_score.final_score(match, log)
        self.assertEqual(result, config.ERROR_FILE_CONFIG)

    def test_verify_id_false(self):
        match = self.create_match()
        self.assertFalse(match.verify_id('123456'))



if __name__ == '__main__':
    unittest.main()

