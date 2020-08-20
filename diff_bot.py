import subprocess
import os
import discord
from discord.ext import tasks

import settings

TOKEN = settings.BOT_TOKEN

TIT_cmd = 'mkdir -p TIT && cd TIT && wget https://admissions.titech.ac.jp/examination/ -O $(date "+%Y%m%d-%H%M") -q'
UO_cmd = 'mkdir -p UO && cd UO && wget https://www.osaka-u.ac.jp/ja/admissions/faculty -O $(date "+%Y%m%d-%H%M") -q'
SU_cmd = 'mkdir -p SU && cd SU && wget http://www.saitama-u.ac.jp/entrance/requirements/ -O $(date "+%Y%m%d-%H%M") -q'
KU_cmd = 'mkdir -p KU && cd KU && wget https://www.keio.ac.jp/ja/admissions/ -O $(date "+%Y%m%d-%H%M") -q'
THU_cmd = 'mkdir -p THU && cd THU && wget http://www.tnc.tohoku.ac.jp/ -O $(date "+%Y%m%d-%H%M") -q'

TIT_flag = False
UO_flag = False
SU_flag = False
KU_flag = False
THU_flag = False


# 接続に必要なオブジェクトを生成
client = discord.Client()

def diff():
  global TIT_flag
  global UO_flag
  global SU_flag
  global KU_flag
  global THU_flag

  TIT_flag = False
  UO_flag = False
  SU_flag = False
  KU_flag = False
  THU_flag = False

  ref = os.system(TIT_cmd)
  if ref != 0:
    print('error1')
  
  ref = os.system(UO_cmd)
  if ref != 0:
    print('error2')
		
  ref = os.system(SU_cmd)
  if ref != 0:
    print('error3')
    
  ref = os.system(KU_cmd)
  if ref != 0:
    print('error4')
    
  ref = os.system(THU_cmd)
  if ref != 0:
    print('error5')
	
  #diff in TIT directory
  TIT_find = 'find TIT -type f -a  -amin -35'
  TIT_data = subprocess.check_output(TIT_find.split())
  TIT_diff_cmd = 'diff' + ' ' + TIT_data.decode().splitlines()[0] + ' ' + TIT_data.decode().splitlines()[1]
  try:
    TIT_ref = subprocess.check_output(TIT_diff_cmd.split())
    print('1_same!')
  
  except subprocess.CalledProcessError as cpe:
    #global TIT_flag
    TIT_flag = True
    print('1_diff!')

  #diff in UO directory
  UO_find = 'find UO -type f -a  -amin -35'
  UO_data = subprocess.check_output(UO_find.split())
  UO_diff_cmd = 'diff' + ' ' + UO_data.decode().splitlines()[0] + ' ' + UO_data.decode().splitlines()[1]
  try:
    UO_ref = subprocess.check_output(UO_diff_cmd.split())
    print('2_same!')
  
  except subprocess.CalledProcessError as cpe:
   # global UO_flag 
    UO_flag = True
    print('2_diff!')

  #diff in SU directory
  SU_find = 'find SU -type f -a  -amin -35'
  SU_data = subprocess.check_output(SU_find.split())
  SU_diff_cmd = 'diff' + ' ' + SU_data.decode().splitlines()[0] + ' ' + SU_data.decode().splitlines()[1]
  try:
    SU_ref = subprocess.check_output(SU_diff_cmd.split())
    print('3_same!')
  
  except subprocess.CalledProcessError as cpe:
    #global SU_flag 
    SU_flag = True
    print('3_diff!')

  #diff in KU directory
  KU_find = 'find KU -type f -a  -amin -35'
  KU_data = subprocess.check_output(KU_find.split())
  KU_diff_cmd = 'diff' + ' ' + KU_data.decode().splitlines()[0] + ' ' + KU_data.decode().splitlines()[1]
  try:
    KU_ref = subprocess.check_output(KU_diff_cmd.split())
    print('4_same!')
  
  except subprocess.CalledProcessError as cpe:
   # global KU_flag 
    KU_flag = True
    print('4_diff!')

  #diff in THU directory
  THU_find = 'find THU -type f -a  -amin -35'
  THU_data = subprocess.check_output(THU_find.split())
  THU_diff_cmd = 'diff' + ' ' + THU_data.decode().splitlines()[0] + ' ' + THU_data.decode().splitlines()[1]
  try:
    THU_ref = subprocess.check_output(THU_diff_cmd.split())
    print('5_same!')
  
  except subprocess.CalledProcessError as cpe:
   # global THU_flag 
    THU_flag = True
    print('5_diff!')


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
      return
    
    if message.content == '!diff':
      diff()

      if TIT_flag == True:
        await message.channel.send('東京工業大学のホームページに更新があります！')
      
      if UO_flag == True:
        await message.channel.send('大阪大学のホームページに更新があります！')

      if SU_flag == True:
        await message.channel.send('埼玉大学のホームページに更新があります！')

      if KU_flag == True:
        await message.channel.send('慶應義塾大学のホームページに更新があります！')

      if THU_flag == True:
        await message.channel.send('東北大学のホームページに更新があります！') 
      
      if THU_flag == False and KU_flag == False and SU_flag == False and UO_flag == False and TIT_flag == False:
        await message.channel.send('各大学ホームページに更新はありません')
      
      find = 'find TIT -type f -a  -amin -35'
      data = subprocess.check_output(find.split())
      rep = '期間 : ' + data.decode().splitlines()[0] + ' ' + 'から' + ' ' + data.decode().splitlines()[1]
      await message.channel.send(rep)

@tasks.loop(seconds=1800)
async def loop():
    channel = client.get_channel(743522168478105649)
    
    diff()

    if TIT_flag == True:
      await channel.send('東京工業大学のホームページに更新があります！') 

    if UO_flag == True:
      await channel.send('大阪大学のホームページに更新があります！')

    if SU_flag == True:
      await channel.send('埼玉大学のホームページに更新があります！')

    if KU_flag == True:
      await channel.send('慶應義塾大学のホームページに更新があります！')

    if THU_flag == True:
      await channel.send('東北大学のホームページに更新があります！') 
      
    if THU_flag == False and KU_flag == False and SU_flag == False and UO_flag == False and TIT_flag == False:
      await channel.send('各大学ホームページに更新はありません')
    
    find = 'find TIT -type f -a  -amin -35'
    data = subprocess.check_output(find.split())
    rep = '期間 : ' + data.decode().splitlines()[0] + ' ' + 'から' + ' ' + data.decode().splitlines()[1]
    await channel.send(rep)

loop.start()

client.run(TOKEN)
