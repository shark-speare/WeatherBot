import discord
from discord.ext import commands
import requests
import json
from classes import Ext


class City(Ext):
    def __init__(self,bot):
        self.apikey = "CWA-3FF8D5E8-035D-4F66-BD63-CFF6EDB21C2D"
        self.url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-007"
        self.params = {"Authorization":self.apikey,"format":"JSON"}
        self.data = requests.get(url=self.url, params=self.params).json()["cwaopendata"]["dataset"]["location"]

    @commands.command()
    async def city(self,ctx,location):
        # 尋找地點在清單中的位置
        for datas in self.data:
            if location == datas["locationName"]:
                index = self.data.index(datas)
                break
        
        # 將dataset設為該地區的資料
        dataset = self.data[index]["weatherElement"]
        
        d1, d2, d3 = {},{},{}
        
        # 將三天的資料分別寫入三個紀錄辭典內
        # 第一個[0]為天氣資料，第二個[0]為天
        # 由於wx的資料結構不同，所以用if else分開處理
        for eindex,ele in enumerate(["wx","tmax","tmin"],start=0):
            for dindex,day in enumerate([d1,d2,d3]):
        
                if ele == "wx":
                    day[ele] = dataset[eindex]["time"][dindex]["elementValue"][0]["value"]
                else:
                    day[ele] = dataset[eindex]["time"][dindex]["elementValue"]["value"]


        # 發送資料
        await ctx.send(f"{location}三日天氣預報")
        for day, des in zip([d1,d2,d3],["明天","後天","大後天"]):
            await ctx.send(f"{des}:\n天氣為{day['wx']}，溫度{day['tmin']}°C - {day['tmax']}")

async def setup(bot):
    await bot.add_cog(City(bot))
