#!/usr/bin/env python3
"""
Secure Password Manager - Main Entry Point
A command-line password manager with AES encryption and secure local storage.
"""

import sys
import getpass
import os
from password_manager import PasswordManager
from crypto_utils import CryptoUtils

def clear_screen():
    """Clear the terminal screen for better UX"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("🔐 SECURE PASSWORD MANAGER")
    print("="*50)
    print("1. Add New Credential")
    print("2. View All Credentials")
    print("3. Search Credential")
    print("4. Update Credential")
    print("5. Delete Credential")
    print("6. Change Master Password")
    print("7. Export Credentials (Encrypted)")
    print("8. Exit")
    print("="*50)

def get_master_password(prompt="Enter master password: "):
    """Securely get master password from user"""
    try:
        password = getpass.getpass(prompt)
        if not password:
            print("❌ Master password cannot be empty!")
            return None
        return password
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error reading password: {e}")
        return None

def validate_password_strength(password):
    """Validate password strength with detailed feedback"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    missing = []
    if not has_upper:
        missing.append("uppercase letter")
    if not has_lower:
        missing.append("lowercase letter")
    if not has_digit:
        missing.append("number")
    if not has_special:
        missing.append("special character")
    
    if missing:
        return False, f"Password must contain: {', '.join(missing)}"
    
    return True, "Strong password"

def add_credential(pm):
    """Add a new credential with validation"""
    print("\n📝 Add New Credential")
    print("-" * 30)
    
    site = input("Site/Service name: ").strip()
    if not site:
        print("❌ Site name cannot be empty!")
        return
    
    username = input("Username/Email: ").strip()
    if not username:
        print("❌ Username cannot be empty!")
        return
    
    password = getpass.getpass("Password: ")
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    # Validate password strength
    is_strong, message = validate_password_strength(password)
    if not is_strong:
        print(f"⚠️  Warning: {message}")
        confirm = input("Continue anyway? (y/N): ").lower()
        if confirm != 'y':
            print("❌ Credential not added.")
            return
    
    notes = input("Notes (optional): ").strip()
    
    try:
        success = pm.add_credential(site, username, password, notes)
        if success:
            print("✅ Credential added successfully!")
        else:
            print("❌ Failed to add credential. Site may already exist.")
    except Exception as e:
        print(f"❌ Error adding credential: {e}")

def view_all_credentials(pm):
    """Display all stored credentials"""
    print("\n📋 All Stored Credentials")
    print("-" * 40)
    
    try:
        credentials = pm.get_all_credentials()
        if not credentials:
            print("📭 No credentials stored yet.")
            return
        
        for i, (site, data) in enumerate(credentials.items(), 1):
            print(f"\n{i}. 🌐 {site}")
            print(f"   👤 Username: {data['username']}")
            print(f"   🔑 Password: {'*' * len(data['password'])}")
            if data.get('notes'):
                print(f"   📝 Notes: {data['notes']}")
            print(f"   📅 Created: {data.get('created_at', 'Unknown')}")
            if data.get('updated_at'):
                print(f"   🔄 Updated: {data['updated_at']}")
        
        # Option to reveal passwords
        reveal = input(f"\nReveal passwords? (y/N): ").lower()
        if reveal == 'y':
            print("\n" + "="*40)
            print("🔓 REVEALED PASSWORDS")
            print("="*40)
            for site, data in credentials.items():
                print(f"🌐 {site}: {data['password']}")
    
    except Exception as e:
        print(f"❌ Error retrieving credentials: {e}")

def search_credential(pm):
    """Search for a specific credential"""
    print("\n🔍 Search Credential")
    print("-" * 25)
    
    site = input("Enter site/service name: ").strip()
    if not site:
        print("❌ Site name cannot be empty!")
        return
    
    try:
        credential = pm.get_credential(site)
        if credential:
            print(f"\n✅ Found credential for: {site}")
            print(f"👤 Username: {credential['username']}")
            
            reveal = input("Reveal password? (y/N): ").lower()
            if reveal == 'y':
                print(f"🔑 Password: {credential['password']}")
            else:
                print(f"🔑 Password: {'*' * len(credential['password'])}")
            
            if credential.get('notes'):
                print(f"📝 Notes: {credential['notes']}")
            print(f"📅 Created: {credential.get('created_at', 'Unknown')}")
            if credential.get('updated_at'):
                print(f"🔄 Updated: {credential['updated_at']}")
        else:
            print(f"❌ No credential found for '{site}'")
    
    except Exception as e:
        print(f"❌ Error searching credential: {e}")

def update_credential(pm):
    """Update an existing credential"""
    print("\n✏️  Update Credential")
    print("-" * 25)
    
    site = input("Enter site/service name to update: ").strip()
    if not site:
        print("❌ Site name cannot be empty!")
        return
    
    try:
        existing = pm.get_credential(site)
        if not existing:
            print(f"❌ No credential found for '{site}'")
            return
        
        print(f"\n📋 Current credential for: {site}")
        print(f"👤 Username: {existing['username']}")
        print(f"🔑 Password: {'*' * len(existing['password'])}")
        if existing.get('notes'):
            print(f"📝 Notes: {existing['notes']}")
        
        print("\n📝 Enter new values (press Enter to keep current):")
        
        new_username = input(f"New username [{existing['username']}]: ").strip()
        if not new_username:
            new_username = existing['username']
        
        new_password = getpass.getpass("New password (leave empty to keep current): ")
        if not new_password:
            new_password = existing['password']
        else:
            # Validate new password strength
            is_strong, message = validate_password_strength(new_password)
            if not is_strong:
                print(f"⚠️  Warning: {message}")
                confirm = input("Continue anyway? (y/N): ").lower()
                if confirm != 'y':
                    print("❌ Update cancelled.")
                    return
        
        new_notes = input(f"New notes [{existing.get('notes', '')}]: ").strip()
        if not new_notes:
            new_notes = existing.get('notes', '')
        
        success = pm.update_credential(site, new_username, new_password, new_notes)
        if success:
            print("✅ Credential updated successfully!")
        else:
            print("❌ Failed to update credential.")
    
    except Exception as e:
        print(f"❌ Error updating credential: {e}")

