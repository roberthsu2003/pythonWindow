import requests
from requests import Response
from pydantic import BaseModel, RootModel, Field,field_validator,ConfigDict
from datetime import datetime

def _download_json():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    try:
        res:Response = requests.get(url)
    except Exception:
        raise Exception("連線失敗")
    else:
        all_data:dict[any] = res.json()
        return all_data
    

class Info(BaseModel):
    sna:str
    sarea:str
    mday:datetime
    ar:str
    act:str
    updateTime:datetime
    total:int
    rent_bikes:int = Field(alias="available_rent_bikes")
    lat:float = Field(alias="latitude")
    lng:float = Field(alias="longitude")
    retuen_bikes:int = Field(alias="available_return_bikes")

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_validator("sna",mode='before')
    @classmethod
    def flex_string(cls, value:str)->str:
        return value.split(sep="_")[-1]

class _Youbike_Data(RootModel):
    root:list[Info]

def load_data()->list[dict]:
    all_data:dict[any] = _download_json()
    youbike_data:_Youbike_Data = _Youbike_Data.model_validate(all_data)
    data = youbike_data.model_dump()
    return data



class FilterData(object):
    @staticmethod
    def get_selected_coordinate(sna:str,data:list[dict]) -> Info:    
        right_list:list[dict] = list(filter(lambda item:True if item['sna']==sna else False ,data))
        data:dict = right_list[0]
        return Info.model_validate(data)
    

__all__ = ['load_data','FilterData']