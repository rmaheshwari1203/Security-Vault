# Secure Key Vault: Password Manager

Secure Key Vault is a Python-based password manager that provides a secure, local solution for managing your credentials. It features robust AES encryption, master password protection, and a choice of a command-line interface (CLI) or a graphical user interface (GUI).

## Key Features

* **Strong Encryption**: Your data is secured with AES-256 encryption, a military-grade standard that keeps your sensitive information safe.
* **Master Password Protection**: A single, strong master password is used to encrypt and decrypt all your credentials, ensuring that only you can access your data.
* **Multiple Interfaces**: Choose between a simple, efficient command-line interface or one of two graphical user interfaces to manage your passwords.
* **Local Storage**: All your encrypted data is stored locally on your machine, giving you full control over your information.
* **Full CRUD Functionality**: Easily **C**reate, **R**ead, **U**pdate, and **D**elete your credentials as needed.
* **Encrypted Backups**: The application includes functionality to export your credentials to an encrypted backup file for safekeeping.

## Getting Started

Follow these simple steps to get Secure Key Vault up and running on your system.

### Prerequisites

* Python 3.11 or newer
* `pip` for installing packages

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/rmaheshwari1203/Security-Vault](https://github.com/rmaheshwari1203/Security-Vault)
    cd secure-key-vault
    ```

2.  **Create and Activate a Virtual Environment**:
    * **macOS/Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Windows**:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```


### Running the Application

You have three options for running the password manager:

* **Command-Line Interface**:
    ```bash
    python main.py
    ```

* **Basic Graphical User Interface**:
    ```bash
    python gui_main.py
    ```

* **Modern Graphical User Interface**:
    ```bash
    python gui_modern.py
    ```

## How to Use

### First-Time Setup

When you run the application for the first time, you will be prompted to create a **master password**. This password is the key to your vault, so be sure to choose a strong, memorable password.


### Main Interface

Once you have set up your master password, you can start managing your credentials.

#### Modern GUI

The modern GUI provides a sleek, futuristic interface for all your password management needs.

* **Authentication Screen**:
    
* **Main Dashboard**:
    
* **Adding a New Credential**:
    
#### Basic GUI

The basic GUI offers a more traditional but equally functional interface.

* **Authentication Screen**:
    
* **Main Window**:
    
### Command-Line Interface

For those who prefer working in the terminal, the CLI provides a fast and efficient way to manage your passwords.


## Security

The security of your data is the top priority for Secure Key Vault. Here’s a look at the security measures in place:

* **Encryption**: The application uses the **Fernet** library, which implements **AES-256** encryption to keep your credentials secure.
* **Key Derivation**: Your master password is not stored directly. Instead, a key is derived from it using **PBKDF2 HMAC with SHA-256**, a standard method for securely deriving cryptographic keys from passwords.
* **Local Storage**: Your encrypted data never leaves your computer, ensuring you have complete control over your sensitive information.

## Contributing


Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to open an issue or submit a pull request.
