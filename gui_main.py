#!/usr/bin/env python3
"""
GUI Password Manager - Secure password manager with graphical interface
Uses tkinter for GUI and maintains all security features from CLI version
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import os
from password_manager import PasswordManager
from crypto_utils import CryptoUtils


class PasswordManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 Secure Password Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Initialize password manager
        self.password_manager = None
        self.is_authenticated = False
        
        # Style configuration
        self.setup_styles()
        
        # Start with authentication screen
        self.show_auth_screen()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_modern_entry(self, parent, **kwargs):
        """Create a modern styled entry widget"""
        entry = tk.Entry(parent, 
                        font=('Segoe UI', 12), 
                        relief='flat',
                        bd=2,
                        bg='#ffffff',
                        fg='#2c3e50',
                        insertbackground='#2c3e50',
                        highlightthickness=2,
                        highlightcolor=self.colors['accent'] if hasattr(self, 'colors') else '#e94560',
                        highlightbackground='#d3d3d3',
                        **kwargs)
        entry.configure(width=25)
        return entry
        
    def setup_styles(self):
        """Configure modern ttk styles for better appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color scheme
        bg_primary = '#1a1a2e'      # Dark blue background
        bg_secondary = '#16213e'     # Slightly lighter blue
        bg_card = '#0f3460'          # Card background
        accent_color = '#e94560'     # Red accent
        text_primary = '#ffffff'     # White text
        text_secondary = '#a8a8a8'   # Gray text
        success_color = '#27ae60'    # Green
        
        # Configure modern styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       background=bg_primary, 
                       foreground=text_primary)
                       
        style.configure('Subtitle.TLabel', 
                       font=('Segoe UI', 14), 
                       background=bg_primary, 
                       foreground=text_secondary)
                       
        style.configure('Heading.TLabel', 
                       font=('Segoe UI', 16, 'bold'), 
                       background=bg_primary, 
                       foreground=text_primary)
                       
        style.configure('Custom.TLabel', 
                       font=('Segoe UI', 11), 
                       background=bg_primary, 
                       foreground=text_primary)
                       
        style.configure('Custom.TFrame', 
                       background=bg_primary)
                       
        style.configure('Card.TFrame', 
                       background=bg_card,
                       relief='flat',
                       borderwidth=1)
                       
        # Modern button styles
        style.configure('Primary.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       background=accent_color,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
                       
        style.map('Primary.TButton',
                 background=[('active', '#d63447'),
                            ('pressed', '#c23147')])
                            
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 10),
                       background=bg_secondary,
                       foreground=text_primary,
                       borderwidth=1,
                       focuscolor='none',
                       padding=(15, 8))
                       
        style.map('Secondary.TButton',
                 background=[('active', bg_card),
                            ('pressed', bg_card)])
                            
        style.configure('Success.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       background=success_color,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
                       
        # Notebook styles
        style.configure('Custom.TNotebook', 
                       background=bg_primary,
                       borderwidth=0)
                       
        style.configure('Custom.TNotebook.Tab',
                       font=('Segoe UI', 11),
                       background=bg_secondary,
                       foreground=text_primary,
                       padding=(20, 12),
                       borderwidth=0)
                       
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', bg_card),
                            ('active', bg_card)],
                 foreground=[('selected', text_primary),
                            ('active', text_primary)])
                            
        # Treeview styles
        style.configure('Custom.Treeview',
                       font=('Segoe UI', 10),
                       background='#ffffff',
                       foreground='#2c3e50',
                       fieldbackground='#ffffff',
                       borderwidth=0,
                       rowheight=30)
                       
        style.configure('Custom.Treeview.Heading',
                       font=('Segoe UI', 11, 'bold'),
                       background=bg_card,
                       foreground=text_primary,
                       borderwidth=0,
                       relief='flat')
                       
        # Store colors for custom widgets
        self.colors = {
            'bg_primary': bg_primary,
            'bg_secondary': bg_secondary,
            'bg_card': bg_card,
            'accent': accent_color,
            'text_primary': text_primary,
            'text_secondary': text_secondary,
            'success': success_color
        }
        
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def show_auth_screen(self):
        """Show modern authentication/setup screen"""
        self.clear_window()
        
        # Create gradient-like background effect
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(expand=True, fill='both')
        
        # Create a centered container
        container = ttk.Frame(main_frame, style='Custom.TFrame')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # App title with icon
        title_frame = ttk.Frame(container, style='Custom.TFrame')
        title_frame.pack(pady=(0, 40))
        
        title_label = ttk.Label(title_frame, text="🔐", style='Title.TLabel')
        title_label.pack()
        
        app_name = ttk.Label(title_frame, text="Secure Password Manager", style='Title.TLabel')
        app_name.pack(pady=(10, 0))
        
        subtitle = ttk.Label(title_frame, text="Your digital vault for secure credential storage", style='Subtitle.TLabel')
        subtitle.pack(pady=(5, 0))
        
        # Check if this is first time setup
        if not os.path.exists('.master_hash'):
            self.show_setup_screen(container)
        else:
            self.show_login_screen(container)
            
    def show_setup_screen(self, parent):
        """Show modern first-time setup screen"""
        # Setup card
        setup_card = ttk.Frame(parent, style='Card.TFrame')
        setup_card.pack(pady=30, padx=40, ipadx=40, ipady=30)
        
        # Setup header
        header_frame = ttk.Frame(setup_card, style='Card.TFrame')
        header_frame.pack(pady=(0, 30))
        
        setup_icon = ttk.Label(header_frame, text="🎉", style='Title.TLabel')
        setup_icon.pack()
        
        setup_title = ttk.Label(header_frame, text="Welcome!", style='Heading.TLabel')
        setup_title.pack(pady=(10, 5))
        
        setup_desc = ttk.Label(header_frame, text="Create a master password to secure your digital vault", style='Custom.TLabel')
        setup_desc.pack()
        
        # Form container
        form_frame = ttk.Frame(setup_card, style='Card.TFrame')
        form_frame.pack(fill='x', padx=20)
        
        # Master password input
        ttk.Label(form_frame, text="Master Password", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        self.master_password_entry = self.create_modern_entry(form_frame, show='*')
        self.master_password_entry.pack(fill='x', pady=(0, 15))
        
        # Confirm password input
        ttk.Label(form_frame, text="Confirm Password", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        self.confirm_password_entry = self.create_modern_entry(form_frame, show='*')
        self.confirm_password_entry.pack(fill='x', pady=(0, 20))
        
        # Security note
        security_note = ttk.Label(form_frame, 
                                 text="💡 Use a strong password with uppercase, lowercase, numbers, and symbols", 
                                 style='Subtitle.TLabel')
        security_note.pack(pady=(0, 25))
        
        # Create button
        create_button = ttk.Button(form_frame, text="Create Master Password", 
                                 command=self.create_master_password, style='Primary.TButton')
        create_button.pack(pady=10)
        
        # Bind Enter key
        self.master_password_entry.bind('<Return>', lambda e: self.confirm_password_entry.focus())
        self.confirm_password_entry.bind('<Return>', lambda e: self.create_master_password())
        
        # Focus on first entry
        self.master_password_entry.focus()
        
    def show_login_screen(self, parent):
        """Show modern login screen"""
        # Login card
        login_card = ttk.Frame(parent, style='Card.TFrame')
        login_card.pack(pady=30, padx=40, ipadx=40, ipady=30)
        
        # Login header
        header_frame = ttk.Frame(login_card, style='Card.TFrame')
        header_frame.pack(pady=(0, 30))
        
        welcome_icon = ttk.Label(header_frame, text="👋", style='Title.TLabel')
        welcome_icon.pack()
        
        welcome_title = ttk.Label(header_frame, text="Welcome Back!", style='Heading.TLabel')
        welcome_title.pack(pady=(10, 5))
        
        welcome_desc = ttk.Label(header_frame, text="Enter your master password to unlock your vault", style='Custom.TLabel')
        welcome_desc.pack()
        
        # Form container
        form_frame = ttk.Frame(login_card, style='Card.TFrame')
        form_frame.pack(fill='x', padx=20)
        
        # Master password input
        ttk.Label(form_frame, text="Master Password", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        self.master_password_entry = self.create_modern_entry(form_frame, show='*')
        self.master_password_entry.pack(fill='x', pady=(0, 25))
        
        # Login button
        login_button = ttk.Button(form_frame, text="Unlock Vault", 
                                command=self.authenticate, style='Primary.TButton')
        login_button.pack(pady=10)
        
        # Bind Enter key
        self.master_password_entry.bind('<Return>', lambda e: self.authenticate())
        
        # Focus on entry
        self.master_password_entry.focus()
        
    def create_master_password(self):
        """Create master password for first-time setup"""
        password = self.master_password_entry.get()
        confirm = self.confirm_password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter a master password")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        # Validate password strength
        if not self.validate_password_strength(password):
            return
            
        try:
            # Initialize password manager and set up master password
            self.password_manager = PasswordManager()
            self.password_manager.initialize_master_password(password)
            self.is_authenticated = True
            messagebox.showinfo("Success", "Master password created successfully!")
            self.show_main_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create master password: {str(e)}")
            
    def authenticate(self):
        """Authenticate user with master password"""
        password = self.master_password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter your master password")
            return
            
        try:
            self.password_manager = PasswordManager()
            if self.password_manager.authenticate(password):
                self.is_authenticated = True
                messagebox.showinfo("Success", "Authentication successful!")
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Invalid master password")
                self.master_password_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {str(e)}")
            
    def validate_password_strength(self, password):
        """Validate password strength"""
        if len(password) < 8:
            messagebox.showerror("Weak Password", "Password must be at least 8 characters long")
            return False
            
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            messagebox.showwarning("Weak Password", 
                "Password should contain:\n" +
                "- At least one uppercase letter\n" +
                "- At least one lowercase letter\n" +
                "- At least one number\n" +
                "- At least one special character")
            return True  # Allow weak passwords but warn user
            
        return True
        
    def show_main_screen(self):
        """Show modern main application screen"""
        self.clear_window()
        
        # Create main container
        main_container = ttk.Frame(self.root, style='Custom.TFrame')
        main_container.pack(fill='both', expand=True)
        
        # Header section
        header_frame = ttk.Frame(main_container, style='Custom.TFrame')
        header_frame.pack(fill='x', padx=20, pady=20)
        
        # Left side of header
        header_left = ttk.Frame(header_frame, style='Custom.TFrame')
        header_left.pack(side='left', fill='x', expand=True)
        
        title_label = ttk.Label(header_left, text="🔐 Your Digital Vault", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_left, text="Manage your passwords securely", style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Right side of header - user actions
        header_right = ttk.Frame(header_frame, style='Custom.TFrame')
        header_right.pack(side='right')
        
        logout_button = ttk.Button(header_right, text="Logout", command=self.logout, style='Secondary.TButton')
        logout_button.pack(side='right', padx=(10, 0))
        
        # Separator line
        separator = ttk.Frame(main_container, height=2, style='Custom.TFrame')
        separator.pack(fill='x', padx=20)
        
        # Content area
        content_frame = ttk.Frame(main_container, style='Custom.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create modern notebook
        notebook = ttk.Notebook(content_frame, style='Custom.TNotebook')
        notebook.pack(fill='both', expand=True)
        
        # Create tab frames with modern styling
        self.credentials_frame = ttk.Frame(notebook, style='Custom.TFrame')
        notebook.add(self.credentials_frame, text="🗂️  All Credentials")
        
        self.add_frame = ttk.Frame(notebook, style='Custom.TFrame')
        notebook.add(self.add_frame, text="➕  Add New")
        
        self.settings_frame = ttk.Frame(notebook, style='Custom.TFrame')
        notebook.add(self.settings_frame, text="⚙️  Settings")
        
        # Setup tabs with modern design
        self.setup_credentials_tab()
        self.setup_add_tab()
        self.setup_settings_tab()
        
        # Load credentials
        self.refresh_credentials()
        
    def setup_credentials_tab(self):
        """Setup the modern credentials viewing tab"""
        # Main content area
        content_frame = ttk.Frame(self.credentials_frame, style='Custom.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Search section
        search_card = ttk.Frame(content_frame, style='Card.TFrame')
        search_card.pack(fill='x', pady=(0, 20), ipadx=20, ipady=15)
        
        search_header = ttk.Label(search_card, text="🔍 Search Credentials", style='Heading.TLabel')
        search_header.pack(anchor='w', pady=(0, 10))
        
        search_input_frame = ttk.Frame(search_card, style='Card.TFrame')
        search_input_frame.pack(fill='x')
        
        self.search_entry = self.create_modern_entry(search_input_frame)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_credentials())
        
        search_button = ttk.Button(search_input_frame, text="Search", command=self.search_credentials, style='Secondary.TButton')
        search_button.pack(side='left', padx=(0, 5))
        
        refresh_button = ttk.Button(search_input_frame, text="Refresh", command=self.refresh_credentials, style='Secondary.TButton')
        refresh_button.pack(side='left')
        
        # Credentials list section
        list_card = ttk.Frame(content_frame, style='Card.TFrame')
        list_card.pack(fill='both', expand=True, ipadx=20, ipady=15)
        
        list_header = ttk.Label(list_card, text="📋 Your Credentials", style='Heading.TLabel')
        list_header.pack(anchor='w', pady=(0, 15))
        
        # Treeview with modern styling
        tree_container = ttk.Frame(list_card, style='Card.TFrame')
        tree_container.pack(fill='both', expand=True, pady=(0, 15))
        
        self.tree = ttk.Treeview(tree_container, 
                                columns=('service', 'username', 'url'), 
                                show='headings',
                                style='Custom.Treeview')
        
        # Configure columns
        self.tree.heading('service', text='Service')
        self.tree.heading('username', text='Username/Email')
        self.tree.heading('url', text='Website/URL')
        
        self.tree.column('service', width=200, minwidth=150)
        self.tree.column('username', width=250, minwidth=200)
        self.tree.column('url', width=300, minwidth=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons
        buttons_frame = ttk.Frame(list_card, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        
        # Left side buttons (primary actions)
        left_buttons = ttk.Frame(buttons_frame, style='Card.TFrame')
        left_buttons.pack(side='left', fill='x', expand=True)
        
        view_button = ttk.Button(left_buttons, text="👁️ View", command=self.view_password, style='Primary.TButton')
        view_button.pack(side='left', padx=(0, 10))
        
        copy_button = ttk.Button(left_buttons, text="📋 Copy Password", command=self.copy_password, style='Success.TButton')
        copy_button.pack(side='left', padx=(0, 10))
        
        # Right side buttons (secondary actions)
        right_buttons = ttk.Frame(buttons_frame, style='Card.TFrame')
        right_buttons.pack(side='right')
        
        edit_button = ttk.Button(right_buttons, text="✏️ Edit", command=self.edit_credential, style='Secondary.TButton')
        edit_button.pack(side='right', padx=(10, 0))
        
        delete_button = ttk.Button(right_buttons, text="🗑️ Delete", command=self.delete_credential, style='Secondary.TButton')
        delete_button.pack(side='right', padx=(10, 0))
        
    def setup_add_tab(self):
        """Setup the modern add credential tab"""
        # Main content area
        content_frame = ttk.Frame(self.add_frame, style='Custom.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Form card
        form_card = ttk.Frame(content_frame, style='Card.TFrame')
        form_card.pack(fill='x', pady=(0, 20), ipadx=30, ipady=25)
        
        # Header
        header_frame = ttk.Frame(form_card, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 25))
        
        add_icon = ttk.Label(header_frame, text="➕", style='Title.TLabel')
        add_icon.pack()
        
        add_title = ttk.Label(header_frame, text="Add New Credential", style='Heading.TLabel')
        add_title.pack(pady=(10, 5))
        
        add_desc = ttk.Label(header_frame, text="Store a new password securely in your vault", style='Custom.TLabel')
        add_desc.pack()
        
        # Form fields
        fields_frame = ttk.Frame(form_card, style='Card.TFrame')
        fields_frame.pack(fill='x', padx=20)
        
        # Service field
        ttk.Label(fields_frame, text="Service/Website *", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        self.service_entry = self.create_modern_entry(fields_frame)
        self.service_entry.pack(fill='x', pady=(0, 15))
        
        # Username field
        ttk.Label(fields_frame, text="Username/Email *", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        self.username_entry = self.create_modern_entry(fields_frame)
        self.username_entry.pack(fill='x', pady=(0, 15))
        
        # Password field with generator
        password_frame = ttk.Frame(fields_frame, style='Card.TFrame')
        password_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(password_frame, text="Password *", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        
        password_input_frame = ttk.Frame(password_frame, style='Card.TFrame')
        password_input_frame.pack(fill='x')
        
        self.password_entry = self.create_modern_entry(password_input_frame, show='*')
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        generate_button = ttk.Button(password_input_frame, text="🎲 Generate", 
                                   command=self.generate_password, style='Secondary.TButton')
        generate_button.pack(side='right')
        
        # URL field
        ttk.Label(fields_frame, text="Website URL (optional)", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        self.url_entry = self.create_modern_entry(fields_frame)
        self.url_entry.pack(fill='x', pady=(0, 15))
        
        # Notes field
        ttk.Label(fields_frame, text="Notes (optional)", style='Custom.TLabel').pack(anchor='w', pady=(0, 5))
        self.notes_text = tk.Text(fields_frame, 
                                 font=('Segoe UI', 11), 
                                 height=4,
                                 relief='flat',
                                 bd=2,
                                 bg='#ffffff',
                                 fg='#2c3e50',
                                 insertbackground='#2c3e50',
                                 highlightthickness=2,
                                 highlightcolor=self.colors['accent'],
                                 highlightbackground='#d3d3d3')
        self.notes_text.pack(fill='x', pady=(0, 25))
        
        # Action buttons
        buttons_frame = ttk.Frame(fields_frame, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        
        # Required fields note
        required_note = ttk.Label(buttons_frame, text="* Required fields", style='Subtitle.TLabel')
        required_note.pack(side='left')
        
        # Add button
        add_button = ttk.Button(buttons_frame, text="💾 Save Credential", 
                              command=self.add_credential, style='Primary.TButton')
        add_button.pack(side='right')
        
    def setup_settings_tab(self):
        """Setup the modern settings tab"""
        # Main content area
        content_frame = ttk.Frame(self.settings_frame, style='Custom.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Security settings card
        security_card = ttk.Frame(content_frame, style='Card.TFrame')
        security_card.pack(fill='x', pady=(0, 20), ipadx=30, ipady=25)
        
        security_header = ttk.Frame(security_card, style='Card.TFrame')
        security_header.pack(fill='x', pady=(0, 20))
        
        security_icon = ttk.Label(security_header, text="🔒", style='Title.TLabel')
        security_icon.pack()
        
        security_title = ttk.Label(security_header, text="Security Settings", style='Heading.TLabel')
        security_title.pack(pady=(10, 5))
        
        security_desc = ttk.Label(security_header, text="Manage your master password and security preferences", style='Custom.TLabel')
        security_desc.pack()
        
        # Security options
        security_options = ttk.Frame(security_card, style='Card.TFrame')
        security_options.pack(fill='x', padx=20)
        
        change_password_button = ttk.Button(security_options, text="🔑 Change Master Password", 
                                          command=self.change_master_password, style='Primary.TButton')
        change_password_button.pack(pady=10)
        
        # Data management card
        data_card = ttk.Frame(content_frame, style='Card.TFrame')
        data_card.pack(fill='x', pady=(0, 20), ipadx=30, ipady=25)
        
        data_header = ttk.Frame(data_card, style='Card.TFrame')
        data_header.pack(fill='x', pady=(0, 20))
        
        data_icon = ttk.Label(data_header, text="💾", style='Title.TLabel')
        data_icon.pack()
        
        data_title = ttk.Label(data_header, text="Data Management", style='Heading.TLabel')
        data_title.pack(pady=(10, 5))
        
        data_desc = ttk.Label(data_header, text="Export and backup your encrypted credentials", style='Custom.TLabel')
        data_desc.pack()
        
        # Data options
        data_options = ttk.Frame(data_card, style='Card.TFrame')
        data_options.pack(fill='x', padx=20)
        
        export_button = ttk.Button(data_options, text="📤 Export Credentials", 
                                 command=self.export_credentials, style='Success.TButton')
        export_button.pack(pady=10)
        
        export_note = ttk.Label(data_options, 
                              text="💡 Exported files are encrypted with your master password", 
                              style='Subtitle.TLabel')
        export_note.pack(pady=(10, 0))
        
    def refresh_credentials(self):
        """Refresh the credentials list"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load credentials
        if not self.password_manager:
            return
            
        try:
            credentials = self.password_manager.get_all_credentials()
            for service, data in credentials.items():
                # Extract URL from notes if it exists
                url = ""
                notes = data.get('notes', '')
                if notes and notes.startswith("URL: "):
                    lines = notes.split('\n', 1)
                    url = lines[0][5:]  # Remove "URL: " prefix
                    
                self.tree.insert('', 'end', values=(service, data.get('username', ''), url))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load credentials: {str(e)}")
            
    def search_credentials(self):
        """Search for credentials"""
        if not self.password_manager:
            return
            
        search_term = self.search_entry.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            credentials = self.password_manager.get_all_credentials()
            for service, data in credentials.items():
                # Extract URL from notes for search
                url = ""
                notes = data.get('notes', '')
                if notes and notes.startswith("URL: "):
                    lines = notes.split('\n', 1)
                    url = lines[0][5:]
                    
                if (search_term in service.lower() or 
                    search_term in data.get('username', '').lower() or
                    search_term in url.lower()):
                    self.tree.insert('', 'end', values=(service, data.get('username', ''), url))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
            
    def view_password(self):
        """View password for selected credential"""
        if not self.password_manager:
            return
            
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a credential to view")
            return
            
        item = self.tree.item(selection[0])
        service = item['values'][0]
        
        try:
            credential = self.password_manager.get_credential(service)
            if credential:
                # Show password in a dialog
                password_dialog = tk.Toplevel(self.root)
                password_dialog.title(f"Password for {service}")
                password_dialog.geometry("400x200")
                password_dialog.configure(bg='#2c3e50')
                
                ttk.Label(password_dialog, text=f"Service: {service}", style='Custom.TLabel').pack(pady=10)
                ttk.Label(password_dialog, text=f"Username: {credential.get('username', '')}", style='Custom.TLabel').pack(pady=5)
                
                password_frame = ttk.Frame(password_dialog, style='Custom.TFrame')
                password_frame.pack(pady=10)
                
                ttk.Label(password_frame, text="Password:", style='Custom.TLabel').pack(side='left')
                password_entry = tk.Entry(password_frame, font=('Arial', 12), width=20)
                password_entry.insert(0, credential['password'])
                password_entry.config(state='readonly')
                password_entry.pack(side='left', padx=(5, 0))
                
                close_button = ttk.Button(password_dialog, text="Close", command=password_dialog.destroy)
                close_button.pack(pady=10)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve password: {str(e)}")
            
    def copy_password(self):
        """Copy password to clipboard"""
        if not self.password_manager:
            return
            
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a credential to copy")
            return
            
        item = self.tree.item(selection[0])
        service = item['values'][0]
        
        try:
            credential = self.password_manager.get_credential(service)
            if credential:
                self.root.clipboard_clear()
                self.root.clipboard_append(credential['password'])
                messagebox.showinfo("Success", "Password copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy password: {str(e)}")
            
    def generate_password(self):
        """Generate a strong password"""
        try:
            crypto_utils = CryptoUtils()
            password = crypto_utils.generate_secure_password()
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
            
    def add_credential(self):
        """Add a new credential"""
        if not self.password_manager:
            return
            
        service = self.service_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        url = self.url_entry.get().strip()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        if not service or not username or not password:
            messagebox.showerror("Error", "Service, username, and password are required")
            return
            
        try:
            # Combine URL and notes into notes field since API expects only 4 parameters
            notes_combined = notes
            if url:
                notes_combined = f"URL: {url}\n{notes}" if notes else f"URL: {url}"
                
            self.password_manager.add_credential(service, username, password, notes_combined)
            messagebox.showinfo("Success", "Credential added successfully!")
            
            # Clear form
            self.service_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.url_entry.delete(0, tk.END)
            self.notes_text.delete(1.0, tk.END)
            
            # Refresh credentials list
            self.refresh_credentials()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add credential: {str(e)}")
            
    def edit_credential(self):
        """Edit selected credential"""
        if not self.password_manager:
            return
            
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a credential to edit")
            return
            
        item = self.tree.item(selection[0])
        service = item['values'][0]
        
        try:
            credential = self.password_manager.get_credential(service)
            if not credential:
                messagebox.showerror("Error", "Credential not found")
                return
                
            # Create edit dialog
            edit_dialog = tk.Toplevel(self.root)
            edit_dialog.title(f"Edit {service}")
            edit_dialog.geometry("400x300")
            edit_dialog.configure(bg='#2c3e50')
            
            # Form fields
            ttk.Label(edit_dialog, text="Username/Email:", style='Custom.TLabel').pack(pady=5)
            username_entry = tk.Entry(edit_dialog, font=('Arial', 10), width=30)
            username_entry.insert(0, credential.get('username', ''))
            username_entry.pack(pady=5)
            
            ttk.Label(edit_dialog, text="Password:", style='Custom.TLabel').pack(pady=5)
            password_entry = tk.Entry(edit_dialog, show='*', font=('Arial', 10), width=30)
            password_entry.insert(0, credential.get('password', ''))
            password_entry.pack(pady=5)
            
            ttk.Label(edit_dialog, text="URL:", style='Custom.TLabel').pack(pady=5)
            url_entry = tk.Entry(edit_dialog, font=('Arial', 10), width=30)
            url_entry.insert(0, credential.get('url', ''))
            url_entry.pack(pady=5)
            
            ttk.Label(edit_dialog, text="Notes:", style='Custom.TLabel').pack(pady=5)
            notes_text = tk.Text(edit_dialog, font=('Arial', 10), width=30, height=3)
            notes_text.insert(1.0, credential.get('notes', ''))
            notes_text.pack(pady=5)
            
            def save_changes():
                new_username = username_entry.get().strip()
                new_password = password_entry.get()
                new_url = url_entry.get().strip()
                new_notes = notes_text.get(1.0, tk.END).strip()
                
                if not new_username or not new_password:
                    messagebox.showerror("Error", "Username and password are required")
                    return
                    
                if not self.password_manager:
                    messagebox.showerror("Error", "Not authenticated")
                    return
                    
                try:
                    # Combine URL and notes like in add_credential
                    notes_combined = new_notes
                    if new_url:
                        notes_combined = f"URL: {new_url}\n{new_notes}" if new_notes else f"URL: {new_url}"
                    
                    self.password_manager.update_credential(service, username=new_username, password=new_password, notes=notes_combined)
                    messagebox.showinfo("Success", "Credential updated successfully!")
                    edit_dialog.destroy()
                    self.refresh_credentials()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update credential: {str(e)}")
                    
            save_button = ttk.Button(edit_dialog, text="Save Changes", command=save_changes)
            save_button.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load credential: {str(e)}")
            
    def delete_credential(self):
        """Delete selected credential"""
        if not self.password_manager:
            return
            
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a credential to delete")
            return
            
        item = self.tree.item(selection[0])
        service = item['values'][0]
        
        result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the credential for '{service}'?")
        if result:
            try:
                self.password_manager.delete_credential(service)
                messagebox.showinfo("Success", "Credential deleted successfully!")
                self.refresh_credentials()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete credential: {str(e)}")
                
    def change_master_password(self):
        """Change master password"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Master Password")
        dialog.geometry("300x200")
        dialog.configure(bg='#2c3e50')
        
        ttk.Label(dialog, text="Current Password:", style='Custom.TLabel').pack(pady=5)
        current_entry = tk.Entry(dialog, show='*', font=('Arial', 10), width=25)
        current_entry.pack(pady=5)
        
        ttk.Label(dialog, text="New Password:", style='Custom.TLabel').pack(pady=5)
        new_entry = tk.Entry(dialog, show='*', font=('Arial', 10), width=25)
        new_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Confirm New Password:", style='Custom.TLabel').pack(pady=5)
        confirm_entry = tk.Entry(dialog, show='*', font=('Arial', 10), width=25)
        confirm_entry.pack(pady=5)
        
        def change_password():
            current = current_entry.get()
            new_password = new_entry.get()
            confirm = confirm_entry.get()
            
            if not current or not new_password:
                messagebox.showerror("Error", "All fields are required")
                return
                
            if new_password != confirm:
                messagebox.showerror("Error", "New passwords do not match")
                return
                
            if not self.validate_password_strength(new_password):
                return
                
            if not self.password_manager:
                messagebox.showerror("Error", "Not authenticated")
                return
                
            try:
                self.password_manager.change_master_password(current, new_password)
                messagebox.showinfo("Success", "Master password changed successfully!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password: {str(e)}")
                
        change_button = ttk.Button(dialog, text="Change Password", command=change_password)
        change_button.pack(pady=10)
        
    def export_credentials(self):
        """Export credentials to encrypted file"""
        if not self.password_manager:
            messagebox.showerror("Error", "Not authenticated")
            return
            
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            title="Export Credentials",
            defaultextension=".json.encrypted",
            filetypes=[("Encrypted files", "*.json.encrypted"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.password_manager.export_credentials(filename)
                messagebox.showinfo("Success", f"Credentials exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export credentials: {str(e)}")
                
    def logout(self):
        """Logout and return to authentication screen"""
        self.password_manager = None
        self.is_authenticated = False
        self.show_auth_screen()
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = PasswordManagerGUI()
    app.run()