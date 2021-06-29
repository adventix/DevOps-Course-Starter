import requests, os
from todo_app.trello_config import Config

def build_auth_query():
    return {'key' : Config.TRELLO_API_KEY, 'token' : Config.TRELLO_API_TOKEN}

BASE_URL= "https://api.trello.com/1/"
BOARD_NAME= "Aaronboard"

def get_trello_board_id():
    boards = requests.get(f"{BASE_URL}members/me/boards", params=build_auth_query())
    boards_json = boards.json()
    boardexists = 0
    for list in boards_json:
        if list['name'] == BOARD_NAME:
            boardexists = 1
            boardid = list['id']
    
    if boardexists == 0:  
        boardid = build_trello_board()
        return boardid
    else:
        return boardid 



def build_trello_board():
    query = build_auth_query()
    query['name'] = BOARD_NAME
    response = requests.post(f"{BASE_URL}boards/", params=query)
    response_json = response.json()
    return response_json["id"]

def get_trello_todo_listid():
    lists = requests.get(f"{BASE_URL}boards/{get_trello_board_id()}/lists", params=build_auth_query())
    lists_json = lists.json()
    for list in lists_json:
        if list['name'] == "To Do":
            return list['id']
#print(get_trello_todo_listid())

def get_trello_doing_listid():
    lists = requests.get(f"{BASE_URL}boards/{get_trello_board_id()}/lists", params=build_auth_query())
    lists_json = lists.json()
    for list in lists_json:
        if list['name'] == "Doing":
            return list['id']
#print(get_trello_doing_listid())

def get_trello_done_listid():
    lists = requests.get(f"{BASE_URL}boards/{get_trello_board_id()}/lists", params=build_auth_query())
    lists_json = lists.json()
    for list in lists_json:
        if list['name'] == "Done":
            return list['id']
#print(get_trello_done_listid())

class Item:
    def __init__(self, id, title, status='To Do'):
        self.id = id
        self.status = status
        self.title = title
        #self.lastmodifieddate = lastmodifieddate


def get_trello_cards():
    cards = requests.get(f"{BASE_URL}boards/{get_trello_board_id()}/cards/", params=build_auth_query())
    cards_json = cards.json()
    items = []
    for card in cards_json:
        if card['idList'] == get_trello_todo_listid():
            cardstatus = "To Do"
        elif card ['idList'] == get_trello_doing_listid():
            cardstatus = "Doing"
        elif card ['idList'] == get_trello_done_listid():
            cardstatus = "Done"
        else: 
            raise AttributeError
        items.append(Item(card['id'], card['name'], cardstatus))
    return items
#print(get_trello_cards())

def add_item_trello(title):
    query = build_auth_query()
    query['idList'] = get_trello_todo_listid()
    query['name'] = title
    requests.post(f"{BASE_URL}cards/", params=query)
    return 

#def create_trello_todo_cards():
def start_item_trello(id):
    query = build_auth_query() 
    query['idList'] = get_trello_doing_listid()
    requests.put(f"{BASE_URL}cards/{id}" , params=query)


def complete_item_trello(id):
    query = build_auth_query() 
    query['idList'] = get_trello_done_listid()
    requests.put(f"{BASE_URL}cards/{id}" , params=query)

def uncomplete_item_trello(id):
    query = build_auth_query() 
    query['idList'] = get_trello_todo_listid()
    requests.put(f"{BASE_URL}cards/{id}" , params=query)

