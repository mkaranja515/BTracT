import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from glob import glob


def crosses():
  dfiles = glob("./data/crosses/*BananaData.csv")
  data = [pd.read_csv(f) for f in dfiles]
  df = pd.concat(data, ignore_index=True)
  df['First_Pollination_Date'] = pd.to_datetime(df["First_Pollination_Date"], utc=True)
  df["Bunch_Harvest_Date"] = pd.to_datetime(df["Bunch_Harvest_Date"], utc=True)
  df["Seed_Extraction_Date"] = pd.to_datetime(df["Seed_Extraction_Date"], utc=True)
  df["Embryo_Rescue_Date"] = pd.to_datetime(df["Embryo_Rescue_Date"], utc=True)
  df["Germination_Date"] = pd.to_datetime(df["Germination_Date"], utc=True)
  df['First_Pollination_Date'] = pd.to_datetime(df["First_Pollination_Date"]).dt.date
  df["Bunch_Harvest_Date"] = pd.to_datetime(df["Bunch_Harvest_Date"]).dt.date
  df["Seed_Extraction_Date"] = pd.to_datetime(df["Seed_Extraction_Date"]).dt.date
  df["Embryo_Rescue_Date"] = pd.to_datetime(df["Embryo_Rescue_Date"]).dt.date
  df["Germination_Date"] = pd.to_datetime(df["Germination_Date"]).dt.date
  df[['Total_Seeds', 'Good_Seeds','Number_of_Embryo_Rescued','Number_of_Embryo_Germinating','Cycle']] = df[['Total_Seeds', 'Good_Seeds','Number_of_Embryo_Rescued','Number_of_Embryo_Germinating','Cycle']].apply(pd.to_numeric)
  df['Year']  = pd.DatetimeIndex(df['First_Pollination_Date']).year
  df['Month']  = pd.DatetimeIndex(df['First_Pollination_Date']).month
  df['Day']  = pd.DatetimeIndex(df['First_Pollination_Date']).day
  return df

sites = crosses()['Location'].drop_duplicates().tolist()
sites.insert(0,'')

def plantlets():
  dfiles = glob("./data/plantlets/*Plantlets.csv")
  data = [pd.read_csv(f) for f in dfiles]
  df = pd.concat(data, ignore_index=True)
  df.Germination_Date = pd.to_datetime(df.Germination_Date, utc=True)
  df.Germination_Submission_Date = pd.to_datetime(df.Germination_Submission_Date, utc=True)
  df.Subculture_Date = pd.to_datetime(df.Subculture_Date, utc=True)
  df.Date_of_Rooting = pd.to_datetime(df.Date_of_Rooting, utc=True)
  df.Sending_Out_Date = pd.to_datetime(df.Sending_Out_Date, utc=True)
  df.Weaning_2_Date = pd.to_datetime(df.Weaning_2_Date, utc=True)
  df.Screenhouse_Transfer_Date = pd.to_datetime(df.Screenhouse_Transfer_Date, utc=True)
  df.Hardening_Date = pd.to_datetime(df.Hardening_Date, utc=True)
  df.Openfield_Transfer_Date = pd.to_datetime(df.Openfield_Transfer_Date, utc=True)
  df.Germination_Date = pd.to_datetime(df.Germination_Date).dt.date
  df.Germination_Submission_Date = pd.to_datetime(df.Germination_Submission_Date).dt.date
  df.Subculture_Date = pd.to_datetime(df.Subculture_Date).dt.date
  df.Date_of_Rooting = pd.to_datetime(df.Date_of_Rooting).dt.date
  df.Sending_Out_Date = pd.to_datetime(df.Sending_Out_Date).dt.date
  df.Weaning_2_Date = pd.to_datetime(df.Weaning_2_Date).dt.date
  df.Screenhouse_Transfer_Date = pd.to_datetime(df.Screenhouse_Transfer_Date).dt.date
  df.Hardening_Date = pd.to_datetime(df.Hardening_Date).dt.date
  df.Openfield_Transfer_Date = pd.to_datetime(df.Openfield_Transfer_Date).dt.date
  return df

def status():
  dfiles = glob("./data/status/*Status.csv")
  data = [pd.read_csv(f) for f in dfiles]
  df = pd.concat(data, ignore_index=True)
  return df

def contamination():
  dfiles = glob("./data/contamination/*Contamination.csv")
  data = [pd.read_csv(f) for f in dfiles]
  df = pd.concat(data, ignore_index=True)
  return df

