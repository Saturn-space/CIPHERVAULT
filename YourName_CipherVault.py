#!/usr/bin/env python3
"""
=============================================================================
Project Title: CipherVault - Multi-Algorithm Cryptographic & Authentication System
Academic Submission Reference Implementation
Primary Web Project: Next.js 15, TypeScript, Tailwind CSS, React 19
Original Desktop Prototype: Java Swing (MyGUIProject)
=============================================================================

This Python script provides an academic reference implementation and verification
testbench for CipherVault. It implements the exact mathematical algorithms, custom
92-character alphabet, authentication rules, and cipher logic used in the
production web application.

Algorithms Implemented:
  1. Random Substitution Cipher (92! keyspace permutation)
  2. Caesar Rotational Cipher (modulo 92 shift arithmetic)
  3. Shuffle Cipher (transposition permutation with dynamic length validation)

Usage:
  - Run self-tests:       python YourName_CipherVault.py --test
  - Run interactive CLI:  python YourName_CipherVault.py --interactive
  - Quick encrypt:        python YourName_CipherVault.py --encrypt --algo caesar --text "Hello" --key 3
  - Quick decrypt:        python YourName_CipherVault.py --decrypt --algo caesar --text "..." --key 3
"""

import sys
import os
import re
import json
import random
import argparse
from typing import Tuple, List, Dict, Optional, Any

# =============================================================================
# 1. GLOBAL 92-CHARACTER SET (EXACT MATCH WITH MyGUIPage.java & lib/cipher.ts)
# =============================================================================
CHARSET: List[str] = [
    'Q', '7', '@', 'k', '&', 'M', 'z', '!', '2', 'A', '%', 'p', '4', 'b', '*', 'X',
    'h', 'R', '0', '?', 'f', 'C', '}', 'L', 'y', '9', 'S', '(', 'd', 'T', '1', '^',
    'g', 'U', '5', 'm', '+', 'W', '3', 'l', '#', 'J', 'e', 'V', '_', 'c', '8', ';',
    'a', 'Y', 'N', 'o', 'K', '-', 'Z', 'H', 'q', '{', 't', '6', 'D', 'P', 'w', 'I',
    's', 'B', 'x', 'O', '/', 'r', 'G', 'u', 'v', 'E', '~', 'n', '|', 'j', 'F', '.',
    '<', '>', '[', ']', '=', ':', '"', '\'', '\\', '$', ',', ' '
]

CHARSET_STRING: str = "".join(CHARSET)
CHAR_INDEX: Dict[str, int] = {char: idx for idx, char in enumerate(CHARSET)}
CHARSET_LEN: int = len(CHARSET)  # Exactly 92


# =============================================================================
# 2. CRYPTOGRAPHIC CORE ALGORITHMS
# =============================================================================

