import tkinter as tk
from tkinter import ttk
base_times = {"S": 90.0, "M": 91.0, "H": 92.0}
bounds = {"S": (8,25), "M": (10,35), "H": (12,45)}
pit_loss = 20.6
race_laps = 70
def degradation(compound, lap):
    params = {"S": 0.06, "M": 0.04, "H": 0.03}  # s/lap
    return params[compound] * lap


def stint_time(compound, n, base_times):
    return n*base_times[compound] + sum(degradation(compound, lap) for lap in range(1, n+1))

def enumerate_strategies(race_laps, pit_loss, base_times, bounds, max_pits=3):
    results = []
    for pits in range(1, max_pits+1):
        parts = pits + 1
        # generuj podziały okrążeń
        def rec_build(remaining, parts, current):
            if parts == 1:
                yield current + [remaining]
            else:
                for i in range(1, remaining - parts + 2):
                    yield from rec_build(remaining - i, parts - 1, current + [i])
        for stint_lengths in rec_build(race_laps, parts, []):
            # sprawdzaj przypisania mieszanek
            from itertools import product
            for compounds in product("SMH", repeat=parts):
                # min/max ograniczenia
                if any(not(bounds[c][0] <= l <= bounds[c][1]) for c,l in zip(compounds, stint_lengths)):
                    continue
                # warunek: ≥2 mieszanki
                if len(set(compounds)) < 2:
                    continue
                total = sum(stint_time(c, l, base_times) for c,l in zip(compounds, stint_lengths))
                total += pits * pit_loss
                results.append({"pits": pits, "stints": stint_lengths, "compounds": compounds, "time": total})
    return sorted(results, key=lambda x: x["time"])

def run():
    results = enumerate_strategies(70, 20.6, base_times, bounds)
    top = results[:5]
    text.delete("1.0", tk.END)
    for r in top:
        text.insert(tk.END, f"Pits: {r['pits']} | {list(r['compounds'])} {r['stints']} | Time: {r['time']:.2f}s\n")

root = tk.Tk()
root.title("F1 Strategy Generator - Hungaroring 70 Laps")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

button = ttk.Button(frame, text="Generate Strategies", command=run)
button.pack(pady=5)

text = tk.Text(frame, height=15, width=70)
text.pack()

root.mainloop()
