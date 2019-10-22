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
        'limit': 1000,
        'sort_by': "modified",
        "sort_order": "descending",
    }

    req = urllib.request.Request(
        url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as response:
        body = json.load(response)

    return body['doc_ids']

def get_doc_title_and_id(doc_id):
    path = '/2/paper/docs/download'
    url = endpoint + path

    headers = {
        'Authorization': 'Bearer ' + token,
        'Dropbox-API-Arg': '{"doc_id":"%s","export_format":{".tag":"markdown"}}' % doc_id,
    }

    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as response:
        body = response.read().decode('utf-8')

    doc_title_and_id = {'title': body.splitlines()[0].lstrip('# '), 'doc_id': doc_id}

    return doc_title_and_id

def alfred_items(docs_list):
    item_list = []
    items = {'items': item_list}

    for d in docs_list:
        doc_title = get_doc_title_and_id(d)
        doc_url = 'https://paper.dropbox.com/doc/%s' % d
        item = {'title': doc_title, 'arg': doc_url}
        item_list.append(item)

    return items

def main():
    docs = get_docs_list()
    items = alfred_items(docs)

    print(json.dumps(items))

main()
