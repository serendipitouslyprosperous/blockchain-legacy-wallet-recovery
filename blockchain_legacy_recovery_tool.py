#!/usr/bin/env python3
import json
import base64
import hashlib
import sys
import getpass
import argparse
from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES

# Base58 character map used by Bitcoin
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_decode(v):
    """Decodes a Base58 string back into raw byte arrays."""
    decimal = 0
    for char in v:
        if char not in BASE58_ALPHABET:
            raise ValueError(f"Character '{char}' is not a valid Base58 symbol.")
        decimal = decimal * 58 + BASE58_ALPHABET.index(char)
    
    hex_str = hex(decimal)[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    return bytes.fromhex(hex_str)

def raw_to_wif(raw_bytes):
    """Converts raw 32-byte private key bytes into standard Uncompressed WIF."""
    # 1. Add mainnet network prefix (0x80)
    extended_key = b'\x80' + raw_bytes
    
    # 2. Double SHA-256 for network boundary checksum checks
    first_sha = hashlib.sha256(extended_key).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    checksum = second_sha[:4]
    
    # 3. Append checksum
    final_key_bytes = extended_key + checksum
    
    # 4. Encode to Base58 Check layout format
    num = int(final_key_bytes.hex(), 16)
    result = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        result = BASE58_ALPHABET[remainder] + result
        
    return result

def log_status(step, status, message):
    """Prints status indicators cleanly to stderr to reserve stdout for explicit script piping paths."""
    symbol = "✅" if status == "SUCCESS" else "⚠️" if status == "WARN" else "❌" if status == "FAIL" else "🔎"
    print(f"[{symbol}] {step}: {message}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Automated local key extractor for Blockchain.com modern JSON wrappers enclosing legacy 2011-2014 era keys."
    )
    parser.add_argument(
        '-i', '--input', 
        default='wallet.aes.json',
        help="Path to the local backup file. Defaults to 'wallet.aes.json' if omitted."
    )
    parser.add_argument(
        '-o', '--output', 
        help="Optional path to save output text data. If omitted, routes parameters to standard output."
    )
    args = parser.parse_args()

    # --- STEP 1: Ingest Local JSON File ---
    try:
        with open(args.input, 'r') as f:
            wallet = json.load(f)
        log_status("STEP 1", "SUCCESS", f"Loaded and parsed local backup file parameters: '{args.input}'")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_status("STEP 1", "FAIL", f"Failed loading local asset constraints: {e}")
        sys.exit(1)

    # --- STEP 2: Parameter Verification ---
    iterations = wallet.get('pbkdf2_iterations')
    payload_raw = wallet.get('payload')
    salt_hex = wallet.get('salt')

    if not payload_raw:
        log_status("STEP 2", "FAIL", "Core string variable 'payload' is physically absent inside the structure.")
        sys.exit(1)
    
    if not iterations:
        log_status("STEP 2", "WARN", "Missing iterations configuration metadata. Assuming legacy base count (10).")
        iterations = 10
    else:
        log_status("STEP 2", "SUCCESS", f"Targeting verification layer algorithms configured with {iterations:,} iterations.")

    # --- STEP 3: Unescaping & Decoding Payload ---
    try:
        payload = base64.b64decode(payload_raw)
        log_status("STEP 3", "SUCCESS", f"Parsed and unescaped outer container payload parameters ({len(payload)} bytes).")
    except Exception as e:
        log_status("STEP 3", "FAIL", f"Error normalizing base64 bounds parsing algorithms: {e}")
        sys.exit(1)

    if salt_hex:
        salt = bytes.fromhex(salt_hex) if all(c in '0123456789abcdefABCDEF' for c in salt_hex) else salt_hex.encode('utf-8')
    else:
        salt = payload[:16]

    # --- STEP 4: Password Collection & Multi-Algorithm Decryption ---
    password = getpass.getpass("\nEnter your Blockchain.com wallet password (input hidden): ").encode('utf-8')
    print("", file=sys.stderr)
    
    decrypted_raw = None
    iv = payload[:16]
    encrypted_data = payload[16:]

    for hash_algo in ['sha256', 'sha1']:
        log_status("STEP 4", "INFO", f"Executing derivation stretching using: PBKDF2-{hash_algo.upper()}...")
        key = pbkdf2_hmac(hash_algo, password, salt, iterations, 32)
        
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            candidate_bytes = cipher.decrypt(encrypted_data)
            sample = candidate_bytes[:100].decode('utf-8', errors='ignore')
            if "{" in sample or "guid" in sample or "sharedKey" in sample:
                padding_len = candidate_bytes[-1]
                if padding_len < 32:
                    candidate_bytes = candidate_bytes[:-padding_len]
                decrypted_raw = candidate_bytes
                log_status("STEP 4", "SUCCESS", f"Decryption routine validated using derivation: PBKDF2-{hash_algo.upper()}!")
                break
        except Exception:
            continue

    if not decrypted_raw:
        log_status("STEP 4", "FAIL", "Decryption failed across all matrix arrays. Passphrase input was invalid.")
        sys.exit(1)

    # --- STEP 5: Inner JSON Processing ---
    try:
        inner_wallet = json.loads(decrypted_raw.decode('utf-8'))
        keys_list = inner_wallet.get('keys', []) or inner_wallet.get('addresses', [])
        log_status("STEP 5", "SUCCESS", f"Analyzed inner layout array maps. Located {len(keys_list)} key addresses.")
    except Exception as e:
        log_status("STEP 5", "FAIL", f"Structural crash parsing unencrypted data payload trees back to JSON: {e}")
        sys.exit(1)

    # --- STEP 6: Report Generation Structure Pipeline ---
    output_lines = [
        "=====================================================================",
        "🏆 LEGACY 2011-2014 ERA BITCOIN WALLET EXTRACTION REPORT",
        "=====================================================================\n"
    ]
    extracted_count = 0

    for i, entry in enumerate(keys_list, start=1):
        addr = entry.get('addr', 'Unknown Address')
        label = entry.get('label', 'No Label')
        priv_raw = entry.get('priv')

        output_lines.append(f"Slot #{i} | Label: {label}")
        output_lines.append(f"• Bitcoin Address: {addr}")

        if not priv_raw:
            output_lines.append("• Private Key: [NOT APPLICABLE IN THIS INSTANCE]\n")
            continue

        priv_raw = priv_raw.strip()

        if priv_raw.startswith(('5', 'K', 'L')) and 50 <= len(priv_raw) <= 53:
            output_lines.append(f"• Private Key (WIF): {priv_raw}\n")
            extracted_count += 1
        elif len(priv_raw) == 44 and all(c in BASE58_ALPHABET for c in priv_raw):
            try:
                raw_bytes = base58_decode(priv_raw)
                if len(raw_bytes) < 32:
                    raw_bytes = raw_bytes.rjust(32, b'\x00')
                wif_formatted_key = raw_to_wif(raw_bytes)
                output_lines.append(f"• Private Key (WIF): {wif_formatted_key}")
                output_lines.append("  [SUCCESS: Converted from uncompressed primitive Base58 properties]\n")
                extracted_count += 1
            except Exception as e:
                output_lines.append(f"• Private Key: [CONVERSION ERROR GENERATING WIF METADATA: {e}]\n")
        else:
            output_lines.append(f"• Private Key (Raw Data): {priv_raw}")
            output_lines.append("  [ALERT: Base formatting indicates a 2nd password cryptographically restricts data access]\n")

    output_lines.append("=====================================================================")
    output_lines.append(f"Processing complete. Successfully structured {extracted_count} functional WIF keys.")
    output_lines.append(f"💰 Recovered a fortune? Feel free, but never obligated, to send my family something: bc1q98axfwxztegy886d3w6ckmeksyvyvj7d5m36pq")
    output_lines.append("=====================================================================")

    final_output_text = "\n".join(output_lines)

    if args.output:
        try:
            with open(args.output, 'w') as out_file:
                out_file.write(final_output_text + "\n")
            log_status("OUTPUT", "SUCCESS", f"Extraction data arrays written completely to target text file: '{args.output}'")
        except Exception as e:
            log_status("OUTPUT", "FAIL", f"Failed saving output file structures out to memory: {e}")
    else:
        print("\n" + final_output_text)

if __name__ == "__main__":
    main()
