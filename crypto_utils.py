"""
Cryptographic Utilities for Password Manager
Handles AES encryption/decryption using Fernet (symmetric encryption)
"""

import base64
import os
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoUtils:
    def __init__(self):
        """Initialize crypto utilities"""
        self.salt_size = 32  # 256 bits
        self.iterations = 100000  # PBKDF2 iterations
    
    def _derive_key_from_password(self, password, salt):
        """Derive a Fernet-compatible key from password using PBKDF2"""
        try:
            # Convert password to bytes
            password_bytes = password.encode('utf-8')
            
            # Create PBKDF2HMAC instance
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,  # 256 bits for Fernet
                salt=salt,
                iterations=self.iterations,
            )
            
            # Derive key and encode for Fernet
            key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
            return key
        
        except Exception as e:
            raise Exception(f"Key derivation failed: {e}")
    
    def encrypt_data(self, data, password):
        """Encrypt data using password-derived key"""
        try:
            # Generate random salt
            salt = os.urandom(self.salt_size)
            
            # Derive encryption key from password
            key = self._derive_key_from_password(password, salt)
            
            # Create Fernet cipher
            fernet = Fernet(key)
            
            # Encrypt data
            data_bytes = data.encode('utf-8')
            encrypted_data = fernet.encrypt(data_bytes)
            
            # Combine salt + encrypted data
            return salt + encrypted_data
        
        except Exception as e:
            raise Exception(f"Encryption failed: {e}")
    
    def decrypt_data(self, encrypted_data, password):
        """Decrypt data using password-derived key"""
        try:
            # Extract salt and encrypted content
            salt = encrypted_data[:self.salt_size]
            encrypted_content = encrypted_data[self.salt_size:]
            
            # Derive decryption key from password
            key = self._derive_key_from_password(password, salt)
            
            # Create Fernet cipher
            fernet = Fernet(key)
            
            # Decrypt data
            decrypted_bytes = fernet.decrypt(encrypted_content)
            return decrypted_bytes.decode('utf-8')
        
        except Exception as e:
            if "InvalidToken" in str(e):
                raise Exception("Invalid master password or corrupted data")
            raise Exception(f"Decryption failed: {e}")
    
    def generate_secure_password(self, length=16, include_symbols=True):
        """Generate a cryptographically secure password"""
        import string
        import secrets
        
        try:
            # Define character sets
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            digits = string.digits
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
            
            # Ensure at least one character from each set
            password = [
                secrets.choice(lowercase),
                secrets.choice(uppercase),
                secrets.choice(digits)
            ]
            
            if include_symbols:
                password.append(secrets.choice(symbols))
            
            # Fill remaining length with random characters from all sets
            all_chars = lowercase + uppercase + digits + symbols
            for _ in range(length - len(password)):
                password.append(secrets.choice(all_chars))
            
            # Shuffle the password list
            secrets.SystemRandom().shuffle(password)
            
            return ''.join(password)
        
        except Exception as e:
            raise Exception(f"Password generation failed: {e}")
    
    def hash_password(self, password, salt=None):
        """Create a secure hash of a password (for verification)"""
        try:
            if salt is None:
                salt = os.urandom(32)  # 256-bit salt
            
            # Use PBKDF2 for secure password hashing
            pwdhash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                self.iterations
            )
            
            return {
                'hash': pwdhash.hex(),
                'salt': salt.hex()
            }
        
        except Exception as e:
            raise Exception(f"Password hashing failed: {e}")
    
    def verify_password_hash(self, password, stored_hash, stored_salt):
        """Verify a password against its stored hash"""
        try:
            salt = bytes.fromhex(stored_salt)
            hash_result = self.hash_password(password, salt)
            return hash_result['hash'] == stored_hash
        
        except Exception as e:
            raise Exception(f"Password verification failed: {e}")
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp for file naming"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def secure_delete_string(string_var):
        """Attempt to securely overwrite string in memory (limited effectiveness in Python)"""
        try:
            # Note: This has limited effectiveness in Python due to string immutability
            # and garbage collection, but we'll do what we can
            if string_var:
                # Overwrite with random data
                import secrets
                random_data = ''.join(secrets.choice('0123456789abcdef') for _ in range(len(string_var)))
                string_var = random_data
                del random_data
            del string_var
        except:
            pass  # Ignore any errors during secure deletion
    
    def validate_encrypted_file(self, filepath, password):
        """Validate that an encrypted file can be decrypted with the given password"""
        try:
            if not os.path.exists(filepath):
                return False, "File does not exist"
            
            with open(filepath, 'rb') as f:
                encrypted_data = f.read()
            
            if len(encrypted_data) < self.salt_size:
                return False, "File is too small to contain valid encrypted data"
            
            # Try to decrypt
            self.decrypt_data(encrypted_data, password)
            return True, "File is valid and decryptable"
        
        except Exception as e:
            return False, f"Validation failed: {e}"
    
    def get_encryption_info(self):
        """Get information about the encryption methods used"""
        return {
            'encryption_algorithm': 'AES-128 (Fernet)',
            'key_derivation': 'PBKDF2-HMAC-SHA256',
            'salt_size_bits': self.salt_size * 8,
            'pbkdf2_iterations': self.iterations,
            'security_level': 'High'
        }
