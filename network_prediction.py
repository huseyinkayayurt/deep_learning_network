import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import numpy as np
from network_functions import ACTIVATION_FUNCTIONS, LOSS_FUNCTIONS, NeuralNetwork
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class NetworkPredictionWindow(tk.Toplevel):
    def __init__(self, parent, network_parameters, output_count):
        super().__init__(parent)

        self.parent = parent
        self.network_parameters = network_parameters
        self.output_count = output_count

        self.title("Ağ Tahmin Sonuçları")
        self.geometry("1000x800")
        self.minsize(800, 600)

        self.scroll_container = ScrolledFrame(self, autohide=True)
        self.scroll_container.pack(fill=BOTH, expand=YES)

        self.main_container = ttk.Frame(self.scroll_container)
        self.main_container.pack(fill=BOTH, expand=YES, padx=20, pady=20)

        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(4, weight=1)  # Loss plot için

        self.create_function_selection()

        self.create_actual_values_section()

        self.create_prediction_section()

        self.create_training_section()

        self.create_loss_plot()

        self.create_buttons()

        self.transient(parent)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_function_selection(self):
        """Aktivasyon ve loss fonksiyonu seçim bölümü"""
        frame = ttk.LabelFrame(
            self.main_container,
            text="Fonksiyon Seçimleri",
            bootstyle="primary"
        )
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(
            frame,
            text="Aktivasyon Fonksiyonu:",
            font=("Helvetica", 12)
        ).grid(row=0, column=0, padx=(10, 10), pady=5, sticky="w")

        self.activation_var = tk.StringVar(value=list(ACTIVATION_FUNCTIONS.keys())[0])
        activation_combo = ttk.Combobox(
            frame,
            textvariable=self.activation_var,
            values=list(ACTIVATION_FUNCTIONS.keys()),
            state="readonly",
            width=20
        )
        activation_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(
            frame,
            text="Loss Fonksiyonu:",
            font=("Helvetica", 12)
        ).grid(row=1, column=0, padx=(10, 10), pady=5, sticky="w")

        self.loss_var = tk.StringVar(value=list(LOSS_FUNCTIONS.keys())[0])
        loss_combo = ttk.Combobox(
            frame,
            textvariable=self.loss_var,
            values=list(LOSS_FUNCTIONS.keys()),
            state="readonly",
            width=20
        )
        loss_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    def create_actual_values_section(self):
        """Gerçek değerler bölümü"""
        frame = ttk.LabelFrame(
            self.main_container,
            text="Gerçek Değerler",
            bootstyle="primary"
        )
        frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        frame.grid_columnconfigure(1, weight=1)

        self.actual_entries = []

        for i in range(self.output_count):
            ttk.Label(
                frame,
                text=f"Y{i + 1} Gerçek Değeri:",
                font=("Helvetica", 12)
            ).grid(row=i, column=0, padx=(10, 10), pady=5, sticky="w")

            entry = ttk.Entry(
                frame,
                width=12,
                bootstyle="primary"
            )
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entry.insert(0, "0.0")
            entry.bind('<KeyRelease>', self.check_actual_values)
            self.actual_entries.append(entry)

    def create_prediction_section(self):
        """Tahmin sonuçları bölümü"""
        self.prediction_frame = ttk.LabelFrame(
            self.main_container,
            text="Tahmin Sonuçları",
            bootstyle="primary"
        )
        self.prediction_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        self.prediction_frame.grid_columnconfigure(0, weight=1)

        self.predict_button = ttk.Button(
            self.prediction_frame,
            text="Tahmin Et",
            bootstyle="info",
            command=self.show_predictions,
            state="disabled"
        )
        self.predict_button.grid(row=0, column=0, pady=10)

        self.results_frame = ttk.Frame(self.prediction_frame)
        self.results_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.results_frame.grid_remove()

        self.results_frame.grid_columnconfigure(1, weight=1)

    def create_training_section(self):
        """Eğitim ayarları bölümü"""
        frame = ttk.LabelFrame(
            self.main_container,
            text="Eğitim Ayarları",
            bootstyle="primary"
        )
        frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))

        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(
            frame,
            text="Epoch Sayısı:",
            font=("Helvetica", 12)
        ).grid(row=0, column=0, padx=(10, 10), pady=5, sticky="w")

        self.epoch_var = tk.StringVar(value="100")
        epoch_entry = ttk.Entry(
            frame,
            textvariable=self.epoch_var,
            width=10
        )
        epoch_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(
            frame,
            text="Learning Rate:",
            font=("Helvetica", 12)
        ).grid(row=1, column=0, padx=(10, 10), pady=5, sticky="w")

        self.lr_var = tk.StringVar(value="0.01")
        lr_entry = ttk.Entry(
            frame,
            textvariable=self.lr_var,
            width=10
        )
        lr_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(
            frame,
            text="Eğitimi Başlat",
            bootstyle="success",
            command=self.train_network
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def create_loss_plot(self):
        """Loss grafiği bölümü"""
        frame = ttk.LabelFrame(
            self.main_container,
            text="Eğitim Loss Grafiği",
            bootstyle="primary"
        )
        frame.grid(row=4, column=0, sticky="nsew", pady=(0, 20))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.ax.set_xlabel('Epoch')
        self.ax.set_ylabel('Loss')
        self.ax.set_title('Eğitim Loss Değişimi')
        self.ax.grid(True)
        self.canvas.draw()

    def create_buttons(self):
        """Butonlar"""
        button_frame = ttk.Frame(self.main_container)
        button_frame.grid(row=5, column=0, pady=20)

        ttk.Button(
            button_frame,
            text="Karşılaştırmayı Göster",
            bootstyle="primary",
            command=self.show_comparison
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Kapat",
            bootstyle="secondary-outline",
            command=self.destroy
        ).pack(side=LEFT, padx=5)

    def calculate_predictions(self):
        """İleri yayılım ile tahminleri hesapla"""
        try:
            current_values = self.network_parameters['inputs']

            for i in range(len(self.network_parameters['weights'])):
                z = np.dot(self.network_parameters['weights'][i], current_values)

                z = z + self.network_parameters['biases'][i]

                current_values = ACTIVATION_FUNCTIONS[self.activation_var.get()][0](z)

            return current_values

        except Exception as e:
            print(f"Tahmin hesaplanırken hata: {str(e)}")
            return np.zeros(self.output_count)

    def update_predictions(self):
        """Tahminleri güncelle ve göster"""
        try:
            predicted_values = self.calculate_predictions()

            if not self.results_frame.winfo_viewable():
                self.results_frame.grid()

            for widget in self.results_frame.winfo_children():
                widget.destroy()

            self.results_frame.grid_columnconfigure(0, weight=1)

            for i in range(self.output_count):
                result_frame = ttk.Frame(self.results_frame)
                result_frame.grid(row=i, column=0, sticky="ew", pady=2)
                result_frame.grid_columnconfigure(1, weight=1)

                ttk.Label(
                    result_frame,
                    text=f"Y{i + 1}:",
                    font=("Helvetica", 12, "bold")
                ).grid(row=0, column=0, padx=(0, 10))

                ttk.Label(
                    result_frame,
                    text=f"Tahmin: {predicted_values[i]:.6f}",
                    font=("Helvetica", 12)
                ).grid(row=0, column=1, sticky="w")

        except Exception as e:
            messagebox.showerror("Hata", f"Tahminler güncellenirken bir hata oluştu: {str(e)}")

    def validate_float(self, value):
        """Girilen değerin float olup olmadığını kontrol et"""
        try:
            float(value)
            return True, None
        except ValueError:
            return False, "Lütfen geçerli bir sayı giriniz"

    def show_predictions(self):
        """Tahminleri hesapla ve göster"""
        try:
            actual_values = []
            for entry in self.actual_entries:
                valid, error = self.validate_float(entry.get())
                if not valid:
                    messagebox.showerror("Hata", f"Gerçek değer hatalı: {error}")
                    return
                actual_values.append(float(entry.get()))

            predicted_values = self.calculate_predictions()

            loss_func = LOSS_FUNCTIONS[self.loss_var.get()][0]
            loss_value = loss_func(predicted_values, np.array(actual_values))

            for widget in self.results_frame.winfo_children():
                widget.destroy()
            self.results_frame.grid()

            self.results_frame.grid_columnconfigure(0, weight=1)

            for i in range(self.output_count):
                result_frame = ttk.Frame(self.results_frame)
                result_frame.grid(row=i, column=0, sticky="ew", pady=2)
                result_frame.grid_columnconfigure(3, weight=1)

                ttk.Label(
                    result_frame,
                    text=f"Y{i + 1}:",
                    font=("Helvetica", 12, "bold")
                ).grid(row=0, column=0, padx=(0, 10))

                ttk.Label(
                    result_frame,
                    text=f"Tahmin: {predicted_values[i]:.6f}",
                    font=("Helvetica", 12)
                ).grid(row=0, column=1, padx=(0, 20))

                ttk.Label(
                    result_frame,
                    text=f"Gerçek: {actual_values[i]:.6f}",
                    font=("Helvetica", 12)
                ).grid(row=0, column=2, padx=(0, 20))

                ttk.Label(
                    result_frame,
                    text=f"Fark: {abs(predicted_values[i] - actual_values[i]):.6f}",
                    font=("Helvetica", 12)
                ).grid(row=0, column=3, sticky="w")

            loss_frame = ttk.Frame(self.results_frame)
            loss_frame.grid(row=self.output_count, column=0, sticky="ew", pady=(10, 0))
            loss_frame.grid_columnconfigure(0, weight=1)

            ttk.Label(
                loss_frame,
                text=f"Loss Değeri: {loss_value:.6f}",
                font=("Helvetica", 12, "bold"),
                bootstyle="info"
            ).grid(row=0, column=0, sticky="w")

        except Exception as e:
            messagebox.showerror("Hata", f"Tahmin hesaplanırken bir hata oluştu: {str(e)}")

    def show_comparison(self):
        """Tahmin ve gerçek değerleri karşılaştır"""
        try:
            actual_values = []
            for entry in self.actual_entries:
                valid, error = self.validate_float(entry.get())
                if not valid:
                    messagebox.showerror("Hata", f"Gerçek değer hatalı: {error}")
                    return
                actual_values.append(float(entry.get()))

            predicted_values = self.calculate_predictions()

            loss_func = LOSS_FUNCTIONS[self.loss_var.get()][0]
            loss_value = loss_func(predicted_values, np.array(actual_values))

            result = "Karşılaştırma Sonuçları:\n\n"
            result += f"Seçilen Aktivasyon Fonksiyonu: {self.activation_var.get()}\n"
            result += f"Seçilen Loss Fonksiyonu: {self.loss_var.get()}\n\n"

            for i in range(self.output_count):
                result += f"Y{i + 1}:\n"
                result += f"  Tahmin: {predicted_values[i]:.6f}\n"
                result += f"  Gerçek: {actual_values[i]:.6f}\n"
                result += f"  Fark: {abs(predicted_values[i] - actual_values[i]):.6f}\n\n"

            result += f"Loss Değeri: {loss_value:.6f}"

            messagebox.showinfo("Sonuçlar", result)

        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {str(e)}")

    def update_loss_plot(self, loss_history):
        """Loss grafiğini güvenli bir şekilde güncelle"""
        try:
            self.ax.clear()

            self.ax.plot(loss_history, 'b-', label='Loss')
            self.ax.set_xlabel('Epoch')
            self.ax.set_ylabel('Loss')
            self.ax.set_title('Eğitim Loss Değişimi')
            self.ax.grid(True)

            if len(loss_history) > 0:
                ymin = min(loss_history)
                ymax = max(loss_history)
                if ymin == ymax:
                    margin = abs(ymin) * 0.1 if ymin != 0 else 0.1
                else:
                    margin = (ymax - ymin) * 0.1
                self.ax.set_ylim([ymin - margin, ymax + margin])

            self.ax.set_xlim([0, len(loss_history)])

            self.fig.tight_layout()

            self.canvas.draw()

        except Exception as e:
            print(f"Grafik güncellenirken hata: {str(e)}")

    def on_closing(self):
        """Pencere kapatılırken matplotlib figure'ı temizle"""
        try:
            plt.close(self.fig)
        except:
            pass
        self.destroy()

    def train_network(self):
        """Ağı eğit - input ve bias değerleri sabit kalır"""
        try:
            epochs = int(self.epoch_var.get())
            if epochs <= 0:
                messagebox.showerror("Hata", "Epoch sayısı pozitif bir tam sayı olmalıdır")
                return

            learning_rate = float(self.lr_var.get())
            if learning_rate <= 0:
                messagebox.showerror("Hata", "Learning rate pozitif bir sayı olmalıdır")
                return

            actual_values = []
            for entry in self.actual_entries:
                valid, error = self.validate_float(entry.get())
                if not valid:
                    messagebox.showerror("Hata", f"Gerçek değer hatalı: {error}")
                    return
                actual_values.append(float(entry.get()))

            activation_name = self.activation_var.get()
            loss_name = self.loss_var.get()

            activation_func, activation_derivative = ACTIVATION_FUNCTIONS[activation_name]
            loss_func, loss_derivative = LOSS_FUNCTIONS[loss_name]

            original_inputs = self.network_parameters['inputs'].copy()
            original_biases = [bias.copy() for bias in self.network_parameters['biases']]

            network = NeuralNetwork(
                weights=self.network_parameters['weights'].copy(),
                biases=original_biases,
                activation_func=activation_func,
                activation_derivative=activation_derivative,
                loss_func=loss_func,
                loss_derivative=loss_derivative,
                learning_rate=learning_rate
            )

            progress_window = tk.Toplevel(self)
            progress_window.title("Eğitim İlerlemesi")
            progress_window.geometry("300x150")
            progress_window.transient(self)

            progress_label = ttk.Label(
                progress_window,
                text="Eğitim devam ediyor...",
                font=("Helvetica", 12)
            )
            progress_label.pack(pady=10)

            progress_bar = ttk.Progressbar(
                progress_window,
                length=200,
                mode='determinate'
            )
            progress_bar.pack(pady=10)

            loss_label = ttk.Label(
                progress_window,
                text="Loss: -",
                font=("Helvetica", 12)
            )
            loss_label.pack(pady=10)

            loss_history = []
            update_interval = max(1, epochs // 100)

            for epoch in range(epochs):
                output = network.forward_propagation(original_inputs)
                current_loss = network.loss_func(output, np.array(actual_values))
                network.backward_propagation(original_inputs, np.array(actual_values))

                loss_history.append(float(current_loss))

                if epoch % update_interval == 0:
                    progress = (epoch + 1) / epochs * 100
                    progress_bar['value'] = progress
                    loss_label['text'] = f"Loss: {current_loss:.6f}"
                    progress_window.update()

                    if epoch % (update_interval * 10) == 0:
                        self.update_loss_plot(loss_history)

            progress_window.destroy()

            self.after(100, lambda: self.update_loss_plot(loss_history))

            self.network_parameters['weights'] = network.weights
            self.network_parameters['inputs'] = original_inputs
            self.network_parameters['biases'] = original_biases

            print("\nGüncellenmiş Ağırlıklar:")
            for i, weights in enumerate(self.network_parameters['weights']):
                layer_name = "Giriş → Gizli" if i == 0 else "Gizli → Çıkış" if i == len(
                    self.network_parameters['weights']) - 1 else f"Gizli {i} → Gizli {i + 1}"
                print(f"\n{layer_name} Katmanı Ağırlıkları:")
                print(weights)

            self.after(200, self.update_predictions)

            def show_completion_and_params():
                messagebox.showinfo(
                    "Eğitim Tamamlandı",
                    f"Eğitim {epochs} epoch sonunda tamamlandı.\nSon loss değeri: {loss_history[-1]:.6f}"
                )
                self.show_updated_parameters()

            self.after(300, show_completion_and_params)

        except Exception as e:
            messagebox.showerror("Hata", f"Eğitim sırasında bir hata oluştu: {str(e)}")

    def show_updated_parameters(self):
        """Güncellenmiş parametreleri yeni bir pencerede göster"""
        try:
            from network_info_window import NetworkInfoWindow
            info_window = NetworkInfoWindow(self, self.network_parameters)

        except Exception as e:
            messagebox.showerror("Hata", f"Parametre penceresi açılırken bir hata oluştu: {str(e)}")

    def check_actual_values(self, event=None):
        """Gerçek değerlerin geçerliliğini kontrol et"""
        all_valid = True

        for entry in self.actual_entries:
            value = entry.get()
            try:
                float(value)
            except ValueError:
                all_valid = False
                break

        self.predict_button.configure(state="normal" if all_valid else "disabled") 