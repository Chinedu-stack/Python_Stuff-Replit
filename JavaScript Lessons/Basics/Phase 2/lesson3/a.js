const game = {
    player : {
        name: "Chinedu",
        score: 100
    },

    villain: {
        health: 200,
        attack: 50
    },

    game_loops: 67 
};

game.player.score += 20;
game["player2"] = {};
game["player2"]["name"] = "Nedu";
game["player2"]["score"] = 500;
console.log(game);
