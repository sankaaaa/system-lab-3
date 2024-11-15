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
        sides = re.findall(r"(\d+)", self.text)
        if sides:
            side = int(sides[0])
            return side
        return None

    def calculate_perimeter(self, side):
        return 4 * side

    def extract_coordinates(self):
        coordinates = re.findall(r"[А-Яа-я]\((\d+)[,;](\d+)\)", self.text)
        return [(int(x), int(y)) for x, y in coordinates]

    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calculate_side_length(self, coordinates):
        side = self.calculate_distance(coordinates[0], coordinates[1])
        return side

    def solve(self):
        side = self.extract_rhombus_side()
        if side:
            perimeter = self.calculate_perimeter(side)
            return f"Периметр ромба з стороною {side} = {perimeter}, довжина сторони = {side}"

        coordinates = self.extract_coordinates()
        if len(coordinates) == 4:
            side_length = self.calculate_side_length(coordinates)

            perimeter = 4 * side_length
            return f"Довжина сторони ромба = {side_length:.2f}, Периметр ромба = {perimeter:.2f}"

        return "Не вдалося знайти достатньо даних для розв'язання задачі."


tests = [
    "Побудувати ромб ABCD зі стороною 2, знайти його периметр.",
    "Побудувати ромб з координатами А(5,0), В(0,5), С(−5,0), D(0,−5), обчислити довжину сторони, знайти його периметр.",
]

for command_text in tests:
    try:
        result = UDPipeAPI.process_text(command_text)
        # print(f"Лінгвістичний аналіз тексту: {result['result']}")

        solver = GeometrySolver(command_text)
        solution = solver.solve()
        print(solution)

    except Exception as e:
        print(f"Помилка при обробці тексту: {e}")
