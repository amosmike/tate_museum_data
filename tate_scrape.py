from git import Repo
from os import walk
import pandas as pd
import shutil
import json
import os

reset = False
repo = 'clone'

if reset == True:
    shutil.rmtree(repo)

isExist = os.path.exists('clone')

if not isExist:
   os.makedirs(repo)
   git_url = 'https://github.com/tategallery/collection.git/'
   repo_dir = os.getcwd() + '/clone'
   Repo.clone_from(git_url, repo_dir)

def extract_json(path: str):
    json_list = []
    for dirpath, dirname, filename in walk(path):
        for x in filename:
            if x.endswith(".json"):
                json_list.append(os.path.join(dirpath, x))
    return json_list

artists_files = extract_json('clone/artists')
artwork_files = extract_json('clone/artworks')
processed_files = extract_json('clone/processed')

def list_to_df(list):
    dfs = pd.DataFrame()
    for file in list:

        # Load the JSON data from file
        with open(file) as f:
            json_data = json.load(f)

        # Convert the JSON data to a pandas DataFrame
        df = pd.json_normalize(json_data)
        df['json_path'] = file
        df['dict'] = file.split('/')[-4]
        df['dict_sub'] = file.split('/')[-3]
        df['dict_sub_sub'] = file.split('/')[-2]
        df['file_name'] = file.split('/')[-1]

        dfs = pd.concat([dfs, df], ignore_index=True) # concatenate all the data frames in the list.
    return dfs

artists_df = list_to_df(artists_files)
artwork_df = list_to_df(artwork_files)
processed_df = list_to_df(processed_files)

artists_df.to_csv("artists_df.csv")
artwork_df.to_csv("artwork_df.csv")
processed_df.to_csv("processed_df.csv")