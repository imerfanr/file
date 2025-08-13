#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cryptocurrency Miner Detection System GUI
Compatible with Windows 7 32-bit
"""

import os
import sys
import json
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from datetime import datetime

# Import our detector module
from crypto_miner_detector import MinerDetector

class ScanThread(threading.Thread):
    def __init__(self, callback, progress_callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.progress_callback = progress_callback
        self.daemon = True
        
    def run(self):
        try:
            self.progress_callback("Starting scan...")
            detector = MinerDetector()
            results = detector.comprehensive_scan()
            self.progress_callback("Scan complete. Generating map...")
            map_file = detector.generate_html_map(results)
            self.progress_callback(f"Map saved: {map_file}")
            report, report_file = detector.generate_report(results)
            self.progress_callback(f"Report saved: {report_file}")
            detector.close_database()
            self.callback(results, map_file, report_file)
        except Exception as e:
            import traceback
            self.progress_callback(f"Error in scan: {str(e)}")
            traceback.print_exc()

class MinerDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptocurrency Miner Detection System")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        self.results = None
        self.report_file = None
        self.map_file = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Cryptocurrency Miner Detection System", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Start scan button
        self.start_button = ttk.Button(main_frame, text="Start Scan", command=self.start_scan)
        self.start_button.pack(pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Status: Ready")
        self.status_label.pack(pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Map preview frame (will show instructions)
        map_frame = ttk.LabelFrame(main_frame, text="Map Preview")
        map_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.map_preview = scrolledtext.ScrolledText(map_frame, wrap=tk.WORD)
        self.map_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.map_preview.insert(tk.END, "Map will be displayed here after scan.\n\n" +
                               "After scan completes, you can open the HTML map file in your browser.")
        self.map_preview.config(state=tk.DISABLED)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Save results button
        self.save_results_button = ttk.Button(buttons_frame, text="Save Results JSON", 
                                             command=self.save_results, state=tk.DISABLED)
        self.save_results_button.pack(side=tk.LEFT, padx=5)
        
        # Save report button
        self.save_report_button = ttk.Button(buttons_frame, text="Save Report JSON", 
                                           command=self.save_report, state=tk.DISABLED)
        self.save_report_button.pack(side=tk.LEFT, padx=5)
        
        # Load results button
        self.load_results_button = ttk.Button(buttons_frame, text="Load Previous Results", 
                                            command=self.load_previous_results)
        self.load_results_button.pack(side=tk.LEFT, padx=5)
        
        # Open map button
        self.open_map_button = ttk.Button(buttons_frame, text="Open Map in Browser", 
                                        command=self.open_map, state=tk.DISABLED)
        self.open_map_button.pack(side=tk.LEFT, padx=5)
    
    def update_log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.status_label.config(text=f"Status: {message}")
        self.root.update_idletasks()
    
    def start_scan(self):
        self.start_button.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)
        self.status_label.config(text="Status: Scanning...")
        
        # Start scan in a separate thread
        scan_thread = ScanThread(self.scan_finished, self.update_log)
        scan_thread.start()
    
    def scan_finished(self, results, map_file, report_file):
        self.results = results
        self.map_file = map_file
        self.report_file = report_file
        
        # Update map preview
        self.map_preview.config(state=tk.NORMAL)
        self.map_preview.delete(1.0, tk.END)
        
        # Show summary in map preview
        stats = results['statistics']
        self.map_preview.insert(tk.END, "Scan Results Summary:\n\n")
        self.map_preview.insert(tk.END, f"Total devices scanned: {stats['total_devices_scanned']}\n")
        self.map_preview.insert(tk.END, f"Suspicious devices: {stats['suspicious_devices']}\n")
        self.map_preview.insert(tk.END, f"Confirmed miners: {stats['confirmed_miners']}\n")
        self.map_preview.insert(tk.END, f"Suspicious WiFi networks: {stats['wifi_suspicious']}\n")
        self.map_preview.insert(tk.END, f"Thermal hotspots: {stats['thermal_hotspots']}\n\n")
        
        self.map_preview.insert(tk.END, f"Map file: {map_file}\n")
        self.map_preview.insert(tk.END, f"Report file: {report_file}\n\n")
        self.map_preview.insert(tk.END, "Click 'Open Map in Browser' to view the interactive map.")
        self.map_preview.config(state=tk.DISABLED)
        
        # Enable buttons
        self.save_results_button.config(state=tk.NORMAL)
        self.save_report_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.open_map_button.config(state=tk.NORMAL)
        
        self.status_label.config(text="Status: Scan and report generation complete.")
        self.update_log("Scan and report generation complete.")
    
    def save_results(self):
        if self.results is None:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Results JSON"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Success", "Results saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving results: {e}")
    
    def save_report(self):
        if self.report_file is None:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Report JSON"
        )
        
        if file_path:
            try:
                with open(self.report_file, 'r', encoding='utf-8') as src:
                    data = src.read()
                with open(file_path, 'w', encoding='utf-8') as dst:
                    dst.write(data)
                messagebox.showinfo("Success", "Report saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving report: {e}")
    
    def load_previous_results(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Previous Results"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.results = json.load(f)
                
                # Look for related map and report files
                base_dir = os.path.dirname(file_path)
                base_name = os.path.basename(file_path).split('_')[0]
                
                # Find map file
                map_files = [f for f in os.listdir(base_dir) if f.startswith(base_name) and f.endswith('.html')]
                if map_files:
                    self.map_file = os.path.join(base_dir, map_files[0])
                
                # Find report file
                report_files = [f for f in os.listdir(base_dir) if f.startswith(base_name) and 'report' in f]
                if report_files:
                    self.report_file = os.path.join(base_dir, report_files[0])
                
                # Update UI
                self.update_log(f"Loaded previous results from {file_path}")
                
                # Update map preview
                self.map_preview.config(state=tk.NORMAL)
                self.map_preview.delete(1.0, tk.END)
                
                # Show summary in map preview
                stats = self.results['statistics']
                self.map_preview.insert(tk.END, "Loaded Results Summary:\n\n")
                self.map_preview.insert(tk.END, f"Total devices scanned: {stats['total_devices_scanned']}\n")
                self.map_preview.insert(tk.END, f"Suspicious devices: {stats['suspicious_devices']}\n")
                self.map_preview.insert(tk.END, f"Confirmed miners: {stats['confirmed_miners']}\n")
                
                if self.map_file:
                    self.map_preview.insert(tk.END, f"\nMap file: {self.map_file}\n")
                    self.open_map_button.config(state=tk.NORMAL)
                
                if self.report_file:
                    self.map_preview.insert(tk.END, f"Report file: {self.report_file}\n")
                
                self.map_preview.config(state=tk.DISABLED)
                
                # Enable buttons
                self.save_results_button.config(state=tk.NORMAL)
                if self.report_file:
                    self.save_report_button.config(state=tk.NORMAL)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading results: {e}")
    
    def open_map(self):
        if self.map_file and os.path.exists(self.map_file):
            # Open in default browser
            webbrowser.open('file://' + os.path.abspath(self.map_file))
        else:
            messagebox.showerror("Error", "Map file not found.")

def main():
    root = tk.Tk()
    app = MinerDetectorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
