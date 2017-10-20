"""
RENAME config_template.py -> _config.py
"""
from collections import namedtuple

TelegramInfo = namedtuple(
    'TelegramInfo',
    'token bot_chat_id group_chat_id channel_id'
)
MySQLInfo = namedtuple(
    'MySQLInfo',
    'host port db user password charset'
)


# Modify None

# TELEGRAM BOT
telegram_info = TelegramInfo(
    token='',
    bot_chat_id=None,
    group_chat_id=None,
    channel_id=None,
)
# AWS RDS
mysql_info = MySQLInfo(
    host=None,
    port=3306,
    db=None,
    user=None,
    password=None,
    charset='utf8',
)
