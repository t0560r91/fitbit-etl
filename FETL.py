#! /Users/Sehokim/anaconda3/bin/python3.6
import base64
import json
import yaml
import os
import sys
import requests
import time
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import psycopg2 as pg





with open('var/creds/app-creds.json', 'r') as f:
    app_creds = json.load(f)

client_id = app_creds['client_id']
client_secret = app_creds['client_secret']
encoded_client_cred = base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf'))




with open('var/creds/rds-creds.json', 'r') as f:
    rds_creds = json.load(f)

host = rds_creds['host']
port = rds_creds['port']
database = rds_creds['database']
rds_user_id = rds_creds['user_id']
password = rds_creds['password']








def datespace(start, end, step=1):
    """
    INPUT:
        start: date string in '%Y-%m-%d'
        end: date string in '%Y-%m-%d'

    OUTPUT:
        list of datetime.date objects ranging from the given start and end date
    """
    if start <= end:
        a = datetime.strptime(start, '%Y-%m-%d')
        z = datetime.strptime(end, '%Y-%m-%d')
        result = []
        result.append(a.date())
        while z > a:
            a += timedelta(days=step)
            if a <= z:
                result.append(a.date())
        return result
    else: 
        raise ValueError('Start Date cannot be before End Date.')











def request_sleep_data(token: dict, start_date: str, end_date: str) -> pd.DataFrame:
    """
    "Request call to Fitbit API for Time-Series Sleep data, following OAuth 2.0 Authorization Code Flow Protocol. "

    INPUT:
        token: Token data in JSON format, a response from the token request with URL encoded code after
                user login. 
        start_date: date string of which the query begins. 
        end_date: date string of which the query ends. 
    OUTPUT:
        new_df: a DataFrame of concatenated time-series sleep data within the date range specified.  
    """
    uuid = token['user_id']
    access_token = token['access_token']
    token_type = token['token_type']

    headers = {
        'content-type' : 'application/json', 
        'authorization' : token_type + " " + access_token
        }
    
    s = datetime.strptime(start_date, '%Y-%m-%d')
    e = datetime.strptime(end_date, '%Y-%m-%d')

    if (e-s).days >= 100:
        new_df = pd.DataFrame()
        date_interval = datespace(start_date, end_date, step=100)
        for i_date in date_interval:
            j_date = i_date + timedelta(days=99)
            endpoint = f'https://api.fitbit.com/1.2/user/{uuid}/sleep/date/{i_date}/{j_date}.json'
            res = requests.get(endpoint, headers = headers)
            new_data = json.loads(res.text)
            if 'sleep' in new_data.keys(): 
                new_df = pd.concat([new_df, pd.DataFrame(new_data['sleep'])])
            else: 
                raise ValueError(new_data['errors'][0]['message'])

        new_df.sort_values('startTime', inplace=True)
        new_df.reset_index(inplace=True, drop=True)
        

    else: 
        endpoint = f'https://api.fitbit.com/1.2/user/{uuid}/sleep/date/{start_date}/{end_date}.json'
        res = requests.get(endpoint, headers = headers)
        new_data = json.loads(res.text)
        
        if 'sleep' in new_data.keys(): 
            new_df = pd.DataFrame(new_data['sleep'])
        else: 
            raise ValueError(new_data['errors'][0]['message'])
      

    return new_df








def parse_datetime(time_str, out_format='datetime'):
    """Reads time_str in any format and writes a datetime, date, or time obejct.
    
    INPUT:
        time_str: time string in any format
        out_format: datetime, date, or time
    
    OUTPUT:
        parsed time_string
    """
    in_formats = ['%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f', 
                  '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', 
                  '%Y-%m-%dT%I:%M%p', '%Y-%m-%d %I:%M%p',
                  '%Y-%m-%d']
    for f in in_formats:
        try:
            if out_format == 'datetime':
                return datetime.strptime(time_str, f)
            elif out_format == 'date':
                return datetime.strptime(time_str, f).date()
            elif out_format == 'time':
                return datetime.strptime(time_str, f).time()
        except:
            raise ValueError







def parse_stage(x, stage='deep'):
    """Parse a Fitbit-generated nested dictionary of sleep stage data 
    and returns a specified stage data.
    
    INPUT:
        x: a nested dictionary
        stage: sleep stage

    OUTPUT:
        minutes or counts of each specified sleep stage
    """
    try:
        if stage in ['deep','rem','light']:
            return x['summary'][stage]['minutes']
        elif stage == 'wake':
            return x['summary'][stage]['count']
    except:
        return np.nan 







