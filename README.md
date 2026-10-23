# CipherVault: Multi-Algorithm Cryptographic & Authentication System

[![Next.js](https://img.shields.io/badge/Next.js-15.4-black.svg)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2-blue.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue.svg)](https://www.typescriptlang.org/)
[![Python Verification](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/Academic-Submission-green.svg)]()

---

## 1. Project Overview & Description

**CipherVault** is a comprehensive, production-grade cryptographic orchestration platform and academic verification suite. Originally designed as a desktop prototype in Java Swing (`MyGUIProject`), the platform was converted and expanded into a modern, full-stack **Next.js 15 (App Router)** and **TypeScript** web application accompanied by an automated **Python 3** verification testbench.

The platform implements three foundational cryptographic cipher algorithms operating over a specialized **92-symbol mathematical character set (`CHARSET`)**:
1. **Random Substitution Cipher**: High-entropy permutation mapping across $92! \approx 1.24 \times 10^{142}$ possible bijection keys.
2. **Caesar Rotational Cipher**: Direct modular arithmetic ($k \pmod{92}$) supporting positive, negative, and wrapping offsets.
3. **Shuffle Cipher**: Transposition permutation where character indices are deterministically rearranged via positional index vectors.

In addition to cipher transformations, CipherVault features client-side session management with strict validation rules (Gmail domain enforcement, 10-digit mobile verification, password complexity), a real-time character-by-character transformation visualizer, an encrypted key vault, operation audit history, and a toggleable **Classic Java Swing 2000s Retro Desktop GUI Mode**.

---

## 2. Problem the Project Solves

- **Runtime & Platform Portability**: Legacy desktop cryptography prototypes (e.g., NetBeans Java Swing projects using local MySQL instances) require complex local JRE and database configurations. CipherVault operates universally in any web browser without installation.
- **Educational Visual Transparency**: Traditional cryptographic tools display only raw input and output, obscuring the mathematical transformations. CipherVault features a live pipeline visualizer tracing each character's index mapping and shift in real time.
- **Cross-Language Algorithmic Verifiability**: By pairing the web frontend with a standalone Python verification testbench (`YourName_CipherVault.py`), students and evaluators can verify identical cipher outputs across languages.

---

## 3. Main Features

- **Dual-Panel Cryptographic Studio**:
  - Left Panel: Dedicated Encryption Studio (styled in deep blue `#0056b3` matching the Java prototype).
  - Right Panel: Dedicated Decryption Studio (styled in emerald green `#28a745` matching the Java prototype).
  - Bottom Utility Toolbar: `Clear`, `About`, and `Reset` controls with formatted terminal output.
- **Global 92-Symbol Custom Alphabet (`CHARSET`)**:
  - Encompasses uppercase, lowercase, numbers, brackets, punctuation, backslash, quotes, and whitespace.
- **Key Generation & Validation**:
  - Fisher-Yates 92-character permutation generator with duplicate and length validation.
  - Dynamic shuffle key generator tailored to the exact length ($N$) of any input string.
  - Interactive Caesar shift slider from $-91$ to $+91$ with one-click presets (`ROT3`, `ROT13`, `ROT42`).
- **Live Pipeline Visualizer**:
  - Real-time character stream trace displaying original character, target character, and respective indices in `CHARSET`.
- **Cryptographic Key Vault & History**:
  - Local storage of encryption keys with custom nicknames and copy-to-clipboard functionality.
  - Audit trail of past operations with timestamps, algorithm badges, and JSON export.
- **User Authentication & Data Validation**:
  - Exact replication of Java Swing validation rules:
    - All fields mandatory.
    - Email address must end with `@gmail.com`.
    - Mobile number must be exactly 10 digits (`^\d{10}$`).
    - Password must be at least 6 characters.
  - Pre-seeded demo accounts (`admin@gmail.com` / `password123`, `alice@gmail.com` / `securepass`) for instant evaluation.
- **Retro Java Swing Mode**:
  - Full-fidelity simulation of the NetBeans/JDK desktop window with Windows titlebar, classic yellow login dialog, green registration panel, and simulated `JOptionPane` dialog boxes.

---

## 4. Technologies & Tools Used

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | Next.js (App Router) | 15.4.9 | Server-side rendering, hydration-safe architecture, routing |
| **UI Library** | React | 19.2.1 | Component-driven reactive user interface |
| **Language** | TypeScript | 5.9.3 | Static typing, interface contracts for cipher models |
| **Styling** | Tailwind CSS & PostCSS | 4.1.11 | Modern utility-first responsive layout |
| **Icons** | Lucide React | 0.553.0 | Modern SVG iconography |
| **Animations** | Motion & Canvas Confetti | 12.23 / 1.4 | Micro-interactions and operation celebrations |
| **Python Testbench** | Python | 3.10+ | Standalone CLI verification and automated test suite |
| **Report Generation**| docx (Node.js) | 9.2.0 | Programmatic compilation of genuine `.docx` report |
| **Legacy Source** | Java Swing / AWT | JDK 17/21 | Original desktop prototype (`MyGUIProject`) |

---

## 5. System Architecture

```
[ User Browser / Client Viewport ]
       │
       ├── Modern Cyber Security UI (app/page.tsx)
       └── Classic Java Swing Retro Mode (components/RetroJavaSwingWrapper.tsx)
              │
              ├── [ Authentication State ] ── useSyncExternalStore ── LocalStorage
              ├── [ Cryptographic Studio ] (components/CipherStudio.tsx)
              │         │
              │         ├── Caesar Cipher Engine (lib/cipher.ts)
              │         ├── Random Substitution Engine (lib/cipher.ts)
              │         └── Shuffle Cipher Engine (lib/cipher.ts)
              │
              ├── [ Live Pipeline Visualizer ] (components/CipherVisualizer.tsx)
              ├── [ Key Vault & Audit Logs ] (lib/vault.ts)
              │
              └── [ Academic Python Testbench ] (YourName_CipherVault.py)
                        ├── Automated Verification Self-Tests
                        └── Interactive CLI Console
```

---

## 6. Dataset Description & Source

> **Academic Note on Datasets:**  
> This project **does not require or use an external machine learning dataset** (e.g., from Kaggle, UCI, or Hugging Face). Cryptographic engines are deterministic mathematical systems that execute encryption and decryption algorithms upon arbitrary user-provided text payloads at runtime. No model training or empirical dataset fitting is involved.

---

## 7. Prerequisites

### For Web Application:
- **Node.js**: Version `18.18.0` or higher (Recommended: Node.js `20.x` LTS).
- **npm**: Version `9.x` or higher.

### For Python Academic Testbench:
- **Python**: Version `3.10` or higher.
- Standard libraries (`sys`, `os`, `re`, `json`, `random`, `argparse`).

---

## 8. Installation & Setup Instructions

### Option A: Running the Full-Stack Web Application

1. **Clone or Extract the Project**:
   ```bash
   cd /path/to/project
   ```

2. **Install Node.js Dependencies**:
   ```bash
   npm install
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env.local` (default keys are already pre-configured for local development):
   ```bash
   cp .env.example .env.local
   ```

4. **Launch the Development Server**:
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your web browser.

5. **Build for Production**:
   ```bash
   npm run build
   npm run start
   ```

---

### Option B: Running the Python Academic Reference Suite

1. **Navigate to the Project Directory**:
   ```bash
   cd /path/to/project
   ```

2. **(Optional) Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: The core Python script runs natively using standard Python libraries.*

3. **Execute Automated Self-Tests**:
   ```bash
   python3 YourName_CipherVault.py --test
   ```

4. **Launch Interactive Terminal CLI**:
   ```bash
   python3 YourName_CipherVault.py --interactive
   ```

5. **Execute Direct Command-Line Operations**:
   ```bash
   # Caesar encryption
   python3 YourName_CipherVault.py --encrypt --algo caesar --text "Hello World" --key 3

   # Caesar decryption
   python3 YourName_CipherVault.py --decrypt --algo caesar --text "..." --key 3

   # Random substitution encryption (auto-generates 92-char key)
   python3 YourName_CipherVault.py --encrypt --algo random-sub --text "Secret Message"
   ```

---

## 9. Folder Structure

```
.
├── app/
│   ├── globals.css              # Tailwind CSS imports & custom typography
│   ├── layout.tsx               # Root layout with suppressHydrationWarning
│   └── page.tsx                 # Main application page (Hero, Studio, Visualizer)
├── components/
│   ├── AboutModal.tsx           # Algorithm documentation & CHARSET viewer
│   ├── AuthModal.tsx            # Login & Registration modal with Java Swing validation
│   ├── CipherStudio.tsx         # Dual-panel encryption & decryption workspace
│   ├── CipherVisualizer.tsx     # Live character mapping stream visualizer
│   ├── Header.tsx               # Top navigation, status badges, profile controls
│   ├── HistoryDrawer.tsx        # Audit trail of cipher operations with JSON export
│   ├── KeyVaultModal.tsx        # Cryptographic key manager & generator
│   └── RetroJavaSwingWrapper.tsx# NetBeans Java Swing desktop simulation mode
├── hooks/
│   └── use-mobile.ts            # Viewport detection via useSyncExternalStore
├── lib/
│   ├── auth.ts                  # User accounts, validation, session subscriptions
│   ├── cipher.ts                # Cryptographic algorithms & 92-char CHARSET
│   ├── utils.ts                 # Utility class merger (clsx & twMerge)
│   └── vault.ts                 # Key vault and audit log persistence
├── public/
│   └── assets/                  # Original Java Swing zip asset and static files
├── scripts/
│   └── build_report_docx.js     # Programmatic generator for Word project report
├── submission/                  # Academic Submission Deliverables Folder
│   ├── YourName_CipherVault.py  # Python reference implementation & test suite
│   ├── requirements.txt         # Python environment requirements
│   ├── YourName_ProjectReport.docx # Formatted academic Microsoft Word report
│   └── README.md                # Submission README documentation
├── metadata.json                # AI Studio application metadata
├── package.json                 # Node.js npm dependencies and build scripts
├── tsconfig.json                # TypeScript compiler configuration
└── README.md                    # Primary project documentation
```

---

## 10. Example Usage & Verification Walkthrough

1. **Sign In or Test as Guest**:
   - Click **Sign In** and use demo credentials: `admin@gmail.com` / `password123`.
   - Alternatively, register a new user: must provide a username, an `@gmail.com` email, a 10-digit mobile number, and a password $\ge 6$ characters.
2. **Perform Random Substitution Encryption**:
   - In the **Encryption Studio** (Blue panel), select **Random Substitution**.
   - Enter plaintext: `Hello World! Cryptography 2026.`.
   - Click **Encrypt**. An authentic 92-character key is generated via Fisher-Yates shuffle.
   - Click **Save Key to Vault** or copy the key.
3. **Inspect Character Mapping**:
   - Scroll down to the **Live Cipher Transformation Pipeline** to see how each symbol was mapped to its target ciphertext symbol.
4. **Decrypt Ciphertext**:
   - In the **Decryption Studio** (Green panel), paste the ciphertext and 92-character key.
   - Click **Decrypt** to restore the exact original message.
5. **Toggle Classic Java Swing Mode**:
   - Click **Classic Swing GUI** in the header to enter the nostalgic NetBeans/JDK desktop simulation.

---

## 11. Troubleshooting

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **"Email must be a valid Gmail address!"** | Registration validation rule | Input an email address ending strictly in `@gmail.com` (as required by the original `RegisterPage.java`). |
| **"Mobile number must be 10 digits!"** | Mobile regex rule | Provide exactly 10 numeric digits without dashes or spaces. |
| **"Shuffle key length mismatch"** | Shuffle permutation constraint | Shuffle cipher requires exactly one index per character. Click **Generate Key for N Chars** to automatically create a valid key. |
| **Hydration Warning in Browser** | Browser extension attribute injection | Fixed in `app/layout.tsx` via `suppressHydrationWarning` on `<html>` and `<body>`. |

---

## 12. Limitations & Future Roadmap

- **Statistical Vulnerability**: Classical monoalphabetic ciphers are susceptible to frequency analysis on long ciphertexts. Future versions could introduce polyalphabetic Vigenère or AES-256-GCM modes.
- **Unmapped Characters**: Characters outside the 92-character alphabet (such as non-English accented glyphs) pass through untransformed.
- **Future Enhancements**:
  - Direct ciphertext export into visual Steganographic PNG carriers.
  - Interactive frequency analysis histogram view for cryptanalysis education.

---

## 13. Author & Academic Submission Info

- **Project Title**: CipherVault - Encryption & Decryption System
- **Candidate Name**: `[YourName / Student Candidate Placeholder]`
- **Primary Contact**: `unknonfiction@gmail.com`
- **Submission Date**: October 2026
- **Deliverables Included**:
  1. `YourName_CipherVault.py` (Python Academic Reference Implementation & Test Suite)
  2. `requirements.txt` (Python Dependency Specification)
  3. `YourName_ProjectReport.docx` (Genuine Formatted Word Document Report)
  4. `README.md` (Technical Project & Academic Submission Guide)
