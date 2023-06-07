import pandas as pd                                 #pip install pandas
from sklearn.cluster import DBSCAN                  #pip install scikit-learn
from sklearn.preprocessing import StandardScaler
import os

pd.options.mode.chained_assignment = None           #not display message about settingWithCopyWarning 




def preprocessingOfBankName(atmMLData):
    # ------------------------------------------------------------
    dataMap = { 'A1':'火車站','A2':'火車站','A3':'火車站','A4':'火車站',
                'B1':'地方政府','B2':'地方政府',
                'H1':'醫院','H2':'醫院','H3':'醫院','H4':'醫院',
                'I1':'學校','I2':'學校','I3':'學校','I4':'學校',
                'C1':'公務機關',
                'D1':'高鐵站','E1':'客運站','F1':'捷運站','G1':'機場',
                'J1':'大賣場百貨','K1':'其他公場所','K2':'其他私場所','L1':'便利商店','O1':'其他私場所',' ':'行內營業所' }
    atmMLData['placetype'] = atmMLData['placetype'].map(dataMap).astype('object')
    
    # add fields of LnLaOfdistCenter-----------------------------------
    ## pd.read_excel('台灣中心點經緯度.xlsx',sheet_name='行政區中心點經緯度')
    LnLaOfdistCenter = pd.read_csv('中心點經緯度_行政區.csv')
    LnLaOfdistCenter['county'] = LnLaOfdistCenter['行政區名'].str[:3]
    LnLaOfdistCenter['district'] = LnLaOfdistCenter['行政區名'].str[3:]
    LnLaOfdistCenter['county'] = LnLaOfdistCenter['county'].str.replace('臺','台') 
    LnLaOfdistCenter['district'] = LnLaOfdistCenter['district'].str.replace('臺','台') 
    #pd.read_excel('台灣中心點經緯度.xlsx',sheet_name='縣市中心點經緯度')
    LnLaOfcoutCenter = pd.read_csv('中心點經緯度_縣市.csv')
    LnLaOfcoutCenter['county'] = LnLaOfcoutCenter['縣市名'].str.replace('臺','台') 
    LnLaOfcoutCenter['county'] = LnLaOfcoutCenter['county'].str.replace('桃園縣','桃園市') 

    ## merger fields from 中心點經緯度_行政區.csv and 中心點經緯度_縣市.csv
    ####中心點經緯度_行政區.csv
    atmMLData = atmMLData.merge(LnLaOfdistCenter, left_on=['county','district'], right_on = ['county','district'], how='left')
    atmMLData = atmMLData.drop(columns=['行政區名'])
    columnNewName = {'3碼郵遞區號':'zip3','中心點經度':'lngOfDisCenter','中心點緯度':'latOfDisCenter'}        
    atmMLData = atmMLData.rename(columns=columnNewName)    
    ####combine 中心點經緯度_縣市.csv
    atmMLData = atmMLData.merge(LnLaOfcoutCenter, left_on=['county'], right_on = ['county'], how='left')    
    atmMLData = atmMLData.drop(columns=['縣市名'])
    columnNewName = {'中心點經度':'lngOfCouCenter','中心點緯度':'latOfCouCenter'}        
    atmMLData = atmMLData.rename(columns=columnNewName)   
    # copy file ---------------------------------------------------
    atmMLData.to_csv('atmMLData.csv',encoding='utf_8_sig',index=False) 

    # add fields of bankbrifname-----------------------------------
    atmMLData['bankbrifname']=atmMLData['bankcode']    
    dataBrifMap = {4:'臺銀', 5:'土銀', 6:'合庫', 7:'一銀', 8:'華銀', 9:'彰銀', 13:'國世', 17:'兆豐', 50:'臺企', 806:'元大', 807:'永豐', 808:'玉山', 812:'台新', 822:'中信'}
    atmMLData['bankbrifname'] = atmMLData['bankbrifname'].map(dataBrifMap).astype('object')
    atmMLData['bankbrifname'] = atmMLData['bankbrifname'].fillna(value='郵局')

    # modify fields of PddtOfficeCode: from 701~723 to 700(all)----
    atmMLData['bankcode'].mask((atmMLData['bankcode'] >= 700) & (atmMLData['bankcode'] < 800), 700, inplace=True)    
    
    # select fields & value_counts---------------------------------
    atmMLData = atmMLData[['bankcode','bankbrifname','type','placetype','county','district','address','longitude','latitude','lngOfDisCenter','latOfDisCenter','lngOfCouCenter','latOfCouCenter']].value_counts().reset_index()
    atmMLData = atmMLData.rename(columns={'count': 'units'}).reset_index()
    atmMLData = atmMLData.drop(columns=['index'])
    
    return(atmMLData)



