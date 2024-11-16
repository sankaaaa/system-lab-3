import requests
import re
import math


class UDPipeAPI:
    BASE_URL = "https://lindat.mff.cuni.cz/services/udpipe/api/"

    @staticmethod
    def process_text(text, model="ukrainian", tokenizer=True, tagger=True, parser=True):
        params = {
            "data": text,
            "model": model,
            "tokenizer": "" if tokenizer else None,
            "tagger": "" if tagger else None,
            "parser": "" if parser else None,
        }
        response = requests.post(UDPipeAPI.BASE_URL + "process", data=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error processing text: {response.status_code}")


class GeometrySolver:
    def __init__(self, text):
        self.text = text

    def extract_rhombus_side(self):
        # Пошук чисел, що можуть бути сторонами ромба
        sides = re.findall(r"(\d+)", self.text)
        if sides:
            side = int(sides[0])  # Перша знайдена сторона
            return side
        return None

    def calculate_perimeter(self, side):
        # Периметр ромба: 4 * сторона
        return 4 * side

    def extract_coordinates(self):
        # Пошук координат точок у форматі (x, y) або (x;y)
        coordinates = re.findall(r"[А-Яа-я]\((\d+)[,;](\d+)\)", self.text)
        return [(int(x), int(y)) for x, y in coordinates]

    def calculate_distance(self, point1, point2):
        # Формула для обчислення відстані між двома точками
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calculate_side_length(self, coordinates):
        # Для ромба, беремо відстань між двома сусідніми точками
        side = self.calculate_distance(coordinates[0], coordinates[1])
        return side

    def extract_angle(self):
        # Пошук кута в градусах
        angle = re.findall(r"(\d+)[°]", self.text)
        if angle:
            return float(angle[0])  # Повертаємо знайдений кут
        return None

    def calculate_area(self, side, angle):
        # Площа ромба: S = a^2 * sin(α), де α — кут у градусах
        angle_rad = math.radians(angle)  # Перетворюємо кут у радіани
        area = side ** 2 * math.sin(angle_rad)
        return area

    def calculate_diagonals(self, side, angle):
        d1 = 2 * side * math.sin(math.radians(angle / 2))
        d2 = d1  # У ромбі діагоналі рівні
        return d1, d2

    def calculate_height(self, side, angle):
        # Висота ромба: h = a * sin(α)
        angle_rad = math.radians(angle)  # Перетворюємо кут у радіани
        height = side * math.sin(angle_rad)
        return height

    def solve(self):
        side = self.extract_rhombus_side()
        coordinates = self.extract_coordinates()
        angle = self.extract_angle()

        # Задача 1: Периметр ромба
        if "периметр" in self.text:
            if side:
                perimeter = self.calculate_perimeter(side)
                return f"Периметр ромба з стороною {side} = {perimeter}, довжина сторони = {side}"
            else:
                return "Не вдалося знайти сторону для обчислення периметра ромба."

        # Задача 2: Площа ромба
        if re.search(r"\bплощ(а|у|і|)", self.text, re.IGNORECASE):
            if side and angle:
                area = self.calculate_area(side, angle)
                return f"Площа ромба з стороною {side} та кутом {angle}° = {area:.2f}"
            elif len(coordinates) == 4 and angle:
                side_length = self.calculate_side_length(coordinates)
                area = self.calculate_area(side_length, angle)
                return f"Площа ромба з довжиною сторони {side_length:.2f} та кутом {angle}° = {area:.2f}"
            elif side:
                return f"Не вистачає кута для обчислення площі ромба з стороною {side}"
            else:
                return "Не вдалося обчислити площу через відсутність даних про сторону або кут"

        # Задача 4: Кути ромба
        if "усі кути ромба" in self.text:
            if angle:
                internal_angle = angle
                double_angle = internal_angle * 2
                other_angle = (360 - double_angle * 2) / 2
                return f"Кути ромба: {double_angle}°, {double_angle}°, {other_angle}°, {other_angle}°"

        # Задача 3: Діагоналі ромба
        if re.search(r"\bдіагонал[іь]\b", self.text, re.IGNORECASE):
            if side and angle:
                d1, d2 = self.calculate_diagonals(side, angle)
                return f"Діагональ ромба з стороною {side} і кутом {angle}° має довжину {d1:.2f}"
            else:
                return "Не вдалося обчислити діагоналі через відсутність сторони або кута."

        # Задача 5: Координати ромба
        if "координатами" in self.text and len(coordinates) == 4:
            side_length = self.calculate_side_length(coordinates)
            perimeter = 4 * side_length
            return f"Довжина сторони ромба = {side_length:.2f}, Периметр ромба = {perimeter:.2f}"

        # Задача 6: Висота ромба
        if re.search(r"\bвисот(а|у|)", self.text, re.IGNORECASE):
            if side and angle:
                height = self.calculate_height(side, angle)
                return f"Висота ромба з стороною {side} і кутом {angle}° = {height:.2f}"
            else:
                return "Не вдалося обчислити висоту через відсутність сторони або кута."

        return "Не вдалося знайти достатньо даних для розв'язання задачі."


# Тестові приклади
tests = [
    "Побудувати ромб ABCD зі стороною 3, знайти його периметр.",
    "Побудувати ромб ABCD зі стороною 2 і кутом 30°, знайти його площу.",
    "Побудувати ромб ABCD зі стороною 8 і кутом 30°, знайти його діагональ.",
    "Діагональ AC ромба ABCD утворює зі стороною AD кут 42°. Знайдіть усі кути ромба.",
    "Ромб зі стороною 4 і кутом 30°, знайти висоту."
]

for i, command_text in enumerate(tests, start=1):
    try:
        print(f"Задача {i}: {command_text}")
        solver = GeometrySolver(command_text)
        solution = solver.solve()
        print(f"Рішення: {solution}\n")

    except Exception as e:
        print(f"Помилка при обробці тексту: {e}\n")
