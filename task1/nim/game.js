const N = 30;
const time = 100;
const removeMax = 3;
const botPlayer = 2;

let game;
let bot;
let scoreElement;

function start() {
    game = new Nim(N,1,removeMax,true);
    bot = initBot();

    initElements()
}

function initBot() {
    return new Mcts(time, botPlayer,game.getN(),game.getRemoveMax(),{}, true);
}


function initElements() {
    scoreElement = document.getElementById("score");
    updateScore();

    for (let i = 1; i <= removeMax; i++) {
        if(document.getElementById(i)){
            continue
        }
        let b = document.createElement('BUTTON');
        b.onclick = function () {
            handleClick(i)
        };
        b.innerText = i;
        b.id = i;
        document.getElementById("board").appendChild(b)
    }
}


function handleClick(n) {
    game.decreaseN(n);
    updateScore();
    game.switchPlayer();

    if(game.over()){
        finish();
        start();
        return
    }

    bot = initBot();
    let botMove = bot.nextMove();

    game.decreaseN(botMove);
    updateScore();
    game.switchPlayer();

    if(game.over()){
        finish();
        start();
    }
}

function updateScore() {
    scoreElement.innerText = " | ".repeat(game.getN() > 0 ? game.getN() : 0).concat(" ", game.getN()) ;
}

function finish() {
    let winner = game.getCurrentPlayer() === botPlayer ? "You" : "Bot";
    alert(winner + " wins!");
}