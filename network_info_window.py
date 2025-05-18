import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np
import platform

class NetworkInfoWindow(tk.Toplevel):
    def __init__(self, parent, network_parameters):
        super().__init__(parent)
        
        self.parent = parent
        self.network_parameters = network_parameters
        
        # Pencere ayarları
        self.title("Ağ Parametreleri")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Ana container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=BOTH, expand=YES)
        
        # Canvas ve scrollbar
        self.canvas = tk.Canvas(self.main_container)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Scrollable frame'i canvas'a bağla
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Canvas'a frame'i yerleştir
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Canvas'ı scrollbar'a bağla
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Layout
        self.canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=5)
        
        # Canvas boyutu değiştiğinde frame genişliğini güncelle
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mousewheel event'lerini güvenli bir şekilde bağla
        self._bind_mousewheel()
        
        # Parametreleri göster
        self.show_parameters()
        
        # Pencere kapatıldığında event'leri temizle
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def _on_canvas_configure(self, event):
        """Canvas boyutu değiştiğinde frame genişliğini güncelle"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
        
    def _bind_mousewheel(self):
        # Sadece canvas'a bağla, platforma göre delta ayarla
        if platform.system() == 'Darwin':
            self.canvas.bind("<MouseWheel>", self._on_mousewheel_mac)
        else:
            self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        # Linux için ek olarak Button-4/5 de eklenebilir
        self.canvas.bind("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self):
        self.canvas.unbind("<MouseWheel>")
        self.canvas.unbind("<Button-4>")
        self.canvas.unbind("<Button-5>")

    def _on_mousewheel(self, event):
        # Windows/Linux
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_mac(self, event):
        # MacOS
        self.canvas.yview_scroll(int(-1 * (event.delta)), "units")

    def _on_mousewheel_linux(self, event):
        # Linux için Button-4/5
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        
    def on_closing(self):
        self._unbind_mousewheel()
        self.destroy()
        
    def show_parameters(self):
        """Ağ parametrelerini göster"""
        # Input değerleri
        input_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="Input Değerleri",
            bootstyle="primary"
        )
        input_frame.pack(fill=X, padx=10, pady=5)
        
        input_values = self.network_parameters['inputs']
        for i, value in enumerate(input_values):
            ttk.Label(
                input_frame,
                text=f"X{i+1}: {value:.6f}",
                font=("Helvetica", 12)
            ).pack(padx=10, pady=2)
            
        # Her katman için ağırlıklar ve bias'lar
        for i in range(len(self.network_parameters['weights'])):
            # Katman başlığı
            layer_name = "Giriş → Gizli" if i == 0 else "Gizli → Çıkış" if i == len(self.network_parameters['weights'])-1 else f"Gizli {i} → Gizli {i+1}"
            
            # Ağırlıklar
            weight_frame = ttk.LabelFrame(
                self.scrollable_frame,
                text=f"{layer_name} Ağırlıkları",
                bootstyle="primary"
            )
            weight_frame.pack(fill=X, padx=10, pady=5)
            
            weights = self.network_parameters['weights'][i]
            for j in range(weights.shape[0]):
                for k in range(weights.shape[1]):
                    ttk.Label(
                        weight_frame,
                        text=f"w{j+1}{k+1}: {weights[j,k]:.6f}",
                        font=("Helvetica", 12)
                    ).pack(padx=10, pady=2)
            
            # Bias değerleri
            bias_frame = ttk.LabelFrame(
                self.scrollable_frame,
                text=f"{layer_name} Bias Değerleri",
                bootstyle="primary"
            )
            bias_frame.pack(fill=X, padx=10, pady=5)
            
            biases = self.network_parameters['biases'][i]
            for j, bias in enumerate(biases):
                ttk.Label(
                    bias_frame,
                    text=f"b{j+1}: {bias:.6f}",
                    font=("Helvetica", 12)
                ).pack(padx=10, pady=2) 