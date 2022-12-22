a = [1, 2, 3, 4, 5, 6, 7] * 5

cycle_length = 4
for i in range(0, len(a) - cycle_length):
    possible_cycle = a[i : i + cycle_length]
    print(f"{possible_cycle=}")
    for k in range(i + cycle_length, len(a) - cycle_length):
        part = a[k : k + cycle_length]
        print(f"{part=}")
        if possible_cycle == part:
            print(f"Found Cycle!")
            exit(0)
