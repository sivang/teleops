#!/usr/bin/env python
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import sqlite3
import shlex
import os
import subprocess
import commands
from two_factor import send_factor

class DevopsBot:
    authenticated = False
    auth_token = None
    MESSAGE_TYPE_START = "/start"
    def __init__(self):
        self.bot=None
        self.conn=None
        self.c=None
        self.mem_alert = False
        self.disk_alert = False

        # Initialize DB
        self.conn = sqlite3.connect('telegram.db')
        self.c = self.conn.cursor()
        
        # Create tables
        self.c.execute('''create table if not exists Telegram (name STRING, last_name STRING, userid STRING UNIQUE)''')

        # Initialize bot
        self.bot = TelegramBot('TELEGRAM_BOT_UNIQUE_ID_GOES_HERE')
        self.bot.update_bot_info().wait()

    def new_user(self, name, lastname, userid):
        # Insert a row of data
        print "DEBUG: %s , %s , %s " % (name , lastname, userid)
        strr="INSERT INTO Telegram VALUES (\""+name+"\",\""+lastname+"\",\""+str(userid)+"\")"
        print(strr)
        # Save (commit) the changes
        try:
            self.c.execute(strr)
            self.conn.commit()
            self._send_message(userid, "Welcome, "+name+" "+lastname)
        except:# sqlite3.IntegrityError:
            self._send_message(userid, "Thanks, "+name+" "+lastname+". No need to reregister")


    def _subproc_run(self, cmd, decode=True):
        print(cmd)
        log = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if not decode:
            return log.communicate()[0]
        return log.communicate()[0].strip()

    def _handle_message(self,message):
        print(str(message.text))
	if message.text == self.MESSAGE_TYPE_START:
		from random import randint
		rand_seed = randint(1000, 1999)
		send_factor.two_factor_authenticate(rand_seed, str(message.sender.id))
		self._send_message(message.sender.id, "Please enter the number token your received via SMS")
		self.auth_token = str(rand_seed)
		return
	if not self.authenticated and message.text.isdigit():
		if self.auth_token == message.text:
			self.new_user(message.sender.first_name, message.sender.last_name, message.sender.id)
			self.authenticated = True
			return 
		else:
			self._send_message(message.sender.id, 'Wrong token, try again.')
			return
	if not self.authenticated:
		if message.sender.id in self._get_users_list():
			self.authenticated = True
		else:
			self._send_message(message.sender.id, "Please authenticate using /start first.")
			return

        res="Command not understood"
        try:
            cmd_list = message.text.split()
            print(cmd_list)
            print(cmd_list[0])
            print(commands.allowable_commands)
            cmd = commands.allowable_commands[cmd_list[0]]
            cmd_list[0] = cmd
            print "DEBUG: %s" % cmd
            print("FINAL:"+cmd+"END")
            res = self._subproc_run(cmd_list)
            self._send_message(message.sender.id, res)
        except:
            self._send_message(message.sender.id, res)

    def _send_message(self, uid, message):
        self.bot.send_message(int(uid), message)

    def operation_loop(self):
        offset=0
        while (True):
            print(offset)
            updates = self.bot.get_updates(offset).wait()
            for cnt,update in enumerate(updates):
                self._handle_message(update.message)
                offset=update.update_id+1
            self._fire_alert()

    def _get_users_list(self):
        userslist = []
        self.c.execute("SELECT userid FROM Telegram")
        for row in self.c.fetchall():
            userslist.append(row[0])
        return userslist

    def _fire_alert(self):
        self.userlist = self._get_users_list()
        self.memory = os.path.isfile("/tmp/memfile")
        if self.memory is True and self.mem_alert is False:
            self.mem_alert = True
            for user in self.userlist:
                self._send_message(int(user), "Your system is unstable, check out Memory by typing /mem -m")
        
        if self.memory is False and self.mem_alert is True:
            for user in self.userlist:
                self._send_message(int(user), "Your system is now OK, Memory-wise")
                self.mem_alert = False
        
        self.disk_space = os.path.isfile("/tmp/diskfile")
        if self.disk_space is True and self.disk_alert is False:
            self.disk_alert = True
            for user in self.userlist:
                self._send_message(int(user), "Your system is unstable, check out disk_space by typing /df -h")
        
        if self.disk_space is False and self.disk_alert is True:
            for user in self.userlist:
                self._send_message(int(user), "Your system is now OK, Disk-wise")
                self.disk_alert = False
        

if (__name__ == "__main__"):
    botInstance = DevopsBot()
    botInstance.operation_loop()