class atmSelectedList():
    def __init__(self,atmMLData,selectedBank='',selectedItem='') -> None:
        self.atmMLData = atmMLData
        self.selectedBank = selectedBank    
        self.selectedItem = selectedItem
        self.selectedCountyOfBank = self.atmMLData[self.atmMLData['bankbrifname']==self.selectedBank]
        #print(self.selectedCountyOfBank['placetype'].unique())

    def atmBankList(self):
        groupBankUnits = self.atmMLData.groupby('bankbrifname').agg(unitsCount=('units', 'count'))
        groupBankUnits = groupBankUnits.sort_values(by = 'unitsCount', ascending=False)
        groupBankUnits.reset_index(inplace=True)
        sumBankUnits = groupBankUnits['unitsCount'].sum()
        groupBankUnits['percent']   = groupBankUnits['unitsCount']/sumBankUnits*100
        groupBankUnits['percent']   = groupBankUnits['percent'].round(decimals = 3)
        groupBankUnits['perCumsum'] = groupBankUnits['percent'].cumsum()
        groupBankUnits['perCumsum'] = groupBankUnits['perCumsum'].round(decimals = 3)
        return groupBankUnits
    
    def atmBankListOfItem(self):
        groupCountyOfBankUnits = self.selectedCountyOfBank.groupby(self.selectedItem).agg(unitsCount=('units', 'count'))
        groupCountyOfBankUnits = groupCountyOfBankUnits.sort_values(by = 'unitsCount', ascending=False)
        groupCountyOfBankUnits.reset_index(inplace=True)
        sumCountyOfBankUnits = groupCountyOfBankUnits['unitsCount'].sum()
        groupCountyOfBankUnits['percent']   = groupCountyOfBankUnits['unitsCount']/sumCountyOfBankUnits*100
        groupCountyOfBankUnits['percent']   = groupCountyOfBankUnits['percent'].round(decimals = 3)
        groupCountyOfBankUnits['perCumsum'] = groupCountyOfBankUnits['percent'].cumsum()
        groupCountyOfBankUnits['perCumsum'] = groupCountyOfBankUnits['perCumsum'].round(decimals = 3)
        return groupCountyOfBankUnits
    


class atmRankAmongCompetitors():
    def __init__(self,atmSelectedData,selectedBank='',rankNo=3) -> None:
        self.atmSelectedData = atmSelectedData
        self.selectedBank = selectedBank       
        self.rankNo = rankNo

    def atmBankRateOfItem(self):
        groupBankUnits = self.atmSelectedData.groupby('bankbrifname').agg(unitsCount=('units', 'count'))
        groupBankUnits = groupBankUnits.sort_values(by = 'unitsCount', ascending=False)
        groupBankUnits.reset_index(inplace=True)
        tagtBank = groupBankUnits[groupBankUnits['bankbrifname']==self.selectedBank]
        rankBank = groupBankUnits[groupBankUnits['bankbrifname']!=self.selectedBank].iloc[ :self.rankNo  ,:]
        restTemp = groupBankUnits[groupBankUnits['bankbrifname']!=self.selectedBank].iloc[  self.rankNo: ,:]
        sizeAll = groupBankUnits['bankbrifname'].size + 10
        sizeRest = restTemp['bankbrifname'].size
        if sizeRest > 0:
            sum = restTemp.sum()
            restTemp.loc[sizeAll]=sum
            restTemp.loc[sizeAll,'bankbrifname']=f'{sizeRest}家'
            restBank = restTemp[restTemp['bankbrifname']==f'{sizeRest}家']        
            rateBankOfCounty = pd.concat([tagtBank,rankBank,restBank])  
        else:                 
            rateBankOfCounty = pd.concat([tagtBank,rankBank])  
        return rateBankOfCounty


   
class atmScatterSizeOfDistrict():
    def __init__(self,atmSelectedData,grpBase='district') -> None:
        self.atmSelectedData = atmSelectedData
        self.grpBase = grpBase
        if self.grpBase == 'district' :
            self.anaLngtude = 'lngOfDisCenter'
            self.anaLattude = 'latOfDisCenter'
        else :
            self.anaLngtude = 'lngOfCouCenter'
            self.anaLattude = 'latOfCouCenter'


    def atmScatterSize(self):
        groupScatterSize = self.atmSelectedData.groupby([self.grpBase,self.anaLngtude,self.anaLattude]).agg(unitsCount=('units', 'count'))
        groupScatterSize = groupScatterSize.sort_values(by = 'unitsCount', ascending=False)
        groupScatterSize.reset_index(inplace=True)

        return groupScatterSize




