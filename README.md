# Bitcoin Wallet Address Brute Force
This is an effective script to Brute Force the Private Key of any Bitcoin Public Address.

## How does brute force script work
This Script creates randomly private and public addresses without checking the balance. Instead of making API Request, the created Public Address is compared against provided<sup id="a1">[1](#f1)</sup> list of Bitcoin addresses. You may use your own list or get it from elsewhere like <sup id="a2">[2](#f2)</sup> or <sup id="a3">[3](#f3)</sup>.

The script generates **compressed** and **uncompressed** public keys out of private key and then compares both against the list. Thus, doubles the chances of success.

The script avoids extra calculations which makes it extremely fast.  
On i5-10210U CPU it checks over 2400 keys per second. Multiplying it by the number of provided addresses, I've got the speed around **70 million checks per second**.

## How to run it
`python brute.py`  
or
execute `run.bat`

## Requirements
 - Python 3.x
 - pip install ecdsa
 - pip install base58
 - 150,000,000,000,000,000,000,000,000,000,000 Years

If you like it or you are so lucky to brute force some bitcoins, let me know by sending some BTC to **1K52E2fgg6sqJHiAk1WDySRpDE5UPVko2K**

Good luck! :)
___ 

<b id="f1">1</b> File `addresses.txt` contains **123,000 Bitcoin Addresses** with 1+ BTC from 2009 to 2013 and NEVER made a transaction, therefore, lost BTC... it is just like huge pirate boats in the bottom of the ocean filled with treasures. [↩](#a1)  
<b id="f2">2</b> http://addresses.loyce.club/ [↩](#a2)  
<b id="f3">3</b> https://balances.crypto-nerdz.org/ [↩](#a3)