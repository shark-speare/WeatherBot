import discord
from discord.ext import commands
import requests
import json
from classes import Ext

class Local(Ext):
    def __init__(self,bot):
        self.apikey = "CWA-3FF8D5E8-035D-4F66-BD63-CFF6EDB21C2D"
        self.url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-089"
        self.params = {"Authorization":self.apikey,"format":"JSON"}

    @commands.command(description="全台縣市近3小時天氣預報")
    async def local(self,ctx,location,hour:int=0):
        if hour <= 96:
            index = hour // 3

            self.params["locationName"] = location
            dataset = requests.get(url= self.url, params=self.params).json()["records"]["locations"][0]["location"][0]["weatherElement"][6]["time"]

            value = dataset[index]["elementValue"][0]["value"]

            await ctx.send(f"{location}近{3*index}~{3*(index+1)}小時預報:\n{value}")
    
        else:
            await ctx.send("最多提供96小時的資料，資料序需小於32")

async def setup(bot):
    await bot.add_cog(Local(bot))

        


