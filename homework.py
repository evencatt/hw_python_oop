from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    coef_callorie_func_for_running_1: int = 18
    coef_callorie_func_for_running_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError('Данный метод не определён'
                                  'в родительском классе')

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    def get_spent_calories(self) -> float:
        return ((self.coef_callorie_func_for_running_1 * self.get_mean_speed()
                 - self.coef_callorie_func_for_running_2)
                * self.weight / self.M_IN_KM * (self.duration * 60))


class SportsWalking(Training):

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coef_callorie_1: float = 0.035
        coef_callorie_2: float = 0.029
        return ((coef_callorie_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * coef_callorie_2 * self.weight)
                * (self.duration * 60))


class Swimming(Training):
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    sport_type_ref: Dict[str, Union[Swimming, Running, SportsWalking]] = {
        'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in sport_type_ref:
        return sport_type_ref[workout_type](*data)
    raise KeyError(f'Неизвестный тип тренировки: {workout_type}')


def main(training: Training) -> None:
    if training:
        info = training.show_training_info()
        print(info.get_message())
        return
    print(f'Неизвестный тип тренировки: {workout_type}')


if __name__ == '__main__':
    packages = [
        ('SWM1', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