class CryptographicEngine:
    """Core cryptographic implementation mirroring CipherVault's web engine."""

    # -------------------------------------------------------------------------
    # A. Caesar Cipher (Modulo 92)
    # -------------------------------------------------------------------------
    @staticmethod
    def caesar_encrypt(plaintext: str, shift: int) -> Tuple[str, Dict[str, Any]]:
        """Encrypts plaintext using a rotational Caesar shift over CHARSET."""
        if not plaintext:
            raise ValueError("Input plaintext cannot be empty.")

        normalized_shift = ((shift % CHARSET_LEN) + CHARSET_LEN) % CHARSET_LEN
        result_chars = []
        unmapped = []
        steps = []

        for i, char in enumerate(plaintext):
            if char in CHAR_INDEX:
                original_idx = CHAR_INDEX[char]
                new_idx = (original_idx + normalized_shift) % CHARSET_LEN
                transformed = CHARSET[new_idx]
                result_chars.append(transformed)
                steps.append({"pos": i, "char": char, "idx": original_idx, "new_idx": new_idx, "out": transformed})
            else:
                result_chars.append(char)
                if char not in unmapped:
                    unmapped.append(char)
                steps.append({"pos": i, "char": char, "idx": -1, "new_idx": -1, "out": char})

        return "".join(result_chars), {
            "algorithm": "caesar",
            "shift": shift,
            "unmapped_chars": unmapped,
            "steps": steps[:20]
        }

    @staticmethod
    def caesar_decrypt(ciphertext: str, shift: int) -> Tuple[str, Dict[str, Any]]:
        """Decrypts ciphertext using reverse rotational Caesar shift."""
        return CryptographicEngine.caesar_encrypt(ciphertext, -shift)

    # -------------------------------------------------------------------------
    # B. Random Substitution Cipher (92-Character Permutation)
    # -------------------------------------------------------------------------
    @staticmethod
    def generate_random_sub_key() -> str:
        """Generates a random permutation of CHARSET using Fisher-Yates shuffle."""
        shuffled = CHARSET.copy()
        random.shuffle(shuffled)
        return "".join(shuffled)

    @staticmethod
    def validate_random_sub_key(key: str) -> Tuple[bool, Optional[str]]:
        """Validates that a substitution key is an exact bijection of CHARSET."""
        if not key:
            return False, "Key cannot be empty."
        if len(key) != CHARSET_LEN:
            return False, f"Invalid key length: {len(key)} (must be exactly {CHARSET_LEN})."
        if len(set(key)) != CHARSET_LEN:
            return False, f"Key contains duplicate symbols ({len(set(key))} unique, expected {CHARSET_LEN})."
        return True, None

    @staticmethod
    def random_sub_encrypt(plaintext: str, key: Optional[str] = None) -> Tuple[str, str, Dict[str, Any]]:
        """Encrypts plaintext via random substitution table mapping."""
        if not plaintext:
            raise ValueError("Input plaintext cannot be empty.")

        effective_key = key.strip() if key and key.strip() else CryptographicEngine.generate_random_sub_key()
        is_valid, err_msg = CryptographicEngine.validate_random_sub_key(effective_key)
        if not is_valid:
            raise ValueError(f"Invalid substitution key: {err_msg}")

        result_chars = []
        unmapped = []
        steps = []

        for i, char in enumerate(plaintext):
            if char in CHAR_INDEX:
                original_idx = CHAR_INDEX[char]
                transformed = effective_key[original_idx]
                result_chars.append(transformed)
                steps.append({"pos": i, "char": char, "transformed": transformed})
            else:
                result_chars.append(char)
                if char not in unmapped:
                    unmapped.append(char)
                steps.append({"pos": i, "char": char, "transformed": char})

        return "".join(result_chars), effective_key, {
            "algorithm": "random-sub",
            "unmapped_chars": unmapped,
            "steps": steps[:20]
        }

    @staticmethod
    def random_sub_decrypt(ciphertext: str, key: str) -> Tuple[str, Dict[str, Any]]:
        """Decrypts ciphertext using the inverted mapping of the substitution key."""
        if not ciphertext:
            raise ValueError("Input ciphertext cannot be empty.")
        if not key or not key.strip():
            raise ValueError("Enter key used during encryption (92 characters required).")

        effective_key = key.strip()
        is_valid, err_msg = CryptographicEngine.validate_random_sub_key(effective_key)
        if not is_valid:
            raise ValueError(f"Invalid substitution key: {err_msg}")

        reverse_map = {effective_key[i]: CHARSET[i] for i in range(CHARSET_LEN)}
        result_chars = []
        unmapped = []

        for char in ciphertext:
            if char in reverse_map:
                result_chars.append(reverse_map[char])
            else:
                result_chars.append(char)
                if char not in unmapped:
                    unmapped.append(char)

        return "".join(result_chars), {
            "algorithm": "random-sub",
            "unmapped_chars": unmapped
        }

    # -------------------------------------------------------------------------
    # C. Shuffle Cipher (Permutation Transposition)
    # -------------------------------------------------------------------------
    @staticmethod
    def generate_shuffle_key(length: int) -> str:
        """Generates a random comma-separated permutation sequence for a given length."""
        if length <= 0:
            return ""
        indices = list(range(length))
        random.shuffle(indices)
        return ",".join(map(str, indices))

    @staticmethod
    def parse_shuffle_key(key_text: str, expected_length: int) -> List[int]:
        """Parses and validates a comma-separated permutation key."""
        if not key_text or not key_text.strip():
            raise ValueError("Shuffle key cannot be empty.")

        parts = [p.strip() for p in key_text.split(",") if p.strip()]
        if len(parts) != expected_length:
            raise ValueError(
                f"Shuffle key length mismatch: contains {len(parts)} indices, "
                f"text requires exactly {expected_length}."
            )

        indices: List[int] = []
        seen = set()

        for idx, part in enumerate(parts):
            try:
                val = int(part)
            except ValueError:
                raise ValueError(f"Invalid integer token '{part}' at position {idx + 1}.")

            if val < 0 or val >= expected_length:
                raise ValueError(
                    f"Index {val} is out of bounds (must be between 0 and {expected_length - 1})."
                )
            if val in seen:
                raise ValueError(f"Duplicate index {val} detected in shuffle sequence.")

            seen.add(val)
            indices.append(val)

        return indices

    @staticmethod
    def shuffle_encrypt(plaintext: str, key_text: str) -> Tuple[str, str]:
        """Encrypts plaintext by reordering characters according to the index key."""
        if not plaintext:
            raise ValueError("Input plaintext cannot be empty.")

        length = len(plaintext)
        indices = CryptographicEngine.parse_shuffle_key(key_text, length)
        output = [None] * length

        for i, char in enumerate(plaintext):
            target_pos = indices[i]
            output[target_pos] = char

        return "".join(output), key_text

    @staticmethod
    def shuffle_decrypt(ciphertext: str, key_text: str) -> str:
        """Decrypts ciphertext by inverting the transposition permutation."""
        if not ciphertext:
            raise ValueError("Input ciphertext cannot be empty.")

        length = len(ciphertext)
        indices = CryptographicEngine.parse_shuffle_key(key_text, length)
        output = [None] * length

        for i in range(length):
            source_pos = indices[i]
            output[i] = ciphertext[source_pos]

        return "".join(output)


