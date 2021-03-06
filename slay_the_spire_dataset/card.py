# -*- coding: utf-8 -*-
"""card_processing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WqoBiAoQHoztyKUXqm8gRoEqCszqSx_Y
"""


import pandas as pd
import json

raw = pd.read_excel('Slay_the_Spire_Reference.xlsx', sheet_name='Cards', engine='openpyxl')
with open('cards.json') as json_file:
    cards = json.load(json_file)


Card_class = ['Ironclad Cards', 'Silent Cards', 'Defect Cards', 'Watcher Cards', 'Colorless Cards', 'Curse Cards', 'Status Cards']

def spilt_card_class(df):
  #declaration
  cut_index = []
  dfs = {}

  #find cut index
  for str in Card_class:
    cut_index.append(df.index[df['Name'] == str].tolist())

  cut_index.append([len(df)])

  #cut
  for i in range(len(Card_class)):
    dfs[Card_class[i]] = df[df.keys()[0:6]].iloc[cut_index[i][0] + 1:cut_index[i + 1][0],:]


  return dfs

df = spilt_card_class(raw)


target = ['choosed', 'all', 'random', 'random all', 'other']
def Info(class_id, card_id):
    return {
        'name': df[Card_class[class_id]]['Name'].iloc[card_id],
        'type': df[Card_class[class_id]]['Type'].iloc[card_id],
        'rarity': df[Card_class[class_id]]['Rarity'].iloc[card_id],
        'cost': df[Card_class[class_id]]['Cost'].iloc[card_id]
    }

def Damage():
    if input('deal damage?') == '0': return {}

    monster = {}
    if input('deal damage to monster?') == '1':
        print(*list(enumerate(target)), sep='\n')
        monster['target'] = target[int(input('target id:'))]
        monster['time'] = input('time:')
        monster['amount'] = input('amount')
        monster['condition'] = input('have condition?')

    player = {}
    if input('deal damage to player?') == '1':
        print(*list(enumerate(target)), sep='\n')
        player['target'] = target[int(input('target id:'))]
        player['time'] = input('time:')
        player['amount'] = input('amount')
        player['condition'] = input('have condition?')

    return {
        'monster': monster,
        'player': player
    }

def Buff():
    if input('have buff?') == '0': return {}

    monster = []
    for i in range(int(input('monster buff num?'))):
        monster.append({
            'name': input('name:'),
            'amount': input('amount:'),
            'condition': input('have condition?')
        })

    player = []
    for i in range(int(input('player buff num?'))):
        player.append({
            'name': input('name:'),
            'amount': input('amount:'),
            'condition': input('have condition?')
        })

    return {
        'monster': monster,
        'player': player
    }

card_pile = ['draw pile', 'discard pile', 'exhaust pile', 'hand', 'other']
place = ['top', 'bottom', 'random']

def Card():
    if input('have add or upgrade or play cards?') == '0': return {}
    card = {}
    for i in range(4):
        pile = {}
        if input('to', card_pile[i], '?') == '1':
            print(*list(enumerate(card_pile)), sep='\n')
            pile['from'] = target[int(input('from pile id:'))]
            print(*list(enumerate(target)), sep='\n')
            pile['target'] = target[int(input('target id:'))]
            pile['place'] = 'other'
            pile['amount'] = input('amount:')
        card[card_pile[i]] = pile

    play = {}
    if input('play card?') == '1':
        print(*list(enumerate(card_pile)), sep='\n')
        play['from'] = target[int(input('from pile id:'))]
        print(*list(enumerate(target)), sep='\n')
        play['target'] = target[int(input('target id:'))]
        play['place'] = 'other'
        play['amount'] = input('amount:')

    card['play'] = play

    upgrade = {}
    if input('upgrade card?') == '1':
        print(*list(enumerate(card_pile)), sep='\n')
        upgrade['from'] = target[int(input('from pile id:'))]
        print(*list(enumerate(target)), sep='\n')
        upgrade['target'] = target[int(input('target id:'))]
        upgrade['amount'] = input('amount:')

    card['upgrade'] = upgrade
    return card

def create_card():
    print(*list(enumerate(Card_class)), sep='\n')
    class_id = int(input('class id:'))
    print(*list(enumerate(df[Card_class[class_id]]['Name'])), sep='\n')
    card_id = int(input('card id:'))

    print(df[Card_class[class_id]].iloc[card_id])

    # card_temp = {
    #     'info': Info(class_id, card_id),
    #     'damage': Damage(),
    #     'block': input('block:'),
    #     'energy': input('energy'),
    #     'buff': Buff(),
    #     'card': Card()
    # }
    card_temp = {
        'name': df[Card_class[class_id]]['Name'].iloc[card_id],
        'type': df[Card_class[class_id]]['Type'].iloc[card_id],
        'rarity': df[Card_class[class_id]]['Rarity'].iloc[card_id],
        'cost': df[Card_class[class_id]]['Cost'].iloc[card_id],
        'damage': Damage(),
        'block': input('block:'),
        'energy': input('energy'),
        'buff': Buff(),
        'card': Card()
    }

    if input('commit') == '1':
        cards[df[Card_class[class_id]]['Name'].iloc[card_id]] = card_temp

def delete_card(card_name):
    try:
        print(json.dumps(cards[card_name], indent=4, sort_keys=False))
        if input('delete?') == '1':
            cards.pop(card_name)
    except KeyError:
        print('invalid key!')


def view_card(card_name):
    try:
        print(json.dumps(cards[card_name], indent=4, sort_keys=False))
    except KeyError:
        print('invalid key!')

commands = ['create', 'delete', 'view', 'save']
print(cards)
while True:
    print(*list(enumerate(commands)), sep='\n')
    command = input()
    if command == '0':
        create_card()
    elif command == '1':
        delete_card(input('name:'))
    elif command == '2':
        view_card(input('name:'))
    elif command == '3':
        with open('cards.json', 'w') as outfile:
            json.dump(cards, outfile)
        break
