import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import numpy as np


class NetworkParametersWindow(tk.Toplevel):
    def __init__(self, parent, network_config):
        super().__init__(parent)

        self.parent = parent
        self.network_config = network_config
        self.layer_sizes = [
            network_config['input_count'],
            *network_config['hidden_layers'],
            network_config['output_count']
        ]

        self.title("Ağ Parametreleri")
        self.geometry("1000x800")
        self.minsize(800, 600)

        self.scroll_container = ScrolledFrame(self, autohide=True)
        self.scroll_container.pack(fill=BOTH, expand=YES)

        self.main_container = ttk.Frame(self.scroll_container)
        self.main_container.pack(fill=BOTH, expand=YES, padx=20, pady=20)

        self.input_entries = []
        self.bias_entries = []
        self.weight_entries = []

        self.create_input_section()
        self.create_bias_section()
        self.create_weight_section()
        self.create_buttons()

    def create_input_section(self):
        """Input değerleri için matris"""
        frame = ttk.LabelFrame(
            self.main_container,
            text="Input Değerleri",
            bootstyle="primary"
        )
        frame.pack(fill=X, pady=(0, 20))

        input_size = self.layer_sizes[0]
        entries_frame = ttk.Frame(frame)
        entries_frame.pack(fill=X, padx=10, pady=10)

        ttk.Label(
            entries_frame,
            text="X değerleri:",
            font=("Helvetica", 12)
        ).pack(side=LEFT, padx=(0, 10))

        for i in range(input_size):
            entry = ttk.Entry(
                entries_frame,
                width=8,
                bootstyle="primary"
            )
            entry.pack(side=LEFT, padx=2)
            entry.insert(0, "0.0")
            self.input_entries.append(entry)

    def create_bias_section(self):
        """Her layer için bias değerleri"""
        frame = ttk.LabelFrame(
            self.main_container,
            text="Bias Değerleri",
            bootstyle="primary"
        )
        frame.pack(fill=X, pady=(0, 20))

        for i in range(1, len(self.layer_sizes)):
            layer_frame = ttk.Frame(frame)
            layer_frame.pack(fill=X, padx=10, pady=5)

            layer_name = "Gizli Katman" if i < len(self.layer_sizes) - 1 else "Çıkış Katmanı"
            ttk.Label(
                layer_frame,
                text=f"{layer_name} {i if i < len(self.layer_sizes) - 1 else ''} Bias:",
                font=("Helvetica", 12)
            ).pack(side=LEFT, padx=(0, 10))

            layer_biases = []
            for j in range(self.layer_sizes[i]):
                entry = ttk.Entry(
                    layer_frame,
                    width=8,
                    bootstyle="primary"
                )
                entry.pack(side=LEFT, padx=2)
                entry.insert(0, "0.0")
                layer_biases.append(entry)

            self.bias_entries.append(layer_biases)

    def create_weight_section(self):
        """Katmanlar arası weight değerleri"""
        frame = ttk.LabelFrame(
            self.main_container,
            text="Weight Değerleri",
            bootstyle="primary"
        )
        frame.pack(fill=X, pady=(0, 20))

        for i in range(len(self.layer_sizes) - 1):
            layer_frame = ttk.LabelFrame(
                frame,
                text=self.get_weight_matrix_label(i),
                bootstyle="secondary"
            )
            layer_frame.pack(fill=X, padx=10, pady=10)

            matrix_frame = ttk.Frame(layer_frame)
            matrix_frame.pack(padx=10, pady=10)

            layer_weights = []
            for j in range(self.layer_sizes[i + 1]):
                row_weights = []
                row_frame = ttk.Frame(matrix_frame)
                row_frame.pack()

                for k in range(self.layer_sizes[i]):
                    entry = ttk.Entry(
                        row_frame,
                        width=8,
                        bootstyle="primary"
                    )
                    entry.grid(row=j, column=k, padx=2, pady=2)
                    entry.insert(0, "0.0")
                    row_weights.append(entry)

                layer_weights.append(row_weights)

            self.weight_entries.append(layer_weights)

    def get_weight_matrix_label(self, layer_idx):
        """Weight matrisi için etiket oluştur"""
        if layer_idx == 0:
            return "Giriş Katmanı → 1. Gizli Katman"
        elif layer_idx == len(self.layer_sizes) - 2:
            if len(self.layer_sizes) == 3:  # Tek gizli katman
                return "1. Gizli Katman → Çıkış Katmanı"
            else:
                return f"{layer_idx}. Gizli Katman → Çıkış Katmanı"
        else:
            return f"{layer_idx}. Gizli Katman → {layer_idx + 1}. Gizli Katman"

    def create_buttons(self):
        """Butonlar"""
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Rastgele Değerler Ata",
            bootstyle="info",
            command=self.randomize_values
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Temizle",
            bootstyle="secondary-outline",
            command=self.clear_values
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Parametreleri Onayla",
            bootstyle="primary",
            command=self.submit_parameters
        ).pack(side=LEFT, padx=5)

    def randomize_values(self):
        """Tüm değerlere rastgele sayılar ata"""

        def get_scale(n_in, n_out):
            return np.sqrt(2.0 / (n_in + n_out))

        for entry in self.input_entries:
            entry.delete(0, tk.END)
            entry.insert(0, f"{np.random.uniform(-1, 1):.3f}")

        for layer_biases in self.bias_entries:
            for entry in layer_biases:
                entry.delete(0, tk.END)
                entry.insert(0, f"{np.random.uniform(0, 0.1):.3f}")

        for i, layer_weights in enumerate(self.weight_entries):
            n_in = self.layer_sizes[i]
            n_out = self.layer_sizes[i + 1]
            scale = get_scale(n_in, n_out)

            for row_weights in layer_weights:
                for entry in row_weights:
                    entry.delete(0, tk.END)
                    value = np.random.normal(0, scale)
                    entry.insert(0, f"{value:.3f}")

    def clear_values(self):
        """Tüm değerleri sıfırla"""
        for entry in self.input_entries:
            entry.delete(0, tk.END)
            entry.insert(0, "0.0")

        for layer_biases in self.bias_entries:
            for entry in layer_biases:
                entry.delete(0, tk.END)
                entry.insert(0, "0.0")

        for layer_weights in self.weight_entries:
            for row_weights in layer_weights:
                for entry in row_weights:
                    entry.delete(0, tk.END)
                    entry.insert(0, "0.0")

    def validate_float(self, value):
        """Girilen değerin float olup olmadığını kontrol et"""
        try:
            float(value)
            return True, None
        except ValueError:
            return False, "Lütfen geçerli bir sayı giriniz"

    def submit_parameters(self):
        """Parametreleri topla ve kontrol et"""
        try:
            input_values = []
            for entry in self.input_entries:
                valid, error = self.validate_float(entry.get())
                if not valid:
                    messagebox.showerror("Hata", f"Input değeri hatalı: {error}")
                    return
                input_values.append(float(entry.get()))

            bias_values = []
            for layer_biases in self.bias_entries:
                layer_bias = []
                for entry in layer_biases:
                    valid, error = self.validate_float(entry.get())
                    if not valid:
                        messagebox.showerror("Hata", f"Bias değeri hatalı: {error}")
                        return
                    layer_bias.append(float(entry.get()))
                bias_values.append(np.array(layer_bias))

            weight_values = []
            for layer_idx, layer_weights in enumerate(self.weight_entries):
                layer_weight = []
                for row_weights in layer_weights:
                    row = []
                    for entry in row_weights:
                        valid, error = self.validate_float(entry.get())
                        if not valid:
                            messagebox.showerror("Hata", f"Weight değeri hatalı: {error}")
                            return
                        row.append(float(entry.get()))
                    layer_weight.append(row)
                weight_values.append(np.array(layer_weight))
                print(f"Layer {layer_idx} weight matrix shape: {np.array(layer_weight).shape}")

            network_parameters = {
                'inputs': np.array(input_values),
                'biases': bias_values,
                'weights': weight_values
            }

            print("\nNetwork parameter shapes:")
            print(f"Inputs shape: {network_parameters['inputs'].shape}")
            for i in range(len(network_parameters['weights'])):
                print(f"Layer {i}:")
                print(f"  Weight shape: {network_parameters['weights'][i].shape}")
                print(f"  Bias shape: {network_parameters['biases'][i].shape}")

            self.parent.on_parameters_configured(network_parameters)
            self.destroy()

        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {str(e)}") 