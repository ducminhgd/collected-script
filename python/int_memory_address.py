import ctypes

x = 5
address_x = id(5)
print(id(x))  # 11381600
print(id(5))  # 11381600

x += 2
print(id(x))  # 11381664
print(ctypes.cast(11381600, ctypes.py_object).value)  # 5
print(ctypes.cast(11381664, ctypes.py_object).value)  # 7

# Consider integer has 32 bits
address_y = address_x + (10 * 32)  # 11381664 + 320
print(ctypes.cast(address_y, ctypes.py_object).value)  # 15


print(x.bit_length()) # 3