# A Subdomain Bruteforcer Tool
This Python script is a subdomain bruteforcer tool. It uses various wordlists and the Gobuster tool to perform DNS enumeration and find subdomains of a given domain. The script also allows for the removal of out-of-scope domains from the results.

### Output
The script outputs the total number of subdomains found and writes them to a file named `{domain_name}_bfsubs.txt`. Out-of-scope domains are removed from the results.

### Installation
```
git clone https://github.com/Mr0Wido/bff-subdomains.git
cd bff-subdomains
python3 bffsubs.py
```

### Usage
```
python3 tools/bfsubs.py -u example.com -bfs fierce -os out.txt
```

### Wordlists
**Tag Options** | Files
--- | ---
bfall | all.txt (2178752)
bfcommonspeak | commonspeak.txt (484701)
bfhttparchive | httparchive_subdomains.txt (2351903)
bf2m | 2m-subdomains.txt (2167059)
bitquark | bitquark-subdomains-top100000.txt (100000)
bbsubs | bug-bounty-program-subdomains-trickest-inventory.txt(16132951)
combined | combined_subdomains.txt(648201)
fierce | fierce-hostlist.txt(2280)
n0kovo | n0kovo_subdomains.txt(3000000)
shubs | shubs-subdomains.txt(4846999)
reconng | sortedcombined-knock-dnsrecon-fierce-reconng.txt(102582)
bf11m | subdomains-top1million-110000.txt(114441)

### Options
**Flags** |    | Description
--- | ---  | ---
-h | --help | Show this help message and exit.
-u | --url | Domain name to scan. This argument is required.
-bfs | --bruteforce_scan | Bruteforcing with specific wordlists using Gobuster. This argument is optional and can take multiple values. If not provided, all available wordlists will be used.
-os | --out_of_scope | Out-of-scope domains file path. This argument is required.

### Requirments
```
colorama
tqdm
argparse
subprocess
os
```

### Notes
This script is intended for educational purposes and should be used responsibly. Always obtain proper authorization before performing any penetration testing activities.

### Todo
- [ ] Add **WFUZZ** option beside of Gobuster
