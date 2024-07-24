import subprocess
import os
import re
from fastapi import FastAPI
from pydantic import BaseModel

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


def filter_and_format_data(data):
    filtered_data = []
    filtered_data2 = []
    for subnet in data:
        vtrust_details = []
        updated_details = []
        for detail in subnet["details"]:
            vtrust = float(detail.get("VTRUST", 0))
            updated = float(detail.get("UPDATED", 0))
            if vtrust < 0.90:
                vtrust_details.append({
                    "VTRUST": detail["VTRUST"],
                    "UPDATED": detail["UPDATED"]
                })
            if  updated > 500:
                updated_details.append({
                    "VTRUST": detail["VTRUST"],
                    "UPDATED": detail["UPDATED"]
                })
        if vtrust_details:
            filtered_data.append({
                "subnet": subnet["subnet"],
                "details": vtrust_details
            })
        if updated_details:
            filtered_data.append({
                "subnet": subnet["subnet"],
                "details": updated_details
            })
    
    # Format as table in string
    formatted_result = ""
    for subnet in filtered_data:
        formatted_result += f"Subnet: {subnet['subnet']}\n"
        formatted_result += "VTRUST\tUPDATED\n"
        for detail in subnet["details"]:
            formatted_result += f"{detail['VTRUST']}\t{detail['UPDATED']}\n"
        formatted_result += "\n"
        # Format as table in string
    formatted_result2 = ""
    for subnet in filtered_data2:
        formatted_result2 += f"Subnet: {subnet['subnet']}\n"
        formatted_result2 += "VTRUST\tUPDATED\n"
        for detail in subnet["details"]:
            formatted_resul2t += f"{detail['VTRUST']}\t{detail['UPDATED']}\n"
        formatted_result2 += "\n"

    return formatted_result,formatted_result2


@app.post("/wallet-info/")
def wallet_info(request: WalletRequest):
    raw_output = get_btcli_wallet_info(request.wallet_name, width=request.width, sort_by=request.sort_by)
    parsed_data = parse_btcli_output(raw_output)
    print(parsed_data)
    
    result = filter_and_format_data(parsed_data)
    return {"result": result}

