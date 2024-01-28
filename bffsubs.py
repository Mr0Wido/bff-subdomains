import colorama
import subprocess
from tqdm.autonotebook import tqdm
import argparse
import os

class SubdomainBruteforcer:
    def __init__(self, domain_name, bruteforce_tools, out_of_scope_file):
        self.domain_name = domain_name
        self.bruteforce_tools = bruteforce_tools
        self.out_of_scope_file = out_of_scope_file
        self.temp_subdomains = set()
        self.output_file = f'{domain_name}_bfsubs.txt'
        self.remain_temp_file = 'remaine.txt'
        self.domain_file = 'domain.txt'

    def run(self):
        self._save_file()
        self._bruteforce()
        self._remove_out_of_scope_domains()

    def _save_file(self):
        if not self.domain_name:
            raise ValueError('Domain name is required: -u/--url')

        if not self.bruteforce_tools:
            self.bruteforce_tools = ['bfall', 'bfcommonspeak', 'bfhttparchive', 'bf2m', 'bitquark', 'bbsubs', 'combined', 'fierce', 'n0kovo', 'shubs', 'reconng', 'bf11m']

        if not self.out_of_scope_file:
            raise ValueError('Out-of-scope file path is required: -os/--out_of_scope')

        with open(self.domain_file, 'w') as f:
            domain = set(self.domain_name.splitlines())
            f.write('\n'.join(domain))

    def _bruteforce(self):
        for tool in tqdm(self.bruteforce_tools, desc=colorama.Fore.BLUE + "Bruteforce ile Subdomain Aranıyor", total=len(self.bruteforce_tools)):
            if tool not in self.bruteforce_tools and 'all' not in self.bruteforce_tools:
                continue

            if tool in self.bruteforce_tools and self.domain_name is None:
                raise ValueError('Domain name is required for the selected bruteforce tool: -u/--url')

            if tool in self.bruteforce_tools and self.out_of_scope_file is None:
                raise ValueError('Out-of-scope file path is required for the selected bruteforce tool: -os/--out_of_scope')

            try:
                output = subprocess.check_output(['gobuster', 'dns', '-d', self.domain_name, '-w', f'wordlists/bruteforce-subdomains/{tool}.txt']).decode()
                tool_subdomains = set(output.splitlines())
                self.temp_subdomains.update(tool_subdomains)
                print(colorama.Fore.GREEN + f"{tool}: {len(tool_subdomains)} Total subdomains: {len(self.temp_subdomains)}")

                with open(f'{tool}.txt', 'w') as f:
                    f.write('\n'.join(tool_subdomains))

            except subprocess.CalledProcessError as e:
                print(colorama.Fore.RED + f"{tool} returned non-zero exit status {e.returncode}. Error message: {e.output.decode()}")
                continue

        if 'all' in self.bruteforce_tools:
            total_subdomains = sum(len(tool_subdomains) for tool_subdomains in self.temp_subdomains.values())
            print(colorama.Fore.GREEN + f"Total subdomains found: {total_subdomains}")
        else:
            print(colorama.Fore.GREEN + f"Total subdomains found: {len(self.temp_subdomains)}")

    def _remove_out_of_scope_domains(self):
        all_subdomains = set()

        for tool in self.bruteforce_tools:
            tool_file_path = f'{tool}.txt'
            try:
                with open(tool_file_path, 'r') as f:
                    tool_subdomains = set(f.read().splitlines())

                all_subdomains.update(tool_subdomains)
                os.remove(tool_file_path)

            except FileNotFoundError:
                continue

        try:
            with open(self.remain_temp_file, 'w'):
                pass

            with open(self.out_of_scope_file, 'r') as f:
                out_of_scope_domains = set(f.read().splitlines())

            remaining_subdomains = all_subdomains - out_of_scope_domains
            with open(self.remain_temp_file, 'w') as f:
                f.write('\n'.join(remaining_subdomains))

            command = f"sed -e '/^$/d' -e '/^\[-\]/d' -e '/^[[:space:]].*$/d' {self.remain_temp_file}"
            sed_out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = sed_out.communicate()

            clear_subs = set(output.splitlines())
            remaining_subdomains.clear()
            remaining_subdomains.update(clear_subs)

            all_subdomains.clear()
            all_subdomains.update(remaining_subdomains)

            os.remove(self.remain_temp_file)

        except Exception as e:
            print(colorama.Fore.RED + f"Something went wrong: {e}")

        print(colorama.Fore.GREEN + f"Out-of-scope domains have been successfully removed.")

        with open(self.output_file, 'a') as f:
            f.write('\n' + '\n'.join(all_subdomains))

        print(colorama.Fore.GREEN + f"Total {len(all_subdomains)} subdomains found. Successfully written to the '{self.output_file}' file.")

# Input
parser = argparse.ArgumentParser(
    prog='bruteforce.py',
    description=colorama.Fore.CYAN + f'Recon Tool',
    epilog='Text at the bottom of help')

parser.add_argument('-u', '--url', help='Domain name to scan', action='store', required=True)
parser.add_argument('-bfs', '--bruteforce_scan', help='Bruteforcing with specific wordlists using Gobuster', nargs='*', choices=['bfall', 'bfcommonspeak', 'bfhttparchive', 'bf2m', 'bitquark', 'bbsubs', 'combined', 'fierce', 'n0kovo', 'shubs', 'reconng', 'bf11m'], default=None)
parser.add_argument('-os', '--out_of_scope', help='Out-of-scope domains file path', default=None, required=True)

args = parser.parse_args()

# Tool sınıfını başlatma ve çalıştırma
bruteforcer = SubdomainBruteforcer(args.url, args.bruteforce_scan, args.out_of_scope)
bruteforcer.run()
