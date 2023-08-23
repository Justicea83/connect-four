export const PLAYER_ONE = 'player_one'
export const PLAYER_TWO = 'player_two'


export default class GameActions {
    constructor() {
        this.top = 0
        this.actions = {}
    }

    get peek() {
        if (this.top === -1) {
            return null;
        }
        return this.actions[this.top];
    }

    push(value) {
        this.top += 1;
        this.actions[this.top] = value;
    }

    pop() {
        delete this.actions[this.top]
        this.top -= 1;
    }
}

export function getColor(player) {
    if (player === PLAYER_ONE) {
        return 'red'
    }
    return 'yellow'
}