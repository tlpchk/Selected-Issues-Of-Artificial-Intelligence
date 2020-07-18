const totalCount = 10;
const botTime = 10;
const removeMax = 3;
const moveOnTree = false;

let game;
let bot1;
let bot2;

let bot1Wins = 0;
let bot2Wins = 0;
let it = 0;
let statistics = {};

function start() {
    while(it < totalCount ) {
        let player = 1 + Math.floor(Math.random() * 2);
        const N = 20 + Math.floor(Math.random() * 30);
        game = new Nim(N, player, removeMax,true);
        initBot1();
        initBot2();
        playGame(player);
        finish();
        it += 1;
    }
    printStatistics();
}

function playGame(startPlayer) {
    let player = startPlayer;
    while(!game.over()) {
        let n;
        if (player === 1) {
            n = bot1.nextMove()
        } else {
            n = bot2.nextMove()
        }
        game.decreaseN(n);
        updateBots(n);
        game.switchPlayer();
        player = game.getCurrentPlayer();
    }
}

function initBot1(){
    //bot1 = new Mcts(botTime, 1, game.getN(), removeMax);
    //bot1 = new Random(game);
    bot1 = new Greedy(game);
}

function initBot2() {
    bot2 = new Mcts(botTime, 2, game.getN(), removeMax, statistics,true);
}

function updateBots(n){
    initBot1();

    if(moveOnTree){
        bot2.moveRoot(n)
    }else {
        initBot2()
    }
}

function finish() {
    if (game.getCurrentPlayer() === 2) {
        bot1Wins++
    } else {
        bot2Wins++
    }
    console.log(bot1Wins, bot2Wins);
}

function printStatistics() {
    const sep = ",";
    const end = "\n";

    const header  = ["n","popularity","avg. convincity","avg. playouts","avg. path","med. path ","max. path"];
    let result = header.join(sep).concat(end);

    const arrAvg = arr => (arr.reduce((a,b) => a + b, 0) / arr.length).toFixed(4);
    const arrMedian = arr => {
        const mid = Math.floor(arr.length / 2),
            nums = [...arr].sort((a, b) => a - b);
        return arr.length % 2 !== 0 ? nums[mid] : (nums[mid - 1] + nums[mid]) / 2;
    };

    for (let [key, value] of Object.entries(statistics)) {
        const row = [
            key,
            value["sims"].length,
            arrAvg(value["conv"]),
            arrAvg(value["sims"]),
            arrAvg(value["paths"]),
            arrMedian(value["paths"]),
            Math.max(...value["paths"])
        ];
        result = result.concat(row.join(sep),end)
    }
    console.log(result);
}
