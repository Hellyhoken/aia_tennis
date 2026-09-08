from AIGamePyLibrary.AIGamePyLibrary import *

def plot_bool(value, name, color="Black"):
    plot_value = ConditionalSetFloat(
        value,
        1, 0
    )
    return TimePlot(name, color, "", plot_value)

def squash_y_axis(vector):
    return squash_axes(vector, squash_y=True)

def squash_axes(vector, squash_x=False, squash_y=False, squash_z=False):
    x,y,z = Vector3Split(vector)
    return Vector3(
        0 if squash_x else x,
        0 if squash_y else y,
        0 if squash_z else z
    )

def max_float(nodes, key=None):
    if key is None:
        key = nodes
    max_value = nodes[0]
    max_key = key[0]
    for i in range(1, len(nodes)):
        max_value = ConditionalSetFloat(
            CompareFloats(key[i], max_key, ">"),
            nodes[i],
            max_value
        )
        max_key = ConditionalSetFloat(
            CompareFloats(key[i], max_key, ">"),
            key[i],
            max_key
        )
    return max_value

def max_vector3(vectors, float_keys):
    max_vector = vectors[0]
    max_float = float_keys[0]
    for i in range(1, len(vectors)):
        max_vector = ConditionalSetVector3(
            CompareFloats(float_keys[i], max_float, ">"),
            vectors[i],
            max_vector
        )
        max_float = ConditionalSetFloat(
            CompareFloats(float_keys[i], max_float, ">"),
            float_keys[i],
            max_float
        )
    return max_vector

def min_float(nodes, key=None):
    if key is None:
        key = nodes
    min_value = nodes[0]
    min_key = key[0]
    for i in range(1, len(nodes)):
        min_value = ConditionalSetFloat(
            CompareFloats(key[i], min_key, "<"),
            nodes[i],
            min_value
        )
        min_key = ConditionalSetFloat(
            CompareFloats(key[i], min_key, "<"),
            key[i],
            min_key
        )
    return min_value

def min_vector3(vectors, float_keys):
    min_vector = vectors[0]
    min_float = float_keys[0]
    for i in range(1, len(vectors)):
        min_vector = ConditionalSetVector3(
            CompareFloats(float_keys[i], min_float, "<"),
            vectors[i],
            min_vector
        )
        min_float = ConditionalSetFloat(
            CompareFloats(float_keys[i], min_float, "<"),
            float_keys[i],
            min_float
        )
    return min_vector

def plot_trajectory(trajectory, color="Black"):
    for i in range(len(trajectory)-1):
        _ = DebugDrawLine(
            trajectory[i],
            trajectory[i+1],
            0.5,
            color
        )

