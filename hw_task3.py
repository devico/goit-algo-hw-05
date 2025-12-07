# Порівняння пошуку підрядка: Боєр–Мур, КМП, Рабін–Карп (без генерації Markdown/файлів)

from pathlib import Path
import timeit
import sys


def kmp_search(text, pattern):
    if pattern == "":
        return 0

    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def boyer_moore_search(text, pattern):
    if pattern == "":
        return 0
    last = {}
    for i, c in enumerate(pattern):
        last[c] = i
    m, n = len(pattern), len(text)
    i = m - 1
    j = m - 1
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            i -= 1
            j -= 1
        else:
            li = last.get(text[i], -1)
            i = i + m - min(j, 1 + li)
            j = m - 1
    return -1

def rabin_karp_search(text, pattern, base=256, mod=10**9+7):
    m, n = len(pattern), len(text)
    if m == 0:
        return 0
    if m > n:
        return -1
    h = pow(base, m - 1, mod)
    ph = 0
    th = 0
    for i in range(m):
        ph = (ph * base + ord(pattern[i])) % mod
        th = (th * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if ph == th and text[i:i+m] == pattern:
            return i
        if i < n - m:
            th = (th - ord(text[i]) * h) % mod
            th = (th * base + ord(text[i + m])) % mod
            th %= mod
    return -1

ALGS = {
    "Boyer-Moore": boyer_moore_search,
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search,
}


def read_text(p):
    return Path(p).read_text(encoding="utf-8", errors="ignore")

def pick_existing_substring(text):
    for w in text.replace("\n", " ").split():
        w = w.strip(".,;:!?()[]{}«»\"'—-")
        if len(w) >= 6:
            return w

    return text[:10] if len(text) >= 10 else text

def bench(func, text, pattern, repeat=3):
    t = timeit.Timer(lambda: func(text, pattern))
    runs = t.repeat(repeat=repeat, number=1)
    return sum(runs) / len(runs)


def main():
    p1 = sys.argv[1] if len(sys.argv) > 1 else "стаття 1.txt"
    p2 = sys.argv[2] if len(sys.argv) > 2 else "стаття 2.txt"

    text1 = read_text(p1)
    text2 = read_text(p2)

    exist1 = pick_existing_substring(text1)
    exist2 = pick_existing_substring(text2)
    missing = "qwertyuiopzxcv"  # вигаданий, гарантовано відсутній

    cases = []
    for txt_name, txt, ex in [("Стаття 1", text1, exist1), ("Стаття 2", text2, exist2)]:
        for kind, pat in [("існує", ex), ("вигаданий", missing)]:
            for name, fn in ALGS.items():
                t = bench(fn, txt, pat, repeat=3)
                cases.append((txt_name, kind, name, len(txt), len(pat), t))

    # Вивід таблиці у консоль
    print("Результати (середній час із 3 вимірів):")
    print("| Текст | Підрядок | Алгоритм | Довжина тексту | Довжина підрядка | Час, с |")
    print("|-------|----------|----------|----------------|------------------|--------|")
    for txt, kind, algo, n, m, t in cases:
        print(f"| {txt} | {kind} | {algo} | {n} | {m} | {t:.6f} |")

    # Найшвидші по кожному тексту і типу підрядка
    def winner(text_name, kind):
        subset = [r for r in cases if r[0] == text_name and r[1] == kind]
        return min(subset, key=lambda x: x[5])[2]

    print("\nНайшвидші:")
    print(f"- Стаття 1, існуючий: {winner('Стаття 1', 'існує')}")
    print(f"- Стаття 1, вигаданий: {winner('Стаття 1', 'вигаданий')}")
    print(f"- Стаття 2, існуючий: {winner('Стаття 2', 'існує')}")
    print(f"- Стаття 2, вигаданий: {winner('Стаття 2', 'вигаданий')}")

    # Середній час по алгоритмах (для загального підсумку)
    avg = {}
    for algo in ALGS.keys():
        times = [t for (_, _, a, _, _, t) in cases if a == algo]
        avg[algo] = sum(times) / len(times)

    print("\nСередній час по всіх кейсах:")
    for k, v in sorted(avg.items(), key=lambda x: x[1]):
        print(f"- {k}: {v:.6f} с")

if __name__ == "__main__":
    main()
