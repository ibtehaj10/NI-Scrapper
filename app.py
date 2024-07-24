import subprocess
import os
import re
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
app = FastAPI()

class WalletRequest(BaseModel):
    wallet_name: str
    width: int = 200
    sort_by: str = 'VTRUST'


def get_btcli_wallet_info(wallet_name, arg='overview', width=200, sort_by='VTRUST'):
    try:
        # Construct the command with the argument, width, and sort_by option
        cmd = ['btcli', 'wallet', arg]

        # Set the COLUMNS environment variable to a larger value
        env = os.environ.copy()
        env['COLUMNS'] = str(width)

        # Run the command and pass the wallet name as input
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True)
        stdout, stderr = process.communicate(input=wallet_name + '\n')

        if process.returncode == 0:
            return stdout
        else:
            return f"Error: {stderr}"
    except Exception as e:
        return str(e)


def parse_btcli_output(output):
    subnets = []
    subnet_pattern = re.compile(r"Subnet: (\d+)")
    header_pattern = re.compile(r"COLDKEY\s+HOTKEY\s+UID\s+ACTIVE\s+STAKE\(\w+\)\s+RANK\s+TRUST\s+CONSENSUS\s+INCENTIVE\s+DIVIDENDS\s+EMISSION\(\w+\)\s+VTRUST\s+VPERMIT\s+UPDATED\s+AXON\s+HOTKEY_SS58")

    lines = output.splitlines()
    current_subnet = None
    headers = []

    for line in lines:
        line = line.strip()
        if subnet_pattern.match(line):
            if current_subnet:
                subnets.append(current_subnet)
            current_subnet = {"subnet": subnet_pattern.match(line).group(1), "details": []}
        elif header_pattern.match(line):
            headers = header_pattern.match(line).group(0).split()
        elif current_subnet is not None and line:
            details = re.split(r'\s{2,}', line)
            if len(details) >= len(headers):
                detail_dict = {headers[i]: details[i] for i in range(len(headers))}
                current_subnet["details"].append(detail_dict)

    if current_subnet:
        subnets.append(current_subnet)

    return subnets


def clean_data(raw_data):
    vtrust_below_90 = []
    updated_above_500 = []
    # print(raw_data)
    for i in raw_data:
        if "details" in I:
            updated = i["details"][0]['UPDATED']
            vtrusts = i["details"][0]['VTRUST']
            SN = i["subnet"]
            lis = {"SN":SN,"Vtrust":vtrusts,"Updated":updated}
            print(lis)
            # print(SN, vtrust, updated)
            if float(vtrusts) < 0.90:
                # print(lis)
                vtrust_below_90.append(lis)
            if int(updated) > 500:
                # print(lis)
                updated_above_500.append(lis)
    return vtrust_below_90 , updated_above_500
def generate_table(data):
    # Determine column widths
    sn_width = max(len(str(row['SN'])) for row in data) + 4
    updated_width = max(len(row['Updated']) for row in data) + 6
    vtrust_width = max(len(row['Vtrust']) for row in data)  + 4

    table = f"+{'-' * sn_width}+{'-' * updated_width}+{'-' * vtrust_width}+\n"
    table += f"| {'SN'.ljust(sn_width-1)}| {'Updated'.ljust(updated_width-1)}| {'Vtrust'.ljust(vtrust_width-1)}|\n"
    table += f"+{'-' * sn_width}+{'-' * updated_width}+{'-' * vtrust_width}+\n"

    for row in data:
        table += f"| {str(row['SN']).ljust(sn_width-1)}| {row['Updated'].ljust(updated_width-1)}| {row['Vtrust'].ljust(vtrust_width-1)}|\n"
    
    table += f"+{'-' * sn_width}+{'-' * updated_width}+{'-' * vtrust_width}+\n"
    print("Generation done")
    return table


@app.post("/wallet-info/")
def wallet_info(request: WalletRequest):
    raw_output = get_btcli_wallet_info(request.wallet_name, width=request.width, sort_by=request.sort_by)
    parsed_data = parse_btcli_output(raw_output)
    print(parsed_data)
    # parsed = pd.DataFrame(parsed_data)
    # parsed.to_json("data.json")
    vtrust_below_090, updated_above_500 = clean_data(parsed_data)
    print("here 2")
    # Prepare strings to hold the table contents
    vtrust_table = ""
    updated_table = ""
    
    # Populate the table strings
    if vtrust_below_090:
        vtrust_table += "The following validators have Vtrust values below 0.90:\n"
        vtrust_table += generate_table(vtrust_below_090)
        vtrust_table += "\n"
    
    if updated_above_500:
        updated_table += "The following validators have Updated values above 500:\n"
        updated_table += generate_table(updated_above_500)
    
    # result = filter_and_format_data(parsed_data)
    return [vtrust_table,updated_table]

