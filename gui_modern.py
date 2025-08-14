#!/usr/bin/env python3
"""
Futuristic Password Manager - Ultra Modern Aesthetic GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
import string
import math
import time
from password_manager import PasswordManager


class FuturisticButton(tk.Frame):
    """Futuristic button with neon glow effects"""
    
    def __init__(self, parent, text, command=None, style="primary", size="normal", **kwargs):
        super().__init__(parent, bg=parent.cget('bg'))
        
        self.command = command
        self.is_hovered = False
        self.animation_id = None
        
        # Futuristic color schemes
        styles = {
            "primary": {"bg": "#0F172A", "hover": "#1E293B", "accent": "#00D4FF", "text": "white"},
            "success": {"bg": "#064E3B", "hover": "#065F46", "accent": "#10F2C5", "text": "white"},
            "warning": {"bg": "#451A03", "hover": "#78350F", "accent": "#FFC107", "text": "white"},
            "danger": {"bg": "#450A0A", "hover": "#7F1D1D", "accent": "#FF073A", "text": "white"},
            "ghost": {"bg": "#111827", "hover": "#1F2937", "accent": "#6366F1", "text": "#E5E7EB"},
            "neon": {"bg": "#000000", "hover": "#111111", "accent": "#00FF41", "text": "#00FF41"}
        }
        
        sizes = {
            "small": {"font": ("Consolas", 10, "bold"), "padx": 20, "pady": 10},
            "normal": {"font": ("Consolas", 11, "bold"), "padx": 28, "pady": 14},
            "large": {"font": ("Consolas", 12, "bold"), "padx": 36, "pady": 18}
        }
        
        self.style_config = styles.get(style, styles["primary"])
        self.size_config = sizes.get(size, sizes["normal"])
        
        # Outer glow frame
        self.glow_frame = tk.Frame(
            self,
            bg=self.style_config["accent"],
            relief="flat",
            bd=0
        )
        self.glow_frame.pack(padx=2, pady=2)
        
        # Main button
        self.button = tk.Label(
            self.glow_frame,
            text=text,
            font=self.size_config["font"],
            bg=self.style_config["bg"],
            fg=self.style_config["text"],
            cursor="hand2",
            padx=self.size_config["padx"],
            pady=self.size_config["pady"],
            relief="flat",
            bd=0
        )
        self.button.pack(padx=1, pady=1)
        
        # Initially hide glow
        self.glow_frame.configure(bg=self.style_config["bg"])
        
        # Bind events
        self.button.bind("<Button-1>", self._on_click)
        self.button.bind("<Enter>", self._on_enter)
        self.button.bind("<Leave>", self._on_leave)
        
    def _on_click(self, event):
        if self.command:
            # Pulse animation
            self._pulse_animation()
            self.command()
            
    def _on_enter(self, event):
        self.is_hovered = True
        self.button.configure(bg=self.style_config["hover"])
        self._start_glow()
        
    def _on_leave(self, event):
        self.is_hovered = False
        self.button.configure(bg=self.style_config["bg"])
        self._stop_glow()
        
    def _start_glow(self):
        self.glow_frame.configure(bg=self.style_config["accent"])
        
    def _stop_glow(self):
        self.glow_frame.configure(bg=self.style_config["bg"])
        
    def _pulse_animation(self):
        # Quick pulse effect
        original_bg = self.button.cget("bg")
        self.button.configure(bg=self.style_config["accent"])
        self.after(150, lambda: self.button.configure(bg=original_bg))


class CyberInput(tk.Frame):
    """Futuristic cyber-styled input field"""
    
    def __init__(self, parent, label="", placeholder="", is_password=False, **kwargs):
        super().__init__(parent, bg=parent.cget('bg'))
        
        self.label_text = label
        self.placeholder_text = placeholder
        self.is_password = is_password
        
        # Label with neon accent
        label_frame = tk.Frame(self, bg=parent.cget('bg'))
        label_frame.pack(fill="x", pady=(0, 6))
        
        self.label = tk.Label(
            label_frame,
            text=f"▶ {label}",
            font=("Consolas", 10, "bold"),
            bg=parent.cget('bg'),
            fg="#00D4FF",
            anchor="w"
        )
        self.label.pack(side="left")
        
        # Cyber line decoration
        self.cyber_line = tk.Frame(label_frame, bg="#00D4FF", height=1)
        self.cyber_line.pack(side="right", fill="x", expand=True, padx=(10, 0), pady=(6, 0))
        
        # Input container with border effects
        self.container = tk.Frame(
            self,
            bg="#0F172A",
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor="#00D4FF",
            highlightbackground="#334155"
        )
        self.container.pack(fill="x", ipady=4)
        
        # Entry widget
        entry_config = {
            "font": ("Consolas", 12),
            "bg": "#0F172A",
            "fg": "#E2E8F0",
            "relief": "flat",
            "bd": 0,
            "insertbackground": "#00D4FF"
        }
        
        if is_password:
            entry_config["show"] = "●"
            
        self.entry = tk.Entry(self.container, **entry_config)
        self.entry.pack(fill="x", padx=16, pady=8)
        
        # Set placeholder
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.configure(fg="#64748B")
            
        # Bind events
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyPress>", self._on_key_press)
        
    def _on_focus_in(self, event):
        self.container.configure(highlightbackground="#00D4FF", highlightthickness=3)
        
        # Clear placeholder
        if self.entry.get() == self.placeholder_text:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg="#E2E8F0")
            
    def _on_focus_out(self, event):
        self.container.configure(highlightbackground="#334155", highlightthickness=2)
        
        # Restore placeholder if empty
        if not self.entry.get():
            self.entry.insert(0, self.placeholder_text)
            self.entry.configure(fg="#64748B")
            
    def _on_key_press(self, event):
        # Cyber typing effect could be added here
        pass
        
    def get(self):
        value = self.entry.get()
        return "" if value == self.placeholder_text else value
        
    def set(self, value):
        self.entry.delete(0, tk.END)
        if value:
            self.entry.insert(0, value)
            self.entry.configure(fg="#E2E8F0")
        else:
            self.entry.insert(0, self.placeholder_text)
            self.entry.configure(fg="#64748B")
            
    def clear(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder_text)
        self.entry.configure(fg="#64748B")
        
    def focus(self):
        self.entry.focus()
        
    def bind(self, sequence, func, add=None):
        return self.entry.bind(sequence, func, add)


class HolographicHeader(tk.Canvas):
    """Futuristic holographic header with animated effects"""
    
    def __init__(self, parent, height=180, **kwargs):
        super().__init__(parent, height=height, highlightthickness=0, bg="#000000", **kwargs)
        self.height = height
        self.animation_active = False
        self.bind('<Configure>', self._draw_header)
        self.after(100, self._start_animation)
        
    def _draw_header(self, event=None):
        self.delete("all")
        width = self.winfo_width()
        height = self.height
        
        if width <= 1:
            return
            
        # Cyber grid background
        self._draw_cyber_grid(width, height)
        
        # Holographic gradient
        self._draw_holographic_gradient(width, height)
        
        # Neon border lines
        self._draw_neon_borders(width, height)
        
    def _draw_cyber_grid(self, width, height):
        # Grid pattern
        grid_size = 20
        for x in range(0, width, grid_size):
            self.create_line(x, 0, x, height, fill="#1E293B", width=1)
        for y in range(0, height, grid_size):
            self.create_line(0, y, width, y, fill="#1E293B", width=1)
            
    def _draw_holographic_gradient(self, width, height):
        # Animated holographic effect
        steps = 50
        for i in range(steps):
            y1 = (height * i) // steps
            y2 = (height * (i + 1)) // steps
            
            # Color animation based on time
            t = time.time() * 2
            ratio = (i / steps + math.sin(t) * 0.1) % 1
            
            # Cyber colors: deep blue to cyan to purple
            if ratio < 0.5:
                r = int(15 + (0 - 15) * (ratio * 2))
                g = int(23 + (212 - 23) * (ratio * 2))
                b = int(42 + (255 - 42) * (ratio * 2))
            else:
                r = int(0 + (139 - 0) * ((ratio - 0.5) * 2))
                g = int(212 + (69 - 212) * ((ratio - 0.5) * 2))
                b = int(255 + (255 - 255) * ((ratio - 0.5) * 2))
                
            color = f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"
            self.create_rectangle(0, y1, width, y2, fill=color, outline="", stipple="gray50")
            
    def _draw_neon_borders(self, width, height):
        # Top and bottom neon lines
        self.create_line(0, 0, width, 0, fill="#00D4FF", width=3)
        self.create_line(0, height-1, width, height-1, fill="#00D4FF", width=3)
        
        # Corner accents
        corner_size = 20
        self.create_line(0, 0, corner_size, 0, fill="#00FF41", width=5)
        self.create_line(0, 0, 0, corner_size, fill="#00FF41", width=5)
        
    def _start_animation(self):
        if not self.animation_active:
            self.animation_active = True
            self._animate()
            
    def _animate(self):
        if self.animation_active:
            self._draw_header()
            self.after(100, self._animate)


class CyberCard(tk.Frame):
    """Futuristic card with holographic effects"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#0F172A", relief="flat", **kwargs)
        
        # Configure cyber styling
        self.configure(
            highlightbackground="#00D4FF",
            highlightthickness=1,
            bd=0
        )
        
        # Add corner decorations
        self._add_corner_decorations()
        
    def _add_corner_decorations(self):
        # Top-left corner accent
        corner1 = tk.Frame(self, bg="#00FF41", width=20, height=3)
        corner1.place(x=0, y=0)
        
        corner2 = tk.Frame(self, bg="#00FF41", width=3, height=20)
        corner2.place(x=0, y=0)


class PasswordManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_futuristic_window()
        
        # Initialize
        self.password_manager = None
        self.is_authenticated = False
        self.current_credentials = {}
        
        # Show initial screen
        self.show_cyber_auth_screen()
        
    def setup_futuristic_window(self):
        """Configure futuristic window"""
        self.root.title("◢ CYBER VAULT ◣ Password Manager")
        self.root.state('zoomed')  # Open in full screen
        self.root.configure(bg="#000000")
        self.root.resizable(True, True)
        self.root.minsize(1000, 700)
        
        # Configure ttk styles for futuristic look
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Cyber.Vertical.TScrollbar",
                       background="#0F172A",
                       troughcolor="#000000",
                       borderwidth=0,
                       arrowcolor="#00D4FF",
                       darkcolor="#1E293B",
                       lightcolor="#334155")
        
    def clear_window(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def show_cyber_auth_screen(self):
        """Show futuristic authentication screen"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(fill="both", expand=True)
        
        # Holographic header
        header = HolographicHeader(main_frame, height=200)
        header.pack(fill="x")
        
        # Logo section on header
        logo_frame = tk.Frame(header, bg="#000000")
        logo_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Cyber logo
        logo_container = tk.Frame(logo_frame, bg="#000000")
        logo_container.pack()
        
        # ASCII art style logo
        logo_lines = [
            "╔═══════════════════════════╗",
            "║    ◢█◣ CYBER VAULT ◢█◣    ║",
            "║   ◥███████████████████◤   ║",
            "║    QUANTUM SECURE v3.0    ║",
            "╚═══════════════════════════╝"
        ]
        
        for line in logo_lines:
            logo_label = tk.Label(
                logo_container,
                text=line,
                font=("Consolas", 10, "bold"),
                bg="#000000",
                fg="#00D4FF"
            )
            logo_label.pack()
            
        # Content area
        content_frame = tk.Frame(main_frame, bg="#000000")
        content_frame.pack(fill="both", expand=True, padx=60, pady=40)
        
        # Auth card
        auth_card = CyberCard(content_frame)
        auth_card.pack(expand=True, fill="both", ipadx=50, ipady=30)
        
        # Determine which form to show
        if not os.path.exists('.master_hash'):
            self.show_cyber_setup_form(auth_card)
        else:
            self.show_cyber_login_form(auth_card)
            
    def show_cyber_setup_form(self, parent):
        """Show futuristic setup form"""
        # Header section
        header_frame = tk.Frame(parent, bg="#0F172A")
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Cyber header decoration
        header_decoration = tk.Frame(header_frame, bg="#00FF41", height=2)
        header_decoration.pack(fill="x", pady=(0, 20))
        
        welcome_title = tk.Label(
            header_frame,
            text="◢ INITIALIZE QUANTUM VAULT ◣",
            font=("Consolas", 18, "bold"),
            bg="#0F172A",
            fg="#00D4FF"
        )
        welcome_title.pack()
        
        welcome_subtitle = tk.Label(
            header_frame,
            text="ESTABLISHING NEURAL LINK...",
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#00FF41"
        )
        welcome_subtitle.pack(pady=(8, 0))
        
        # Status indicators
        status_frame = tk.Frame(header_frame, bg="#0F172A")
        status_frame.pack(pady=(15, 0))
        
        status_items = [
            "► QUANTUM ENCRYPTION: READY",
            "► NEURAL INTERFACE: ACTIVE", 
            "► SECURITY PROTOCOL: STANDBY"
        ]
        
        for status in status_items:
            status_label = tk.Label(
                status_frame,
                text=status,
                font=("Consolas", 9),
                bg="#0F172A",
                fg="#64748B"
            )
            status_label.pack(anchor="w")
            
        # Form section
        form_frame = tk.Frame(parent, bg="#0F172A")
        form_frame.pack(fill="x", padx=40)
        
        # Master password
        self.master_password_input = CyberInput(
            form_frame,
            label="MASTER ACCESS CODE",
            placeholder="Enter quantum key sequence",
            is_password=True
        )
        self.master_password_input.pack(fill="x", pady=(0, 20))
        
        # Confirm password
        self.confirm_password_input = CyberInput(
            form_frame,
            label="CONFIRM ACCESS CODE",
            placeholder="Re-enter quantum key sequence",
            is_password=True
        )
        self.confirm_password_input.pack(fill="x", pady=(0, 25))
        
        # Security status
        security_frame = tk.Frame(form_frame, bg="#064E3B", relief="flat")
        security_frame.pack(fill="x", pady=(0, 30), ipady=15, ipadx=20)
        
        security_icon = tk.Label(
            security_frame,
            text="◢◣ QUANTUM SHIELD ACTIVE ◢◣",
            font=("Consolas", 10, "bold"),
            bg="#064E3B",
            fg="#10F2C5"
        )
        security_icon.pack()
        
        security_desc = tk.Label(
            security_frame,
            text="AES-256 NEURAL ENCRYPTION | QUANTUM ENTANGLEMENT SECURITY",
            font=("Consolas", 8),
            bg="#064E3B",
            fg="#6EE7B7"
        )
        security_desc.pack(pady=(5, 0))
        
        # Initialize button
        init_btn = FuturisticButton(
            form_frame,
            text="◢ INITIALIZE VAULT ◣",
            command=self.create_master_password,
            style="neon",
            size="large"
        )
        init_btn.pack(pady=20)
        
        # Key bindings
        self.master_password_input.bind('<Return>', lambda e: self.confirm_password_input.focus())
        self.confirm_password_input.bind('<Return>', lambda e: self.create_master_password())
        
        # Focus
        self.master_password_input.focus()
        
    def show_cyber_login_form(self, parent):
        """Show futuristic login form"""
        # Header section
        header_frame = tk.Frame(parent, bg="#0F172A")
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Cyber header decoration
        header_decoration = tk.Frame(header_frame, bg="#00FF41", height=2)
        header_decoration.pack(fill="x", pady=(0, 20))
        
        welcome_title = tk.Label(
            header_frame,
            text="◢ NEURAL INTERFACE DETECTED ◣",
            font=("Consolas", 18, "bold"),
            bg="#0F172A",
            fg="#00D4FF"
        )
        welcome_title.pack()
        
        welcome_subtitle = tk.Label(
            header_frame,
            text="AWAITING QUANTUM AUTHENTICATION...",
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#00FF41"
        )
        welcome_subtitle.pack(pady=(8, 0))
        
        # System status
        status_frame = tk.Frame(header_frame, bg="#0F172A")
        status_frame.pack(pady=(15, 0))
        
        status_items = [
            "► VAULT STATUS: SECURED",
            "► ENCRYPTION: QUANTUM LOCKED",
            "► ACCESS LEVEL: AWAITING AUTH"
        ]
        
        for status in status_items:
            status_label = tk.Label(
                status_frame,
                text=status,
                font=("Consolas", 9),
                bg="#0F172A",
                fg="#64748B"
            )
            status_label.pack(anchor="w")
            
        # Form section
        form_frame = tk.Frame(parent, bg="#0F172A")
        form_frame.pack(fill="x", padx=40)
        
        # Master password
        self.master_password_input = CyberInput(
            form_frame,
            label="QUANTUM ACCESS CODE",
            placeholder="Enter your neural key",
            is_password=True
        )
        self.master_password_input.pack(fill="x", pady=(0, 30))
        
        # Access button
        access_btn = FuturisticButton(
            form_frame,
            text="◢ ACCESS VAULT ◣",
            command=self.authenticate,
            style="neon",
            size="large"
        )
        access_btn.pack(pady=20)
        
        # Key binding
        self.master_password_input.bind('<Return>', lambda e: self.authenticate())
        
        # Focus
        self.master_password_input.focus()
        
    def create_master_password(self):
        """Create master password"""
        password = self.master_password_input.get()
        confirm = self.confirm_password_input.get()
        
        if not password:
            messagebox.showerror("SYSTEM ERROR", "◢ QUANTUM KEY REQUIRED ◣")
            return
            
        if password != confirm:
            messagebox.showerror("SYNC ERROR", "◢ KEY SEQUENCES DO NOT MATCH ◣")
            return
            
        if len(password) < 8:
            messagebox.showerror("SECURITY ERROR", "◢ MINIMUM 8 CHARACTER QUANTUM KEY ◣")
            return
            
        try:
            self.password_manager = PasswordManager()
            self.password_manager.initialize_master_password(password)
            self.is_authenticated = True
            
            messagebox.showinfo("SYSTEM ONLINE", "◢ QUANTUM VAULT INITIALIZED ◣")
            self.show_cyber_main_screen()
        except Exception as e:
            messagebox.showerror("SYSTEM FAILURE", f"◢ INITIALIZATION ERROR ◣\n{str(e)}")
            
    def authenticate(self):
        """Authenticate user"""
        password = self.master_password_input.get()
        
        if not password:
            messagebox.showerror("ACCESS DENIED", "◢ QUANTUM KEY REQUIRED ◣")
            return
            
        try:
            self.password_manager = PasswordManager()
            if self.password_manager.authenticate(password):
                self.is_authenticated = True
                messagebox.showinfo("ACCESS GRANTED", "◢ NEURAL LINK ESTABLISHED ◣")
                self.show_cyber_main_screen()
            else:
                messagebox.showerror("ACCESS DENIED", "◢ INVALID QUANTUM KEY ◣")
                self.master_password_input.clear()
        except Exception as e:
            messagebox.showerror("SYSTEM ERROR", f"◢ AUTHENTICATION FAILURE ◣\n{str(e)}")
            
    def show_cyber_main_screen(self):
        """Show futuristic main interface"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(fill="both", expand=True)
        
        # Animated header
        header = HolographicHeader(main_frame, height=100)
        header.pack(fill="x")
        
        # Header content
        header_content = tk.Frame(header, bg="#000000")
        header_content.place(x=30, y=10, relheight=1)
        
        # Left side - system info
        system_info = tk.Frame(header_content, bg="#000000")
        system_info.pack(side="left", fill="y")
        
        system_title = tk.Label(
            system_info,
            text="◢ CYBER VAULT ◣",
            font=("Consolas", 16, "bold"),
            bg="#000000",
            fg="#00D4FF"
        )
        system_title.pack(side="left", pady=20)
        
        system_status = tk.Label(
            system_info,
            text="ONLINE",
            font=("Consolas", 10),
            bg="#000000",
            fg="#00FF41"
        )
        system_status.pack(side="left", padx=(15, 0), pady=20)
        
        # Right side - logout
        logout_frame = tk.Frame(header, bg="#000000")
        logout_frame.place(relx=1, x=-30, y=25, anchor="ne")
        
        logout_btn = FuturisticButton(
            logout_frame,
            text="◢ DISCONNECT ◣",
            command=self.logout,
            style="danger",
            size="small"
        )
        logout_btn.pack()
        
        # Main interface
        interface_frame = tk.Frame(main_frame, bg="#000000")
        interface_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Control panel
        control_panel = tk.Frame(interface_frame, bg="#000000")
        control_panel.pack(fill="x", pady=(0, 20))
        
        # Title section
        title_section = tk.Frame(control_panel, bg="#000000")
        title_section.pack(side="left")
        
        main_title = tk.Label(
            title_section,
            text="◢ ENCRYPTED DATA MATRIX ◣",
            font=("Consolas", 16, "bold"),
            bg="#000000",
            fg="#E2E8F0"
        )
        main_title.pack(anchor="w")
        
        # Control buttons
        controls_frame = tk.Frame(control_panel, bg="#000000")
        controls_frame.pack(side="right")
        
        # Search interface
        search_frame = tk.Frame(controls_frame, bg="#000000")
        search_frame.pack(side="right", padx=(0, 20))
        
        self.search_input = CyberInput(
            search_frame,
            label="SCAN",
            placeholder="Search quantum data..."
        )
        self.search_input.pack()
        self.search_input.bind('<KeyRelease>', lambda e: self.search_credentials())
        
        # Add new data
        add_btn = FuturisticButton(
            controls_frame,
            text="◢ + NEW DATA ◣",
            command=self.show_cyber_add_dialog,
            style="success"
        )
        add_btn.pack(side="right")
        
        # Data matrix (credentials area)
        matrix_card = CyberCard(interface_frame)
        matrix_card.pack(fill="both", expand=True, ipady=25, ipadx=30)
        
        # Scrollable matrix
        canvas = tk.Canvas(matrix_card, bg="#0F172A", highlightthickness=0)
        scrollbar = ttk.Scrollbar(matrix_card, orient="vertical", command=canvas.yview, style="Cyber.Vertical.TScrollbar")
        self.credentials_frame = tk.Frame(canvas, bg="#0F172A")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.create_window((0, 0), window=self.credentials_frame, anchor="nw")
        self.credentials_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Load data matrix
        self.refresh_data_matrix()
        
    def refresh_data_matrix(self):
        """Load and display credentials in cyber style"""
        if not self.password_manager:
            return
            
        # Clear existing
        for widget in self.credentials_frame.winfo_children():
            widget.destroy()
            
        try:
            credentials = self.password_manager.get_all_credentials()
            self.current_credentials = credentials
            
            if not credentials:
                # Empty matrix state
                empty_frame = tk.Frame(self.credentials_frame, bg="#0F172A")
                empty_frame.pack(expand=True, fill="both", pady=80)
                
                empty_art = [
                    "╔═══════════════════════════╗",
                    "║     DATA MATRIX EMPTY     ║",
                    "║                           ║",
                    "║    ◢◣ NO RECORDS ◢◣     ║",
                    "║                           ║",
                    "║   INITIALIZE NEW DATA     ║",
                    "╚═══════════════════════════╝"
                ]
                
                for line in empty_art:
                    empty_label = tk.Label(
                        empty_frame,
                        text=line,
                        font=("Consolas", 10),
                        bg="#0F172A",
                        fg="#334155"
                    )
                    empty_label.pack()
            else:
                for service, data in credentials.items():
                    self.create_cyber_data_item(service, data)
                    
        except Exception as e:
            messagebox.showerror("MATRIX ERROR", f"◢ DATA LOAD FAILURE ◣\n{str(e)}")
            
    def create_cyber_data_item(self, service, data):
        """Create futuristic credential item"""
        # Data record container
        record_frame = tk.Frame(
            self.credentials_frame,
            bg="#1E293B",
            relief="flat",
            highlightbackground="#00D4FF",
            highlightthickness=1
        )
        record_frame.pack(fill="x", padx=10, pady=6, ipady=18, ipadx=25)
        
        # Record header
        header_frame = tk.Frame(record_frame, bg="#1E293B")
        header_frame.pack(fill="x", pady=(0, 8))
        
        # Cyber decoration
        decoration = tk.Label(
            header_frame,
            text="◢◣",
            font=("Consolas", 10),
            bg="#1E293B",
            fg="#00FF41"
        )
        decoration.pack(side="left")
        
        # Service name
        service_label = tk.Label(
            header_frame,
            text=service.upper(),
            font=("Consolas", 13, "bold"),
            bg="#1E293B",
            fg="#E2E8F0"
        )
        service_label.pack(side="left", padx=(10, 0))
        
        # Status indicator
        status_indicator = tk.Label(
            header_frame,
            text="[ENCRYPTED]",
            font=("Consolas", 8),
            bg="#1E293B",
            fg="#10F2C5"
        )
        status_indicator.pack(side="right")
        
        # Data info
        info_frame = tk.Frame(record_frame, bg="#1E293B")
        info_frame.pack(fill="x", pady=(0, 12))
        
        # Username
        username = data.get('username', 'NO_USER')
        user_label = tk.Label(
            info_frame,
            text=f"► USER_ID: {username}",
            font=("Consolas", 10),
            bg="#1E293B",
            fg="#94A3B8"
        )
        user_label.pack(anchor="w")
        
        # Actions panel
        actions_frame = tk.Frame(record_frame, bg="#1E293B")
        actions_frame.pack(fill="x")
        
        # Action buttons
        copy_btn = FuturisticButton(
            actions_frame,
            text="COPY",
            command=lambda s=service: self.copy_password(s),
            style="success",
            size="small"
        )
        copy_btn.pack(side="right", padx=(6, 0))
        
        edit_btn = FuturisticButton(
            actions_frame,
            text="EDIT",
            command=lambda s=service: self.edit_credential(s),
            style="warning",
            size="small"
        )
        edit_btn.pack(side="right", padx=(6, 0))
        
        delete_btn = FuturisticButton(
            actions_frame,
            text="DELETE",
            command=lambda s=service: self.delete_credential(s),
            style="danger",
            size="small"
        )
        delete_btn.pack(side="right", padx=(6, 0))
        
    def show_cyber_add_dialog(self):
        """Show futuristic add dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("◢ NEW DATA ENTRY ◣")
        dialog.geometry("550x700")
        dialog.configure(bg="#000000")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center dialog
        x = self.root.winfo_rootx() + (self.root.winfo_width() - 550) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - 700) // 2
        dialog.geometry(f"550x700+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg="#0F172A", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Header decoration
        decoration_line = tk.Frame(header_frame, bg="#00FF41", height=3)
        decoration_line.pack(fill="x")
        
        header_title = tk.Label(
            header_frame,
            text="◢ QUANTUM DATA INITIALIZATION ◣",
            font=("Consolas", 14, "bold"),
            bg="#0F172A",
            fg="#00D4FF"
        )
        header_title.pack(expand=True)
        
        # Form container
        form_container = CyberCard(dialog)
        form_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Form
        form_frame = tk.Frame(form_container, bg="#0F172A")
        form_frame.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Service
        service_input = CyberInput(
            form_frame,
            label="TARGET SYSTEM",
            placeholder="e.g., NEURAL_NET_GMAIL, QUANTUM_GITHUB"
        )
        service_input.pack(fill="x", pady=(0, 25))
        
        # Username
        username_input = CyberInput(
            form_frame,
            label="USER IDENTIFIER",
            placeholder="neural.user@quantum.net"
        )
        username_input.pack(fill="x", pady=(0, 25))
        
        # Password section
        password_section = tk.Frame(form_frame, bg="#0F172A")
        password_section.pack(fill="x", pady=(0, 25))
        
        password_input = CyberInput(
            password_section,
            label="ACCESS KEY",
            placeholder="quantum_encryption_key",
            is_password=True
        )
        password_input.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        generate_btn = FuturisticButton(
            password_section,
            text="◢ GEN ◣",
            command=lambda: self.generate_quantum_password(password_input),
            style="neon",
            size="small"
        )
        generate_btn.pack(side="right", anchor="s", pady=(28, 0))
        
        # URL
        url_input = CyberInput(
            form_frame,
            label="NETWORK ADDRESS",
            placeholder="https://quantum.target.system"
        )
        url_input.pack(fill="x", pady=(0, 35))
        
        # Control panel
        control_frame = tk.Frame(form_frame, bg="#0F172A")
        control_frame.pack(fill="x")
        
        # Cyber decoration
        control_decoration = tk.Frame(control_frame, bg="#00D4FF", height=2)
        control_decoration.pack(fill="x", pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg="#0F172A")
        button_frame.pack(fill="x")
        
        cancel_btn = FuturisticButton(
            button_frame,
            text="◢ ABORT ◣",
            command=dialog.destroy,
            style="danger"
        )
        cancel_btn.pack(side="right", padx=(15, 0))
        
        save_btn = FuturisticButton(
            button_frame,
            text="◢ COMMIT DATA ◣",
            command=lambda: self.save_cyber_credential(
                service_input.get(),
                username_input.get(),
                password_input.get(),
                url_input.get(),
                dialog
            ),
            style="neon"
        )
        save_btn.pack(side="right")
        
        # Focus
        service_input.focus()
        
    def generate_quantum_password(self, password_input):
        """Generate futuristic password"""
        # Cyber-style password generation
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = ''.join(random.choice(chars) for _ in range(18))
        password_input.set(password)
        messagebox.showinfo("QUANTUM GEN", "◢ ENCRYPTION KEY GENERATED ◣")
        
    def save_cyber_credential(self, service, username, password, url, dialog):
        """Save new credential"""
        if not all([service, username, password]):
            messagebox.showerror("DATA ERROR", "◢ MISSING REQUIRED FIELDS ◣")
            return
            
        try:
            notes = f"URL: {url}" if url else ""
            self.password_manager.add_credential(service, username, password, notes)
            dialog.destroy()
            self.refresh_data_matrix()
            messagebox.showinfo("DATA COMMIT", "◢ QUANTUM RECORD CREATED ◣")
        except Exception as e:
            messagebox.showerror("COMMIT ERROR", f"◢ DATA SAVE FAILURE ◣\n{str(e)}")
            
    def copy_password(self, service):
        """Copy password to clipboard"""
        try:
            credentials = self.password_manager.get_all_credentials()
            password = credentials[service]['password']
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("DATA TRANSFER", f"◢ {service} KEY COPIED ◣")
        except Exception as e:
            messagebox.showerror("TRANSFER ERROR", f"◢ COPY FAILURE ◣\n{str(e)}")
            
    def edit_credential(self, service):
        """Show futuristic edit dialog"""
        credential = self.password_manager.get_credential(service)
        if not credential:
            messagebox.showerror("SYSTEM ERROR", "◢ UNABLE TO LOAD DATA ◣")
            return
        self.show_cyber_edit_dialog(service, credential)

    def show_cyber_edit_dialog(self, service, credential):
        """Show futuristic edit dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("◢ EDIT DATA ENTRY ◣")
        dialog.geometry("550x700")
        dialog.configure(bg="#000000")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # Center dialog
        x = self.root.winfo_rootx() + (self.root.winfo_width() - 550) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - 700) // 2
        dialog.geometry(f"550x700+{x}+{y}")

        # Header
        header_frame = tk.Frame(dialog, bg="#0F172A", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Header decoration
        decoration_line = tk.Frame(header_frame, bg="#00FF41", height=3)
        decoration_line.pack(fill="x")

        header_title = tk.Label(
            header_frame,
            text="◢ QUANTUM DATA MODIFICATION ◣",
            font=("Consolas", 14, "bold"),
            bg="#0F172A",
            fg="#00D4FF"
        )
        header_title.pack(expand=True)

        # Form container
        form_container = CyberCard(dialog)
        form_container.pack(fill="both", expand=True, padx=25, pady=25)

        # Form
        form_frame = tk.Frame(form_container, bg="#0F172A")
        form_frame.pack(fill="both", expand=True, padx=35, pady=35)

        # Service (read-only)
        service_input = CyberInput(
            form_frame,
            label="TARGET SYSTEM",
            placeholder="e.g., NEURAL_NET_GMAIL, QUANTUM_GITHUB"
        )
        service_input.pack(fill="x", pady=(0, 25))
        service_input.set(service)
        service_input.entry.config(state='disabled')


        # Username
        username_input = CyberInput(
            form_frame,
            label="USER IDENTIFIER",
            placeholder="neural.user@quantum.net"
        )
        username_input.pack(fill="x", pady=(0, 25))
        username_input.set(credential.get('username', ''))

        # Password section
        password_section = tk.Frame(form_frame, bg="#0F172A")
        password_section.pack(fill="x", pady=(0, 25))

        password_input = CyberInput(
            password_section,
            label="ACCESS KEY",
            placeholder="quantum_encryption_key",
            is_password=True
        )
        password_input.pack(side="left", fill="x", expand=True, padx=(0, 15))
        password_input.set(credential.get('password', ''))

        generate_btn = FuturisticButton(
            password_section,
            text="◢ GEN ◣",
            command=lambda: self.generate_quantum_password(password_input),
            style="neon",
            size="small"
        )
        generate_btn.pack(side="right", anchor="s", pady=(28, 0))

        # URL
        url_input = CyberInput(
            form_frame,
            label="NETWORK ADDRESS",
            placeholder="https://quantum.target.system"
        )
        url_input.pack(fill="x", pady=(0, 35))
        notes = credential.get('notes', '')
        url = notes.replace("URL: ", "") if notes.startswith("URL: ") else ""
        url_input.set(url)


        # Control panel
        control_frame = tk.Frame(form_frame, bg="#0F172A")
        control_frame.pack(fill="x")

        # Cyber decoration
        control_decoration = tk.Frame(control_frame, bg="#00D4FF", height=2)
        control_decoration.pack(fill="x", pady=(0, 20))

        # Buttons
        button_frame = tk.Frame(control_frame, bg="#0F172A")
        button_frame.pack(fill="x")

        cancel_btn = FuturisticButton(
            button_frame,
            text="◢ ABORT ◣",
            command=dialog.destroy,
            style="danger"
        )
        cancel_btn.pack(side="right", padx=(15, 0))

        save_btn = FuturisticButton(
            button_frame,
            text="◢ UPDATE DATA ◣",
            command=lambda: self.update_cyber_credential(
                service,
                username_input.get(),
                password_input.get(),
                url_input.get(),
                dialog
            ),
            style="neon"
        )
        save_btn.pack(side="right")

        # Focus
        username_input.focus()

    def update_cyber_credential(self, service, username, password, url, dialog):
        """Update credential"""
        if not all([service, username, password]):
            messagebox.showerror("DATA ERROR", "◢ MISSING REQUIRED FIELDS ◣")
            return

        try:
            notes = f"URL: {url}" if url else ""
            self.password_manager.update_credential(service, username, password, notes)
            dialog.destroy()
            self.refresh_data_matrix()
            messagebox.showinfo("DATA UPDATE", "◢ QUANTUM RECORD UPDATED ◣")
        except Exception as e:
            messagebox.showerror("UPDATE ERROR", f"◢ DATA UPDATE FAILURE ◣\n{str(e)}")

    def delete_credential(self, service):
        """Delete credential"""
        if messagebox.askyesno("CONFIRM DELETE", f"◢ PURGE {service} DATA? ◣"):
            try:
                self.password_manager.delete_credential(service)
                self.refresh_data_matrix()
                messagebox.showinfo("DATA PURGED", f"◢ {service} DELETED ◣")
            except Exception as e:
                messagebox.showerror("PURGE ERROR", f"◢ DELETE FAILURE ◣\n{str(e)}")
                
    def search_credentials(self):
        """Search credentials with cyber styling"""
        query = self.search_input.get().lower()
        
        # Clear existing
        for widget in self.credentials_frame.winfo_children():
            widget.destroy()
            
        if not query:
            # Show all
            for service, data in self.current_credentials.items():
                self.create_cyber_data_item(service, data)
        else:
            # Filter
            filtered = {
                k: v for k, v in self.current_credentials.items()
                if query in k.lower() or query in v.get('username', '').lower()
            }
            
            if filtered:
                for service, data in filtered.items():
                    self.create_cyber_data_item(service, data)
            else:
                # No results
                no_results_frame = tk.Frame(self.credentials_frame, bg="#0F172A")
                no_results_frame.pack(pady=60)
                
                no_results = tk.Label(
                    no_results_frame,
                    text="◢ NO QUANTUM MATCHES FOUND ◣",
                    font=("Consolas", 12, "bold"),
                    bg="#0F172A",
                    fg="#64748B"
                )
                no_results.pack()
                
    def logout(self):
        """Logout with cyber style"""
        self.is_authenticated = False
        self.password_manager = None
        self.current_credentials = {}
        messagebox.showinfo("NEURAL DISCONNECT", "◢ QUANTUM LINK TERMINATED ◣")
        self.show_cyber_auth_screen()
        
    def run(self):
        """Start the futuristic application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = PasswordManagerGUI()
    app.run()