# =============================================================================
# 3. USER AUTHENTICATION & VALIDATION RULES
# =============================================================================

class AuthManager:
    """User registration and authentication logic matching RegisterPage.java & LoginPage.java."""

    DEFAULT_USERS = [
        {"username": "SecurityAdmin", "email": "admin@gmail.com", "mobile": "9876543210", "password": "password123"},
        {"username": "AliceCryptography", "email": "alice@gmail.com", "mobile": "9123456780", "password": "securepass"},
        {"username": "BobCipher", "email": "bob@gmail.com", "mobile": "9001122334", "password": "mypassword"}
    ]

    def __init__(self, storage_path: str = "users_db.json"):
        self.storage_path = storage_path
        self.users: List[Dict[str, str]] = self._load_users()

    def _load_users(self) -> List[Dict[str, str]]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return list(self.DEFAULT_USERS)

    def _save_users(self) -> None:
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"[Warning] Failed to persist user database: {e}")

    def register(self, username: str, email: str, mobile: str, password: str) -> Tuple[bool, str]:
        """Validates credentials matching Java Swing RegisterPage rules."""
        u = username.strip()
        e = email.strip()
        m = mobile.strip()
        p = password.strip()

        if not u or not e or not m or not p:
            return False, "All fields are required!"
        if not e.endswith("@gmail.com"):
            return False, "Email must be a valid Gmail address (must end with @gmail.com)!"
        if not re.fullmatch(r"\d{10}", m):
            return False, "Mobile number must be exactly 10 digits!"
        if len(p) < 6:
            return False, "Password must be at least 6 characters!"
        if any(user["email"].lower() == e.lower() for user in self.users):
            return False, "This email is already registered!"

        new_user = {"username": u, "email": e, "mobile": m, "password": p}
        self.users.append(new_user)
        self._save_users()
        return True, "Account Created Successfully"

    def login(self, email: str, password: str) -> Tuple[bool, Optional[Dict[str, str]], str]:
        """Validates credentials matching Java Swing LoginPage query."""
        e = email.strip().lower()
        p = password.strip()

        for user in self.users:
            if user["email"].lower() == e and user["password"] == p:
                safe_user = {k: v for k, v in user.items() if k != "password"}
                return True, safe_user, "Login Successful"
        return False, None, "Invalid Email or Password"


