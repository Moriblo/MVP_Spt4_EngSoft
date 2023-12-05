import numpy as np
import pickle
import joblib

class Model:
    
    def carrega_modelo(self, pathmodel, pathscaler):
        # Carrega modelo CART
        with open(pathmodel, "rb") as f:
            modelo = pickle.load(f)
        # Carrega scaler utilizado
        with open(pathscaler, "rb") as s:
            scaler = pickle.load(s)
        
        return modelo, scaler