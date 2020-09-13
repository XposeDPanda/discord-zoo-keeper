import os
import discord
import mysql.connector
from mysql.connector import errorcode

class Storage():
    def __init__(self):
        self.DB_user = os.getenv('DB_user')
        self.DB_pass = os.getenv('DB_pass')
        self.DB_host = os.getenv('DB_host')
        self.DB_name = os.getenv('DB_name')

        self.defaultGuildQuery = "INSERT INTO guilds (guildID, titleRecog) VALUES ({}, 0);"

        try:
            self.cnx = mysql.connector.connect(
                host = self.DB_host,
                user = self.DB_user,
                password = self.DB_pass,
                database = self.DB_name
            )
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access to database Denied, please ensure your .env file is configured correctly.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist, please ensure your .env file is configured correctly.")
            else:
                print(err)


    def isEnabled(self, guild: discord.Guild, module: str):
        self.cursor.execute(f"SELECT {module} FROM guilds WHERE guildID = '{guild.id}'")
        result = self.cursor.fetchone().get(f'{module}')
        if result == 1:
            return True
        else:
            return False


    def checkTableExists(self, tableName: str):
        self.cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{tableName}'
        """)
        if self.cursor.fetchone()[0] == 1:
            return True

        return False


    def add_guild(self, guild: discord.Guild):
        if self.checkTableExists('guilds') == True:
            try:
                self.cursor.execute(self.defaultGuildQuery.format(guild.id))
                self.cnx.commit()
            except mysql.connector.Error as err:
                print(err)
        else:
            try:
                self.cursor.execute(f"""CREATE TABLE `guilds` (
                    `ID` int NOT NULL AUTO_INCREMENT,
                    `guildID` varchar(255) DEFAULT NULL,
                    `titleRecog` TINYINT(1) DEFAULT NULL,
                    PRIMARY KEY (`ID`),
                    UNIQUE KEY `ID_UNIQUE` (`ID`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")
                self.cursor.execute(self.defaultGuildQuery.format(guild.id))
                self.cnx.commit()
            except mysql.connector.Error as err:
                print(err)