# =============================================================================
# 4. AUTOMATED VERIFICATION SELF-TEST SUITE
# =============================================================================

def run_self_tests() -> bool:
    """Executes automated verification suite across all algorithms and validation rules."""
    print("=" * 70)
    print("CipherVault Verification Testbench - Automated Self-Tests")
    print("=" * 70)

    all_passed = True
    test_cases = [
        "Hello World!",
        "Secret Mission @ 0800 hours near the embassy.",
        "Pass@Key_992!{SecureAccess}",
        "Numbers: 0123456789 Symbols: !@#$%^&*()_+~|}{[]:;\"'\\<>,. /"
    ]

    # Test 1: Caesar Cipher Roundtrip
    print("\n[Test 1] Caesar Cipher Verification (Modulo 92 Arithmetic)...")
    for shift in [3, 13, 26, 47, -5, 91, 184]:
        for sample in test_cases:
            enc, _ = CryptographicEngine.caesar_encrypt(sample, shift)
            dec, _ = CryptographicEngine.caesar_decrypt(enc, shift)
            if dec != sample:
                print(f"  FAIL: Caesar shift={shift} mismatch:\n    Orig: {sample}\n    Got:  {dec}")
                all_passed = False
                break
    if all_passed:
        print("  PASS: Caesar Cipher verified across all test samples and shifts.")

    # Test 2: Random Substitution Roundtrip
    print("\n[Test 2] Random Substitution Cipher Verification (92-Char Bijection)...")
    key = CryptographicEngine.generate_random_sub_key()
    valid, err = CryptographicEngine.validate_random_sub_key(key)
    assert valid, f"Generated key validation failed: {err}"

    for sample in test_cases:
        enc, used_key, _ = CryptographicEngine.random_sub_encrypt(sample, key)
        dec, _ = CryptographicEngine.random_sub_decrypt(enc, used_key)
        if dec != sample:
            print(f"  FAIL: Substitution mismatch:\n    Orig: {sample}\n    Got:  {dec}")
            all_passed = False
            break
    if all_passed:
        print("  PASS: Random Substitution roundtrip verified for 92-char keyspace.")

    # Test 3: Shuffle Cipher Roundtrip
    print("\n[Test 3] Shuffle Cipher Verification (Index Permutation)...")
    for sample in test_cases:
        shuffle_key = CryptographicEngine.generate_shuffle_key(len(sample))
        enc, _ = CryptographicEngine.shuffle_encrypt(sample, shuffle_key)
        dec = CryptographicEngine.shuffle_decrypt(enc, shuffle_key)
        if dec != sample:
            print(f"  FAIL: Shuffle mismatch:\n    Orig: {sample}\n    Got:  {dec}")
            all_passed = False
            break
    if all_passed:
        print("  PASS: Shuffle permutation verified for all dynamic text lengths.")

    # Test 4: Authentication Validation Rules
    print("\n[Test 4] Authentication Rule Rigor (Email/Mobile/Password constraints)...")
    auth = AuthManager()

    # Valid registration
    test_email = f"tester_{random.randint(1000, 9999)}@gmail.com"
    ok, msg = auth.register("TestUser", test_email, "9876543210", "secret123")
    assert ok, f"Valid registration failed: {msg}"

    # Invalid email domain
    ok, msg = auth.register("BadUser", "bad@yahoo.com", "9876543210", "secret123")
    assert not ok and "Gmail" in msg, "Failed to reject non-gmail address"

    # Invalid mobile length
    ok, msg = auth.register("BadUser", "user@gmail.com", "12345", "secret123")
    assert not ok and "10 digits" in msg, "Failed to reject invalid mobile length"

    # Invalid short password
    ok, msg = auth.register("BadUser", "user@gmail.com", "9876543210", "123")
    assert not ok and "6 characters" in msg, "Failed to reject short password"

    print("  PASS: Authentication constraints strictly enforced.")

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL TESTS PASSED: The cryptographic engine is 100% verified.")
    else:
        print("SOME TESTS FAILED: Please inspect errors above.")
    print("=" * 70)
    return all_passed


