# Blockchain.info / Blockchain.com ca. 2011-2014 era Legacy Wallet Recovery Script

A secure, offline Python script to extract ca. 2011-2014 era Bitcoin private keys from modern Blockchain.com `wallet.aes.json` wrappers.

**This script may help you, if your wallet's balance on Blockchain.com is unexpectedly missing funds, old addresses, or you are unable to send funds using their web interface.**

## 🚨 IMPORTANT 🚨

**⚠️ Running the script and following any single one of these steps happens at your own risk! ⚠️**

Please make sure you understand what you or the script are about to do, before actually doing it. The script may contain errors or security flaws the author is not aware of. Any personal message, help from the Internet, or anywhere should be treated with the utmost caution, as people might try to gain access to your wallet and its funds. The author of this script, and potentially any contributors, is not affiliated with Blockchain.com in any way.

Before trying this script, also consider contacting Blockchain.com's official support first: https://support.blockchain.com/hc/en-us/requests/new

## 🤔 When should you use this?

If you have an old Blockchain.info or Blockchain.com account from approximately 2011-2014, and you assume there may be funds hidden inside it, but after logging in their web interface or app shows a zero balance, or any existing funds can't be sent successfully to another address.

There are currently at least 3 cases in which you should try to gain access:
1. You are absolutely **100% certain**, that there should be funds in that wallet, but none are being shown.
2. You log in using the Blockchain.com Android app and **funds are being displayed, but are not spendable**. _Note: You **have to** use the Android app, not the web interface or the iOS app._
3. You navigate to `Settings` -> `Tax Center` and generate a `Tax Report`. After waiting a few moments, reload the page and download the report. Check the addresses in the report using a block explorer (e.g. https://blockchair.com/) and see if any of them actually contain funds, which are not shown otherwise.

## 💡 How it works
The non-custodial wallet of Blockchain.info, and later Blockchain.com, works in a way that the private keys or seeds for a wallet are stored in an encrypted form on their servers. When you login to your account, you are receiving this encrypted version of your wallet. By using your wallet's password, your computer's browser (or the Blockchain app on mobile devices) is now decrypting these information _locally_ and uses them to perform any actions. This means that Blockchain.com doesn't have direct access to your keys or seeds*.

This also means that you are always receiving a copy of your wallet any time you log in. And since this copy usually contains any and all of the seeds or straight-out private keys you have ever used on that account, we can now attempt to extract them locally, even if their web interface isn't showing them anymore or funds can't be sent. And this is exactly what this script is trying to do.

*_This is, of course, only true as long as their systems aren't compromised and their web interface or app runs malformed code on your browser or device._

## 📋 What you need
You only need your `Wallet ID` and your `Password`. You **DO NOT NEED** an old backup of your `wallet.aes.json` - but if you do have one, check if https://github.com/3rdIteration/btcrecover may help you, as well.

You need to use the developer tools of your browser to capture the wallet data, while you're logging into your Blockchain.com account. There's a really great how-to to be found on https://btcrecover.readthedocs.io/en/latest/TUTORIAL/#downloading-blockchaincom-wallet-files
Store the contents of the `payload` field into a plaintext file called `wallet.aes.json`. You don't need to worry about unescaping the contained JSON values in any way. If you have that file ready, you are ready to run the script.

## ⚙️ Setup
1. Make sure you have a working version of **Python 3.6** _or newer_ and **pip** at your disposal.
2. Install the required cryptographic dependency:
   ```bash
   pip install pycryptodome
   ```
3. Obtain the `blockchain_legacy_recovery_tool.py` from this repository.

## 🚀 Usage
1. Make sure you have obtained the `wallet.aes.json`, as described under **What you need**.
2. Place the `blockchain_legacy_recovery_tool.py` and `wallet.aes.json` into the same folder, or make sure to remember the wallet-file's path.
3. Run this script locally on your - preferrably offline or even airgapped - machine:
   ```bash
   python3 blockchain_legacy_recovery_tool.py
   ```
4. Enter your wallet password when prompted. The tool will parse the container, unlock the parameters, and automatically convert any raw Base58 key primitives into standard WIF keys that can be cleanly imported into wallets like Electrum.
5. If the script is able to process the wallet, it will now output any legacy private keys it can find in it. **Important: Remember that having these private keys enables you or anyone else to have absolute and full control over the associated address and any funds it may contain. Do not share, screenshot, post, or store them in any unsafe manner!**
6. Import the private key(s) into a newly created wallet you trust. You can e.g. use Electrum - but please see what wallet is currently considered safe, and fits your needs best. **Important: Imported private keys and their addresses are _not_ covered by the recovery seed phrase of a modern deterministic wallet! You should consider "sweeping" your recovered funds from their old address and transfer them over into a native receiving address the new wallet provides!**

## 🙂 What's left to say?
I hope this script helps people recovering their presumed lost funds. It handles a very niche issue for which the Blockchain.com support didn't have a solution for in over half a year of presumably aimless debugging. I was finally able to recover funds using this method. Feel free to improve upon the script or adjust it. It may very well fail for you out-of-the-box, if your issue isn't related to the one I was having. Feel free to reach out to me, but my options are limited, as it is very hard to debug these kind of things without having the wallet and its password. **And those two things are something you should not send anyone**.

🏆 Been successful? ❤️ Let me know, I'd love to hear success stories!!! 💰 Recovered a fortune and feeling super extra thankful? Feel free, but not obligated, to drop my family something: `bc1q98axfwxztegy886d3w6ckmeksyvyvj7d5m36pq`
