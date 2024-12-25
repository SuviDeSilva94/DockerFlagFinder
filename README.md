# DockerFlagFinder
Flag Finder inside multiple docker images : Ethical security 

<img width="1267" alt="image" src="https://github.com/user-attachments/assets/42391bc5-524c-4c55-a95c-bb7b2d599838" />

## Overview
**DockerFlagFinder** is a Python-based tool designed to search for hidden flags across a set of Docker images, while leveraging security tools such as Nmap, John the Ripper, and Hashcat for vulnerability assessment and password cracking. This project is particularly useful in security-oriented tasks, such as penetration testing and container vulnerability assessment, where finding and analyzing hidden secrets is essential.

## Features
1. **Flag Search**: Automatically searches for predefined flags in specified file paths across Docker containers.
2. **Nmap Integration**: Scans the container's open ports for security assessments.
3. **John the Ripper Integration**: Attempts to crack password hashes using a wordlist.
4. **Hashcat Integration**: Performs GPU-accelerated password cracking for bcrypt and other hash types.
5. **Error Handling**: Provides detailed logs of successes and failures during the flag search process.

## Requirements
1. Python 3.x
2. Docker installed and running on your system.
3. Access to the `rockyou.txt` wordlist for password cracking.
4. Security tools installed:
   - **Nmap**
   - **John the Ripper**
   - **Hashcat**

## Installation
### Clone the Repository
```bash
$ git clone https://github.com/SuviDeSilva94/DockerFlagFinder.git
$ cd DockerFlagFinder
```

### Install Dependencies
Ensure you have Python and Docker installed. Install additional required libraries:
```bash
$ pip install docker
```

### Security Tools Installation
- **Nmap**: Install using the package manager for your OS.
  ```bash
  # Ubuntu
  $ sudo apt-get install nmap

  # macOS (via Homebrew)
  $ brew install nmap
  ```

- **John the Ripper**: Install via the package manager or download from the official site.
  ```bash
  # Ubuntu
  $ sudo apt-get install john
  ```

- **Hashcat**: Install via package manager or download the latest version.
  ```bash
  # Ubuntu
  $ sudo apt-get install hashcat
  ```

## Usage

1. **Prepare Docker Images**: Ensure the images you want to analyze are pulled and accessible.

2. **Prepare the Environment**: Ensure `rockyou.txt` is present in the same directory or specify its path.

3. **Run the Script**:
   ```bash
   $ python3 DockerFlagFinder.py
   ```

4. **View Results**:
   - **Flag Results**: Check the `flag_results.txt` file for flag details.
   - **Nmap Results**: Check the `nmap_results.txt` file for open port details.
   - **Hashcat Results**: Check the `hashcat_results.txt` file for cracked hashes.

## Explanation of Code

### Docker Container Processing
The script iterates through a list of Docker images, identifies running containers, and searches for flags within predefined file paths. If a container for the image is not running, it logs the information and moves to the next image.

### Flag Search
For each container, the script:
- Checks the existence of predefined flag files.
- Searches for flags within these files using the `grep` command, including hidden files.
- Logs the results in `flag_results.txt`.

### Security Tool Integration
1. **Nmap**:
   - Scans the container's IP for open ports and services.
   - Results are saved in `nmap_results.txt`.

2. **John the Ripper**:
   - Attempts to crack password hashes found in the flag files.
   - Requires `rockyou.txt` or another wordlist.
   - Results are appended to `flag_results.txt`.

3. **Hashcat**:
   - Uses GPU acceleration to crack bcrypt and other hashes.
   - Results are saved in `hashcat_results.txt`.

### Error Handling
The script handles various errors, including missing files, inaccessible containers, and invalid commands, logging these in the output file for easy debugging.

## File Structure
- **DockerFlagFinder.py**: Main script for flag searching and vulnerability analysis.
- **flag_results.txt**: Stores the results of the flag search.
- **nmap_results.txt**: Stores the results of Nmap scans.
- **hashcat_results.txt**: Stores the results of Hashcat operations.
- **rockyou.txt**: Wordlist for password cracking (user-provided).

## Customization
1. **Add New Flags**:
   - Update the `flag_files` dictionary with new file paths.

2. **Change Wordlist**:
   - Replace `rockyou.txt` with your preferred wordlist.

3. **Add New Security Tools**:
   - Extend the `run_command` function to integrate additional tools.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
This tool is for educational and ethical penetration testing purposes only. Unauthorized use on systems you do not own or have explicit permission to test is illegal.

## Author
Developed by [Suvi De Silva](https://github.com/SuviDeSilva94).

## Contribution
Contributions are welcome! Feel free to open issues or submit pull requests.



