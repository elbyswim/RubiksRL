from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import RMSprop


def build_model(moves, factor=1):
    assert moves in (12, 18)
    cube = Input((54,))
    layer1 = Dense(4096 / factor, 'elu')(cube)
    layer2 = Dense(2048 / factor, 'elu')(layer1)
    values = Dense(512 / factor, 'elu')(layer2)
    policy = Dense(512 / factor, 'elu')(layer2)
    value_output = Dense(1, name='value')(values)
    policy_output = Dense(moves, activation='softmax', name='policy')(policy)
    return Model(cube, (value_output, policy_output))


def compile_model(model, lr):
    model.compile(optimizer=RMSprop(lr),
                  loss={'value': 'mean_squared_error', 'policy': 'sparse_categorical_crossentropy'})