def parse_sleep_data(sleep_df: pd.DataFrame) -> pd.DataFrame:
    
    new_df = pd.DataFrame()
    new_df['start'] = sleep_df['startTime'].apply(parse_datetime)
    new_df['end'] = sleep_df['endTime'].apply(parse_datetime)     
    new_df['light'] = sleep_df['levels'].apply(parse_stage, stage='light')
    new_df['rem'] = sleep_df['levels'].apply(parse_stage, stage='rem')
    new_df['deep'] = sleep_df['levels'].apply(parse_stage, stage='deep')
    new_df['awakening'] = sleep_df['levels'].apply(parse_stage, stage='wake')

    new_df.sort_values('start', inplace=True)
    new_df.reset_index(inplace=True, drop=True)
    return new_df






        










if __name__ == "__main__":


    # Date Range Input
    start_date = input('> start date (yyyy-mm-dd):  ')
    end_date = input('> end date (yyyy-mm-dd):  ')        










    # Extract
    # Loop Over User Tokens
    token_names = os.listdir('var/tokens/')
    for i, tn in enumerate(token_names):
        
        with open(f'var/tokens/{tn}', 'r') as f: 
            token = json.load(f)
        uuid = token['user_id']

        with open('var/users.yaml', 'r') as f:
            users = yaml.load(f)
        user_id = f'user{i+1}'
        name = users[user_id]['name']
        bod = users[user_id]['bod']
        gender = users[user_id]['gender']
        country = users[user_id]['country']

        print(f'# Iteration: {user_id} ({(i+1)}/{len(token_names)})')

        try: 
            # request data with old token
            print('> extracting sleep data...')
            sleep = request_sleep_data(token, start_date, end_date)

        except:
            print('> token expired, refreshing token...')
            # refresh token
            url = "https://api.fitbit.com/oauth2/token"
            headers = {
                'content-type' : 'application/x-www-form-urlencoded', 
                'authorization' : 'Basic ' + encoded_client_cred.decode('utf')
                }
            refresh_token = token['refresh_token']
            data = f'client_id={client_id}&grant_type=refresh_token&refresh_token={refresh_token}'
            new_token = json.loads(requests.post(url, headers=headers, data=data).text)
            # save new token to a file
            with open(f'var/tokens/token_{user_id}.json', 'w+') as f:
                json.dump(new_token, f)

            
            # request data with new token
            print('> retrying extracting sleep data with new token...')
            sleep = request_sleep_data(new_token, start_date, end_date)










 
        # Transform Sleep Data...
        print('> transforming sleep data...')
        if sleep.shape[0] > 0: sleep = parse_sleep_data(sleep)
        else: sleep = pd.DataFrame()
        








        
        # Load
        ## Connect to RDS
        print('> connecting RDS...')
        conn = pg.connect(
            host=host,
            port=port,
            database=database,
            user=rds_user_id,
            password=password
        )
        




        # Create Users Table If Not Exist...
        print('> creating a user table...')
        try:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE users (
                            "userID" SERIAL PRIMARY KEY,
                            "name" varchar,
                            "bod" date,
                            "gender" varchar,
                            "uuid" char(6)
                            );''')

        except:
            conn.rollback()
            print('> user table already exits')


        print('> inserting user data...')
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO users VALUES 
                    ({i+1}, '{name}', '{bod}', '{gender}', '{uuid}')
                    ON CONFLICT DO NOTHING;''')

        conn.commit()

        
    

                
        # Create Sleep Table If Not Exist...
        try: 
            print('> creating a sleep table...')
            cur = conn.cursor()
            cur.execute('''CREATE TABLE sleep (
                            "start" timestamp PRIMARY KEY,
                            "end" timestamp,
                            light int2,
                            rem int2,
                            deep int2,
                            awakening int2,
                            userID int2 REFERENCES users("userID")
                            );''' 
                        )
        
        except: 
            print('> sleep table already exists')
            conn.rollback()


        # Insert Sleep Data
        print('> inserting sleep data...')
        cur = conn.cursor()
        sleep_null = sleep.fillna('null')
        for ind in range(sleep.shape[0]):
            start = str(sleep_null.loc[ind, 'start'])
            end = str(sleep_null.loc[ind, 'end'])
            light = sleep_null.loc[ind, 'light']
            rem = sleep_null.loc[ind, 'rem']
            deep = sleep_null.loc[ind, 'deep']
            awakening = sleep_null.loc[ind, 'awakening']
            cur.execute(
                f'''INSERT INTO sleep (start, "end", light, rem, deep, awakening, userID) 
                        VALUES ('{start}','{end}',{light},{rem},{deep},{awakening},'{i+1}')
                            ON CONFLICT (start) DO NOTHING;''')
        cur.close()
        conn.commit() #indiv commit
        











        # Disconnect RDS
        print('> disconnecting RDS...')
        conn.close()