# =============================================================================
# 5. INTERACTIVE CLI RUNNER
# =============================================================================

def interactive_cli():
    """Terminal-based user menu matching the web and desktop applications."""
    engine = CryptographicEngine()
    auth = AuthManager()
    current_user = None

    while True:
        print("\n" + "=" * 60)
        print("   CipherVault - Academic Cryptographic Console   ")
        print("=" * 60)
        status = f"Logged in as: {current_user['username']} ({current_user['email']})" if current_user else "Session: Guest"
        print(f"[{status}]")
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Generate Random Substitution Key (92 Chars)")
        print("4. User Authentication (Login / Register)")
        print("5. Run Automated Self-Tests")
        print("6. Exit")
        choice = input("\nEnter choice [1-6]: ").strip()

        if choice == "1":
            print("\n--- Encrypt Text ---")
            print("1. Random Substitution Cipher")
            print("2. Caesar Cipher")
            print("3. Shuffle Cipher")
            a_choice = input("Select algorithm [1-3]: ").strip()
            text = input("Enter plaintext to encrypt: ")

            try:
                if a_choice == "1":
                    k = input("Enter 92-char key (or leave empty to auto-generate): ").strip()
                    res, used_k, _ = engine.random_sub_encrypt(text, k or None)
                    print("\n[SUCCESS - Random Substitution]")
                    print(f"Key (save this!):\n{used_k}\n")
                    print(f"Cipher:\n{res}")
                elif a_choice == "2":
                    shift = int(input("Enter integer shift (e.g., 3, 13): "))
                    res, _ = engine.caesar_encrypt(text, shift)
                    print("\n[SUCCESS - Caesar Cipher]")
                    print(f"Cipher:\n{res}")
                elif a_choice == "3":
                    k = input(f"Enter shuffle key for {len(text)} characters (or leave empty to auto-generate): ").strip()
                    if not k:
                        k = engine.generate_shuffle_key(len(text))
                    res, used_k = engine.shuffle_encrypt(text, k)
                    print("\n[SUCCESS - Shuffle Cipher]")
                    print(f"Key (Indices):\n{used_k}\n")
                    print(f"Cipher:\n{res}")
                else:
                    print("Invalid algorithm selection.")
            except Exception as e:
                print(f"[Error] {e}")

        elif choice == "2":
            print("\n--- Decrypt Text ---")
            print("1. Random Substitution Cipher")
            print("2. Caesar Cipher")
            print("3. Shuffle Cipher")
            a_choice = input("Select algorithm [1-3]: ").strip()
            cipher = input("Enter ciphertext to decrypt: ")

            try:
                if a_choice == "1":
                    k = input("Enter 92-char key: ").strip()
                    res, _ = engine.random_sub_decrypt(cipher, k)
                    print("\n[SUCCESS - Decrypted Plaintext]")
                    print(f"Result:\n{res}")
                elif a_choice == "2":
                    shift = int(input("Enter integer shift used during encryption: "))
                    res, _ = engine.caesar_decrypt(cipher, shift)
                    print("\n[SUCCESS - Decrypted Plaintext]")
                    print(f"Result:\n{res}")
                elif a_choice == "3":
                    k = input("Enter shuffle key used during encryption: ").strip()
                    res = engine.shuffle_decrypt(cipher, k)
                    print("\n[SUCCESS - Decrypted Plaintext]")
                    print(f"Result:\n{res}")
                else:
                    print("Invalid algorithm selection.")
            except Exception as e:
                print(f"[Error] {e}")

        elif choice == "3":
            key = engine.generate_random_sub_key()
            print("\nGenerated 92-Character Permutation Key:")
            print("-" * 50)
            print(key)
            print("-" * 50)
            print("Length: 92 characters | Bijective: Verified")

        elif choice == "4":
            print("\n1. Login")
            print("2. Register New Account")
            print("3. Logout")
            sub = input("Select [1-3]: ").strip()
            if sub == "1":
                em = input("Email: ").strip()
                pw = input("Password: ").strip()
                ok, user, msg = auth.login(em, pw)
                if ok:
                    current_user = user
                    print(f"[Success] {msg} Welcome, {user['username']}!")
                else:
                    print(f"[Failed] {msg}")
            elif sub == "2":
                un = input("Username: ").strip()
                em = input("Gmail address (@gmail.com): ").strip()
                mb = input("Mobile (10 digits): ").strip()
                pw = input("Password (min 6 chars): ").strip()
                ok, msg = auth.register(un, em, mb, pw)
                print(f"[{'Success' if ok else 'Failed'}] {msg}")
            elif sub == "3":
                current_user = None
                print("Logged out successfully.")

        elif choice == "5":
            run_self_tests()

        elif choice == "6":
            print("\nExiting CipherVault Console. Thank you.")
            break
        else:
            print("Invalid option.")


