from http.server import HTTPServer, BaseHTTPRequestHandler
import json

data = {'result': 'true'}
data1 = {'result': 'false'}
import time


def add(par):
    # Adding Simon data
    symbool = par.split("&")[0].split("=")[1]
    Quantity = par.split("&")[1].split("=")[1]
    Price = par.split("&")[2].split("=")[1]
    print(Quantity + "changed")
    with open('./py/portfolio.json', encoding='utf8') as f:
        js = json.load(f)
    for index, item in enumerate(js):
        if item["Stock"] == symbool:
            del js[index]
    if Quantity != "0":
        newjson = {'Stock': symbool, "Quantity": Quantity, "Price": Price}
        js.append(newjson)
    with open("./py/portfolio.json", "w") as json_file:
        json_dict = json.dump(js, json_file)
    # Return of successful data
    body = json.dumps(data).encode()
    return body;
