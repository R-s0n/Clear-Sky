import subprocess, sys

print("[-] Installing necessary dependencies...")

pip3_check = subprocess.run(["pip3 --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if pip3_check.returncode == 0:
    print("[+] Pip3 is installed")
else :
    print("[!] Pip3 is NOT installed -- Installing now...")
    cloning = subprocess.run(["sudo apt-get install -y python3-pip"], stdout=subprocess.DEVNULL, shell=True)
    print("[+] Pip3 was successfully installed")

print("[-] Installing required packages...")
subprocess.run(["pip3 install argparse datetime"], shell=True)

masscan_check = subprocess.run(["masscan --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if masscan_check.returncode == 1:
    print("[+] Masscan is installed")
else :
    print("[!] Masscan is NOT installed -- Installing now...")
    subprocess.run(['sudo apt-get --assume-yes install git make gcc'], shell=True)
    subprocess.run(['git clone https://github.com/robertdavidgraham/masscan'], shell=True)
    subprocess.run(['cd masscan; sudo make install;'], shell=True)
    masscan_check2 = subprocess.run(["masscan --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if masscan_check2.returncode == 1:
        print("[+] Masscan was successfully installed")
    else:
        print("[-] Something went wrong!  Check the stack trace, make any necessary adjustments, and try again.  Exiting...")
        sys.exit(2)

tls_scan_check = subprocess.run(["tls-scan/tls-scan --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
if tls_scan_check.returncode == 0:
    print("[+] Tls-scan is installed")
else :
    print("[!] Tls-scan is NOT installed -- Installing now...")
    subprocess.run(['wget "https://github.com/prbinu/tls-scan/releases/latest"'], shell=True)
    subprocess.run(['tar -xvzf tls-scan-linux.tar.gz'], shell=True)
    tls_scan_check2 = subprocess.run(["tls-scan/tls-scan --version"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)
    if tls_scan_check2.returncode == 0:
        print("[+] Tls-scan was successfully installed")
    else:
        print("[-] Something went wrong!  Check the stack trace, make any necessary adjustments, and try again.  Exiting...")
        sys.exit(2)

print("[+] Installation complete!")