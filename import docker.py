import docker
import os
import subprocess

# Initialize Docker client
client = docker.from_env()

# List of image names to search for
image_names = [
    "nharrand/intsec-group-1:latest",
    "nharrand/intsec-group-2:latest",
    "nharrand/intsec-group-3:latest",
    "noorabh/passoire_group4_hardened:v1",
    "kivayuri/group5_phase2:v5",
    "0x00a0/passoire_group06:latest",
    "nharrand/intsec-group-7:latest",
    "laldemar/group8_hardend:latest",
    "nharrand/intsec-group-9:latest",
    "amanjuman/passoire:final",
    "nharrand/intsec-group-11:latest",
    "qdbjo/group_submission:latest",
    "nharrand/intsec-group-14:latest",
    "nharrand/intsec-group-20:latest",
    "nharrand/intsec-group-21:latest",
    "heishi99/passoire:V3.2",
    "erangis/group24:3.0",
    "nharrand/intsec-group-25:latest",
    "nharrand/intsec-group-27:latest",
    "hagendaz123/group28:finalv2",
    "nharrand/intsec-group-30:latest",
    "intsecproject/passoire-final:v2",
    "udeshim/group_32_intsec:final-tag",
    "nharrand/intsec-group-33:latest",
    "nharrand/intsec-group-34:latest",
    "nharrand/intsec-group-35:latest",
    "qtung/g36-passoire-0512-v4:latest",
    "nharrand/intsec-group-38:latest",
    "kentfre/group40_passoire:latest",
    "jonybotto/passoire:final",
    "toxillo/intsec_passoire:v1",
    "nharrand/intsec-group-44:latest",
    "ngwaru/group46:1.3.3",
    "intsecgroup48/passoire-ready:latest",
    "denny1024/is-grp50:v2.5.5",
    "niu1028/sthlm-insec-ht2024-grp52:latest",
    "nharrand/intsec-group-56:latest",
    "balkongen/passoire-improved:latest",
    "qlvin/grupp64:latest",
    "nharrand/intsec-group-66:latest",
    "helss/passoire:patch_17",
    "victorlejon/intsec_defense:latest"
]

# Tools setup
nmap_output_file = "nmap_results.txt"
john_wordlist = "rockyou.txt"
hashcat_wordlist = "rockyou.txt"
hashcat_output_file = "hashcat_results.txt"

# List of flag file names and paths
flag_files = {
    "flag_1": "../home/passoire",
    "flag_2": "../root/flag_2",
    "flag_3": "web/flag_3",
    "flag_4": "web/index.php",
    "flag_5": "config/passoire.sql",
    "flag_7": "web/uploads/secret",
    "flag_9": "crypto-helper/flag_9",
    "flag_10": "crypto-helper/server.js",
    "flag_13": "web/index.php",
    "flag_14": "../home/admin/flag_14"
}

# Output file
output_file = "flag_results.txt"

# Helper function to run system commands
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# Open the output file for writing
with open(output_file, "w") as f:
    f.write("Group No\tFlag\t\n")

    for image_name in image_names:
        try:
            # Find the container running the desired image
            container = None
            for cont in client.containers.list():
                if image_name in cont.image.tags:  # Match the image name with its tag
                    container = cont
                    break

            if not container:
                f.write(f"{image_name}\tNo running container found\n")
                continue

            f.write(f"{image_name}\n")

            for flag, path in flag_files.items():
                try:
                    # Check if the exact path exists
                    check_path = container.exec_run(f"ls {path}", stderr=False)
                    if check_path.exit_code != 0:
                        # If not found, attempt to locate the file within the broader parent directory
                        parent_dir = "/".join(path.split("/")[:-1])
                        find_result = container.exec_run(f"find {parent_dir} -name {path.split('/')[-1]}", stderr=False)
                        if find_result.exit_code == 0 and find_result.output.strip():
                            path = find_result.output.decode().strip()
                        else:
                            f.write(f"\t{flag}\tFile not found\n")
                            continue

                    # Search specifically for the target flag including hidden files
                    grep_result = container.exec_run(f"grep -rn '{flag}' {path}", stderr=False)
                    if grep_result.exit_code == 0:
                        flag_content = grep_result.output.decode().strip()
                        # Filter only lines containing the exact flag
                        relevant_lines = [line for line in flag_content.split("\n") if flag in line]
                        if relevant_lines:
                            for line in relevant_lines:
                                f.write(f"\t{flag}\t{line}\n")
                        else:
                            f.write(f"\t{flag}\tNo relevant content found\n")
                    else:
                        f.write(f"\t{flag}\tNo matching content found\n")

                    # Run security tools
                    # 1. Run nmap
                    container_ip = container.attrs['NetworkSettings']['IPAddress']
                    nmap_command = f"nmap -p- {container_ip}"
                    nmap_results = run_command(nmap_command)
                    with open(nmap_output_file, "a") as nmap_f:
                        nmap_f.write(f"{image_name}:\n{nmap_results}\n")

                    # 2. Use john for password cracking if hashes are found
                    if "hash:" in flag_content:  # Assuming hash presence
                        with open("hashes.txt", "w") as hash_f:
                            hash_f.write(flag_content)
                        john_command = f"john --wordlist={john_wordlist} hashes.txt"
                        john_results = run_command(john_command)
                        f.write(f"John Results: {john_results}\n")

                    # 3. Use hashcat if bcrypt or other hashes are identified
                    hashcat_command = f"hashcat -a 0 -m 3200 hashes.txt {hashcat_wordlist}"
                    hashcat_results = run_command(hashcat_command)
                    with open(hashcat_output_file, "a") as hashcat_f:
                        hashcat_f.write(f"{image_name}:\n{hashcat_results}\n")

                except Exception as e:
                    f.write(f"\t{flag}\tError: {str(e)}\n")
        except Exception as e:
            f.write(f"{image_name}\tError: {str(e)}\n")

print(f"Search and security scanning completed. Results saved in {output_file}.")
