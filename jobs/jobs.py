from django.conf import settings
from reviews.models import Food
import pandas
from django.utils import timezone
import datetime

#get_foods() code edited from https://github.com/AdamSedla/TelegramMenuBot/blob/main/MenuPart.py


def get_foods():
    GSheet = "1JpEUpUJ3slFP1y2PgJV1J_2_sBf5VOek4TUcq90P_Cs"

    sheet_url = "https://docs.google.com/spreadsheets/d/"+ GSheet + "/export?format=csv"

    x = pandas.read_csv(sheet_url).to_dict()


    FirstLane = 4
    DayDifference = 7
    Message = []
    day = datetime.datetime.today().weekday()

    Menu = {"Polévka": x["Unnamed: 2"][FirstLane + DayDifference * day],
            "Ňamka": x["Unnamed: 2"][FirstLane + DayDifference * day + 1],
            "Oběd 1": x["Unnamed: 2"][FirstLane + DayDifference * day + 2],
            "Oběd 2": x["Unnamed: 2"][FirstLane + DayDifference * day + 3],
            "Oběd 3": x["Unnamed: 2"][FirstLane + DayDifference * day + 4]
            }

    for key, value in Menu.items():
        if str(value) != "nan":
            Message.append(value)

    
    return Message

def job():
    scrape_food = get_foods()
                   
    for i in scrape_food:
            if not Food.objects.filter(title=str(i)).exists():
                food_instance = Food()
                food_instance.upload_date = timezone.now()
                food_instance.title = i
                food_instance.save()
                print(f"Food {i} saved")


