def fibonacci_series(n):
    """Return a list containing the first n Fibonacci numbers."""
    if n <= 0:
        return []
    series = [0]
    if n == 1:
        return series
    series.append(1)
    for _ in range(2, n):
        series.append(series[-1] + series[-2])
    return series


def main():
    try:
        count = int(input("Enter the number of Fibonacci terms: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    fib = fibonacci_series(count)
    print("Fibonacci series:", " ".join(str(x) for x in fib))


if __name__ == "__main__":
    main()
