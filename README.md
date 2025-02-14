# Blockpad Automate
Blockpad Testnet automate perform task script.
- Another script, [Blockpad Autoref](https://github.com/im-hanzou/blockpad-autoref)
## Tools and components required
1. Blockpad Account, Register here: [https://testnet.blockpad.fun/register](https://testnet.blockpad.fun/register?ref=V779JC)
2. Blockpad Account Bearer Token
3. VPS or RDP (OPTIONAL)
## How to get Bearer Token
1. Open your browser console, here's the tutorial [YouTube](https://www.youtube.com/watch?v=Vmi-mVcn1uQ&ab_channel=SpeedyTutorials)
2. Paste this script to browser console:
  ```bash
  try {
  const token = localStorage.getItem('token');
  if (token) {
    console.log('Token found:', token);
  } else {
    console.log('No token found in localStorage, Please login blockpad first: https://testnet.blockpad.fun/register?ref=TZSXOS');
  }
} catch (error) {
  console.error('Error accessing localStorage:', error);
}
  ```
3. The token must be like: `eyJhbGciXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
## Installation
- Install Python For Windows: [Python](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)
- For Unix:
```bash
apt install python3 python3-pip git -y
```
- For Termux:
```bash
pkg install python python-pip git -y
```
- Download script [Manually](https://github.com/im-hanzou/blockpad-automate/archive/refs/heads/main.zip) or use git:
```bash
git clone https://github.com/im-hanzou/blockpad-automate
```
### Requirements installation
- Make sure you already in bot folder:
```bash
cd blockpad-automate
```
#### Windows and Termux:
```bash
pip install -r requirements.txt
```
#### Unix:
```bash
pip3 install -r requirements.txt
```
## Run the Bot
- Windows and Termux:
```bash
python main.py
```
- Unix:
```bash
python3 main.py
```
- Then insert your Bearer Token
# Notes
- Run this bot, use my referral code if you don't have one.
- You can just run this bot at your own risk, I'm not responsible for any loss or damage caused by this bot.
- This bot is for educational purposes only.
