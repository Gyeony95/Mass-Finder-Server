import random
from collections import namedtuple
from math import ceil, floor, exp

from mass_finder_app.logic.amino_model import AminoModel
from mass_finder_app.logic.enums import FormyType, IonType

# 상수 선언
top_solutions_count = 20
sa_iterations = 100  # 시뮬레이티드 어닐링 반복 횟수
initial_temperature = 10000.0  # 초기 온도
cooling_rate = 0.99  # 냉각률
absolute_temperature = 0.00001  # 최소 온도
f_weight = 27.99  # 포밀레이스의 분자량

# calc 함수에서 초기화 될 사용가능한 아미노산의 리스트
data_map = {}

# namedtuple을 사용하여 Tuple2 유사 구조체를 생성
Range = namedtuple('Range', ['min', 'max'])


def calc_by_ion_type(target_mass, init_aminos, fomy_type, ion_type, amino_map):
    _ion_type = IonType.decode(ion_type)
    best_solutions = []

    if _ion_type == IonType.UNKNOWN:
        # IonType을 모르면 UNKNOWN을 제외하고 모든 타입을 계산
        for i in IonType:
            if i == IonType.UNKNOWN:
                continue
            solutions = calc(target_mass - i.weight, init_aminos, fomy_type, i.text, amino_map)
            for solution in solutions:
                solution.weight += i.weight
            best_solutions.extend(solutions)

        # 다시 정렬 후 상위 20개 자름
        best_solutions = sort_amino(best_solutions, target_mass)
        best_solutions = best_solutions[:top_solutions_count]
    else:
        # H, Na, K 일 때 총 무게에서만 제외해서 계산
        solutions = calc(target_mass - _ion_type.weight, init_aminos, fomy_type, ion_type, amino_map)
        for solution in solutions:
            solution.weight += _ion_type.weight
        best_solutions.extend(solutions)

    # 유사도 계산
    for solution in best_solutions:
        solution.similarity = calculate_similarity(target_mass, solution.weight)

    # JSON 으로 변환
    return [solution.to_json() for solution in best_solutions]


def calc(target_mass, init_aminos, fomy_type, ion_type, input_aminos):
    global data_map  # 전역 변수를 함수 내에서 사용하겠다고 선언
    _formy_type = FormyType.decode(fomy_type)
    data_map = dict(input_aminos)
    best_solutions = []

    init_amino_weight = get_init_amino_weight(init_aminos)
    target_mass -= init_amino_weight

    range = get_min_max_range(_formy_type, target_mass)

    for i in range:
        add_weight = get_water_weight(i)
        solutions = calc_by_ftype(_formy_type, target_mass + add_weight)
        solutions = remove_duplicates(solutions)
        best_solutions.extend(solutions)

    best_solutions = sort_amino(best_solutions, target_mass)
    best_solutions = best_solutions[:top_solutions_count]

    best_solutions = set_init_amino_to_result(best_solutions, init_aminos, init_amino_weight)
    best_solutions = set_meta_data(best_solutions, _formy_type, IonType.decode(ion_type), init_aminos)

    for solution in best_solutions:
        print(f'combins: {solution.code}, result: {solution.weight}')

    return best_solutions


def calc_by_ftype(f_type, target_mass):
    best_solutions = []

    for i in range(sa_iterations):
        if f_type == FormyType.N:
            solution = simulated_annealing(target_mass)
            key = list(solution.keys())[0]
            best_solutions.append(AminoModel(code=key, weight=get_weight_sum(key)))
        elif f_type == FormyType.Y:
            solution = simulated_annealing(target_mass - f_weight)
            key = f'f{list(solution.keys())[0]}'
            best_solutions.append(AminoModel(code=key, weight=get_weight_sum(key)))
        elif f_type == FormyType.UNKNOWN:
            solution1 = simulated_annealing(target_mass)
            solution2 = simulated_annealing(target_mass - f_weight)
            solution2 = {f'f{list(solution2.keys())[0]}': list(solution2.values())[0]}
            key1 = list(solution1.keys())[0]
            key2 = list(solution2.keys())[0]
            best_solutions.append(AminoModel(code=key1, weight=get_weight_sum(key1)))
            best_solutions.append(AminoModel(code=key2, weight=get_weight_sum(key2)))

    return best_solutions


def simulated_annealing(target_mass):
    temperature = initial_temperature

    # 1차 비교군을 위한 조합 추출해서 목표값과의 차이 저장
    current_solution = random_solution(target_mass)
    current_energy = evaluate(current_solution, target_mass)

    # 1차 비교군을 베스트로 지정
    best_solution = current_solution[:]
    best_energy = current_energy

    # 초기온도에 계속해서 냉각률을 곱해서 최소온도가 될 때까지 반복
    while temperature > absolute_temperature:
        # 기존 조합을 기준으로 새로운 조합 추출
        new_solution = neighbor_solution(current_solution, target_mass)
        new_energy = evaluate(new_solution, target_mass)

        # 새 조합이 합격되는지 체크
        if acceptance_probability(current_energy, new_energy, temperature) > random.random():
            current_solution = new_solution
            current_energy = new_energy

        # 새 조합이 목표값과의 차이가 더 적으면 새로운 베스트로 설정
        if current_energy < best_energy:
            best_solution = current_solution[:]
            best_solution.sort()
            best_energy = current_energy

        temperature *= cooling_rate

    return {''.join(best_solution): best_energy}