def delete_credential(pm):
    """Delete a credential with confirmation"""
    print("\n🗑️  Delete Credential")
    print("-" * 25)
    
    site = input("Enter site/service name to delete: ").strip()
    if not site:
        print("❌ Site name cannot be empty!")
        return
    
    try:
        existing = pm.get_credential(site)
        if not existing:
            print(f"❌ No credential found for '{site}'")
            return
        
        print(f"\n⚠️  You are about to delete:")
        print(f"🌐 Site: {site}")
        print(f"👤 Username: {existing['username']}")
        
        confirm = input("\nAre you sure? Type 'DELETE' to confirm: ")
        if confirm != 'DELETE':
            print("❌ Deletion cancelled.")
            return
        
        success = pm.delete_credential(site)
        if success:
            print("✅ Credential deleted successfully!")
        else:
            print("❌ Failed to delete credential.")
    
    except Exception as e:
        print(f"❌ Error deleting credential: {e}")

def change_master_password(pm):
    """Change the master password"""
    print("\n🔐 Change Master Password")
    print("-" * 30)
    
    current_password = get_master_password("Enter current master password: ")
    if not current_password:
        return
    
    # Verify current password
    if not pm.verify_master_password(current_password):
        print("❌ Current master password is incorrect!")
        return
    
    new_password = get_master_password("Enter new master password: ")
    if not new_password:
        return
    
    # Validate new password strength
    is_strong, message = validate_password_strength(new_password)
    if not is_strong:
        print(f"⚠️  Warning: {message}")
        confirm = input("Continue anyway? (y/N): ").lower()
        if confirm != 'y':
            print("❌ Password change cancelled.")
            return
    
    confirm_password = get_master_password("Confirm new master password: ")
    if new_password != confirm_password:
        print("❌ Passwords do not match!")
        return
    
    try:
        success = pm.change_master_password(current_password, new_password)
        if success:
            print("✅ Master password changed successfully!")
        else:
            print("❌ Failed to change master password.")
    except Exception as e:
        print(f"❌ Error changing master password: {e}")

def export_credentials(pm):
    """Export credentials to an encrypted backup file"""
    print("\n💾 Export Credentials")
    print("-" * 25)
    
    filename = input("Enter backup filename (without extension): ").strip()
    if not filename:
        filename = f"password_backup_{CryptoUtils.get_timestamp()}"
    
    filename += ".encrypted"
    
    try:
        success = pm.export_credentials(filename)
        if success:
            print(f"✅ Credentials exported to '{filename}'")
        else:
            print("❌ Failed to export credentials.")
    except Exception as e:
        print(f"❌ Error exporting credentials: {e}")

def main():
    """Main application loop"""
    clear_screen()
    print("🔐 Welcome to Secure Password Manager!")
    print("=" * 50)
    
    # Initialize password manager
    pm = PasswordManager()
    
    # Check if this is first run
    if pm.is_first_run():
        print("\n🎉 First time setup!")
        print("Please create a master password to secure your credentials.")
        
        while True:
            master_password = get_master_password("Create master password: ")
            if not master_password:
                continue
            
            # Validate password strength
            is_strong, message = validate_password_strength(master_password)
            if not is_strong:
                print(f"❌ {message}")
                continue
            
            confirm_password = get_master_password("Confirm master password: ")
            if master_password != confirm_password:
                print("❌ Passwords do not match!")
                continue
            
            try:
                pm.initialize_master_password(master_password)
                print("✅ Master password set successfully!")
                break
            except Exception as e:
                print(f"❌ Error setting up master password: {e}")
                sys.exit(1)
    
    # Authentication loop
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        master_password = get_master_password()
        if not master_password:
            attempts += 1
            continue
        
        try:
            if pm.authenticate(master_password):
                print("✅ Authentication successful!")
                break
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"❌ Invalid master password! {remaining} attempts remaining.")
                else:
                    print("❌ Maximum attempts exceeded. Access denied!")
                    sys.exit(1)
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            sys.exit(1)
    
    # Main application loop
    while True:
        try:
            display_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                add_credential(pm)
            elif choice == '2':
                view_all_credentials(pm)
            elif choice == '3':
                search_credential(pm)
            elif choice == '4':
                update_credential(pm)
            elif choice == '5':
                delete_credential(pm)
            elif choice == '6':
                change_master_password(pm)
            elif choice == '7':
                export_credentials(pm)
            elif choice == '8':
                print("\n👋 Thank you for using Secure Password Manager!")
                print("Your credentials are safely encrypted and stored.")
                sys.exit(0)
            else:
                print("❌ Invalid choice! Please select 1-8.")
            
            input("\nPress Enter to continue...")
            clear_screen()
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
