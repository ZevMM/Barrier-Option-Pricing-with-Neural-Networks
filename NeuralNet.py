import keras
from keras import layers

model = keras.Sequential (
    [
        layers.Dense(32, activation = "relu", input_shape=(6,)),
        layers.Dense(16),
        layers.Dense(1)
    ]
)

def Train_Net():
    file = open("Simulated_Price_Data", "r")
    cases = file.readlines()
    file.close()
    xcases = []
    ycases = []

    for case in cases:
        data = case.split(" ")
        xtoappend = [float(x) for x in data[:-1]]
        ytoappend = [float(data[-1][:-2])]
        xcases.append(xtoappend)
        ycases.append(ytoappend)

    x_val = xcases[:int(len(cases) * 0.25)]
    x_train = xcases[int(len(cases) * 0.25):int(len(cases) * 0.9)]
    x_test = xcases[int(len(cases) * 0.9):]
    y_val = ycases[:int(len(cases) * 0.25)]
    y_train = ycases[int(len(cases) * 0.25):int(len(cases) * 0.9)]
    y_test = ycases[int(len(cases) * 0.9) :]

    model.compile(
        optimizer="adam",
        loss="mean_squared_error"
    )

    model.fit(
        x_train,
        y_train,
        batch_size = 5,
        epochs = 10,
        validation_data=(x_val, y_val),
    )

def Make_Prediction(r, t, s0, K, B, european):
    params = [float(x) for x in [r, t, s0, K, B, european]]
    return model.predict([params])[0][0]

