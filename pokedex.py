import requests, six
import lxml.html as lh
from itertools import cycle, islice
from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline

url='http://pokemondb.net/pokedex/all'

page = requests.get(url)

#print(page)

doc = lh.fromstring(page.content)

#print(doc)

# parse data stored in table rows
tr_elements = doc.xpath('//tr')

#print(tr_elements)

#debug - should all be 10
#[len(T) for T in tr_elements[:12]]

col = []
i = 0

for t in tr_elements[0]:
    i+=1
    name = t.text_content()
    #print '%d:"%s"'%(i,name)
    print(str(i)+": "+str(name))
    col.append((name,[]))

# first row is header, data is second-onward
for j in range(1,len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]

    # ensure data is from correct table
    if len(T)!=10:
        break

    i=0

    for t in T.iterchildren():
        data=t.text_content()
        if i>0:
            try:
                data=int(data)
            except:
                pass
        col[i][1].append(data)
        i+=1

#[len(C) for (title,C) in col]

Dict={title:column for (title,column) in col}
import pandas as pd
df=pd.DataFrame(Dict)

#print(df.head(160))

def str_bracket(word):
    # Add brackets around second term
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper(): # check if letter is uppercase
            list[char_ind] = ' ' + list[char_ind] # if so, insert whitespace before it
    
    # if whitespace exists, add to list
    fin_list = ''.join(list).split(' ')
    length = len(fin_list)
    if length>1: # surround in parenths
        fin_list.insert(1,'(')
        fin_list.append(')')
    return ' '.join(fin_list)

def str_break(word):
    # Break strings at upper case
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = ' ' + list[char_ind]
    fin_list = ''.join(list).split(' ')
    return fin_list

# debug
#word = 'ILoveStuff'
#print(str_bracket(word))
#print(str_break(word))

df['Name']=df['Name'].apply(str_bracket)
df['Type']=df['Type'].apply(str_break)
#print(df.head())

df.to_json('PokemonData.json')

# debug
df = pd.read_json('PokemonData.json')
df = df.set_index(['#'])
#print(df.head())

#####
# STATISTICS TIME #
#####

def max_stats(df, col_list):
    # Get highest value of the column in the Data Frame
    message = ''
    for col in col_list:
        stat = df[col].max()
        name = df[df[col]==df[col].max()]['Name'].values[0]
        message += name + ' has the greatest ' + col + ' of ' + str(stat) + '.\n'
    return message

def min_stats(df, col_list):
    # Get lowest value of the column in the Data Frame
    message = ''
    for col in col_list:
        stat = df[col].min()
        name = df[df[col]==df[col].min()]['Name'].values[0]
        message += name + ' has the worst ' + col + ' of ' + str(stat) + '.\n'
    return message

stats=['Attack', 'Defense', 'HP', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']
print(max_stats(df, stats))
print(min_stats(df, stats))

from pandas.plotting import scatter_matrix
print(scatter_matrix(df[stats], alpha=0.2, figsize=(10, 10), diagonal='kde'))
