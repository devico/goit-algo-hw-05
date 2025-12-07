def upper_bound(arr, x):
    """
    arr — відсортований за зростанням список дробових чисел.
    Повертає (кількість_ітерацій, верхня_межа),
    де верхня_межа — найменший елемент у arr, який >= x.
    Якщо всі елементи < x — повертає None як верхню межу.
    """
    left, right = 0, len(arr) - 1
    iters = 0
    ans = None

    while left <= right:
        iters += 1
        mid = (left + right) // 2
        if arr[mid] >= x:
            ans = arr[mid]
            right = mid - 1     # пробуємо знайти ще менший індекс
        else:
            left = mid + 1

    return iters, ans


# Приклади:
a = [-3.5, -1.0, 0.0, 0.5, 2.2, 2.2, 3.9, 10.0]  # відсортований масив
print(upper_bound(a, -2.0))  # -> (ітерації, -1.0)
print(upper_bound(a, 2.2))   # -> (ітерації, 2.2)
print(upper_bound(a, 5.0))   # -> (ітерації, 10.0)
print(upper_bound(a, 11.0))  # -> (ітерації, None)
