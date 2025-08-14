"""
Password Manager Core Functionality
Handles CRUD operations, master password management, and credential storage.
"""

import json
import os
import hashlib
from datetime import datetime
from crypto_utils import CryptoUtils

class PasswordManager:
    def __init__(self, data_file="credentials.json.encrypted"):
        """Initialize the password manager with encrypted storage file"""
        self.data_file = data_file
        self.master_hash_file = ".master_hash"
        self.crypto = CryptoUtils()
        self.master_password = None
        self.credentials = {}
        
        # Set secure file permissions
        self._ensure_secure_permissions()
    
    def _ensure_secure_permissions(self):
        """Ensure secure file permissions for sensitive files"""
        try:
            # Set restrictive permissions (owner read/write only)
            for file_path in [self.data_file, self.master_hash_file]:
                if os.path.exists(file_path):
                    os.chmod(file_path, 0o600)  # rw-------
        except OSError:
            pass  # Ignore permission errors on systems that don't support it
    
    def _hash_master_password(self, password):
        """Create a secure hash of the master password"""
        # Use PBKDF2 with SHA-256 for secure password hashing
        salt = b"secure_password_manager_salt_2024"  # In production, use random salt per user
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    
    def is_first_run(self):
        """Check if this is the first time running the application"""
        return not os.path.exists(self.master_hash_file)
    
    def initialize_master_password(self, password):
        """Initialize the master password for first-time setup"""
        try:
            master_hash = self._hash_master_password(password)
            with open(self.master_hash_file, 'w') as f:
                f.write(master_hash)
            
            # Set secure permissions
            os.chmod(self.master_hash_file, 0o600)
            
            # Initialize empty credentials file
            self.master_password = password
            self.credentials = {}
            self._save_credentials()
            
            return True
        except Exception as e:
            raise Exception(f"Failed to initialize master password: {e}")
    
    def verify_master_password(self, password):
        """Verify the master password against stored hash"""
        try:
            if not os.path.exists(self.master_hash_file):
                return False
            
            with open(self.master_hash_file, 'r') as f:
                stored_hash = f.read().strip()
            
            provided_hash = self._hash_master_password(password)
            return stored_hash == provided_hash
        except Exception:
            return False
    
    def authenticate(self, password):
        """Authenticate user and load credentials"""
        if not self.verify_master_password(password):
            return False
        
        self.master_password = password
        return self._load_credentials()
    
    def _load_credentials(self):
        """Load and decrypt credentials from file"""
        try:
            if not os.path.exists(self.data_file):
                self.credentials = {}
                return True
            
            with open(self.data_file, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                self.credentials = {}
                return True
            
            # Decrypt the data using master password
            decrypted_data = self.crypto.decrypt_data(encrypted_data, self.master_password)
            self.credentials = json.loads(decrypted_data)
            return True
        
        except json.JSONDecodeError:
            raise Exception("Corrupted credentials file. Unable to parse data.")
        except Exception as e:
            raise Exception(f"Failed to load credentials: {e}")
    
    def _save_credentials(self):
        """Encrypt and save credentials to file"""
        try:
            # Convert credentials to JSON
            json_data = json.dumps(self.credentials, indent=2)
            
            # Encrypt the data using master password
            encrypted_data = self.crypto.encrypt_data(json_data, self.master_password)
            
            # Write encrypted data to file
            with open(self.data_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions
            os.chmod(self.data_file, 0o600)
            return True
        
        except Exception as e:
            raise Exception(f"Failed to save credentials: {e}")
    
    def add_credential(self, service, username, password, notes=""):
        """Add a new credential"""
        if service in self.credentials:
            raise Exception(f"Service '{service}' already exists.")
        
        self.credentials[service] = {
            "username": username,
            "password": password,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self._save_credentials()
        return True

    def get_credential(self, service):
        """Return a specific credential"""
        return self.credentials.get(service)

    def update_credential(self, service, username, password, notes=""):
        """Update an existing credential"""
        if service not in self.credentials:
            raise Exception(f"Service '{service}' not found.")
        
        self.credentials[service] = {
            "username": username,
            "password": password,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self._save_credentials()
        return True

    def get_credential(self, service):
        """Return a specific credential"""
        return self.credentials.get(service)

    def update_credential(self, service, username, password, notes=""):
        """Update an existing credential"""
        if service not in self.credentials:
            raise Exception(f"Service '{service}' not found.")
        
        self.credentials[service] = {
            "username": username,
            "password": password,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self._save_credentials()
        return True

    def get_credential(self, service):
        """Return a specific credential"""
        return self.credentials.get(service)

    def update_credential(self, service, username, password, notes=""):
        """Update an existing credential"""
        if service not in self.credentials:
            raise Exception(f"Service '{service}' not found.")
        
        self.credentials[service] = {
            "username": username,
            "password": password,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self._save_credentials()
        return True
    
    def get_credential(self, site):
        """Retrieve a specific credential"""
        try:
            site_key = site.lower().strip()
            return self.credentials.get(site_key)
        except Exception as e:
            raise Exception(f"Failed to retrieve credential: {e}")
    
    def get_all_credentials(self):
        """Retrieve all credentials"""
        try:
            return self.credentials.copy()
        except Exception as e:
            raise Exception(f"Failed to retrieve credentials: {e}")
    
    def update_credential(self, site, username=None, password=None, notes=None):
        """Update an existing credential"""
        try:
            site_key = site.lower().strip()
            
            if site_key not in self.credentials:
                return False
            
            credential = self.credentials[site_key]
            
            # Update only provided fields
            if username is not None:
                credential['username'] = username
            if password is not None:
                credential['password'] = password
            if notes is not None:
                credential['notes'] = notes
            
            credential['updated_at'] = datetime.now().isoformat()
            
            return self._save_credentials()
        
        except Exception as e:
            raise Exception(f"Failed to update credential: {e}")
    
    def delete_credential(self, site):
        """Delete a credential"""
        try:
            site_key = site.lower().strip()
            
            if site_key not in self.credentials:
                return False
            
            del self.credentials[site_key]
            return self._save_credentials()
        
        except Exception as e:
            raise Exception(f"Failed to delete credential: {e}")
    
    def change_master_password(self, current_password, new_password):
        """Change the master password and re-encrypt all data"""
        try:
            # Verify current password
            if not self.verify_master_password(current_password):
                return False
            
            # Update master password hash
            new_hash = self._hash_master_password(new_password)
            with open(self.master_hash_file, 'w') as f:
                f.write(new_hash)
            
            # Update master password and re-encrypt credentials
            self.master_password = new_password
            return self._save_credentials()
        
        except Exception as e:
            raise Exception(f"Failed to change master password: {e}")
    
    def export_credentials(self, filename):
        """Export credentials to an encrypted backup file"""
        try:
            if not self.credentials:
                return False
            
            # Create export data with metadata
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'version': '1.0',
                'credentials': self.credentials
            }
            
            json_data = json.dumps(export_data, indent=2)
            encrypted_data = self.crypto.encrypt_data(json_data, self.master_password)
            
            with open(filename, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions
            os.chmod(filename, 0o600)
            return True
        
        except Exception as e:
            raise Exception(f"Failed to export credentials: {e}")
    
    def import_credentials(self, filename, master_password):
        """Import credentials from an encrypted backup file"""
        try:
            if not os.path.exists(filename):
                return False
            
            with open(filename, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.crypto.decrypt_data(encrypted_data, master_password)
            import_data = json.loads(decrypted_data)
            
            # Merge imported credentials (overwrite existing)
            if 'credentials' in import_data:
                for site_key, credential in import_data['credentials'].items():
                    self.credentials[site_key] = credential
            
            return self._save_credentials()
        
        except Exception as e:
            raise Exception(f"Failed to import credentials: {e}")
    
    def get_statistics(self):
        """Get statistics about stored credentials"""
        try:
            total_credentials = len(self.credentials)
            sites_with_notes = sum(1 for cred in self.credentials.values() if cred.get('notes'))
            
            # Password strength analysis
            weak_passwords = 0
            for cred in self.credentials.values():
                password = cred.get('password', '')
                if len(password) < 8:
                    weak_passwords += 1
            
            return {
                'total_credentials': total_credentials,
                'sites_with_notes': sites_with_notes,
                'weak_passwords': weak_passwords,
                'strong_passwords': total_credentials - weak_passwords
            }
        
        except Exception as e:
            raise Exception(f"Failed to get statistics: {e}")
