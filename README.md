# Asteroids

Asteroids - реализация одноименной аркадной игры.

# Описание

Цель игры - набрать как можно больше очков, уничтожая астероиды и НЛО  
У ракеты ограниченные топливо и боезапас, для пополнения нужно собирать капсулы снабжения.


# Запуск игры
Чтобы начать игру, запустите файл main.py. (Технические требования к игре описаны в файле 'requirements.txt').

# Управление
 W - ускорение  
 A - поворот налево  
 D - поворот направо  
 Spase(Пробел) - выстрел
 
# Тестирование
В проекте представлены тесты в папке tests, проверяющие корректную работу игровых функций.

# Классы

## GameObject

Базовый класс для игровых объектов, от него наследуются:
Asteroid, Bullet, Rocket, SupplyCapsule, Ufo - классы
соответствующих игровых объектов.

## GameObjectLogic  
Содержит освновные методы взаимодействия игровых объектов между собой.

## Game
Содержит методы отрисовки игры и UI.

## GameRecords
Содержит логику формирования и получения таблицы рекордов.





 
