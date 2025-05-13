import numpy as np

class ActivationFunctions:
    @staticmethod
    def relu(x):
        """ReLU aktivasyon fonksiyonu"""
        return np.maximum(0, x)
    
    @staticmethod
    def relu_derivative(x):
        """ReLU fonksiyonunun türevi"""
        return np.where(x > 0, 1, 0)
        
    @staticmethod
    def sigmoid(x):
        """Sigmoid aktivasyon fonksiyonu"""
        return 1 / (1 + np.exp(-x))
    
    @staticmethod
    def sigmoid_derivative(x):
        """Sigmoid fonksiyonunun türevi"""
        sigmoid_x = ActivationFunctions.sigmoid(x)
        return sigmoid_x * (1 - sigmoid_x)

class LossFunctions:
    @staticmethod
    def mse(y_pred, y_true):
        """Mean Square Error loss fonksiyonu"""
        return np.mean((y_pred - y_true) ** 2)
    
    @staticmethod
    def mse_derivative(y_pred, y_true):
        """MSE fonksiyonunun türevi"""
        return 2 * (y_pred - y_true) / y_pred.size
        
    @staticmethod
    def cross_entropy(y_pred, y_true):
        """Cross Entropy loss fonksiyonu
        
        Numerik stabilite için epsilon değeri kullanılır
        y_pred değerleri 0-1 arasında olmalıdır (sigmoid sonrası)
        """
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  # Numerik stabilite için
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    
    @staticmethod
    def cross_entropy_derivative(y_pred, y_true):
        """Cross Entropy fonksiyonunun türevi
        
        Numerik stabilite için epsilon değeri kullanılır
        y_pred değerleri 0-1 arasında olmalıdır (sigmoid sonrası)
        """
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        return -(y_true / y_pred - (1 - y_true) / (1 - y_pred)) / y_pred.size

class NeuralNetwork:
    def __init__(self, weights, biases, activation_func, activation_derivative, loss_func, loss_derivative, learning_rate=0.01):
        self.weights = weights
        self.biases = biases
        self.activation_func = activation_func
        self.activation_derivative = activation_derivative
        self.loss_func = loss_func
        self.loss_derivative = loss_derivative
        self.learning_rate = learning_rate
        
    def forward_propagation(self, inputs):
        """İleri yayılım"""
        self.layer_inputs = []  # Her katmanın girişi
        self.layer_outputs = []  # Her katmanın çıkışı
        
        current_values = inputs
        self.layer_outputs.append(current_values)
        
        for i in range(len(self.weights)):
            # Ağırlıklı toplam
            z = np.dot(self.weights[i], current_values)
            z = z + self.biases[i]
            self.layer_inputs.append(z)
            
            # Aktivasyon fonksiyonu
            current_values = self.activation_func(z)
            self.layer_outputs.append(current_values)
            
        return current_values
    
    def backward_propagation(self, x, y):
        """Geri yayılım"""
        m = y.shape[0]
        
        # Çıkış katmanındaki hata
        delta = self.loss_derivative(self.layer_outputs[-1], y) * \
                self.activation_derivative(self.layer_inputs[-1])
        
        # Ağırlık ve bias güncellemeleri için gradyanları sakla
        weight_gradients = []
        bias_gradients = []
        
        # Çıkış katmanından giriş katmanına doğru
        for i in range(len(self.weights) - 1, -1, -1):
            # Ağırlık gradyanı
            weight_grad = np.outer(delta, self.layer_outputs[i])
            weight_gradients.insert(0, weight_grad)
            
            # Bias gradyanı
            bias_gradients.insert(0, delta)
            
            if i > 0:
                # Bir önceki katman için delta hesapla
                delta = np.dot(self.weights[i].T, delta) * \
                        self.activation_derivative(self.layer_inputs[i-1])
        
        # Ağırlıkları ve bias'ları güncelle
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * weight_gradients[i]
            self.biases[i] -= self.learning_rate * bias_gradients[i]
    
    def train(self, x, y, epochs):
        """Ağı eğit"""
        loss_history = []
        
        for epoch in range(epochs):
            # İleri yayılım
            output = self.forward_propagation(x)
            
            # Loss hesapla
            current_loss = self.loss_func(output, y)
            loss_history.append(current_loss)
            
            # Geri yayılım
            self.backward_propagation(x, y)
        
        return loss_history

# Kullanılabilir fonksiyonlar
ACTIVATION_FUNCTIONS = {
    "ReLU": (ActivationFunctions.relu, ActivationFunctions.relu_derivative),
    "Sigmoid": (ActivationFunctions.sigmoid, ActivationFunctions.sigmoid_derivative)
}

LOSS_FUNCTIONS = {
    "Mean Square Error": (LossFunctions.mse, LossFunctions.mse_derivative),
    "Cross Entropy": (LossFunctions.cross_entropy, LossFunctions.cross_entropy_derivative)
} 