class atmSklearnCluster():
    def __init__(self,atmMLData, stdType = 'maxStd', stdRatio = 1/55, stdQ25 = 'Y' , minSampleDbscan = 2) -> None:
        self.atmMLData = atmMLData
        self.stdType = stdType
        self.stdRatio = stdRatio
        self.stdQ25 = stdQ25
        self.minSampleDbscan = minSampleDbscan     
       
        # calculate radiusDBSCAN
        self.clusterRadiusDBSCAN = self.atmMLData.groupby(['county'], as_index=False).agg({'longitude': ['count','mean','std'],'latitude': ['mean','std']})          
        self.clusterRadiusDBSCAN.columns = ['county', 'units', 'lngMean', 'lngStd', 'latMean', 'latStd']
        self.clusterRadiusDBSCAN['stdType'] = self.stdType
        if self.stdType == 'minStd':
            self.clusterRadiusDBSCAN['selectedStd'] = self.clusterRadiusDBSCAN[['lngStd','latStd']].min(axis=1)
        else:
            self.clusterRadiusDBSCAN['selectedStd'] = self.clusterRadiusDBSCAN[['lngStd','latStd']].max(axis=1)
        self.clusterRadiusDBSCAN['q25Std'] = (self.clusterRadiusDBSCAN['selectedStd']).quantile(0.25)  
        self.clusterRadiusDBSCAN['stdRatio'] = self.stdRatio

        if self.stdQ25 == 'Y':
            for couVar in range(self.clusterRadiusDBSCAN['county'].size): 
                if self.clusterRadiusDBSCAN.loc[couVar,'selectedStd'] < self.clusterRadiusDBSCAN.loc[couVar,'q25Std']:
                    self.clusterRadiusDBSCAN.loc[couVar,'selectedStd'] = self.clusterRadiusDBSCAN.loc[couVar,'q25Std']
                    self.clusterRadiusDBSCAN.loc[couVar,'stdType'] = 'q25Std'


        self.clusterRadiusDBSCAN['radiusDbscan'] = self.clusterRadiusDBSCAN['selectedStd'] * self.clusterRadiusDBSCAN['stdRatio']
        #print(self.clusterRadiusDBSCAN)
        # extra adjust radius when stdQ25 than Q3-Q1 or upper than Q3-Q1        
       
        self.clusterRadiusDBSCAN = self.clusterRadiusDBSCAN.sort_values(by = 'units', ascending=False)
        self.clusterRadiusDBSCAN.reset_index(inplace=True)
        self.clusterRadiusDBSCAN = self.clusterRadiusDBSCAN.drop(columns=['index'])
        

    
    def atmClusterDBSCAN(self):   
        for i in range(self.clusterRadiusDBSCAN['county'].size): 
            # prepare parameters of DBSCAN: eps
            tmpDBSCAN = self.atmMLData[self.atmMLData['county']==self.clusterRadiusDBSCAN.iloc[i,0]]            
            radiusDbscan = self.clusterRadiusDBSCAN['radiusDbscan'][i]

            # process Z分數標準化 before DBSCAN
            zStd = StandardScaler()
            stdTmpDBSCAN = tmpDBSCAN[['longitude','latitude']]
            arr = zStd.fit_transform(stdTmpDBSCAN)
            tmpDBSCAN[['stdLongitude','stdLatitude']] = arr

            # build 非監督學習:DBSCAN
            dbscan = DBSCAN( eps = radiusDbscan, min_samples = self.minSampleDbscan)
            dbs = dbscan.fit(tmpDBSCAN[['longitude','latitude']])                        
            tmpDBSCAN['dbscan組'] = dbs.labels_
            tmpDBSCAN['縣市據點數'] = self.clusterRadiusDBSCAN.iloc[i,1]

            # accumulate result of DBSCAN
            tmpDBSCAN.sort_values(['county','dbscan組'], ascending=[True, False], inplace=True) 
            if i==0:
                clusterDBSCAN = tmpDBSCAN
                #print(clusterDBSCAN['county'].size)
            else:
                clusterDBSCAN = pd.concat([clusterDBSCAN,tmpDBSCAN],ignore_index=True)
                #print(clusterDBSCAN['county'].size)
        
        # see bankcompetitor group by dbscan
        self.clusterTeamDBSCAN = pd.pivot_table(clusterDBSCAN,index=['county','縣市據點數','dbscan組'],columns=['bankbrifname'],values=['units'],aggfunc=['count'])

        # get dbs據點數
        self.clusterTeamDBSCAN = self.clusterTeamDBSCAN.fillna(value = 0)
        self.clusterTeamDBSCAN.reset_index(inplace = True)
        self.clusterTeamDBSCAN.columns = ['縣市','縣市據點數','dbscan組','一銀','中信','元大','兆豐','台新','合庫','國世','土銀','彰銀','永豐','玉山','臺企','臺銀','華銀','郵局']
        self.clusterTeamDBSCAN['dbs據點數'] = self.clusterTeamDBSCAN.iloc[:,3:].sum(axis=1)
        self.clusterTeamDBSCAN['dbs據點比'] = self.clusterTeamDBSCAN['dbs據點數']/self.clusterTeamDBSCAN['縣市據點數']*100        
        self.clusterTeamDBSCAN['dbs據點比'] = self.clusterTeamDBSCAN['dbs據點比'].round(decimals = 3)

        # save file
        current = os.path.abspath("./")        
        clusterDBSCAN_path      = os.path.join(current,'clusterDBSCAN.csv') 
        clusterTeamDBSCAN_path  = os.path.join(current,'clusterTeamDBSCAN.csv') 
        clusterRadiusDBSCAN_path    = os.path.join(current,'clusterRadiusDBSCAN.csv')  
        clusterDBSCAN.to_csv(clusterDBSCAN_path, encoding='utf_8_sig') 
        self.clusterTeamDBSCAN.to_csv(clusterTeamDBSCAN_path, encoding='utf_8_sig') 
        self.clusterRadiusDBSCAN.to_csv(clusterRadiusDBSCAN_path, encoding='utf_8_sig') 

        return (self.clusterTeamDBSCAN, self.clusterRadiusDBSCAN)
    
    
