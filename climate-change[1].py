# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import warnings
import math
import seaborn as sb

sb.color_palette("Paired")

def read_data(file_path,file_name):
    """ 
    Reading World Development Indicators Data File
    
    """
    path=os.path.join(file_path,file_name)
    data1=pd.read_csv(path)
    data2=data1.transpose()
    
    return data1,data2;       


def clean_data(data_last_10_years):
    data_last_10_years=data_last_10_years.dropna();
    data_last_10_years.replace('..',math.nan, inplace=True)
    cols = data_last_10_years.columns
    return data_last_10_years;

def summary_stats(data_last_10_years):
    
    years=['2012 [YR2012]', '2013 [YR2013]', '2014 [YR2014]',
    '2015 [YR2015]', '2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]',
    '2019 [YR2019]', '2020 [YR2020]','2021 [YR2021]']
    data_last_10_years.dtypes
    for col in years:
        data_last_10_years[col] = data_last_10_years[col].astype(float)
        
    data_last_10_years=data_last_10_years.T.fillna(data_last_10_years.mean(axis=1)).T
    
    data_last_10_years["mean"]=data_last_10_years[years].mean(axis=1)
    
    ''''Access to electricity'''
    access_to_elc=data_last_10_years.loc[data_last_10_years["Series Code"]=="EG.ELC.ACCS.ZS"]
    access_to_elc.reset_index(drop=True, inplace=True)

    access_to_elc.set_index("Country Code",inplace=True)

    
    '''C02 Emissions'''
    co2_emissions=data_last_10_years.loc[data_last_10_years["Series Code"]=="EN.ATM.CO2E.KT"]
    
    co2_emissions.set_index("Country Code",inplace=True)

    ''' Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)'''
    povert_count=data_last_10_years.loc[data_last_10_years["Series Code"]=="SI.POV.DDAY"]
    povert_count.set_index("Country Code",inplace=True)

    ''' Electric power consumption (kWh per capita)'''
    
    elec_usage=data_last_10_years.loc[data_last_10_years["Series Code"]=="EG.USE.ELEC.KH.PC"]
    elec_usage.set_index("Country Code",inplace=True)

    """Energy use (kg of oil equivalent per capita) """
    energy_usage=data_last_10_years.loc[data_last_10_years["Series Code"]=="EG.USE.PCAP.KG.OE"]
    energy_usage.set_index("Country Code",inplace=True)

    """Ease of doing business rank (1=most business-friendly regulations) """
    ease_business=data_last_10_years.loc[data_last_10_years["Series Code"]=="IC.BUS.EASE.XQ"]
    ease_business.set_index("Country Code",inplace=True)


    ''' Urban population (% of total population)'''
    urban=data_last_10_years.loc[data_last_10_years["Series Code"]=="SP.URB.TOTL.IN.ZS"]
    urban.set_index("Country Code",inplace=True)


    wdi_ind=pd.DataFrame()
    wdi_ind['country']=access_to_elc.index
    wdi_ind.set_index("country",inplace=True)
    wdi_ind['country_name']=access_to_elc["Country Name"]
    wdi_ind["access_to_electricity"]=access_to_elc["mean"]
    wdi_ind["co2_emission"]=co2_emissions["mean"]
    wdi_ind["poverty_indicator"]=povert_count["mean"]
    wdi_ind["urbanization_ind"]=urban["mean"]
    wdi_ind["energy_usage"]=energy_usage["mean"]
    wdi_ind["ease_of_business_ind"]=ease_business["mean"]

    
    countries=["USA","GBR","RUS","CHN","IND","BRA"]
    
    data_ind=wdi_ind[wdi_ind.index.isin(countries)]
    
    print("Summary of indicators for countries neighbourhood to  :")
    print(data_ind.to_string())
    
    first_regions=["USA","GBR"]
    second_regions=["RUS","CHN"]
    third_regions=["IND","BRA"]
    data_ind=wdi_ind[wdi_ind.index.isin(first_regions)]
    
    print("Summary of indicators for first world countries  :")
    print(data_ind.to_string())

    data_ind=wdi_ind[wdi_ind.index.isin(second_regions)]
    
    print("Summary of indicators for first world countries  :")
    print(data_ind.to_string())
    
    data_ind=wdi_ind[wdi_ind.index.isin(third_regions)]
    
    print("Summary of indicators for first world countries  :")
    print(data_ind.to_string())

    return wdi_ind


