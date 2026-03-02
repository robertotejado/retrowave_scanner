import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import sys
import datetime
import os

# ==========================================
# CONFIGURACION DE COLORES SYNTHWAVE / 80s
# ==========================================
BG_COLOR = "#0D0221"
TEXT_NEON_CYAN = "#00FFFF"
TEXT_NEON_MAGENTA = "#FF00FF"
BTN_BG = "#FF00FF"
BTN_FG = "#0D0221"
BTN_ACTIVE_BG = "#00FFFF"
CONSOLE_BG = "#050014"
CONSOLE_FG = "#39FF14"
FONT_TITLE = ("Courier New", 22, "bold")
FONT_LABEL = ("Courier New", 12, "bold")
FONT_CONSOLE = ("Consolas", 10)
# ==========================================

class RetroWaveScanner(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("RETROWAVE ICS & IT SECURITY SCANNER")
        self.geometry("820x680")
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)

        self.running_processes = []
        self.cancel_requested = False
        
        # Log file with date, hour, minute, second
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = f"neon_scanner_activity_{current_time}.log"

        self.create_widgets()
        self.write_log("--- SESSION STARTED ---")

    def create_widgets(self):
        title_label = tk.Label(
            self, 
            text="[ NEON SECURITY SCANNER ]", 
            font=FONT_TITLE, 
            bg=BG_COLOR, 
            fg=TEXT_NEON_MAGENTA
        )
        title_label.pack(pady=20)

        input_frame = tk.Frame(self, bg=BG_COLOR)
        input_frame.pack(pady=10)

        target_label = tk.Label(
            input_frame, 
            text="TARGET IP / RANGE:", 
            font=FONT_LABEL, 
            bg=BG_COLOR, 
            fg=TEXT_NEON_CYAN
        )
        target_label.grid(row=0, column=0, padx=10)

        self.target_entry = tk.Entry(
            input_frame, 
            font=FONT_LABEL, 
            bg=CONSOLE_BG, 
            fg=TEXT_NEON_CYAN, 
            insertbackground=TEXT_NEON_CYAN,
            width=25,
            relief=tk.FLAT
        )
        self.target_entry.grid(row=0, column=1, padx=10)
        self.target_entry.insert(0, "192.168.1.0/24")

        # Protocols Frame
        protocol_frame = tk.LabelFrame(
            self, 
            text=" PROTOCOLS TO SCAN ", 
            font=("Courier New", 10, "bold"), 
            bg=BG_COLOR, 
            fg=TEXT_NEON_MAGENTA,
            labelanchor='n',
            padx=10,
            pady=10,
            relief=tk.GROOVE
        )
        protocol_frame.pack(pady=10, expand=False)

        # Protocol definitions with Nmap scripts mapping
        self.protocols = {
            "FTP (21)": tk.BooleanVar(value=True),
            "SSH (22)": tk.BooleanVar(value=True),
            "HTTP (80)": tk.BooleanVar(value=True),
            "HTTPS (443)": tk.BooleanVar(value=True),
            "RDP (3389)": tk.BooleanVar(value=True),
            "S7 (102)": tk.BooleanVar(value=True),
            "Modbus (502)": tk.BooleanVar(value=True),
            "OPC UA (4840)": tk.BooleanVar(value=True)
        }

        # Specific Nmap attacks/scripts mapped to ports
        self.protocol_scripts = {
            "21": "ftp-anon,ftp-bounce,ftp-syst,ftp-vsftpd-backdoor,ftp-proftpd-backdoor",
            "22": "ssh2-enum-algos,ssh-hostkey,ssh-auth-methods",
            "80": "http-enum,http-title,http-methods,http-sql-injection",
            "443": "ssl-enum-ciphers,ssl-heartbleed,ssl-cert",
            "3389": "rdp-enum-encryption,rdp-vuln-ms12-020",
            "102": "s7-info",
            "502": "modbus-discover",
            "4840": "default"  # Assuming standard discovery defaults for OPC UA
        }

        # Grid layout for checkboxes
        cols = 4
        for i, (name, var) in enumerate(self.protocols.items()):
            cb = tk.Checkbutton(
                protocol_frame,
                text=name,
                variable=var,
                font=("Courier New", 9, "bold"),
                bg=BG_COLOR,
                fg=TEXT_NEON_CYAN,
                selectcolor=BG_COLOR,
                activebackground=BG_COLOR,
                activeforeground=TEXT_NEON_CYAN,
                pady=2
            )
            cb.grid(row=i // cols, column=i % cols, sticky="w", padx=10)

        # Reset button to uncheck all protocols
        self.reset_protocols_btn = tk.Button(
            protocol_frame,
            text="[RESET]",
            font=("Courier New", 9, "bold"),
            bg="#FFAAAA", 
            fg="#000000",
            activebackground="#FF0000",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            command=self.uncheck_all_protocols
        )
        self.reset_protocols_btn.grid(row=(len(self.protocols)-1) // cols, column=(len(self.protocols)-1) % cols + 1, sticky="w", padx=10)

        buttons_frame = tk.Frame(self, bg=BG_COLOR)
        buttons_frame.pack(pady=15)

        self.scan_btn = tk.Button(
            buttons_frame, 
            text="INITIATE NEON SCAN", 
            font=FONT_LABEL, 
            bg=BTN_BG, 
            fg=BTN_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=BTN_FG,
            relief=tk.FLAT,
            command=self.start_scan_thread
        )
        self.scan_btn.grid(row=0, column=0, padx=10)

        self.cancel_btn = tk.Button(
            buttons_frame, 
            text="ABORT OPERATION", 
            font=FONT_LABEL, 
            bg="#FF0000", 
            fg="#FFFFFF",
            activebackground="#FFAAAA",
            activeforeground="#000000",
            relief=tk.FLAT,
            state=tk.DISABLED,
            command=self.cancel_scan
        )
        self.cancel_btn.grid(row=0, column=1, padx=10)

        self.console = scrolledtext.ScrolledText(
            self, 
            wrap=tk.WORD, 
            width=85, 
            height=20, 
            bg=CONSOLE_BG, 
            fg=CONSOLE_FG, 
            font=FONT_CONSOLE,
            insertbackground=CONSOLE_FG,
            relief=tk.FLAT
        )
        self.console.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.log_to_console(f"READY... WAITING FOR TARGET INPUT.\nLOG FILE SET TO: {self.log_file}\n")

    def uncheck_all_protocols(self):
        for var in self.protocols.values():
            var.set(False)

    def write_log(self, text):
        '''Guarda eventos en el archivo log con fecha y hora'''
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {text.strip()}\n")
        except Exception as e:
            print(f"Failed to write log: {e}")

    def log_to_console(self, text):
        '''Muestra info en la GUI, en la terminal del sistema y la escribe en disco.'''
        self.console.insert(tk.END, text)
        self.console.see(tk.END)
        print(text, end="")
        self.write_log(text)

    def cancel_scan(self):
        self.cancel_requested = True
        self.log_to_console("\n[!] CANCELLATION REQUESTED. TERMINATING PROCESSES...\n")
        
        for proc in self.running_processes:
            try:
                proc.terminate()
            except Exception as e:
                self.write_log(f"Failed to terminate process: {e}")
        
        self.cancel_btn.config(state=tk.DISABLED)

    def start_scan_thread(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("INPUT ERROR", "Please provide a valid IP or Range.")
            return

        selected_ports = []
        selected_scripts = []
        for name, var in self.protocols.items():
            if var.get():
                port = name.split("(")[1].split(")")[0]
                selected_ports.append(port)
                if port in self.protocol_scripts:
                    script = self.protocol_scripts[port]
                    if script != "default":
                        selected_scripts.append(script)

        if not selected_ports:
            messagebox.showwarning("INPUT ERROR", "Please select at least one protocol to scan.")
            return

        self.cancel_requested = False
        self.running_processes.clear()

        self.scan_btn.config(state=tk.DISABLED, text="[ SCANNING... ]", bg=TEXT_NEON_CYAN)
        self.cancel_btn.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        
        self.write_log("==================================================")
        self.log_to_console(f"[*] INITIATING SYNTHWAVE SCAN ON TARGET: {target}\n")
        self.log_to_console(f"[*] SELECTED PORTS: {', '.join(selected_ports)}\n")
        self.log_to_console("[*] HUNTING FOR ICS & IT PROTOCOLS...\n")
        self.log_to_console("-" * 65 + "\n")

        scan_thread = threading.Thread(target=self.run_nmap_scan, args=(target, selected_ports, selected_scripts))
        scan_thread.daemon = True
        scan_thread.start()

    def run_nmap_scan(self, target, selected_ports, selected_scripts):
        ports_to_scan = ",".join(selected_ports)
        
        # Base Nmap command
        nmap_cmd = ["nmap", "-p", ports_to_scan, "-Pn", "-sV", "--open", "-T4"]
        
        # Add scripts if any were selected
        if selected_scripts:
            scripts_arg = ",".join(selected_scripts)
            nmap_cmd.extend(["--script", scripts_arg])
            
        nmap_cmd.append(target)

        try:
            if self.cancel_requested:
                raise Exception("Scan aborted by user.")

            # Run Nmap Attack & Scan
            self.execute_command(nmap_cmd, "NMAP ATTACK & SCAN")

            # Additional ICS Scans if selected and not cancelled
            if "502" in selected_ports and not self.cancel_requested:
                self.log_to_console("\n[*] RUNNING ADVANCED MODBUS SCAN (NPING)...\n")
                nping_modbus = ["sudo", "nping", "--tcp", "-p", "502", "--data", "000100000006010600010002", target, "-c", "1"]
                self.execute_command(nping_modbus, "MODBUS NPING SCAN")

            if "102" in selected_ports and not self.cancel_requested:
                self.log_to_console("\n[*] RUNNING ADVANCED S7 SCAN (NPING)...\n")
                nping_s7 = ["sudo", "nping", "--tcp", "-p", "102", "--data", "000100000006010600010002", target, "-c", "1"]
                self.execute_command(nping_s7, "S7 NPING SCAN")

            if "4840" in selected_ports and not self.cancel_requested:
                self.log_to_console("\n[*] RUNNING ADVANCED OPCUA SCAN (NPING & NC)...\n")
                # OPCUA Nping
                nping_opcua = ["sudo", "nping", "--tcp", "-p", "4840", "--data", "000100000006010600010002", target, "-c", "1"]
                self.execute_command(nping_opcua, "OPCUA NPING SCAN")
                
                # OPCUA Netcat
                self.log_to_console("\n[*] SENDING OPCUA 'HEL' PACKET (NC)...\n")
                nc_cmd = f"echo -n \"HEL\" | nc {target} 4840"
                if not self.cancel_requested:
                    self.execute_command(nc_cmd, "OPCUA NC SCAN", use_shell=True)

            if self.cancel_requested:
                self.after(0, self.log_to_console, "\n[X] OPERATION ABORTED BY USER.\n")
            else:
                self.after(0, self.log_to_console, "\n[OK] ALL SCANS COMPLETE. STAY RADICAL.\n")

        except FileNotFoundError as e:
            self.after(0, self.log_to_console, f"\n[!] CRITICAL ERROR: command not found: {str(e)}\n")
        except Exception as e:
            self.after(0, self.log_to_console, f"\n[!] ERROR: {str(e)}\n")
        finally:
            self.write_log("==================================================\n")
            self.after(0, self.reset_button)

    def execute_command(self, cmd, label, use_shell=False):
        try:
            # On Windows, sudo isn't standard. We check if it exists or just run without if missing/windows.
            if isinstance(cmd, list) and cmd[0] == "sudo" and sys.platform == 'win32':
                cmd = cmd[1:] # Strip sudo on windows

            cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
            self.after(0, self.log_to_console, f"\n[>] EXECUTING {label}: {cmd_str}\n")

            if use_shell or isinstance(cmd, str):
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    shell=True
                )
            else:
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    shell=(sys.platform == 'win32')
                )

            self.running_processes.append(process)

            for line in process.stdout:
                if self.cancel_requested:
                    break
                self.after(0, self.log_to_console, line)

            process.wait()
            
            if process in self.running_processes:
                self.running_processes.remove(process)
                
            return process.returncode
        except Exception as e:
            if not self.cancel_requested:
                self.after(0, self.log_to_console, f"\n[!] ERROR EXECUTING {label}: {str(e)}\n")
            return -1

    def reset_button(self):
        self.scan_btn.config(state=tk.NORMAL, text="INITIATE NEON SCAN", bg=BTN_BG)
        self.cancel_btn.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = RetroWaveScanner()
    app.mainloop()
