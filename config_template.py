"""
RENAME config_template.py -> _config.py
Modify None
Auxiliary 인스턴스에서 이 파일이 있어야 데이터베이스 접속이 가능합니다.
이 프로젝트를 Fork 후 사용해보시기 바랍니다.
"""
# FIXME
# TELEGRAM BOT
telegram_info = {
    'token': None,
    'bot_chat_id': None,
    'group_chat_id': None,
    'channel_id': None,
}

# AWS RDS
mysql_info = {
    'host': None,
    'port': 3306,
    'db': 'gdg',
    'user': 'gdg_master',
    'password': None,       # TODO: Database password 은닉화
    'charset': 'utf8',
}
