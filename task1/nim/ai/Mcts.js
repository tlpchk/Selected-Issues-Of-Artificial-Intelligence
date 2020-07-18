class Mcts {
    #maxTime;
    #rootNode;
    #statistics;
    #withCoin;
    #randomPlayout;

    constructor(maxTime, player, N, removeMax, statistics = {},  withCoin = false, randomPlayout = true) {
        this.#maxTime = maxTime;
        const state = new NodeState(player, N, removeMax);
        this.#rootNode = new Node(state);
        this.#statistics = statistics;
        this.#withCoin = withCoin;
        this.#randomPlayout = randomPlayout;
    }

    getRandomItem = (items) => items[Math.floor(Math.random() * items.length)];

    moveRoot(n){
        const children = this.#rootNode.getChildren();
        for (let i = 0; i < children.length; i++) {
            let child = children[i];
            if (child.getState().getLabel() === n) {
                this.#rootNode = child;
                this.#rootNode.setParent(undefined);
                return
            }
        }
    }

    nextMove() {
        let simulations = 0;
        const timeOfEnd = new Date().getTime() + this.#maxTime;

        while ((new Date().getTime()) < timeOfEnd) {
            if(this.#withCoin) {
                let node;
                let winner;

                // Selection
                const selectionRes = this.selectNodeWithCoin();
                node = selectionRes["node"];
                if(!selectionRes["winByCoin"]){
                    let removedByCoin = selectionRes["removedByCoin"];

                    // Expanding
                    node = this.expandNode(node);

                    // Simulation
                    winner = this.simulatePlayoutWithCoin(node,removedByCoin);
                }else{
                    winner = node.getState().getNim().getNextPlayer()
                }

                // Back propagation
                this.backPropagate(node, winner);
            }else {
                let node = this.selectNode(this.#rootNode);

                // Expanding
                node = this.expandNode(node);

                // Simulation
                let winner = this.simulatePlayout(node);

                // Back propagation
                this.backPropagate(node, winner);
            }

            simulations += 1;
        }

        const best = this.chooseBest();
        const convincity = 1. - best.getState().getWinCount() / best.getState().getVisitCount();
        // this.print2DUtil(this.#rootNode, 0);
        // console.log("Bot sees ", this.#rootNode.getState().getNim().getN(), " sticks");
        // console.log("After  ", simulations, " simulations bot chose ", best.getState().getLabel());
        this.gatherStatistics(simulations,convincity);
        return best.getState().getLabel();
    }

    selectNode(rootNode) {
        let node = rootNode;

        while (!node.isLeaf()) {
            if (!node.isAllChildrenVisited()) {
                break
            }
            node = this.UCT(node);
        }
        return node
    }

    selectNodeWithCoin() {
        let node = this.#rootNode;
        let tossCoin = node.getState().getNim().tossCoin;
        let removedByCoin = 0;
        let winByCoin = false;

        while (!node.isLeaf() && !winByCoin) {
            if (!node.isAllChildrenVisited()) {
                break
            }
            node = this.UCT(node);
            removedByCoin += tossCoin();
            winByCoin = node.getState().getNim().getN() - removedByCoin <= 0
        }
        return { "node" : node, "winByCoin": winByCoin, "removedByCoin" : removedByCoin}
    }

    UCT(node) {
        let choice;
        let bestScore = -Infinity;
        let children = node.getChildren();

        for (let i = 0; i < children.length; i++) {
            let child = children[i];
            let score = this.USB1(child);
            if (score > bestScore) {
                bestScore = score;
                choice = child
            }
        }
        return choice
    }

    USB1(node, explorationParam = Math.sqrt(2)) {
        const nodeWins = node.getState().getWinCount();
        const nodeVisits = node.getState().getVisitCount();
        const parentVisits = node.getParent().getState().getVisitCount();
        const exploitationTerm = 1 - nodeWins / nodeVisits;

        return exploitationTerm + explorationParam * Math.sqrt((Math.log(parentVisits)) / (nodeVisits));
    }

    expandNode(node) {
        if(node.getState().getNim().over()){
            return node
        }
        let unexploredLabels = node.getUnexploredLabels();
        let label = this.getRandomItem(unexploredLabels);
        let state = node.getState().createChildState(label);
        let child = new Node(state, node);
        node.addChild(child);
        return child;
    }

    simulatePlayout(node) {
        const nimCopy = node.getState().getNim().copy();
        const player = this.#rootNode.getState().getNim().getPlayer();

        while (!nimCopy.over()) {
            if (!this.#randomPlayout && nimCopy.getCurrentPlayer() === player) {
                let choice = nimCopy.getN() % (nimCopy.getRemoveMax() + 1);
                if (choice === 0) {
                    nimCopy.randomPlay();
                }else {
                    nimCopy.decreaseN(choice)
                }
            } else {
                nimCopy.randomPlay();
            }
            nimCopy.switchPlayer()
        }

        return nimCopy.getNextPlayer()
    }

    simulatePlayoutWithCoin(node, removedByCoin) {
        const nimCopy = node.getState().getNim().copy();
        nimCopy.decreaseN(removedByCoin);
        const player = this.#rootNode.getState().getNim().getPlayer();

        while (!nimCopy.over()) {
            if (!this.#randomPlayout && nimCopy.getCurrentPlayer() === player) {
                let choice = nimCopy.getN() % (nimCopy.getRemoveMax() + 1);
                if (choice === 0) {
                    nimCopy.randomPlay();
                }else {
                    nimCopy.decreaseN(choice)
                }
            } else {
                nimCopy.randomPlay();
            }
            nimCopy.switchPlayer()
        }

        return nimCopy.getNextPlayer()
    }

    backPropagate(node, winner) {
        let tempNode = node;
        while (tempNode) {
            tempNode.getState().incrementVisitCount();
            if (tempNode.getState().getNim().getPlayer() === winner) {
                tempNode.getState().incrementWinCount()
            }
            tempNode = tempNode.getParent()
        }
    }

    chooseBest() {
        let children = this.#rootNode.getChildren();
        let temp = -Infinity;
        let choice;

        for (let i = 0; i < children.length; i++) {
            const child = children[i];
            const rate = 1 - child.getState().getWinCount() / child.getState().getVisitCount();
            if (rate >= temp) {
                temp = rate;
                choice = child
            }
        }
        return choice
    }

    print2DUtil(node, space) {
        const COUNT = 15;
        space += COUNT;

        if (node === undefined) {
            return;
        }

        const children = node.getChildren();

        this.print2DUtil(children[0], space);

        const child1 = children[1] ? children[1].getState().toString() : "";

        console.log("\n"," ".repeat(space),
            node.getState().toString(),
            " ".repeat(COUNT - child1.length - 2),
            child1);

        this.print2DUtil(children[1], space);

        this.print2DUtil(children[2], space);
    }

    gatherStatistics(simulations, convincity) {
        const N = this.#rootNode.getState().getNim().getN();
        let dict = this.#statistics[N];
        if(!dict){
            this.#statistics[N] = {};
            dict = this.#statistics[N]
        }

        if(!dict["sims"]){dict["sims"] = []}
        if(!dict["paths"]){dict["paths"] = []}
        if(!dict["conv"]){dict["conv"] = []}

        dict["sims"].push(simulations);
        this.walkTree(this.#rootNode, 0, dict["paths"])
        dict["conv"].push(convincity);
    }

    walkTree(node,depth,paths){
        const children = node.getChildren();
        if(children.length === 0){
            paths.push(depth);
            return;
        }
        children.forEach(child => this.walkTree(child,depth+1,paths));
    }

}