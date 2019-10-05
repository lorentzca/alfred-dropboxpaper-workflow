import urllib.request
import os
import json

endpoint = 'https://api.dropboxapi.com'
token = os.environ['DROPBOX_ACCESS_TOKEN']

def get_docs_list():
    path = '/2/paper/docs/list'
    url = endpoint + path
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = {
        'limit': 1000
    }

    req = urllib.request.Request(
        url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as response:
        body = json.load(response)

    return body

def get_title_list(docs_list):
    path = '/2/paper/docs/download'
    url = endpoint + path

    title_list = []
    for doc_id in docs_list['doc_ids']:
        headers = {
            'Authorization': 'Bearer ' + token,
            'Dropbox-API-Arg': '{"doc_id":"%s","export_format":{".tag":"markdown"}}' % doc_id,
        }

        req = urllib.request.Request(url, headers = headers)
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')

        title = {'title': body.splitlines()[0].lstrip('# '), 'doc_id': doc_id}
        title_list.append(title)

    return title_list

def alfred_items(title_list):
    item_list = []
    items = {'items': item_list}

    for tl in title_list:
        doc_url = 'https://paper.dropbox.com/doc/%s' % tl['doc_id']
        item = {'title': tl['title'], 'arg': doc_url}
        item_list.append(item)

    return items

def main():
    d = get_docs_list()
    t = get_title_list(d)
    a = alfred_items(t)

    print(json.dumps(a))

main()
