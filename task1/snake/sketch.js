const numberOfPlayers = 2;

let map = new Map(20, 20, numberOfPlayers, numberOfPlayers);
let bot = new GreedyBot(map.snakes[1], map.fruit);
let backgroundColor = 0;

function setup() {
    createCanvas(400, 400);
}

function draw() {
    background(backgroundColor);

    fill(color(255, 255, 255));
    map.snakes.forEach(snake => snake.draw());

    fill(color(255, 0, 0));
    map.fruit.draw();
}

const fruitEaten = () => map.checkCollision(map.fruit, map.getSnake().getHead());

function keyPressed() {
    let direction = keysMap[keyCode];
    if (map.isHumansMove() && direction && map.getSnake().isAllowedToMove(direction)) {
        playTurn(direction);
        map.nextTurn();
        direction = bot.decision();

        playTurn(direction);
        map.nextTurn();
    }
}

function playTurn(direction){
    if (!map.isGameOver) {
        map.getSnake().setDirection(direction);
        const lastCellCopy = copyCell(map.getSnake().getLast());
        map.getSnake().move(direction);
        if (
            map.checkCollisionWithAnotherSnakes() 
            || map.getSnake().hasCollisionWithYourself()
            || map.checkIfActualSnakeIsOutsideMap() 
        ) {
            backgroundColor = map.isHumansMove() ? color(255, 0, 0) : color(0, 255, 0);
            map.isGameOver = true;
        }
        if (fruitEaten()) {
            map.getSnake().cells.push(lastCellCopy);
            map.fruit = map.createFruit();
            bot.setFruit(map.fruit);
        }
    }
}