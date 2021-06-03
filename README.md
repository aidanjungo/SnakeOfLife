# SnakeOfLife
Snake game mixed with Conway's Game of Life

The rules are the same than a normal snake game but you have to avoid cells created by Conway's Game of Life. New pattern are added every 3, 2 or 1 food eaten (depending the chosen level). However, if one of these cell is in contact with food it turns to food.


## Requirements

- numpy
- pygame


## Usage

You can pass the level (1 to 3) as argument, by default it will be 1.

```
python snakeoflife.py 3
```
