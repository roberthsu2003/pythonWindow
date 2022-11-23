import datasource

def main():
    print("這裏是main function")
    all_data = datasource.get_forcast_data()
    print(type(all_data))

if __name__ == "__main__":
    print("這裏是程式的執行點")
    main()