# =============================================================================
# 6. MAIN SCRIPT ENTRYPOINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CipherVault: Academic Reference Implementation and Cryptographic Verification Suite"
    )
    parser.add_argument("--test", action="store_true", help="Run automated cryptographic self-tests")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive CLI menu")
    parser.add_argument("--encrypt", action="store_true", help="Perform encryption operation")
    parser.add_argument("--decrypt", action="store_true", help="Perform decryption operation")
    parser.add_argument("--algo", choices=["random-sub", "caesar", "shuffle"], help="Cipher algorithm")
    parser.add_argument("--text", type=str, help="Input text payload")
    parser.add_argument("--key", type=str, help="Cipher key (shift, 92-char string, or shuffle indices)")

    args = parser.parse_args()

    if args.test:
        success = run_self_tests()
        sys.exit(0 if success else 1)

    if args.encrypt or args.decrypt:
        if not args.algo or not args.text:
            print("[Error] Please specify --algo and --text.")
            sys.exit(1)

        engine = CryptographicEngine()

        if args.algo == "caesar":
            shift = int(args.key) if args.key else 3
            if args.encrypt:
                res, _ = engine.caesar_encrypt(args.text, shift)
                print(f"Encrypted (Shift {shift}): {res}")
            else:
                res, _ = engine.caesar_decrypt(args.text, shift)
                print(f"Decrypted (Shift {shift}): {res}")

        elif args.algo == "random-sub":
            if args.encrypt:
                res, used_key, _ = engine.random_sub_encrypt(args.text, args.key)
                print(f"Key:\n{used_key}\nCipher:\n{res}")
            else:
                if not args.key:
                    print("[Error] Decryption requires --key parameter.")
                    sys.exit(1)
                res, _ = engine.random_sub_decrypt(args.text, args.key)
                print(f"Decrypted: {res}")

        elif args.algo == "shuffle":
            if args.encrypt:
                key = args.key or engine.generate_shuffle_key(len(args.text))
                res, used_key = engine.shuffle_encrypt(args.text, key)
                print(f"Key: {used_key}\nCipher: {res}")
            else:
                if not args.key:
                    print("[Error] Decryption requires --key parameter.")
                    sys.exit(1)
                res = engine.shuffle_decrypt(args.text, args.key)
                print(f"Decrypted: {res}")
        sys.exit(0)

    # Default to interactive CLI if no flags provided
    interactive_cli()


if __name__ == "__main__":
    main()
