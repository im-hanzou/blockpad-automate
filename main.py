import requests
import time
import random
import json
from datetime import datetime, timedelta, timezone
from colorama import init, Fore, Style
import sys

init(autoreset=True)

class BlockpadAutomation:
    def __init__(self, bearer_token):
        self.base_url = "https://api3.blockpad.fun/api"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json',
            'Origin': 'https://testnet.blockpad.fun',
            'Referer': 'https://testnet.blockpad.fun/'
        }
        self.min_tice_balance = 10
        
    def log(self, message, color=Fore.WHITE):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}{message}{Style.RESET_ALL}")

    def log_with_time(self, message, color=Fore.WHITE):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.CYAN}[{timestamp}] {color}{message}{Style.RESET_ALL}")

    def get_user_info(self):
        response = requests.get(f"{self.base_url}/auth/me", headers=self.headers)
        if response.status_code == 200:
            return response.json()['user']
        else:
            self.log_with_time(f"Error getting user info: {response.text}", Fore.RED)
            return None

    def display_user_stats(self):
        user = self.get_user_info()
        if user:
            self.log(f"\n{Fore.BLUE}[ User Statistics ]{Style.RESET_ALL}")
            self.log(f"{Fore.MAGENTA}Username     : {Fore.YELLOW}{user['username']}")
            self.log(f"{Fore.MAGENTA}tICE Balance : {Fore.GREEN}{user['tICEBalance']}")
            self.log(f"{Fore.MAGENTA}BPAD Balance : {Fore.GREEN}{user['BPADBalance']}")
            self.log(f"{Fore.MAGENTA}USDT Balance : {Fore.GREEN}{user['USDTBalance']}")
            self.log(f"{Fore.MAGENTA}XP Balance   : {Fore.GREEN}{user['xpBalance']}")

    def claim_faucet(self):
        self.log_with_time("Attempting to claim faucet...", Fore.YELLOW)
        response = requests.post(f"{self.base_url}/faucet/claim", headers=self.headers)
        data = response.json()
        
        if 'error' in data:
            self.log_with_time(f"Faucet claim failed: {data['error']}", Fore.RED)
            return False
        else:
            self.log_with_time("Faucet claimed successfully!", Fore.GREEN)
            return True

    def execute_swap(self, from_token, to_token, amount):
        self.log_with_time(f"Executing swap: {amount} {from_token} → {to_token}", Fore.YELLOW)
        payload = {
            "fromToken": from_token,
            "toToken": to_token,
            "amount": amount
        }
        response = requests.post(f"{self.base_url}/swap/execute", headers=self.headers, json=payload)
        if response.status_code == 200:
            self.log_with_time(f"Swap successful: {from_token} to {to_token}", Fore.GREEN)
            return True
        else:
            self.log_with_time(f"Swap failed: {response.text}", Fore.RED)
            return False

    def check_and_swap_to_tice(self):
        user = self.get_user_info()
        if float(user['tICEBalance']) < self.min_tice_balance:
            self.log_with_time("tICE balance is low. Converting other tokens to tICE...", Fore.YELLOW)
            
            bpad_balance = float(user['BPADBalance'])
            if bpad_balance > 0:
                self.log_with_time(f"Converting {bpad_balance} BPAD to tICE", Fore.YELLOW)
                self.execute_swap("BPAD", "tICE", bpad_balance)
            
            usdt_balance = float(user['USDTBalance'])
            if usdt_balance > 0:
                self.log_with_time(f"Converting {usdt_balance} USDT to tICE", Fore.YELLOW)
                self.execute_swap("USDT", "tICE", usdt_balance)
            
            return True
        return False

    def get_swap_amount(self, token, balance):
        if token in ["tICE", "BPAD"]:
            min_amount = 0.00001
            max_amount = min(10, float(balance))
            if max_amount <= min_amount:
                return 0
            return round(random.uniform(min_amount, max_amount), 6)
        else:  
            min_amount = 0.00001
            max_amount = min(100, float(balance))
            if max_amount <= min_amount:
                return 0
            return round(random.uniform(min_amount, max_amount), 6)

    def perform_task_swaps(self):
        self.log(f"\n{Fore.MAGENTA}[ Performing Swap Task ]{Style.RESET_ALL}")
        
        if self.check_and_swap_to_tice():
            self.log_with_time("Completed emergency tICE conversion", Fore.GREEN)
            return
            
        user = self.get_user_info()
        
        swap_pairs = [
            ("tICE", "BPAD"),
            ("tICE", "USDT"),
            ("BPAD", "tICE"),
            ("BPAD", "USDT"),
            ("USDT", "tICE"),
            ("USDT", "BPAD")
        ]
        
        for from_token, to_token in swap_pairs:
            balance_key = f"{from_token}Balance"
            balance = float(user[balance_key])
            
            if balance > 0:
                amount = self.get_swap_amount(from_token, balance)
                if amount > 0:
                    self.execute_swap(from_token, to_token, amount)
                    user = self.get_user_info()
                else:
                    self.log_with_time(f"Insufficient {from_token} balance for swap", Fore.YELLOW)

    def perform_liquidity_task(self):
        self.log(f"\n{Fore.MAGENTA}[ Performing Liquidity Task ]{Style.RESET_ALL}")
        
        self.check_and_swap_to_tice()
        
        user = self.get_user_info()
        if float(user['tICEBalance']) < 10 or float(user['BPADBalance']) < 1:
            self.log_with_time("Need to swap for required tokens first", Fore.YELLOW)
            if float(user['tICEBalance']) < 10:
                self.execute_swap("BPAD", "tICE", 1)
            if float(user['BPADBalance']) < 1:
                self.execute_swap("tICE", "BPAD", 10)
            user = self.get_user_info()
        
        if float(user['tICEBalance']) >= 10:
            self.log_with_time("Adding liquidity...", Fore.YELLOW)
            response = requests.post(f"{self.base_url}/liquidity/add", 
                                   headers=self.headers, 
                                   json={"tICEAmount": 10})
            if response.status_code == 200:
                self.log_with_time("Liquidity added successfully!", Fore.GREEN)
                
                self.log_with_time("Removing liquidity...", Fore.YELLOW)
                remove_response = requests.post(f"{self.base_url}/liquidity/remove", 
                                             headers=self.headers, 
                                             json={"tICEAmount": 10})
                if remove_response.status_code == 200:
                    self.log_with_time("Liquidity removed successfully!", Fore.GREEN)
                    return True
        else:
            self.log_with_time("Insufficient balance for liquidity task", Fore.YELLOW)
        return False

    def perform_staking_task(self):
        self.log(f"\n{Fore.MAGENTA}[ Performing Staking Task ]{Style.RESET_ALL}")
        
        self.check_and_swap_to_tice()
        
        user = self.get_user_info()
        if float(user['tICEBalance']) < 1:
            self.log_with_time("Need to swap for tICE first", Fore.YELLOW)
            self.execute_swap("BPAD", "tICE", 1)
            user = self.get_user_info()
        
        if float(user['tICEBalance']) >= 1:
            self.log_with_time("Staking 1 tICE...", Fore.YELLOW)
            response = requests.post(f"{self.base_url}/staking/stake", 
                                   headers=self.headers, 
                                   json={"token": "tICE", "amount": 1})
            if response.status_code == 200:
                self.log_with_time("Staking successful!", Fore.GREEN)
                
                self.log_with_time("Unstaking 1 tICE...", Fore.YELLOW)
                unstake_response = requests.post(f"{self.base_url}/staking/unstake", 
                                              headers=self.headers, 
                                              json={"token": "tICE", "amount": 1})
                if unstake_response.status_code == 200:
                    self.log_with_time("Unstaking successful!", Fore.GREEN)
                    return True
        else:
            self.log_with_time("Insufficient balance for staking task", Fore.YELLOW)
        return False

    def perform_random_task(self):
        tasks = [
            self.perform_task_swaps,
            self.perform_liquidity_task,
            self.perform_staking_task
        ]
        task = random.choice(tasks)
        task()
        self.display_user_stats()