def repeatpoll():
  dfiles = glob("./data/repeatpollination/*RepeatPollination.csv")
  data = [pd.read_csv(f) for f in dfiles]
  df = pd.concat(data, ignore_index=True)
  return df

def flowering():
  dfiles = glob("./data/flowering/*AllFlowering.csv")
  data = [pd.read_csv(f) for f in dfiles]
  df = pd.concat(data, ignore_index=True)
  return df


def summary():
  d1 = crosses()[['Location','Crossnumber','Mother','Father','First_Pollination_Date','Total_Seeds','Number_of_Embryo_Rescued','Number_of_Embryo_Germinating']]
  d2 = plantlets()[['Crossnumber','Copies','Number_Rooting','Number_Sent_Out','Weaning_2_Plantlets','Number_in_Screenhouse','Number_in_Hardening','Number_in_Openfield']]
  d = pd.merge(d1, d2, how='left', on='Crossnumber')
  d[['Total_Seeds','Number_of_Embryo_Rescued','Number_of_Embryo_Germinating','Copies','Number_Rooting','Number_Sent_Out','Weaning_2_Plantlets','Number_in_Screenhouse','Number_in_Hardening','Number_in_Openfield']] = d[['Total_Seeds','Number_of_Embryo_Rescued','Number_of_Embryo_Germinating','Copies','Number_Rooting','Number_Sent_Out','Weaning_2_Plantlets','Number_in_Screenhouse','Number_in_Hardening','Number_in_Openfield']].apply(pd.to_numeric)
  d.First_Pollination_Date = pd.to_datetime(d.First_Pollination_Date, utc=True)
  d['First_Pollination_Date'] = pd.to_datetime(d["First_Pollination_Date"]).dt.date
  d['Pollination_Year']  = pd.DatetimeIndex(d['First_Pollination_Date']).year
  d['Pollination_Month']  = pd.DatetimeIndex(d['First_Pollination_Date']).month
  return d


# Labels
#labelType = col1.radio("", ('Crosses', 'Germinating Embryo','Subcultures','Rooting','Weaning1/ Sending Out', 'Weaning2','Screenhouse', 'Hardening','Openfield'))

def label_data(name):
    if name == 'Crosses':
        dt = crosses()
        dt = dt[dt['Number_of_Embryo_Rescued'] > 0]
        dt = dt[['Location','Crossnumber','Embryo_Rescue_Date','Number_of_Embryo_Rescued']]
        dt['id'] = dt.Crossnumber
        dt2 = pd.DataFrame(dt.id.str.split('_',1).tolist(),
                                 columns = ['Prefix','Suffix'])
        df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
        df.pop('id')
    else:
        dt = plantlets()
        if name == 'Germinating Embryo':
            dt = dt[['Location','PlantletID','Germination_Date','Germination_Submission_Date']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')
        elif name == 'Subcultures':
            dt = dt[dt['Copies'] > 0]
            dt = dt[['Location','PlantletID','Subculture_Date','Copies']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')
        elif name == 'Rooting':
            dt = dt[dt['Number_Rooting'] > 0]
            dt = dt[['Location','PlantletID','Date_of_Rooting','Number_Rooting']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')
        elif name == 'Weaning1/ Sending Out':
            dt = dt[dt['Number_Sent_Out'] > 0]
            dt = dt[['Location','PlantletID','Sending_Out_Date','Number_Sent_Out']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')
        elif name == 'Weaning2':
            dt = dt[dt['Weaning_2_Plantlets'] > 0]
            dt = dt[['Location','PlantletID','Weaning_2_Date','Weaning_2_Plantlets']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')
        elif name == 'Screenhouse':
            dt = dt[dt['Number_in_Screenhouse'] > 0]
            dt = dt[['Location','PlantletID','Screenhouse_Transfer_Date','Number_in_Screenhouse']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')
        elif name == 'Hardening':
            dt = dt[dt['Number_in_Hardening'] > 0]
            dt = dt[['Location','PlantletID','Hardening_Date','Number_in_Hardening']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')
        elif name == 'Openfield':
            dt = dt[dt['Number_in_Openfield'] > 0]
            dt = dt[['Location','PlantletID','Openfield_Transfer_Date','Number_in_Openfield']]
            dt['id'] = dt.PlantletID
            dt2 = pd.DataFrame(dt.id.str.split('_',2).tolist(),
                                     columns = ['Prefix','Suffix','EmbryoNo'])
            df = pd.concat([dt.reset_index(drop=True), dt2], axis=1)
            df.pop('id')

    return df
