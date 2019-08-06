import numpy as np
import pandas as pd
import re
import os
import json

def removeSpaces(word):
    word = re.sub(r' +$','',word)
    word = re.sub(r'^ +','',word)
    word = re.sub(r' +','_',word)
    return word

raw_data = pd.ExcelFile(r'../../data/raw/Registro Fluidez 7 prueba mac.xlsx')
sheets = raw_data.sheet_names
for sheet in sheets:
    pd.read_excel(raw_data, sheet).to_csv(
        r'../../data/interim/interim_fluency_'+sheet+'.csv', 
        encoding='utf-8',
        index=False,
        header=False
    )

semantic_fluency = {sheet:{} for sheet in sheets if not sheet.endswith('_color')}
for csv in os.listdir(r'../../data/interim/'):
    if not csv.endswith('_color.csv'):
        with open(r'../../data/interim/'+csv, encoding='utf-8') as file:
            with open(r'../../data/interim/'+csv.replace('.csv','_color.csv'), encoding='utf-8') as color:
                color_lines = color.readlines()
                for line_number,line in enumerate(file):
                    line = line.rstrip().split(',')
                    if line[0] != '':
                        test = csv.replace('interim_fluency_','').replace('.csv','')
                        subject = int(float(line[0])) if '.' in line[0] else int(line[0])
                        words = line[1:]
                        words = [removeSpaces(word) for word in words if len(word)>0]
                        correct = color_lines[line_number].rstrip().split(',')[1:][:len(words)]
                        correct = [False if color == "6" else True for color in correct]
                        semantic_fluency[test][subject] = {}
                        # print(test)
                        # print(subject)
                        # print(len(words))
                        # print(len(correct))
                        # print('#####')
                        assert(len(words) == len(correct))
                        semantic_fluency[test][subject]['words'] = words
                        semantic_fluency[test][subject]['correct'] = correct
with open(r'../../data/processed/semantic_fluency.json', 'w', encoding='utf-8') as json_file:
    json.dump(semantic_fluency, json_file, indent=4, ensure_ascii=False)