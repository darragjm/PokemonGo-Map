import time

import pymysql


class SpawnTracker(object):
    def __init__(self, connection_timeout=300):
        self.connection = None
        self.connection_timeout = connection_timeout
        self.reconnect_time = 0

    def connect(self):
        if time.time() > self.reconnect_time:
            try:
                self.connection.close()
            except:
                pass

            self.connection = pymysql.connect(host='HOSTNAME',
                                              user='USERNAME',
                                              password='PASSWORD',
                                              db='DATABASE',
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)

            self.reconnect_time = self.connection_timeout

    def add_spawn(self, pokemon_id, encounter_id, spawn_ts, spawn_duration, spawn_lat, spawn_lng):
        # Make sure we have a good connection
        self.connect()

        with self.connection.cursor() as cursor:
            # Create a new spawn record
            sql = """
                INSERT INTO `spawns`
                (`pokemon_id`, `encounter_id`, `spawn_ts`, `spawn_duration`, `spawn_lat`, `spawn_lng`)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE `pokemon_id` = `pokemon_id`"""
            cursor.execute(sql, (pokemon_id, encounter_id, spawn_ts, spawn_duration, spawn_lat, spawn_lng))

        self.connection.commit()

        return
