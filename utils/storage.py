import os
import discord
import mysql.connector

class Storage:
    def __init__(self):
        self.dbUser = os.getenv("DB_USER")
        self.dbPass = os.getenv("DB_PASS")
        self.dbName = os.getenv("DB_NAME")

        if not all((self.dbUser, self.dbPass, self.dbName)):
            print("Something went wrong while fetching the environment variables for the database. Please check the .env file is configured correctly.")
            sys.exit(1)

        self.conn = mysql.connector.connect(
            host="localhost",
            user=self.dbUser,
            password=self.dbPass,
            database=self.dbName
        )
    
    def getCursor(self):
        return self.conn.cursor(buffered=True)
    
    def executeSingleQuery(self, query):
        cursor = self.getCursor()
        cursor.execute(query)
        self.conn.commit()
        row = cursor.fetchone()
        cursor.close()
        return row

    def isEnabled(self, guild: discord.Guild, module: str):
        query = f'SELECT {module} FROM modules WHERE GuildID = {guild.id}'
        result = self.executeSingleQuery(query)
        if(result[0] == 1):
            return True
        else:
            return False

    def addGuild(self, guild: discord.Guild):
        query = f'INSERT INTO guilds (GuildID) VALUES ({guild.id})'
        self.executeSingleQuery(query)
        query = f'INSERT INTO modules (GuildID, mMderation, titleRecog, AmongUs) VALUES ({guild.id},{1},{0},{0})'
        self.executeSingleQuery(query)

    def leaveGuild(self, guild: discord.Guild):
        query = f'DELETE FROM guilds WHERE GuildID={guild.id}'
        self.executeSingleQuery(query)
        query = f'DELETE FROM modules WHERE GuildID={guild.id}'
        self.executeSingleQuery(query)

    def toggleModule(self, guild: discord.Guild, module: str):
        if(self.isEnabled(guild, module)):
            query = f'UPDATE modules SET {module} = 0 WHERE GuildID = {guild.id}'
        else:
            query = f'UPDATE modules SET {module} = 1 WHERE GuildID = {guild.id}'
        self.executeSingleQuery(query)

    def addWarn(self, warnID: str, guildID, user: discord.Member, wMsg):
        query = f'INSERT INTO warnings (WarnID, GuildID, User, Reason) VALUES ("{warnID}","{guildID}","{user.name}","{wMsg}")'
        self.executeSingleQuery(query)
    
    def removeWarn(self, warnID: str, guildID: str):
        query = f'DELETE FROM warnings WHERE WarnID = "{warnID}" AND GuildID = {guildID}'
        self.executeSingleQuery(query)