# Wallet Recovery and Random Wallet Checker
This tool is designed to recover Bitcoin wallets from randomly generated mnemonic phrases or partially remembered mnemonic phrases. It leverages multiple blockchain APIs to check the balance of recovered wallets.

---

### Files:

- **check_random_wallets.py**: Generates random mnemonic phrases and attempts to recover wallets associated with them. If a wallet with a non-zero balance is found, it logs the details into `wallet.txt`.
  
- **recover_wallet.py**: Allows recovery of wallets from partially remembered mnemonic phrases. It iterates through possible combinations of missing words to recover the complete mnemonic phrase, then attempts to recover the wallet similarly to `check_random_wallets.py`.

---

### Dependencies:

- **mnemonic**: Python library for generating and handling mnemonic phrases.
- **bip32utils**: Library for BIP32 hierarchical deterministic keys.
- **requests**: For making HTTP requests to blockchain APIs.
- **logging**: Used for logging events and errors.
- **time**: Used for adding delays between retries.

---

### How to Run:

#### Prerequisites:

1. **Python Installation**: Ensure Python 3.x is installed on your system.
   
2. **Install Dependencies**: Use pip to install required libraries:
   ```
   pip install mnemonic bip32utils requests
   ```

#### Running `check_random_wallets.py`:

1. **Navigate to Directory**: Open a terminal or command prompt and navigate to the directory containing `check_random_wallets.py`.

2. **Run the Script**:
   ```
   python check_random_wallets.py
   ```

3. **Follow Instructions**: The script will start generating random mnemonic phrases and attempting to recover wallets. If a wallet with a non-zero balance is found, details will be logged into `wallet.txt`.

#### Running `recover_wallet.py`:

1. **Navigate to Directory**: Open a terminal or command prompt and navigate to the directory containing `recover_wallet.py`.

2. **Run the Script**:
   ```
   python recover_wallet.py
   ```

3. **Enter Partial Mnemonic**: When prompted, enter the words you remember from your mnemonic phrase, separated by spaces.

4. **Follow Instructions**: The script will attempt to reconstruct the full mnemonic phrase and recover the associated wallet. If successful, details will be logged into `wallet.txt`.

---

### Detailed Functionality:

#### `generate_mnemonic()` (in both scripts)

- Generates a random mnemonic phrase with a specified strength of 128 bits using the English wordlist.

#### `recover_wallet_from_mnemonic(mnemonic_phrase, last_api_used=None, api_usage_count=0, error_counts=None)` (in both scripts)

- Converts the mnemonic phrase into a seed, derives a BIP32 root key, and checks the balance of the associated Bitcoin wallet using multiple blockchain APIs (`blockchain.info`, `blockcypher`, `blockchair`).

#### `recover_wallet_from_partial_mnemonic(partial_mnemonic)` (only in `recover_wallet.py`)

- Prompts the user to enter partially remembered words from a mnemonic phrase.
- Tries to reconstruct the full mnemonic phrase by iterating through possible combinations of missing words.
- Recovers the associated Bitcoin wallet similarly to `recover_wallet_from_mnemonic()`.

#### `check_BTC_balance(address, last_api_used=None, api_usage_count=0, error_counts=None, retries=3, delay=5)` (in both scripts)

- Tries multiple APIs (`blockchain.info`, `blockcypher`, `blockchair`) to check the wallet balance.
- Handles errors, retries failed attempts, and rotates through APIs to avoid rate limits and errors.

#### `get_balance_from_blockchain_info(address)`, `get_balance_from_blockcypher(address)`, `get_balance_from_blockchair(address)` (in both scripts)

- Functions that make HTTP requests to blockchain APIs to retrieve the balance of a Bitcoin wallet given its address.

---

### Logging:

- **Level:** INFO
- **Format:** `%(asctime)s - %(levelname)s - %(message)s`
- Logs include details such as mnemonic phrases generated, wallet addresses checked, API usage, and errors encountered during balance checks.

---

### Support

If you find this project helpful and would like to support its development, consider the following options:

- **Star the Repository**: Give a star on GitHub to show your appreciation.

- **Contribute**: If you have any improvements or bug fixes, feel free to submit a pull request.

- **Donate**: If you wish to support financially, you can make a donation to the Bitcoin address below:

  **Bitcoin Address**: bc1qgh7en65e239yrutp83hrlg2c3c26w22xjlytce

Your support helps in maintaining and improving this tool for the community. Thank you for your contribution!

---

### Notes:

- This tool is intended for educational purposes to demonstrate the process of recovering Bitcoin wallets from mnemonic phrases.
- Use caution when running this tool, as it interacts with real blockchain data and could potentially consume API limits.
- Ensure compliance with local laws and regulations regarding cryptocurrency usage and recovery.

---

### Contact:

For questions or suggestions, please contact [https://t.me/A_LIREZA_ME].

---

### License:

This tool is provided under the MIT License. Feel free to modify and distribute it as needed.
