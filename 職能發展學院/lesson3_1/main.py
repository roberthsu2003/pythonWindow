import report as re  #改名
from report import PI,get_description,Student #import 局部的module內容
import source.weather as sw
import source.daily as sd

if __name__ == "__main__":
    sw.callMyName()
    sd.callMyName()