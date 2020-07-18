class Map {

    constructor(rows, columns, numberOfSnakes, numberOfPlayers) {
        this.columns = columns;
        this.rows = rows;
        this.numberOfPlayers = numberOfPlayers;
        this.actualSnakeIdx = 0;
        this.map = this.#createMap();
        this.fruit = this.createFruit();
        this.snakes = this.#createSnakes(numberOfSnakes);
        this.isGameOver = false;
    }

    #createMap = () => {
        return Array.from(new Array(this.rows))
            .map((row, idX) => this.#createRow(this.columns, idX));
    };

    #createRow = (columns, idX) => {
        return Array.from(new Array(columns))
            .map((column, idY) => ({ id: idX * columns + idY, x: idX, y: idY, isEmpty: true }))
    };

    createFruit = () => {
        const emptyCell = this.#getEmptyCell();
        emptyCell.isEmpty = false;
        return new Cell(Direction.NONE, emptyCell.x, emptyCell.y);
    };

    #getEmptyCell = () => this.#getRandomItemFromArray(this.#getEmptyCells());

    #getRandomItemFromArray = array => array[Math.floor(Math.random() * array.length)];

    #getEmptyCells = () => this.map.reduce((acc, curr) => acc.concat(...curr.filter(mapCell => mapCell.isEmpty)), []);

    #createSnakes = numberOfSnakes => {
        return Array.from(new Array(numberOfSnakes)).map(idx => {
            const emptyCell = this.#getEmptyCell();
            emptyCell.isEmpty = false;
            const x = emptyCell.x;
            const y = emptyCell.y;
            return new Snake(x, y);
        });
    };

    getSnake = () => {
        return this.snakes[this.actualSnakeIdx];
    };

    getAllSnakes = () => this.snakes;

    nextTurn = () => {
        if(!this.isGameOver) {
            this.actualSnakeIdx = (this.actualSnakeIdx + 1) % this.numberOfPlayers;
        }
    };

    isHumansMove = () => this.actualSnakeIdx === 0;

    checkCollision = (a, b) => a.x == b.x && a.y == b.y;

    checkCollisionWithAnotherSnakes = () => {
        const actualSnakeHead = this.getSnake().getHead();
        const allNotActualSnakes = this.getAllSnakes()
            .filter(snake => !(snake.getHead().x === actualSnakeHead.x && snake.getHead().y === actualSnakeHead.y));
        const crashed = allNotActualSnakes
            .every(snake => snake.hasCollision(actualSnakeHead))
        return crashed;
    }

    checkIfActualSnakeIsOutsideMap = () => {
        return this.getSnake().getHead().x < 0 
            || this.getSnake().getHead().x >= 20 
            || this.getSnake().getHead().y < 0 
            || this.getSnake().getHead().y >= 20;
    }
}