import subprocess, json, argparse
from datetime import datetime

def get_aws_ips():
    print("[-] Checking for AWS IP Range JSON...")
    document_check = subprocess.run([f"ls resources/aws-ip-ranges.json"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, shell=True)
    if document_check.returncode == 0:
        print("[+] AWS IP Range JSON Identified!")
    else:
        print("[!] Could not locate AWS IP Range JSON -- Downloading now...")
        subprocess.run([f"wget -O resources/aws-ip-ranges.json https://ip-ranges.amazonaws.com/ip-ranges.json"], stdout=subprocess.DEVNULL, shell=True)
        print("[+] Tools directory successfully created")
    print("[-] Pulling IP Ranges from JSON...")
    f = open(f'resources/aws-ip-ranges.json')
    aws_ips = json.load(f)
    ip_ranges = []
    ip_ranges_str = ""
    for ip_range in aws_ips['prefixes']:
        ip_ranges.append(ip_range['ip_prefix'])
        ip_ranges_str += f"{ip_range['ip_prefix']}\n"
    f.close()
    f = open("resources/aws_ips.tmp", "w")
    f.write(ip_ranges_str)
    f.close()


def update_data(args):
    print("[-] Updating Scan Data")
    get_aws_ips()
    print(f"[-] Running initial scan to identify hosts...")
    ip_count = subprocess.run([f"nmap -n -sL -iL resources/aws_ips.tmp | wc -l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    ips = ip_count.stdout.replace("\n", "")
    print(f"[-] Running masscan against {ips} IPs...")
    if args.rate:
        subprocess.run([f"sudo masscan -p443 --rate {args.rate} -iL resources/aws_ips.tmp -oL data/clear_sky_masscan.tmp"], shell=True)
    else:
        subprocess.run([f"sudo masscan -p443 --rate 40000 -iL resources/aws_ips.tmp -oL data/clear_sky_masscan.tmp"], shell=True)
    subprocess.run(["cat data/clear_sky_masscan.tmp | awk {'print $4'} | awk NF | sort -u > data/tls-scan-in.tmp"], shell=True)
    print(f"[+] Successfully completed running masscan against {ips} IPs!")
    print(f"[-] Running tls-scan on masscan results to collect SSL/TLS Certificates...")
    subprocess.run([f"cat data/tls-scan-in.tmp | tls-scan/tls-scan --port=443 --concurrency=150 --cacert=tls-scan/ca-bundle.crt 2>/dev/null -o data/tls-results.json"], shell=True)
    print(f"[+] Successfully completed the tls-scan!")
    return True

def search_data(args):
    print(f"[-] Searching for certificates w/ '{args.search}'...")
    print(f"[-] Using jq to parse for the FQDN...")
    subprocess.run([f"""cat data/tls-results.json | jq --slurp -r '.[]? | select(.certificateChain[]?.subject | test("\\\{args.search}\\\W")) | .ip | @text' > data/tls_filtered.tmp"""], shell=True)
    print(f"[+] Successfully parsed tls-scan results!")
    now = datetime.now().strftime("%d-%m-%y_%I%p")
    results_str = subprocess.run([f"cat data/tls_filtered.tmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    results_arr = results_str.stdout.split("\n")
    print(f"[-] Running final NMap scan on identified targets...")
    if len(results_arr) < 10:
        subprocess.run([f"sudo nmap -T 4 -iL data/tls_filtered.tmp -Pn --script=http-title -p- --open > reports/{args.search}_{now}"], shell=True)
    else:
        subprocess.run([f"sudo nmap -T 4 -iL data/tls_filtered.tmp -Pn --script=http-title --top-ports 100 --open > reports/{args.search}_{now}"], shell=True)
    print(f"[+] NMap scan completed successfully!  A report has been created in the /reports directory")
    return True

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--search', help='FQDN or Extension to Search', required=True)
    parser.add_argument('-r','--rate', help='Masscan Rate ( Default: 40000 )', required=False)
    parser.add_argument('-u', '--update', help='Update Certificate Data ( Can Take 30+ Minutes )', required=False, action='store_true')
    return parser.parse_args()

def main(args):
    if args.update:
        update_data(args)
    search_data(args)
    print("[+] Done!")

if __name__ == "__main__":
    args = arg_parse()
    main(args)
