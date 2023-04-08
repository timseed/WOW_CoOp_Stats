#1028590701	BannerMan
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_clan_members()->pd.DataFrame:
    CLAN_URL="https://na.wows-numbers.com/clan/1000079900,RSR-Red-Storm-Rising/"

    clan_data=requests.get(CLAN_URL)
    clan_dfs=pd.read_html(clan_data.text)

    #Convert to straight HTML
    soup=BeautifulSoup(clan_data.text, "html.parser")

    #in Firefox inspector - select this
    #we can see this is table id="members-table" so.... 
    members_html=soup.find( "table", {"id":"members-table"})
    
    # Need to convert the HTML - remove and href and replace with two TD values
    #We want to grab the PlayerName and the ID from this href construct
    ref_syntax = re.compile(r"<a href=\"/player/([0-9]+),([A-Za-z0-9_]+)/\">[A-Za-z0-9_]+</a>")
    b=""
    for a in members_html.decode().split('\n'):
        wanted = ref_syntax.findall(a)
        if len(wanted)!=0:
            #print(wanted)
            a=f"<td>{wanted[0][0]}</td><td>{wanted[0][1]}</td>"
        b+=a+"\n"
    rsr_clan=pd.read_html(b)[0]
    rsr_clan.head()
    
    #rsr_clan.reset_index(0,inplace=True)
    cols=[]
    if (len(rsr_clan.columns)==17):
        cols=['unk1','pid','Player','rank','Battles',
          'Win rate','PR','Avg. damage','Max. damage','StrengthCA','StrengthCV',
          'StrengthDD','StrengthBB','StrengthTotal','StrengthClan battles','T-10Ships','UNK2']
    else:
        cols=['unk1','pid','Player','rank','Battles',
          'Win rate','PR','Avg. damage','Max. damage','StrengthCA','StrengthCV',
          'StrengthDD','StrengthBB','StrengthTotal','StrengthClan battles','T-10Ships']
    b=[a[0] for a in list(rsr_clan.columns)]
    rsr_clan.columns=cols
    rsr_clan.drop(['unk1'],axis=1,inplace=True)
    
    return rsr_clan
      
    
    
def get_player_random_count(pid,name)->int:
    try:
        PLAYER_URL="https://na.wows-numbers.com/player/{0},{1}/"
        pu = str.format(f"{PLAYER_URL}",pid,name)
        print(f"Url is {pu}")
        person_data=requests.get(pu)

        #Get data parse
        soup=BeautifulSoup(person_data.text, "html.parser")
        #Find table
        table_random = soup.find("div",{"class":"table-responsive"})
        df_random=pd.read_html(table_random.decode())[0]
        # Read Extracted secion as html
        #This can have random size... for active player (me, banner etc)
        df_random.columns=['unk1','Overall','Recent','Last7','Unk2','Unk3']

        rand_total=int(df_random.iloc[[1]]['Overall'][1].replace(' ',''))
    except Exception as e:
        return -1
    return rand_total


def get_player_coop_count(pid,name)->int:
    try:
        # Slightly different URL
        PLAYER_URL="https://na.wows-numbers.com/player/{0},{1}/?type=pve"
        pu = str.format(f"{PLAYER_URL}",pid,name)
        print(f"Url is {pu}")
        person_data=requests.get(pu)
        soup=BeautifulSoup(person_data.text, "html.parser")

        table_random = soup.find("div",{"class":"table-responsive"})
        coop_stats=pd.read_html(table_random.decode())[0]

        if len(coop_stats.columns)==6:
            coop_stats.columns=['unk1','Overall','Recent','Last7','Unk2','Unk3']
        #data is on 2nd line index of 1
        battle_total=int(coop_stats.iloc[[1]]['Overall'][1].replace(' ',''))
    except Exception as err:
        return -1
    return battle_total
