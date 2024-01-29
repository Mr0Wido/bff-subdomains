import colorama
import subprocess
from tqdm.autonotebook import tqdm
import argparse

class SubdomainBruteforcer:
    def __init__(self, domain_name, bruteforce_tools):
        self.domain_name = domain_name
        self.bruteforce_tools = bruteforce_tools
        self.temp_subdomains = set()
        self.output_file = f'{domain_name}_bfsubs.txt'
        self.domain_file = 'domain.txt'

    def run(self):
        self._save_file()
        self._bruteforce()

    def _save_file(self):
        if not self.domain_name:
            raise ValueError('Domain name is required: -u/--url')

        if not self.bruteforce_tools:
            self.bruteforce_tools = ['bfall', 'bfcommonspeak', 'bfhttparchive', 'bf2m', 'bitquark', 'bbsubs', 'combined', 'fierce', 'n0kovo', 'shubs', 'reconng', 'bf11m']

        with open(self.domain_file, 'w') as f:
            domain = set(self.domain_name.splitlines())
            f.write('\n'.join(domain))

    def _bruteforce(self):
        for tool in self.bruteforce_tools:

            if tool in self.bruteforce_tools and self.domain_name is None:
                raise ValueError('Domain name is required for the selected bruteforce tool: -u/--url')

            try:
                with open(self.domain_file, 'r') as f:
                    subdomains = set(f.read().splitlines())
                    
                for subdomain in tqdm(subdomains, desc=colorama.Fore.BLUE + f"With {tool}.txt: "):
                    command = f'gobuster dns -d {subdomain} -w wordlists/{tool}.txt'
                    command_out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = command_out.communicate()
                    tool_subdomains = set(output.splitlines())

                self.temp_subdomains.update(tool_subdomains)

                with open(f'{tool}.txt', 'w') as f:
                    f.write('\n'.join(tool_subdomains))

            except subprocess.CalledProcessError as e:
                print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
                continue

            print(colorama.Fore.GREEN + f"{tool}: {len(tool_subdomains)} Total subdomains: {len(self.temp_subdomains)} Successfully printed to the '{tool}.txt' file.")

# Input
parser = argparse.ArgumentParser(
    prog='bruteforce.py',
    description=colorama.Fore.CYAN + f'Recon Tool',
    epilog='python3 bfsubs.py -u example.com -bfs fierce ')

parser.add_argument('-u', '--url', help='Domain name to scan', action='store', required=True)
parser.add_argument('-bfs', '--bruteforce_scan', help='Bruteforcing with specific wordlists using Gobuster', nargs='*', choices=['bfall', 'bfcommonspeak', 'bfhttparchive', 'bf2m', 'bitquark', 'bbsubs', 'combined', 'fierce', 'n0kovo', 'shubs', 'reconng', 'bf11m'], default=None)

args = parser.parse_args()

# Starting tool class
bruteforcer = SubdomainBruteforcer(args.url, args.bruteforce_scan)
bruteforcer.run()