class atmClusterCntTypeDBSCAN():  
    def __init__(self, clusterTeamDBSCAN):
        self.clusterTeamDBSCAN = clusterTeamDBSCAN

    def atmClusterCntType(self):
        # cut&group by dbs據點數別
        clusterCntTypeDBSCAN = self.clusterTeamDBSCAN[self.clusterTeamDBSCAN['dbscan組']!=-1].groupby(['dbs據點數'], as_index=False).agg(筆數 =('dbs據點數', 'count'), 據點總數 = ('dbs據點數', 'sum'))
        clusterCntTempDBSCAN = self.clusterTeamDBSCAN[self.clusterTeamDBSCAN['dbscan組']==-1].groupby(['dbscan組'], as_index=False).agg(筆數= ('dbs據點數', 'sum'), 據點總數 = ('dbs據點數', 'sum')) 
        clusterCntTempDBSCAN.columns = ['dbs據點數','筆數','據點總數']
        clusterCntTempDBSCAN['dbs據點數'] = clusterCntTempDBSCAN['dbs據點數'].replace(-1, 1)      #or .replace({-1: 1})
        clusterCntTempDBSCAN = pd.concat([clusterCntTempDBSCAN, clusterCntTypeDBSCAN], ignore_index=True)
        cntTypeMax = clusterCntTempDBSCAN['dbs據點數'].max().astype(int)
        if cntTypeMax >200:
            bins = [0,1,5,10,20,50,100,200,cntTypeMax+1]
            label = ['1','2~5','6~10','11~20','21~50','51~100','101~200',f'201~{cntTypeMax}']
        elif cntTypeMax >100:
            bins = [0,1,5,10,20,50,100,cntTypeMax+1]
            label = ['1','2~5','6~10','11~20','21~50','51~100',f'101~{cntTypeMax}']
        elif cntTypeMax >50:
            bins = [0,1,5,10,20,50,cntTypeMax+1]
            label = ['1','2~5','6~10','11~20','21~50',f'51~{cntTypeMax}']
        elif cntTypeMax >20:
            bins = [0,1,5,10,20,cntTypeMax+1]
            label = ['1','2~5','6~10','11~20',f'21~{cntTypeMax}']        
        elif cntTypeMax >10:
            bins = [0,1,5,10,cntTypeMax+1]
            label = ['1','2~5','6~10',f'11~{cntTypeMax}']
        else:
            bins = [0,1,cntTypeMax+1]
            label = ['1',f'2~{cntTypeMax}']

        clusterCntTempDBSCAN['dbs據點數別'] = pd.cut(clusterCntTempDBSCAN['dbs據點數'], bins, labels = label)
        clusterCntTypeDBSCAN = clusterCntTempDBSCAN.groupby(['dbs據點數別'], as_index=False).agg(筆數 =('筆數', 'sum'), 據點總數 = ('據點總數', 'sum')) 
        clusterCntTypeDBSCAN['筆數'] = clusterCntTypeDBSCAN['筆數'].astype(int)
        clusterCntTypeDBSCAN['據點總數'] = clusterCntTypeDBSCAN['據點總數'].astype(int)
        sumCntType = clusterCntTypeDBSCAN['據點總數'].sum()
        clusterCntTypeDBSCAN['percent'] = clusterCntTypeDBSCAN['據點總數']/sumCntType*100
        clusterCntTypeDBSCAN['percent'] = clusterCntTypeDBSCAN['percent'].round(decimals = 1)
        

        return clusterCntTypeDBSCAN