def check_corelation(development_ind):
    corr = development_ind.corr()
    print(corr.to_string())
    sb.heatmap(corr, cmap="Blues", annot=True)

def visualize(data_last_10_years):
    
    regions=["USA","GBR","RUS","CHN","IND","BRA"]
    series_codes=["SP.URB.TOTL.IN.ZS","SI.POV.DDAY","IC.BUS.EASE.XQ","EG.ELC.ACCS.ZS","EG.USE.PCAP.KG.OE","EN.ATM.CO2E.KT"]
    data_regions=data_last_10_years[data_last_10_years['Country Code'].isin(regions)]       
    
    ''''Access to electricity'''
    access_to_elc=data_regions.loc[data_regions["Series Code"]=="EG.ELC.ACCS.ZS"]
    access_to_elc.set_index('Country Code',inplace=True)

    access_to_elc=access_to_elc.iloc[:,3:].T
    plt.figure(figsize = (15,8))
        

    chart=sb.lineplot(data=access_to_elc,linewidth=5)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.title("Access to electricity (% of population)")

    None

    '''C02 Emissions'''
    co2_emissions=data_regions.loc[data_regions["Series Code"]=="EN.ATM.CO2E.KT"]
    
    co2_emissions.set_index("Country Code",inplace=True)
    
    co2_emissions=co2_emissions.iloc[:,3:].T
    plt.figure(figsize = (15,8))
        

    chart=sb.lineplot(data=co2_emissions,linewidth=5)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.title("ATotal CO2 emissions (thousand metric tons of CO2 excluding Land-Use Change and Forestry)")

    None

    ''' Urban population (% of total population)'''
    
    urban=data_regions.loc[data_regions["Series Code"]=="SP.URB.TOTL.IN.ZS"]
    urban.set_index("Country Code",inplace=True)
    urban=urban.iloc[:,3:].T

    plt.figure(figsize = (15,8))
        

    chart=sb.lineplot(data=urban,linewidth=5)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.title("Urban population (% of total population)")

    None

    ''' Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)'''
    
    poverty=data_regions.loc[data_regions["Series Code"]=="SI.POV.DDAY"]
    poverty.set_index("Country Code",inplace=True)
    poverty=poverty.iloc[:,3:].T

    plt.figure(figsize = (15,8))
        

    chart=sb.lineplot(data=poverty,linewidth=5)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.title("Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)")

    None
    
    """Energy use (kg of oil equivalent per capita) """
    energy_usage=data_regions.loc[data_regions["Series Code"]=="EG.USE.PCAP.KG.OE"]
    energy_usage.set_index("Country Code",inplace=True)
    energy_usage=energy_usage.iloc[:,3:].T

    plt.figure(figsize = (15,8))
        

    chart=sb.lineplot(data=energy_usage,linewidth=5)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.title("Energy use (kg of oil equivalent per capita)")

    None

    """Ease of doing business rank (1=most business-friendly regulations) """
    ease_business=data_regions.loc[data_regions["Series Code"]=="IC.BUS.EASE.XQ"]
    ease_business.set_index("Country Code",inplace=True)
    ease_business=energy_usage.iloc[:,3:].T

    plt.figure(figsize = (15,8))
        

    chart=sb.lineplot(data=energy_usage,linewidth=5)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.title("Ease of doing business rank (1=most business-friendly regulations)")

    None
    

def main():
    #Reading Data
    file_path="./data"
    file_name="wdi.csv"
    print(read_data.__doc__)
    data1,data2=read_data(file_path,file_name);
    data_last_10_years=data1[["Series Code","Country Code","Country Name",'2012 [YR2012]', '2013 [YR2013]', '2014 [YR2014]',
    '2015 [YR2015]', '2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]',
    '2019 [YR2019]', '2020 [YR2020]','2021 [YR2021]']]
    data_last_10_years=clean_data(data_last_10_years)
    
    wdi_ind=summary_stats(data_last_10_years)
    check_corelation(wdi_ind)
    visualize(data_last_10_years)
    




if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()


    
