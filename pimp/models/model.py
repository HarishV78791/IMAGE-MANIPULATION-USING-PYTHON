import json
import settings as st
import datetime

def update_config_file(data, file_path = st.CONFIG_FILE):
    with open(file_path) as config_file:
        config = json.load(config_file)
        config.update(data)
    
    with open(file_path,'w') as config_file:
        json.dump(config, config_file, indent=4)


def update_last_login_date_time():
    now = datetime.datetime.now()
    data = {"LAST_LOGIN" : str(now)}
    update_config_file(data)


def update_last_image():
    pass