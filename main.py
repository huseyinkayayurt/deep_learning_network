import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from network_visualizer import NetworkVisualizer
from network_parameters import NetworkParametersWindow
from network_prediction import NetworkPredictionWindow

class HiddenLayerConfig(tk.Toplevel):
    def __init__(self, parent, hidden_count, input_count, output_count):
        super().__init__(parent)
        
        self.parent = parent
        self.hidden_count = hidden_count
        self.input_count = input_count
        self.output_count = output_count
        
        # Pencere ayarları
        self.title("Gizli Katman Yapılandırması")
        self.geometry("600x500")
        self.minsize(400, 300)
        
        # Ana container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # Başlık
        title = ttk.Label(
            self.main_container,
            text="Gizli Katmanların Yapılandırması",
            font=("Helvetica", 20),
            bootstyle="primary"
        )
        title.pack(pady=(0, 20))
        
        # Açıklama
        description = ttk.Label(
            self.main_container,
            text=f"Lütfen {hidden_count} gizli katman için nöron sayılarını belirleyin",
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        description.pack(pady=(0, 20))
        
        # Scrollable frame for inputs
        self.scroll_frame = ScrolledFrame(self.main_container, autohide=True)
        self.scroll_frame.pack(fill=BOTH, expand=YES)
        
        # Input alanları
        self.inputs = []
        self.create_inputs()
        
        # Butonlar
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Temizle",
            bootstyle="secondary-outline",
            command=self.clear_form
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Yapılandırmayı Tamamla",
            bootstyle="primary",
            command=self.submit_form
        ).pack(side=LEFT, padx=5)
        
        # Modal pencere olarak ayarla
        self.transient(parent)
        self.grab_set()
        
    def create_inputs(self):
        """Hidden layer input alanlarını oluştur"""
        prev_size = self.input_count
        
        for i in range(self.hidden_count):
            frame = ttk.Frame(self.scroll_frame)
            frame.pack(fill=X, pady=5)
            
            # Label container
            label_container = ttk.Frame(frame)
            label_container.pack(side=LEFT)
            
            # Layer label
            ttk.Label(
                label_container,
                text=f"{i+1}. Gizli Katman:",
                font=("Helvetica", 12)
            ).pack(side=LEFT, padx=(0, 5))
            
            # Info icon ve tooltip
            next_size = self.output_count if i == self.hidden_count - 1 else "?"
            tooltip_text = f"Önceki Katman: {prev_size} nöron\nSonraki Katman: {next_size} nöron"
            
            info_label = ttk.Label(
                label_container,
                text="ℹ",
                font=("Helvetica", 12),
                bootstyle="info"
            )
            info_label.pack(side=LEFT, padx=(5, 0))
            
            def show_tooltip(event, tooltip=tooltip_text):
                x, y, _, _ = event.widget.bbox("insert")
                x += event.widget.winfo_rootx() + 25
                y += event.widget.winfo_rooty() + 25
                
                tip = tk.Toplevel(self)
                tip.wm_overrideredirect(True)
                tip.wm_geometry(f"+{x}+{y}")
                
                label = ttk.Label(
                    tip,
                    text=tooltip,
                    justify=LEFT,
                    font=("Helvetica", 10),
                    bootstyle="info",
                    padding=(5, 3)
                )
                label.pack()
                
                def hide_tooltip(event, window=tip):
                    window.destroy()
                
                info_label.bind('<Leave>', hide_tooltip)
                tip.bind('<Leave>', hide_tooltip)
            
            info_label.bind('<Enter>', show_tooltip)
            
            # Input container
            input_container = ttk.Frame(frame)
            input_container.pack(side=LEFT, fill=X, expand=YES, padx=10)
            
            # Entry
            entry = ttk.Entry(
                input_container,
                bootstyle="primary",
                font=("Helvetica", 12)
            )
            entry.pack(fill=X)
            
            # Error label
            error_label = ttk.Label(
                input_container,
                text="",
                font=("Helvetica", 10),
                bootstyle="danger"
            )
            error_label.pack(anchor="w")
            
            self.inputs.append({
                'entry': entry,
                'error_label': error_label
            })
            
            prev_size = "?"
            
    def clear_form(self):
        """Formu temizle"""
        for input_data in self.inputs:
            input_data['entry'].delete(0, tk.END)
            input_data['error_label'].configure(text="")
            
    def validate_input(self, value):
        """Input değerini doğrula"""
        if not value:
            return False, "Bu alan boş bırakılamaz"
        try:
            int_value = int(value)
            if int_value <= 0:
                return False, "Değer pozitif bir tam sayı olmalıdır"
            return True, None
        except ValueError:
            return False, "Lütfen geçerli bir tam sayı giriniz"
            
    def submit_form(self):
        """Form gönderme işlemi"""
        is_valid = True
        values = []
        
        # Tüm inputları doğrula
        for i, input_data in enumerate(self.inputs):
            entry = input_data['entry']
            error_label = input_data['error_label']
            
            valid, error_message = self.validate_input(entry.get())
            if not valid:
                is_valid = False
                error_label.configure(text=error_message)
                entry.configure(bootstyle="danger")
            else:
                error_label.configure(text="")
                entry.configure(bootstyle="primary")
                values.append(int(entry.get()))
        
        # Eğer form geçerliyse sonuçları göster ve pencereyi kapat
        if is_valid:
            self.parent.on_hidden_layers_configured(values)
            self.destroy()

class NeuralNetworkConfigUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Ana pencere ayarları
        self.title("YSA Yapılandırma Arayüzü")
        self.geometry("1000x800")
        self.minsize(800, 600)
        
        # Tema ve stil ayarları
        self.style = ttk.Style(theme="cosmo")
        
        # Scrollable ana container
        self.scroll_container = ScrolledFrame(self, autohide=True)
        self.scroll_container.pack(fill=BOTH, expand=YES)
        
        # Ana container (responsive için)
        self.main_container = ttk.Frame(self.scroll_container)
        self.main_container.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # Grid yapılandırması
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=0)
        self.main_container.grid_rowconfigure(2, weight=0)
        self.main_container.grid_rowconfigure(3, weight=1)
        
        # Başlık
        self.create_header()
        
        # Form alanı
        self.create_form()
        
        # Sonuç alanı
        self.create_result_area()
        
        # Visualization alanı
        self.create_visualization_area()
        
        # Ağ yapılandırması
        self.network_config = {
            'input_count': 0,
            'hidden_count': 0,
            'output_count': 0,
            'hidden_layers': []
        }
        
    def create_header(self):
        """Başlık ve açıklama bölümü"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ttk.Label(
            header_frame,
            text="Yapay Sinir Ağı Yapılandırması",
            font=("Helvetica", 24),
            bootstyle="primary"
        )
        title.pack(pady=(0, 10))
        
        description = ttk.Label(
            header_frame,
            text="Lütfen ağ yapısı için gerekli parametreleri giriniz",
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        description.pack()
        
    def create_form(self):
        """Form alanı oluşturma"""
        # Form container
        self.form_frame = ttk.Frame(self.main_container)
        self.form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Form grid yapılandırması
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        # Input alanları
        self.inputs = {}
        input_fields = [
            ("input_count", "Input Layer Nöron Sayısı:", "Giriş katmanındaki nöron sayısı"),
            ("output_count", "Output Layer Nöron Sayısı:", "Çıkış katmanındaki nöron sayısı"),
            ("hidden_count", "Hidden Layer Sayısı:", "Gizli katman sayısı")
        ]
        
        # Her input için bilgi ikonları ve açıklamaları
        tooltips = [
            "Giriş katmanındaki nöron sayısı, ağa girilecek veri boyutunu belirler",
            "Çıkış katmanındaki nöron sayısı, ağın üreteceği sonuç boyutunu belirler",
            "Gizli katman sayısı, ağın derinliğini belirler"
        ]
        
        for idx, ((key, label, placeholder), tooltip) in enumerate(zip(input_fields, tooltips)):
            # Label ve info icon container
            label_container = ttk.Frame(self.form_frame)
            label_container.grid(row=idx, column=0, padx=(0, 10), pady=10, sticky="e")
            
            # Label
            ttk.Label(
                label_container,
                text=label,
                font=("Helvetica", 12)
            ).pack(side=LEFT)
            
            # Info icon
            info_label = ttk.Label(
                label_container,
                text="ℹ",
                font=("Helvetica", 12),
                bootstyle="info"
            )
            info_label.pack(side=LEFT, padx=(5, 0))
            
            # Tooltip için binding
            def show_tooltip(event, tooltip=tooltip):
                x, y, _, _ = event.widget.bbox("insert")
                x += event.widget.winfo_rootx() + 25
                y += event.widget.winfo_rooty() + 25
                
                # Tooltip penceresi
                tip = tk.Toplevel(self)
                tip.wm_overrideredirect(True)
                tip.wm_geometry(f"+{x}+{y}")
                
                label = ttk.Label(
                    tip,
                    text=tooltip,
                    justify=LEFT,
                    font=("Helvetica", 10),
                    bootstyle="info",
                    padding=(5, 3)
                )
                label.pack()
                
                def hide_tooltip(event, window=tip):
                    window.destroy()
                
                info_label.bind('<Leave>', hide_tooltip)
                tip.bind('<Leave>', hide_tooltip)
            
            info_label.bind('<Enter>', show_tooltip)
            
            # Input container (input ve hata mesajı için)
            input_container = ttk.Frame(self.form_frame)
            input_container.grid(row=idx, column=1, sticky="ew")
            input_container.grid_columnconfigure(0, weight=1)
            
            # Input field
            entry = ttk.Entry(
                input_container,
                bootstyle="primary",
                font=("Helvetica", 12)
            )
            entry.grid(row=0, column=0, sticky="ew")
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e, entry=entry, ph=placeholder: self.on_focus_in(e, entry, ph))
            entry.bind('<FocusOut>', lambda e, entry=entry, ph=placeholder: self.on_focus_out(e, entry, ph))
            
            # Hata mesajı label'ı
            error_label = ttk.Label(
                input_container,
                text="",
                font=("Helvetica", 10),
                bootstyle="danger"
            )
            error_label.grid(row=1, column=0, sticky="w")
            
            self.inputs[key] = {
                'entry': entry,
                'error_label': error_label,
                'placeholder': placeholder
            }
        
        # Butonlar
        self.button_frame = ttk.Frame(self.form_frame)
        self.button_frame.grid(row=len(input_fields), column=0, columnspan=2, pady=20)
        
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Temizle",
            bootstyle="secondary-outline",
            command=self.clear_form
        )
        self.clear_button.pack(side=LEFT, padx=5)
        
        self.submit_button = ttk.Button(
            self.button_frame,
            text="Yapılandırmayı Onayla",
            bootstyle="primary",
            command=self.submit_form
        )
        self.submit_button.pack(side=LEFT, padx=5)
        
    def create_result_area(self):
        """Sonuç gösterim alanı"""
        self.result_frame = ttk.LabelFrame(
            self.main_container,
            text="Ağ Yapılandırması",
            bootstyle="primary"
        )
        self.result_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        self.result_label = ttk.Label(
            self.result_frame,
            text="Henüz yapılandırma girilmedi",
            font=("Helvetica", 12),
            bootstyle="secondary",
            justify=LEFT
        )
        self.result_label.pack(pady=10, padx=10, anchor=W)
        
    def create_visualization_area(self):
        """Ağ görselleştirme alanı"""
        self.viz_frame = ttk.LabelFrame(
            self.main_container,
            text="Ağ Görselleştirmesi",
            bootstyle="primary"
        )
        self.viz_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 20))
        
        # Canvas
        self.viz_canvas = tk.Canvas(
            self.viz_frame,
            width=800,
            height=400,
            bg="white"
        )
        self.viz_canvas.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
    def update_visualization(self):
        """Ağ görselleştirmesini güncelle"""
        if not hasattr(self, 'viz_canvas'):
            return
            
        layer_sizes = [
            self.network_config['input_count'],
            *self.network_config['hidden_layers'],
            self.network_config['output_count']
        ]
        
        visualizer = NetworkVisualizer(self.viz_canvas, layer_sizes)
        visualizer.draw_network()
        
    def on_focus_in(self, event, entry, placeholder):
        """Input focus olduğunda placeholder'ı temizle"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(bootstyle="primary")
            
    def on_focus_out(self, event, entry, placeholder):
        """Input focus'tan çıkınca boşsa placeholder'ı göster"""
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(bootstyle="primary")
            
    def clear_form(self):
        """Formu temizle"""
        for input_data in self.inputs.values():
            entry = input_data['entry']
            entry.delete(0, tk.END)
            entry.insert(0, input_data['placeholder'])
            input_data['error_label'].configure(text="")
            entry.configure(bootstyle="primary")
        
        self.result_label.configure(text="Henüz yapılandırma girilmedi")
        if hasattr(self, 'viz_canvas'):
            self.viz_canvas.delete("all")
        
    def validate_input(self, value, placeholder):
        """Input değerini doğrula"""
        if value == "" or value == placeholder:
            return False, "Bu alan boş bırakılamaz"
        try:
            int_value = int(value)
            if int_value <= 0:
                return False, "Değer pozitif bir tam sayı olmalıdır"
            return True, None
        except ValueError:
            return False, "Lütfen geçerli bir tam sayı giriniz"
            
    def submit_form(self):
        """Form gönderme işlemi"""
        is_valid = True
        values = {}
        
        # Tüm inputları doğrula
        for key, input_data in self.inputs.items():
            entry = input_data['entry']
            error_label = input_data['error_label']
            placeholder = input_data['placeholder']
            
            valid, error_message = self.validate_input(entry.get(), placeholder)
            if not valid:
                is_valid = False
                error_label.configure(text=error_message)
                entry.configure(bootstyle="danger")
            else:
                error_label.configure(text="")
                entry.configure(bootstyle="primary")
                values[key] = int(entry.get())
        
        # Eğer form geçerliyse hidden layer yapılandırma penceresini aç
        if is_valid:
            self.network_config.update({
                'input_count': values['input_count'],
                'hidden_count': values['hidden_count'],
                'output_count': values['output_count']
            })
            
            # Hidden layer yapılandırma penceresini aç
            hidden_config = HiddenLayerConfig(
                self,
                values['hidden_count'],
                values['input_count'],
                values['output_count']
            )
            
    def on_hidden_layers_configured(self, hidden_layers):
        """Hidden layer yapılandırması tamamlandığında çağrılır"""
        self.network_config['hidden_layers'] = hidden_layers
        
        # Sonuç metnini güncelle
        result_text = "Ağ Yapılandırması:\n\n"
        result_text += f"• Giriş Katmanı: {self.network_config['input_count']} nöron\n"
        result_text += "• Gizli Katmanlar:\n"
        
        for i, neurons in enumerate(hidden_layers):
            result_text += f"  - Katman {i+1}: {neurons} nöron\n"
            
        result_text += f"• Çıkış Katmanı: {self.network_config['output_count']} nöron"
        
        self.result_label.configure(text=result_text)
        
        # Görselleştirmeyi güncelle
        self.update_visualization()
        
        # Parametre penceresini aç
        self.open_parameters_window()
        
    def open_parameters_window(self):
        """Ağ parametreleri penceresini aç"""
        parameters_window = NetworkParametersWindow(self, self.network_config)
        
    def on_parameters_configured(self, parameters):
        """Ağ parametreleri yapılandırıldığında çağrılır"""
        self.network_parameters = parameters
        messagebox.showinfo(
            "Parametreler Kaydedildi",
            "Ağ parametreleri başarıyla kaydedildi!"
        )
        
        # Tahmin penceresini aç
        prediction_window = NetworkPredictionWindow(
            self,
            parameters,
            self.network_config['output_count']
        )

if __name__ == "__main__":
    app = NeuralNetworkConfigUI()
    app.mainloop() 