import json

def get_pwd():
    try:
        f = open('../credentials/key_store.json')
        data = json.load(f)
        postgre_pwd = data["postgre_pwd"]
        return postgre_pwd
    except:
        print('Impossible d\'ouvrir le fichier de credential')


