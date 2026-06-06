import numpy as np
import time

print("=" * 50)
print("DAY 1 - NUMPY PRACTICE")
print("=" * 50)

# 1. Array Creation
print("\n1. ARRAY CREATION")

arr = np.array([10, 20, 30, 40, 50])

print("Array:", arr)

# 2. Indexing & Slicing
print("\n2. INDEXING & SLICING")

print("First Element:", arr[0])
print("Last Element:", arr[-1])
print("Slice [1:4]:", arr[1:4])

# 3. Broadcasting
print("\n3. BROADCASTING")

print("Original:", arr)
print("Add 10:", arr + 10)

# 4. Vectorized Operations
print("\n4. VECTORIZED OPERATIONS")

print("Multiply by 2:", arr * 2)
print("Square:", arr ** 2)
print("Square Root:", np.sqrt(arr))

# 5. Random Numbers
print("\n5. RANDOM NUMBERS")

np.random.seed(42)

print("Random Integers:")
print(np.random.randint(1, 100, 5))

# 6. Reshape
print("\n6. RESHAPING")

numbers = np.arange(1, 13)

matrix = numbers.reshape(3, 4)

print(matrix)

# 7. Stacking
print("\n7. STACKING")

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("Vertical Stack:")
print(np.vstack((a, b)))

print("Horizontal Stack:")
print(np.hstack((a, b)))

# 8. Performance Test
print("\n8. PERFORMANCE COMPARISON")

start = time.time()

python_list = list(range(100000))
result = [x * 2 for x in python_list]

python_time = time.time() - start

start = time.time()

numpy_array = np.arange(100000)
result = numpy_array * 2

numpy_time = time.time() - start

print(f"Python Time: {python_time:.6f} sec")
print(f"NumPy Time : {numpy_time:.6f} sec")

print("\nDay 1 Completed Successfully!")