"""
this is a commands 'database' to whitelist allowed command for
executiong on remote machine. The same simple manner as used
here: 
  - https://github.com/sivang/navistore/blob/master/navistore/backend/conf.py#L17
"""


allowable_commands = {
"/ls": "ls",
"/df": "df",
"/locate": "locate",
"/tail": "tail",
"/who": "who",
"/ps": "ps",
"/moo": "cowsay",
"/mem": "free",
}
