from waves_handler import get_todo
from eth_handler import mint_nft
from time import sleep


def run_throttle():
    # get list of gateway requests
    todo = get_todo()
    for mint_data in todo:
        print("minting ", mint_data)
        mint_nft(mint_data)
    print("sleeping 15 sec")
    sleep(15)


if __name__ == "__main__":
    run_throttle()
