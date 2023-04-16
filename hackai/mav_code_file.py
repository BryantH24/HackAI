# -*- coding: utf-8 -*-
"""
This file contains all the code used to clean the data and build the model.
Note that some paths are hardcoded in or used in google drive
"""


# Get libraries
import os
import sklearn
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import FactorAnalysis
from sklearn.linear_model import Ridge
import scipy 
from scipy.stats import norm
import sys
requisite='boto3'
os.system(f"pip install {requisite}")
os.system("pip install fastparquet")
import boto3
import io
import pyarrow
import datetime
import fastparquet
import pandas as pd
import numpy as np

# Mount drive, requires username and password 
from google.colab import drive
drive.mount('/content/drive')

def get_data():
    
    """
    This function returns three data frames
    Player data
    Twitter data 
    Play by Play data

    Please ensure twitter data is loaded as csv in directory 
    before running
    """
    
    # Set Buffer
    buffer_pbp = io.BytesIO()
    buffer_players = io.BytesIO()

    # Create connection to S3
    s3 = boto3.resource('s3', aws_access_key_id = 'AKIAWNNDBSXELJDB2NPI', aws_secret_access_key = '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')

    # Read PBP Data from S3
    pbp_object = s3.Object('utd-hackathon', 'event_pbp.parquet')
    pbp_object.download_fileobj(buffer_pbp)
    df_pbp = pd.read_parquet(buffer_pbp)

    # Read Players Data from S3
    players_object = s3.Object('utd-hackathon', 'game_players.parquet')
    players_object.download_fileobj(buffer_players)
    df_players = pd.read_parquet(buffer_players)

    # Get twitter data
    df_tweets = pd.read_excel("/content/drive/MyDrive/mavs_twitter_2223.xlsx") # Change this later

    return df_tweets, df_pbp, df_players

# Get data
df_t, df_pbp, df_players = get_data()

# Drop fully null rows and columns
df_t = df_t.dropna(axis=0,thresh=23)
df_t = df_t.dropna(axis=1,thresh=4000)

# Drop irrelevant account data
for i in df_t["AuthorUserName"].unique()[2:]:
  df_t = df_t[~(df_t["AuthorUserName"] == i)]

# Drop irrelevant columns
df_t = df_t.drop(columns = ["AuthorId", "AuthorDisplayName", "PhotoUrl", "Created", 
                     "Source", "ContextUrl", "Links",
                     "Status", "Tags"]) # Maybe drop verification column for twitter

# Get rid of those 355 null values 
df_t = df_t.dropna(axis=0, thresh=23)

# Reset the index
df_t.index = range(df_t.shape[0])                                                          TAGS

# Function to convert ids to timestamps
def get_tweet_timestamp(tid_s):
  dates = []
  for tid in tid_s:
    offset = 1288834974657
    tstamp = (tid >> 22) + offset
    dt = datetime.datetime.utcfromtimestamp(tstamp/1000)
    dates.append(dt)
  return dates

# Function for getting indices of valid strings
def get_good_strings_indices(i):
  indices = []
  for it in i: 
    indices.append(type(it)==int)
  return indices

# Get rid of ugly ids
ids=get_good_strings_indices(df_t["ID"])
df_t = df_t[ids]

# Generate date column
df_t["date"] = get_tweet_timestamp(df_t["ID"].astype(int))
df_t.drop(columns = ["ID"])

# Get target variables
tar_v_list = ["TWReplyCount", "TWEngagement", "TWEngagementAndInteractions", "TWRetweetCount", 
           "EngagementAndInteractionRate", "FollowerInteractionRate", "EngagementRate", 
           "TotalInteractions", "TotalEngagementsAndInteractions", "Comments", "LikeCount",
           "TotalPublicEngagements", "PostImpressions(Organic)", "SocialValue"]

# Get rid of ugly values for target variables
dropped_cols = []
for i in tar_v_list: 
  ids=get_good_strings_indices(df_t[i])
  if sum(ids) < 4000: 
    df_t = df_t.drop(columns = [i])
    dropped_cols.append(i)
    continue
  df_t = df_t[ids]

# Get new target variables
tar_v_list = [item for item in tar_v_list if item not in dropped_cols]

# Get target variable data
tv = df_t[tar_v_list]

# For whatever reason we need to conver them to floats
for i in tv.columns:
  tv.loc[:,i] = tv.loc[:,i].astype(float)

# Heat map of target variables
sns.heatmap(tv.corr())

# Scale data
scaler = StandardScaler()
scaler.fit(tv)
tv_scale = scaler.transform(tv)

# Fit PCA on target variables
pca = PCA(n_components=1)
final_target = pca.fit_transform(tv_scale)
final_target = pd.Series(final_target.reshape((final_target.shape[0],)))

# Add them to data frame, drop original predictors
df_t["y"] = final_target
df_t = df_t.drop(columns = tar_v_list)

# Finally cleaned twitter data
df_t_cleaned = df_t[["y","date"]]

# Get rid of all non-mav data
df_pbp = df_pbp[(df_pbp['team'] == 'DAL') | (df_pbp['opponent']=='DAL')]
df_pbp.index = range(df_pbp.shape[0])

