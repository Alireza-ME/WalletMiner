import mnemonic
import bip32utils
import requests
import logging
import time
import itertools

def generate_mnemonic():
    mnemo = mnemonic.Mnemonic("english")
    return mnemo.generate(strength=128)

def recover_wallet_from_mnemonic(mnemonic_phrase, last_api_used=None, api_usage_count=0, error_counts=None):
    seed = mnemonic.Mnemonic.to_seed(mnemonic_phrase)
    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    child_key = root_key.ChildKey(44 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    address = child_key.Address()
    balance, api_used, api_usage_count, error_counts = check_BTC_balance(address, last_api_used, api_usage_count, error_counts)
    return mnemonic_phrase, balance, address, api_used, api_usage_count, error_counts

def recover_wallet_from_partial_mnemonic(partial_mnemonic):
    partial_mnemonic_words = partial_mnemonic.split()
    if len(partial_mnemonic_words) >= 12:
        logging.error("Provided mnemonic phrase should contain less than 12 words.")
        return None, 0, None, None, 0, {}

    provided_words = len(partial_mnemonic_words)
    missing_words = 12 - provided_words
    logging.info(f"Attempting to recover wallet from {provided_words} words. Missing {missing_words} words.")

    wordlist = mnemonic.Mnemonic("english").wordlist
    last_api_used = None
    api_usage_count = 0
    error_counts = {}

    for guess in itertools.product(wordlist, repeat=missing_words):
        full_mnemonic = ' '.join(partial_mnemonic_words + list(guess))
        mnemonic_phrase, balance, address, last_api_used, api_usage_count, error_counts = recover_wallet_from_mnemonic(full_mnemonic, last_api_used, api_usage_count, error_counts)
        logging.info(f"Trying mnemonic phrase: {full_mnemonic}")
        logging.info(f"Wallet Address: {address}, Balance: {balance} BTC, API Used: {last_api_used}")
        if balance > 0:
            logging.info(f"Found wallet with non-zero balance: {balance} BTC")
            logging.info(f"Mnemonic Phrase: {mnemonic_phrase}")
            with open("wallet.txt", "a") as f:
                f.write(f"Mnemonic Phrase: {mnemonic_phrase}\n")
                f.write(f"Wallet Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n")
                f.write(f"API Used: {last_api_used}\n\n")
            return mnemonic_phrase, balance, address, last_api_used, api_usage_count, error_counts

    logging.info("No wallet found with the provided partial mnemonic phrase.")
    return None, 0, None, None, 0, error_counts

def check_BTC_balance(address, last_api_used=None, api_usage_count=0, error_counts=None, retries=3, delay=5):
    apis = [get_balance_from_blockchain_info, get_balance_from_blockcypher, get_balance_from_blockchair]
    api_names = ["blockchain.info", "blockcypher", "blockchair"]

    if error_counts is None:
        error_counts = {api_name: 0 for api_name in api_names}

    if last_api_used is not None:
        last_api_index = api_names.index(last_api_used)
        if api_usage_count >= 3:
            apis = apis[last_api_index+1:] + apis[:last_api_index+1]
            api_names = api_names[last_api_index+1:] + api_names[:last_api_index+1]

    for attempt in range(retries):
        for api, api_name in zip(apis, api_names):
            if error_counts.get(api_name, 0) >= 2:  # Using get() method to handle KeyError
                continue
            try:
                balance = api(address)
                if api_name == last_api_used:
                    api_usage_count += 1
                else:
                    api_usage_count = 1
                logging.info(f"API Used: {api_name}")
                return balance, api_name, api_usage_count, error_counts
            except Exception as e:
                logging.error(f"Error checking balance with {api_name}: {str(e)}. Trying next API.")
                error_counts[api_name] = error_counts.get(api_name, 0) + 1
                continue
        logging.error(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds.")
        time.sleep(delay)
    return 0, None, api_usage_count, error_counts

def get_balance_from_blockchain_info(address):
    response = requests.get(f"https://blockchain.info/balance?active={address}", timeout=10)
    response.raise_for_status()
    data = response.json()
    balance = data[address]["final_balance"]
    return balance / 100000000

def get_balance_from_blockcypher(address):
    response = requests.get(f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance", timeout=10)
    response.raise_for_status()
    data = response.json()
    balance = data['balance']
    return balance / 100000000

def get_balance_from_blockchair(address):
    response = requests.get(f"https://api.blockchair.com/bitcoin/dashboards/address/{address}", timeout=10)
    response.raise_for_status()
    data = response.json()
    balance = data['data'][address]['address']['balance']
    return balance / 100000000

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    partial_mnemonic = input("Enter the words you remember from your mnemonic phrase, separated by spaces: ")
    recover_wallet_from_partial_mnemonic(partial_mnemonic)
