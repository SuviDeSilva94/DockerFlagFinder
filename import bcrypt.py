import bcrypt

# Bcrypt hash to decode
bcrypt_hash = "$2y$10$8.JDGhoKggC8NcXEUosODeEoOuL0COHx6mgQ2ebC7SpxacjILVnrC"

# Load passwords from a wordlist file (e.g., rockyou.txt) or predefined list
# Ensure you have a valid wordlist file in the same directory or provide its path
password_file = "rockyou.txt"

# Function to brute-force bcrypt hash
def crack_bcrypt(hash_to_crack, wordlist_path):
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                password = line.strip()  # Remove whitespace and newline characters
                if bcrypt.checkpw(password.encode(), hash_to_crack.encode()):
                    print(f"Password found: {password}")
                    return password
                
        print("Password not found in the wordlist.")
        return None
    except FileNotFoundError:
        print(f"Wordlist file not found: {wordlist_path}")
        return None

# Run the brute-force attack
cracked_password = crack_bcrypt(bcrypt_hash, password_file)

if cracked_password:
    print(f"The password is: {cracked_password}")
else:
    print("Failed to crack the hash.")