# Variables to drop, continuous predictors and categorical predictors
drop_vars = ['nbaGameId', 'gameId', 'id', 'season', 'seasonType', 'team', 'defTeamId',
             'pbpId', 'option1', 'option2', 'option3', 'option4', 'description', 'wallClockInt',
              'lastName1', 'lastName2', 'lastName3', 'statCategory1', 'statCategory2', 'gameStatus',
             'changeDate', 'pbpOrder', 'msgType', 'date', 'nbaTeamId', 'gameClock', 'statValue1', 
             'statValue2', 'statValue3', 'playerId1', 'playerId2', 'playerId3', 'opponent'
             ]
pred_vars_cont = ['homeScore', 'awayScore', 'locX', 'locY']
pred_vars_cat = ['period', 'pts', 'actionType', "offTeamId"]

# Drop unnecessary variables
df_pbp_dropped = df_pbp.drop(columns = drop_vars)

# Scale continuous predictors
df_pbp_cont = df_pbp_dropped[pred_vars_cont]
scaler = StandardScaler()
scaler.fit(df_pbp_cont)
data_cont = scaler.transform(df_pbp_cont)
data_cont = pd.DataFrame(data_cont, columns = df_pbp_cont.columns)

# Dataframe that is going to hold dummys
data_dums = df_pbp_dropped['wallClock']

# Create dummy variables
for i, value in enumerate(pred_vars_cat):
  dums = pd.get_dummies(df_pbp_dropped[f"{value}"], prefix = value)
  data_dums = pd.concat([data_dums, dums], axis = 1)

# Merge dummy and continous variables
dataX = pd.concat([data_dums, data_cont], axis = 1)
dataX = dataX.drop(columns = ["wallClock"])

# MFA reduction
mfa = FactorAnalysis(n_components=5)
final_pred = mfa.fit_transform(dataX)
final_pred = pd.DataFrame(final_pred)

# Add in dates to final predictors
final_pred["date"] = pd.to_datetime(df_pbp["wallClock"]).dt.tz_localize(None)

# Sort by time
final_pred.sort_values("date", inplace=True)
df_t_cleaned.sort_values("date", inplace=True)
df_t_cleaned = df_t_cleaned.dropna()

# Merge predictors and targets
data_merged = pd.merge_asof(final_pred, df_t_cleaned, on = "date", allow_exact_matches=False,
                            direction="backward", tolerance = pd.Timedelta("5m"))

# Drop the null values in the data set
data_final = data_merged.dropna()

# Sort the final data by date 
data_final = data_final.sort_values('date')

# Get the months of data
data_final['month_year'] = data_final['date'].dt.to_period('M')

# Iterate by date
results = []
intercepts = []
dates = []
for date, data in data_final.groupby(["month_year"]):

  # Reset the model
  rr = Ridge()

  # Grab the data
  X = data.drop(columns = ['y','date', 'month_year'])
  X.columns = X.columns.astype(str)
  y = data['y']

  # Transform y data
  scaled = y.rank()/(len(y)+1) 
  y_t= norm.ppf(scaled, 0, 1)

  # Fit the model 
  rr.fit(X, y_t)

  # grab the coefficients
  intercepts.append(rr.intercept_)
  results.append(rr.coef_)
  dates.append(date)

# Get results into nice data frame
coefs = pd.DataFrame(results, columns = ['factor_1', 'factor_2', 'factor_3', 'factor_4', 'factor_5'])
coefs['intercept'] = intercepts
coefs['date'] = dates

# Distribution
y_t = data_final['y'].rank()/(len(data_final['y'])+1)
y_t = norm.ppf(y_t, 0, 1)
y_t = pd.DataFrame(y_t, columns = ['engagementComposite'])
sns.kdeplot(data = y_t, x='engagementComposite').set(title="Engagement Distribution")

# Grab random compressed factor data
X = data_final.drop(columns = ['y'])
last_date = X[X['month_year']==dates[6]]
last_date = last_date.drop(columns=['month_year'])
data_sample = last_date.sample(n=5)
data_sample.columns = ["Factor1", "Factor2","Factor3","Factor4","Factor5", "Date"]

# Grab random un-compressed factor data and description
drop_vars = ['nbaGameId', 'id', 'season', 'seasonType', 'team', 'defTeamId',
             'pbpId', 'option1', 'option2', 'option3', 'option4', 'wallClockInt',
              'lastName1', 'lastName2', 'lastName3', 'statCategory1', 'statCategory2', 'gameStatus',
             'changeDate', 'pbpOrder', 'msgType', 'date', 'nbaTeamId', 'gameClock', 'statValue1', 
             'statValue2', 'statValue3', 'playerId1', 'playerId2', 'playerId3', 'opponent', 'gameId'
             ]
df_pbp_some_dropped = df_pbp.drop(columns=drop_vars)
X = df_pbp_some_dropped
X["date"] = pd.to_datetime(X["wallClock"]).dt.tz_localize(None)
X = X.drop(columns=["wallClock"])
last_date = X[X['date'].dt.to_period('M')==dates[6]]