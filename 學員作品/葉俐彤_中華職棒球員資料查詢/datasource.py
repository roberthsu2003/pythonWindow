import csv
import sqlite3

__all__=['update_sqlite_data']

def __open_cpbl_data() ->list[dict]:

    pitchings_2022 = 'pitchings_2022_updated.csv'
    try:
        with open (pitchings_2022, mode='r', encoding='utf-8', newline='') as pitchings_file:
            pitchings_dictReader = csv.DictReader(pitchings_file)
            print('讀取成功')
            return list(pitchings_dictReader)
    except Exception as e:
            print(f'讀取錯誤{e}')
            return  []
def pr_value():
    #計算K9平均值
    def calculate_k9(so, ip):
        try:
            k9 = (so / ip) * 9
            return round(k9, 2)
        except ZeroDivisionError:
            return 0.0

    #計算ERA平均值
    def calculate_era(er, ip):
        try:
            era = (er * 9) / ip
            return round(era, 2)
        except ZeroDivisionError:
            return 0.0
    pitchings_2022 = 'pitchings_2022_updated.csv'

    # 初始化變數以保存平均值
    total_k9 = 0.0
    total_era = 0.0
    count = 0

    with open(pitchings_2022, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            so = float(row['SO'])
            ip = float(row['IP'])
            er = float(row['ER'])

            k9 = calculate_k9(so, ip)
            era = calculate_era(er, ip)

            total_k9 += k9
            total_era += era
            count += 1

    # 計算平均值
    average_k9 =round((total_k9 / count if count > 0 else 0.0),2)
    average_era =round((total_era / count if count > 0 else 0.0),2)

    print(f'平均 K9: {average_k9}')
    print(f'平均 ERA: {average_era}')

    return average_k9, average_era


#-------------------建立資料庫--------------------
def __create_table(conn:sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute( 
        '''
        CREATE TABLE  IF NOT EXISTS 'cpbl_pitchings'(        
            "年份"	TEXT NOT NULL,
            "所屬球隊" TEXT NOT NULL,
            "球員編號" INTEGER NOT NULL,
            "球員姓名" TEXT NOT NULL,
            "出場數" TEXT NOT NULL,
            "先發次數" INTEGER,
            "中繼次數" INTEGER,
            "勝場數" INTEGER,
            "敗場數" INTEGER,
            "救援成功" INTEGER,
            "中繼成功" INTEGER,
            "有效局數" INTEGER,
            "面對打者數" INTEGER,
            "被安打數" INTEGER,
            "被全壘打數" INTEGER,
            "保送數" INTEGER,
            "三振數" INTEGER,
            "自責分" INTEGER,
            "投打習慣" TEXT NOT NULL,
            "背號" INTEGER,
            "身高體重" TEXT NOT NULL,
            "生日" TEXT NOT NULL,
            "照片網址" TEXT NOT NULL,
            "奪三振率" FLOAT NOT NULL,
            "防禦率" FLOAT NOT NULL,
            PRIMARY KEY("球員編號" AUTOINCREMENT),
            UNIQUE(年份, 球員編號, 球員姓名) ON CONFLICT REPLACE
        ); 
        '''
    ) 
    conn.commit() 
    cursor.close()

def __insert_data(conn:sqlite3.Connection,values:list[any])->None:
    cursor = conn.cursor()
    sql='''
    REPLACE INTO cpbl_pitchings(年份, 所屬球隊, 球員編號, 球員姓名, 出場數, 先發次數, 中繼次數, 勝場數, 敗場數, 救援成功, 中繼成功, 有效局數, 面對打者數, 被安打數, 被全壘打數, 保送數, 三振數, 自責分, 投打習慣, 背號, 身高體重, 生日, 照片網址, 奪三振率, 防禦率)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    cursor.execute(sql,values)
    conn.commit()
    cursor.close()

#把資料匯入資料庫sqlite
def update_sqlite_data()->None:
    '''
    讀取資料並寫入資料庫
    '''
    data = __open_cpbl_data()
    conn = sqlite3.connect('cpbl.db')
    print('寫入環節')
    #print(data)
    __create_table(conn)
    for item in data:
        __insert_data(conn, values=[item['Year'], item['Team Name'], item['ID'], item['Name'], item['G'], item['GS'], item['GR'],item['W'], item['L'], item['SV'], item['HLD'], item['IP'], item['BF'], item['H'],item['HR'], item['BB'], item['SO'], item['ER'], item['B_t'], item['Number'], item['Ht_wt'],item['Born'],item['Img'],item['K9'],item['ERA']])
    conn.close() 

#從資料庫中呼叫最新的資料
def lastest_datetime_data()->list[tuple]: 
    conn = sqlite3.connect('cpbl.db')    
    cursor = conn.cursor() 
    #匯入SQL語法
    sql = '''
    SELECT *
    FROM cpbl_pitchings
    '''
    cursor.execute(sql) #執行SQL
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#---------------------查詢功能------------------------

def search_sitename(word:str) ->list[tuple]:
    conn = sqlite3.connect('cpbl.db')    
    cursor = conn.cursor() 
    sql = '''
    SELECT *
    FROM cpbl_pitchings
    WHERE 球員姓名 LIKE ?
        '''
    cursor.execute(sql,[f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows

def team_selected(event, selectVar):
    select_value = selectVar.get()
    print(f"隊伍選擇: {select_value}")
    return select_value

def search_by_team(event,word:str):
    print(word) #使用者輸入的文字
    conn = sqlite3.connect('cpbl.db')    
    cursor = conn.cursor() 
    sql = '''
    SELECT *
    FROM cpbl_pitchings
    WHERE 所屬球隊 LIKE ?
    '''
    cursor.execute(sql, [f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    #print(rows)
    return rows