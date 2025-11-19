import os
import random
import numpy as np

def home_away_seq_layer():
    from tensorflow.keras import layers, Input
    form_input = Input(shape=(4, 6))  
    form_branch = layers.Conv1D(32, 2, activation='relu')(form_input)
    return form_input, layers.GlobalMaxPooling1D()(form_branch)


def h2h_layer():
    from tensorflow.keras import layers, Input
    h2h_input = Input(shape=(4, 3))
    h2h_branch = layers.Conv1D(32, 2, activation='relu')(h2h_input)
    return h2h_input, layers.GlobalMaxPooling1D()(h2h_branch)


def odds_layer():
    from tensorflow.keras import layers, Input
    odds_input = Input(shape=(3,))
    return odds_input, layers.Dense(16, activation='relu')(odds_input)


def contextual_layer():
    from tensorflow.keras import layers, Input
    context_input = Input(shape=(18,)) 
    context_branch = layers.Dense(64, activation='relu')(context_input)
    context_branch = layers.Dropout(0.3)(context_branch)
    return context_input, layers.Dense(32, activation='relu')(context_branch)

 
def deep_model():
    from tensorflow.keras import layers, Model
    form_input, home_away_branch = home_away_seq_layer()
    h2h_input, h2h_branch = h2h_layer()
    odds_input, odds_branch = odds_layer()
    context_input, context_branch = contextual_layer() 
    merged = layers.concatenate([h2h_branch, context_branch, home_away_branch, odds_branch])

    x = layers.Dense(64, activation='relu')(merged)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(32, activation='relu')(x)
    output = layers.Dense(1, activation='sigmoid')(x)

    return Model(inputs=[h2h_input, context_input, form_input, odds_input], outputs=output)


def train_tf_model(form_X_train, h2h_X_train, odds_X_train, context_X_train, odds_y_train):
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    import tensorflow as tf
    
    def set_tf_seed(seed=42):
        os.environ['PYTHONHASHSEED'] = str(seed)
        tf.random.set_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
    
    set_tf_seed(42)
    model = deep_model()
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ReduceLROnPlateau(factor=0.5, patience=3)
    ]

    history = model.fit([h2h_X_train, context_X_train, form_X_train, odds_X_train], odds_y_train, epochs=30, validation_split=0.2, batch_size=32, callbacks=callbacks, verbose=0)
    
    return model
