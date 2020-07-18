class GreedyBot {
    constructor(snake, fruit) {
        this.snake = snake;
        this.fruit = fruit;
    }

    setFruit(fruit) {
        this.fruit = fruit
    }

    decision() {
        let dx = this.fruit.x - this.snake.getHead().x;
        let dy = this.fruit.y - this.snake.getHead().y;
        let optimalDirectionX = dx < 0 ? Direction.LEFT : Direction.RIGHT;
        let optimalDirectionY = dy < 0 ? Direction.UP : Direction.DOWN;

        let finalDirection;

        if (dx === 0 && this.snake.isAllowedToMove(optimalDirectionY)) {
            finalDirection = optimalDirectionY
        }else if(dy === 0 && this.snake.isAllowedToMove(optimalDirectionX)){
            finalDirection = optimalDirectionX
        }else {
            finalDirection = this.snake.isAllowedToMove(optimalDirectionY)
                ? optimalDirectionY
                : optimalDirectionX;
        }
        return finalDirection
    }
}