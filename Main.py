import NeuralNet
import VolatilitySurface

#take user input for the barrier option they want to know the price of
#generate a european price using the volatility surface
#input european price and params into neural net to generate barrier price

ticker = input("Ticker:")
K = input("Strike Price:")
B = input("Knock-out Price:")
T = input("Days until expiration:")

r = VolatilitySurface.Get_Risk_Free_Rate()
price = VolatilitySurface.Get_Price(ticker)

European_Price = VolatilitySurface.European_Price(ticker, K, T)
print(NeuralNet.Make_Prediction(r, T, price, K, B, European_Price ))