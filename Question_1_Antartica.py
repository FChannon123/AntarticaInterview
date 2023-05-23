#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 16:10:26 2023

@author: chess
"""
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import pandas as pd

# ----- GUI Definition ----- #
layout = [[sg.Text('GitHub Username:'), sg.Input(key='-USERNAME-')],
          [sg.Text("Save to File Location:"), sg.Input(key="-OUT-"), sg.FileBrowse(file_types=(("Excel files", "*.xls*"),))],
          [sg.Exit(), sg.Button("Save Repos to Excel")]]

window = sg.Window('GitHub Repo Scraper', layout)

def get_repo_names(username):
    url = f"https://github.com/{username}?tab=repositories"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    repo_list = soup.find_all('h3', {'class': 'wb-break-all'})
    return [repo.text.strip() for repo in repo_list]

# ----- Main Event Loop ----- #
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    if event == 'Save Repos to Excel':
        username = values['-USERNAME-']
        repos = get_repo_names(username)
        if repos:  # Only save to Excel if there are repositories
            df = pd.DataFrame(repos, columns=["Repository"])
            df.to_excel(values['-OUT-'], index=False)
            sg.Popup('File saved successfully!')
        else:
            sg.Popup('No repositories found for this user')


window.close()
