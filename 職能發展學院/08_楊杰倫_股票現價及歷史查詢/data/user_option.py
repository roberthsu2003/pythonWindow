import json


def load_user_option():
    '''讀取股票列表用'''
    with open("user_option.json", "r", encoding="utf-8") as f:
        a = json.loads(f.read())

    return a

def save_user_option(new_list):
    '''儲存股票列表用'''
    with open("user_option.json", "w", encoding="utf-8") as f:
        json.dump(new_list, f, ensure_ascii=False)


def load_history_option():
    '''讀取歷史視窗設定用'''
    with open("history_option.json", "r", encoding="utf-8") as f:
        a = json.loads(f.read())

    return a

def save_history_option(a,b):
    '''儲存歷史視窗設定用'''

    history_option = []
    history_option.append(str(a))
    history_option.append(str(b))
    with open("history_option.json", "w", encoding="utf-8") as f:
        json.dump(history_option, f, ensure_ascii=False)