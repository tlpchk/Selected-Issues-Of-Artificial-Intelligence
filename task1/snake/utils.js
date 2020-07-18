const Direction = {
    UP: 'up',
    DOWN: 'down',
    LEFT: 'left',
    RIGHT: 'right',
    NONE: 'none'
};

const keysMap = {
    37: Direction.LEFT,
    39: Direction.RIGHT,
    38: Direction.UP,
    40: Direction.DOWN
};

function oppositeDirection(direction) {
    switch (direction) {
        case Direction.DOWN:
            return Direction.UP
        case Direction.UP:
            return Direction.DOWN
        case Direction.LEFT:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.LEFT
    }
};

function copyCell(cell){
    return Object.assign(new Cell(), cell);
}