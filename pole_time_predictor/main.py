import csv

def time_to_seconds(time_str):
    minutes, rest = time_str.split(":")
    seconds = float(rest)
    return int(minutes) * 60 + seconds

def seconds_to_time(seconds):
    minutes = int(seconds // 60)
    sec = seconds % 60
    return f"{minutes}:{sec:.3f}"

def load_data(filename):
    races = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            race_name = row['nazwa_wyscigu']
            races[race_name] = row
    return races

def calculate_average_delta(row, year):
    """Oblicza średnią różnicę między FP2/FP3 a pole position dla danego roku"""
    fp2 = time_to_seconds(row[f'fp2_{year}'])
    fp3 = time_to_seconds(row[f'fp3_{year}'])
    pp = time_to_seconds(row[f'pp_{year}'])
    avg_fp = (fp2 + fp3) / 2
    delta = avg_fp - pp
    return delta

def main():
    filename = 'data.csv'  
    data = load_data(filename)

    print("Dostępne wyścigi:")
    for race in data:
        print("-", race)

    selected_race = input("\nWybierz nazwę wyścigu dokładnie tak, jak widnieje w pliku: ")
    if selected_race not in data:
        print("Nie znaleziono wyścigu.")
        return

    try:
        fp2_input = input("Podaj czas FP2 (format mm:ss.xxx): ")
        fp3_input = input("Podaj czas FP3 (format mm:ss.xxx): ")
        fp2_sec = time_to_seconds(fp2_input)
        fp3_sec = time_to_seconds(fp3_input)
        avg_input = (fp2_sec + fp3_sec) / 2
    except Exception as e:
        print("Błąd w formacie czasu:", e)
        return

    # Oblicz średnią różnicę z lat 2022–2024
    row = data[selected_race]
    deltas = []
    for year in ['2022', '2023', '2024']:
        try:
            delta = calculate_average_delta(row, year)
            deltas.append(delta)
        except:
            continue

    if not deltas:
        print("Brak danych historycznych do obliczeń.")
        return

    avg_delta = sum(deltas) / len(deltas)
    predicted_pp = avg_input - avg_delta

    print(f"\nPrzewidywany czas pole position dla {selected_race}: {seconds_to_time(predicted_pp)}")

if __name__ == "__main__":
    main()
