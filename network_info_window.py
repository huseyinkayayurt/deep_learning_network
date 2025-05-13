import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np

class NetworkInfoWindow(tk.Toplevel):
    def __init__(self, parent, network_parameters):
        super().__init__(parent)
        
        self.parent = parent
        self.network_parameters = network_parameters
        
        # Pencere ayarları
        self.title("Güncellenmiş Ağ Parametreleri")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Ana grid yapılandırması
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Canvas ve Scrollbar oluştur
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Ana içerik frame'i
        self.main_frame = ttk.Frame(self.canvas)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Scrollbar'ı canvas'a bağla
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Yerleşim
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(10,0), pady=10)
        
        # Canvas'a frame'i ekle
        self.canvas_frame = self.canvas.create_window((0,0), window=self.main_frame, anchor="nw", width=self.canvas.winfo_width())
        
        # Event bindings
        self.main_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # İçerik oluştur
        self.create_content()
        
    def _on_frame_configure(self, event=None):
        """Frame boyutu değiştiğinde scroll bölgesini güncelle"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_canvas_configure(self, event):
        """Canvas boyutu değiştiğinde frame genişliğini güncelle"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
        
    def _on_mousewheel(self, event):
        """Mouse tekerleği ile scroll"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_content(self):
        """Pencere içeriğini oluştur"""
        current_row = 0
        
        # Başlık
        title = ttk.Label(
            self.main_frame,
            text="Eğitim Sonrası Güncellenmiş Ağ Parametreleri",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary",
            wraplength=700  # Uzun başlıklar için satır sonu
        )
        title.grid(row=current_row, column=0, pady=(0, 20), sticky="ew")
        current_row += 1
        
        # Input değerleri
        input_frame = ttk.LabelFrame(
            self.main_frame,
            text="Input Değerleri",
            bootstyle="primary"
        )
        input_frame.grid(row=current_row, column=0, sticky="ew", pady=(0, 20))
        input_frame.grid_columnconfigure(0, weight=1)
        current_row += 1
        
        # Input değerlerini grid olarak düzenle
        input_grid = ttk.Frame(input_frame)
        input_grid.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        cols_per_row = 3  # Her satırda gösterilecek input sayısı
        for i, value in enumerate(self.network_parameters['inputs']):
            row = i // cols_per_row
            col = i % cols_per_row
            input_grid.grid_columnconfigure(col, weight=1)
            
            cell_frame = ttk.Frame(input_grid)
            cell_frame.grid(row=row, column=col, padx=5, pady=2, sticky="ew")
            cell_frame.grid_columnconfigure(1, weight=1)
            
            ttk.Label(
                cell_frame,
                text=f"X{i+1}:",
                font=("Helvetica", 11)
            ).grid(row=0, column=0, padx=(0, 5))
            
            ttk.Label(
                cell_frame,
                text=f"{value:.6f}",
                font=("Helvetica", 11)
            ).grid(row=0, column=1, sticky="w")
        
        # Bias değerleri
        bias_frame = ttk.LabelFrame(
            self.main_frame,
            text="Bias Değerleri",
            bootstyle="primary"
        )
        bias_frame.grid(row=current_row, column=0, sticky="ew", pady=(0, 20))
        bias_frame.grid_columnconfigure(0, weight=1)
        current_row += 1
        
        for layer_idx, layer_biases in enumerate(self.network_parameters['biases']):
            layer_name = f"Gizli Katman {layer_idx+1}" if layer_idx < len(self.network_parameters['biases'])-1 else "Çıkış Katmanı"
            
            layer_frame = ttk.Frame(bias_frame)
            layer_frame.grid(row=layer_idx, column=0, sticky="ew", padx=10, pady=5)
            layer_frame.grid_columnconfigure(0, weight=1)
            
            ttk.Label(
                layer_frame,
                text=f"{layer_name} Bias Değerleri:",
                font=("Helvetica", 12, "bold")
            ).grid(row=0, column=0, sticky="w", pady=(5, 2))
            
            # Bias değerlerini grid olarak düzenle
            values_grid = ttk.Frame(layer_frame)
            values_grid.grid(row=1, column=0, sticky="ew", padx=20)
            
            cols_per_row = 3  # Her satırda gösterilecek bias sayısı
            for j, bias in enumerate(layer_biases):
                row = j // cols_per_row
                col = j % cols_per_row
                values_grid.grid_columnconfigure(col, weight=1)
                
                ttk.Label(
                    values_grid,
                    text=f"Nöron {j+1}: {bias:.6f}",
                    font=("Helvetica", 11)
                ).grid(row=row, column=col, padx=10, pady=2, sticky="w")
        
        # Weight değerleri
        weight_frame = ttk.LabelFrame(
            self.main_frame,
            text="Weight Değerleri",
            bootstyle="primary"
        )
        weight_frame.grid(row=current_row, column=0, sticky="ew", pady=(0, 20))
        weight_frame.grid_columnconfigure(0, weight=1)
        current_row += 1
        
        # Her katman için weight matrisi
        for layer_idx, weights in enumerate(self.network_parameters['weights']):
            from_layer = "Giriş Katmanı" if layer_idx == 0 else f"Gizli Katman {layer_idx}"
            to_layer = "Çıkış Katmanı" if layer_idx == len(self.network_parameters['weights'])-1 else f"Gizli Katman {layer_idx+1}"
            
            layer_frame = ttk.LabelFrame(
                weight_frame,
                text=f"{from_layer} → {to_layer}",
                bootstyle="secondary"
            )
            layer_frame.grid(row=layer_idx, column=0, sticky="ew", padx=10, pady=5)
            layer_frame.grid_columnconfigure(0, weight=1)
            
            # Tablo container
            table_container = ttk.Frame(layer_frame)
            table_container.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            # Her sütuna eşit ağırlık ver
            for j in range(weights.shape[1] + 1):  # +1 for row headers
                table_container.grid_columnconfigure(j, weight=1)
            
            # Sütun başlıkları
            ttk.Label(
                table_container,
                text="Nöron",
                font=("Helvetica", 10, "bold")
            ).grid(row=0, column=0, padx=5, pady=2)
            
            for j in range(weights.shape[1]):
                ttk.Label(
                    table_container,
                    text=f"X{j+1}" if layer_idx == 0 else f"H{layer_idx}{j+1}",
                    font=("Helvetica", 10, "bold")
                ).grid(row=0, column=j+1, padx=5, pady=2)
            
            # Weight değerleri
            for i in range(weights.shape[0]):
                # Satır başlığı
                ttk.Label(
                    table_container,
                    text=f"{'Y' if layer_idx == len(self.network_parameters['weights'])-1 else 'H'}{i+1}",
                    font=("Helvetica", 10, "bold")
                ).grid(row=i+1, column=0, padx=5, pady=2)
                
                # Weight değerleri
                for j in range(weights.shape[1]):
                    value_frame = ttk.Frame(table_container)
                    value_frame.grid(row=i+1, column=j+1, sticky="ew", padx=2, pady=1)
                    value_frame.grid_columnconfigure(0, weight=1)
                    
                    ttk.Label(
                        value_frame,
                        text=f"{weights[i,j]:.6f}",
                        font=("Courier", 10)
                    ).grid(row=0, column=0, sticky="ew")
        
        # Kapat butonu
        ttk.Button(
            self.main_frame,
            text="Kapat",
            bootstyle="secondary",
            command=self.destroy
        ).grid(row=current_row, column=0, pady=10) 