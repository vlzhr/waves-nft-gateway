from requests import get
from json import loads, dumps
from glob import glob
import os


ADDRESS_DATA_URL = "https://wavesducks.wavesnodes.com/addresses/data/{}"
ADDRESS_TXS_URL = "https://nodes.wavesnodes.com/transactions/address/{}/limit/1000"
ASSET_DATA_URL = "https://wavesducks.wavesnodes.com/assets/details/{}"
NFT_CREATION_ADDRESS = "3P8LVqVKhTViMJau96KNir6FhHr4WnfoW57"
GATEWAY_ADDRESS = "3PPfDHC6hNqDMxRArJvJRkYfC8y6S3rSnYb"

creation_protocol_data = loads(get(ADDRESS_DATA_URL.format(NFT_CREATION_ADDRESS)).text)


def link(*args):
    return os.path.join(os.path.dirname(__file__), *args)


def get_by_key(s):
    return [n for n in creation_protocol_data if n["key"] == s][0]["value"]


def get_nft_data(nftid="HznabdeXiRWS9v7PdwrF6DgA3GS7Tm6pUS3EyXMmKZqT"):
    asset_data = loads(get(ASSET_DATA_URL.format(nftid)).text)
    collection = loads(get_by_key("nft_{}_data".format(nftid)).replace("'", "\""))["collection"]
    n = str(loads(get_by_key("nft_{}_data".format(nftid)).replace("'", "\""))["num"])
    url = get_by_key("nft_{}_image".format(nftid))

    desc_text = "NFT ported from Waves Protocol using bridge (puzzlemarket.org). Collection {col} #{n}".format(
        desc=asset_data["description"] + ". " if len(asset_data["description"]) > 0 else "",
        col=collection,
        n=n
    )
    return {
        "name": asset_data["name"],
        "url": url,
        "desc": desc_text,
        "col": "Waves NFT",
        "link": "https://wavesexplorer.com/asset/" + nftid
    }


def get_todo():
    txs = loads(get(ADDRESS_TXS_URL.format(GATEWAY_ADDRESS)).text)[0]
    todo = []
    for tx in txs:
        if tx["type"] == 16 and tx["call"]["function"] == "sendToGateway":
            swap_id = tx["id"]
            if len(glob(link("completed_swaps", swap_id+".json"))) == 0:  # TODO: track complete status more secure to avoid double spend
                nft_id = tx["payment"][0]["assetId"]
                todo.append({
                    "tokenData": get_nft_data(nft_id),
                    "recipient": tx["call"]["args"][0]["value"]
                })
    return todo


if __name__ == "__main__":
    print(get_todo())
