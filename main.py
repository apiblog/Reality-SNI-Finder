from subprocess import check_output, run, CalledProcessError, DEVNULL
from re import findall
from pandas import DataFrame
from tabulate import tabulate

# Read the sni.txt file and split it into a list of domain names
with open("sni.txt", "r") as my_file:
    data = my_file.read()
    sni_list = data.split("\n")

# Remove any empty strings from the sni_list
sni_list = list(filter(None, sni_list))

# Test all the domains in sni.txt file and put the results in a dictionary
domain_ping_dict = {}

for domain in sni_list:
    try:
        x = check_output(f"./tlsping {domain}:443", shell=True, stderr=DEVNULL).rstrip().decode('utf-8')
        # Use regular expressions to extract the "avg" value
        avg_match = findall(r"avg/.*?ms.*?(\d+\.?\d*)ms", x)
        if avg_match:
            avg_value = float(avg_match[0])
            domain_ping_dict[domain] = avg_value
            print(f"✓ {domain}: {avg_value} ms")
        else:
            print(f"✗ {domain}: No avg value found")
    except CalledProcessError as e:
        print(f"✗ {domain}: Connection error")
    except Exception as e:
        print(f"✗ {domain}: {str(e)}")

# Sort the dictionary by the values in ascending order
sorted_dict = dict(sorted(domain_ping_dict.items(), key=lambda item: item[1]))

# Convert the sorted dictionary to a pandas DataFrame and print it using tabulate
if sorted_dict:
    df = DataFrame(sorted_dict.items(), columns=['domains', 'pings(ms)'])
    run('clear', shell=True)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    print(f"\nTotal successful: {len(sorted_dict)} out of {len(sni_list)} domains")
else:
    print("No successful domain tests found")