def random_solution(target_mass):
    solution = []
    mass = 0.0
    while mass < target_mass:
        amino_acid = random.choice(list(data_map.keys()))
        amino_acid_mass = data_map[amino_acid]
        if mass + amino_acid_mass > target_mass:
            break
        solution.append(amino_acid)
        mass += amino_acid_mass
    return solution


def neighbor_solution(current_solution, target_mass):
    new_solution = current_solution[:]
    if new_solution:
        index = random.randint(0, len(new_solution) - 1)
        new_amino_acid = random.choice(list(data_map.keys()))
        new_solution[index] = new_amino_acid

        # Ensure the new solution is under the target mass
        while evaluate(new_solution, target_mass) > target_mass:
            new_solution.pop(random.randint(0, len(new_solution) - 1))
    return new_solution


def evaluate(solution, target_mass):
    total_mass = sum(data_map[gene] for gene in solution)
    return abs(target_mass - total_mass)


def acceptance_probability(current_energy, new_energy, temperature):
    if new_energy < current_energy:
        return 1.0
    else:
        return exp((current_energy - new_energy) / temperature)


def get_weight_sum(solution_combine):
    result = sum(data_map.get(e, 0) for e in solution_combine)
    if solution_combine.startswith('f'):
        # 포멜레이스 포함 시 물 증발량을 제외하고 순수 무게 증가
        result -= get_water_weight(len(solution_combine) - 1)
        result += f_weight
    else:
        # 물 증발량 제거
        result -= get_water_weight(len(solution_combine))

    return result


def get_water_weight(amino_length):
    if amino_length == 0:
        return 0.0
    return 18.01 * (amino_length - 1)


def sort_amino(amino_list, compare_value):
    def sort_key(amino):
        if amino.weight is None:
            return float('inf')  # None이면 무한대로 처리하여 맨 뒤로 정렬
        else:
            return abs(amino.weight - compare_value)

    amino_list.sort(key=sort_key)
    return amino_list


def remove_duplicates(amino_list):
    unique_map = {}
    for amino_model in amino_list:
        unique_map[amino_model.code] = amino_model
    return list(unique_map.values())


def get_min_max_range(type, target_mass):
    global f_weight  # 전역 변수를 함수 내에서 사용하겠다고 선언
    min_value = min(data_map.values())
    max_value = max(data_map.values())
    min_range = 0
    max_range = 0

    if type in [FormyType.Y, FormyType.UNKNOWN]:
        max_range = ceil(target_mass / f_weight)
    else:
        max_range = ceil(target_mass / min_value)

    min_range = floor(target_mass / max_value)
    if min_range is None or max_range is None:  # 초기화되지 않은 경우 처리
        raise ValueError("min or max is not properly initialized")

    return range(min_range, max_range)


def get_init_amino_weight(init_amino):
    init_amino_water_weight = get_water_weight(len(init_amino) + 1)
    init_amino_weight = 0

    if init_amino:
        for i in init_amino:
            init_amino_weight += amino_map.get(i, 0)

    return init_amino_weight - init_amino_water_weight


# 기존 베스트 솔루션 에서 init 값을 앞에 붙여주는 로직
def set_init_amino_to_result(best_solutions, init_amino, init_amino_weight):
    if not init_amino:
        return best_solutions

    for item in best_solutions:
        if not item.code:  # item.code가 비어있는지 확인
            item.code = init_amino
        else:
            first_char = item.code[0]  # 첫 문자 가져오기
            if first_char == 'f':
                item.code = item.code.replace('f', f'f{init_amino}', 1)
            else:
                item.code = item.code.replace(first_char, f'{init_amino}{first_char}', 1)

        item.weight += init_amino_weight  # 초기 아미노산 무게 추가

    return best_solutions


# FormyType, IonType, essential seq 붙여주는 부분
def set_meta_data(best_solutions, formy_type, ion_type, essential_seq):
    for solution in best_solutions:
        solution.formyType = formy_type
        solution.ionType = ion_type
        solution.essentialSeq = essential_seq
    return best_solutions


# 유사도 체크
def calculate_similarity(a, b):
    if a == 0:
        return 0  # a가 0이면 유사도를 0으로 처리
    difference = abs(a - b)
    similarity = 100 - ((difference / a) * 100)
    similarity = round(similarity, 2)
    similarity = max(similarity, 0)
    return similarity


amino_map = {
    'G': 75.03,
    'A': 89.05,
    'S': 105.04,
    'T': 119.06,
    'C': 121.02,
    'V': 117.08,
    'L': 131.09,
    'I': 131.09,
    'M': 149.05,
    'P': 115.06,
    'F': 165.08,
    'Y': 181.07,
    'W': 204.09,
    'D': 133.04,
    'E': 147.05,
    'N': 132.05,
    'Q': 146.07,
    'H': 155.07,
    'K': 146.11,
    'R': 174.11,
}
