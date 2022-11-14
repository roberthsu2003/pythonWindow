import private
import datasource



def main():
    api_key = private.secret.open_weather_key
    try:
        city = datasource.get_forcase_data("Taipei",api_key)
    except Exception as e:
        print(e)
        return

    print(city)
    



if __name__ == "__main__":
    main()