def main():
    banner = """
╔══════════════════════════════════════════════╗
║           Blockpad Task Automate             ║
║     Github: https://github.com/im-hanzou     ║
╚══════════════════════════════════════════════╝
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)
    
    print(f"{Fore.CYAN}Register first: {Fore.GREEN}https://testnet.blockpad.fun/register?ref=V779JC\n{Style.RESET_ALL}")
    bearer_token = input(f"{Fore.YELLOW}Now enter your Bearer token: {Style.RESET_ALL}")
    
    bot = BlockpadAutomation(bearer_token)
    bot.display_user_stats()

    while True:
        try:
            user = bot.get_user_info()
            if user:
                last_claim = user.get('lastFaucetClaim')
                
                if last_claim is None:
                    bot.log_with_time("No previous faucet claim found. Attempting to claim...", Fore.YELLOW)
                    retry_count = 0
                    while retry_count < 5:
                        if bot.claim_faucet():
                            break
                        retry_count += 1
                        if retry_count < 5:
                            bot.log_with_time(f"Retrying faucet claim in 1 minute... (Attempt {retry_count}/6)", Fore.YELLOW)
                            time.sleep(60)
                else:
                    last_claim_date = datetime.strptime(last_claim, "%Y-%m-%dT%H:%M:%S.%fZ")
                    last_claim_date = last_claim_date.replace(tzinfo=timezone.utc)
                    
                    next_claim = last_claim_date + timedelta(hours=24)
                    now = datetime.now(timezone.utc)

                    if now >= next_claim:
                        retry_count = 0
                        while retry_count < 5:
                            if bot.claim_faucet():
                                break
                            retry_count += 1
                            if retry_count < 5:
                                bot.log_with_time(f"Retrying faucet claim in 1 minute... (Attempt {retry_count}/6)", Fore.YELLOW)
                                time.sleep(60)

                bot.display_user_stats()

            bot.perform_random_task()

        except KeyboardInterrupt:
            bot.log_with_time("\nStopping the bot...", Fore.RED)
            sys.exit(0)
        except Exception as e:
            bot.log_with_time(f"Error occurred: {str(e)}", Fore.RED)

if __name__ == "__main__":
    main()
