import datasource

def main():
    print("這裏是main function")
    list_data = datasource.get_forcast_data()
    for item in list_data:
        print(item['dt_txt'])

if __name__ == "__main__":
    print("這裏是程式的執行點")
    main()
