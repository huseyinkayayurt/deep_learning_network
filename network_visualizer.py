import tkinter as tk
from tkinter import ttk
import math

class NetworkVisualizer:
    def __init__(self, canvas, layer_sizes, padding=50):
        """
        Neural Network görselleştirici
        
        Args:
            canvas: Çizim yapılacak tkinter canvas
            layer_sizes: Her katmandaki nöron sayılarını içeren liste
            padding: Kenarlardan bırakılacak boşluk
        """
        self.canvas = canvas
        self.layer_sizes = layer_sizes
        self.padding = padding
        
        # Görsel parametreler
        self.neuron_radius = 15
        self.layer_spacing = None  # Katmanlar arası mesafe
        self.vertical_spacing = None  # Dikey nöron aralığı
        self.colors = {
            'input': "#4CAF50",    # Yeşil
            'hidden': "#2196F3",    # Mavi
            'output': "#E53935",    # Kırmızı
            'connection': "#888888"  # Gri
        }
        
    def calculate_layout(self):
        """Canvas boyutlarına göre yerleşimi hesapla"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Katmanlar arası yatay mesafe
        self.layer_spacing = (width - 2 * self.padding) / (len(self.layer_sizes) - 1)
        
        # Her katman için maksimum dikey aralık hesapla
        max_neurons = max(self.layer_sizes)
        self.vertical_spacing = min(
            (height - 2 * self.padding) / (max_neurons - 1) if max_neurons > 1 else height - 2 * self.padding,
            50  # Maksimum dikey aralık
        )
        
    def get_neuron_position(self, layer_idx, neuron_idx):
        """Belirli bir nöronun x,y koordinatlarını hesapla"""
        x = self.padding + layer_idx * self.layer_spacing
        
        layer_size = self.layer_sizes[layer_idx]
        layer_height = (layer_size - 1) * self.vertical_spacing
        y_start = (self.canvas.winfo_height() - layer_height) / 2
        y = y_start + neuron_idx * self.vertical_spacing
        
        return x, y
        
    def draw_network(self):
        """Ağ yapısını çiz"""
        self.canvas.delete("all")  # Canvas'ı temizle
        self.calculate_layout()
        
        # Bağlantıları çiz (arkada kalması için önce çiziyoruz)
        for i in range(len(self.layer_sizes) - 1):
            for j in range(self.layer_sizes[i]):
                for k in range(self.layer_sizes[i + 1]):
                    x1, y1 = self.get_neuron_position(i, j)
                    x2, y2 = self.get_neuron_position(i + 1, k)
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=self.colors['connection'],
                        width=1
                    )
        
        # Nöronları çiz
        for i, layer_size in enumerate(self.layer_sizes):
            for j in range(layer_size):
                x, y = self.get_neuron_position(i, j)
                
                # Katman tipine göre renk seç
                if i == 0:
                    color = self.colors['input']
                    label = f"X{j+1}"
                elif i == len(self.layer_sizes) - 1:
                    color = self.colors['output']
                    label = f"Y{j+1}"
                else:
                    color = self.colors['hidden']
                    label = f"H{i}{j+1}"
                
                # Nöron çemberi
                self.canvas.create_oval(
                    x - self.neuron_radius,
                    y - self.neuron_radius,
                    x + self.neuron_radius,
                    y + self.neuron_radius,
                    fill=color,
                    outline="black"
                )
                
                # Nöron etiketi
                if i == 0:  # Input layer
                    self.canvas.create_text(
                        x - self.neuron_radius - 20,
                        y,
                        text=label,
                        anchor="e"
                    )
                elif i == len(self.layer_sizes) - 1:  # Output layer
                    self.canvas.create_text(
                        x + self.neuron_radius + 20,
                        y,
                        text=label,
                        anchor="w"
                    )
        
        # Katman etiketleri
        layer_names = ["Giriş Katmanı"] + [f"Gizli Katman {i+1}" for i in range(len(self.layer_sizes)-2)] + ["Çıkış Katmanı"]
        for i, name in enumerate(layer_names):
            x = self.padding + i * self.layer_spacing
            self.canvas.create_text(
                x,
                self.padding / 2,
                text=name,
                anchor="center",
                font=("Helvetica", 10)
            ) 