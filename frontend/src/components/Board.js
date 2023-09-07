import {useEffect, useRef, useState} from "react";
import GameRow from "@/components/game/game-row";
import GameActions, {getColor, PLAYER_ONE, PLAYER_TWO} from "@/utils/GameActions";
import classNames from "@/utils/misc";
import useGame from "@/utils/hooks/useGame";

export const COLS = 7
const ROWS = 7
const gameCell = null
const WINDOW_SIZE = 4
const TOTAL_ACTIONS = COLS * ROWS
const LEFT = 'L'
const RIGHT = 'R'

const SINGLE_GAME_ID = 1
const ACTION_PLAY = 'action.play'
const ACTION_RESET = 'action.reset'

const initialGame = () => Array.from({length: ROWS}, () =>
    Array.from({length: COLS}, () => gameCell)
)

const LEFT_COORS = {}
const RIGHT_COORS = {}

for (let i = 0; i < ROWS; i++) {
    LEFT_COORS[`${i}:${0}`] = 1
    RIGHT_COORS[`${i}:${ROWS - 1}`] = 1
}

export default function Board() {
    const [gameActions, setGameActions] = useState(new GameActions())
    const [winner, setWinner] = useState(null)
    const [gameOver, setGameOver] = useState(false)
    const initialized = useRef(false)

    const [game, setGame] = useState(initialGame())
    const socketRef = useRef(null);

    useEffect(() => {
        if (!initialized.current) {
            initialized.current = true
            fetchData()
        }
    }, [])

    const fetchData = async () => {
        const {getSingleGame} = useGame()

        const {data} = await getSingleGame(SINGLE_GAME_ID)
        if (data && !data.is_complete) {
            const actions = data.game_actions

            actions.forEach(({action, player}) => {
                const user = parseInt(player)

                let incomingCurrentPlayer

                if (user === 1) {
                    incomingCurrentPlayer = PLAYER_ONE
                }

                if (user === 2) {
                    incomingCurrentPlayer = PLAYER_TWO
                }

                const [rowIndex, colIndex] = action.toString().split(',')
                tileClicked(rowIndex, colIndex, incomingCurrentPlayer, true)
            })
        }
    }

    useEffect(() => {
        const token = localStorage.getItem('token')
        if (!token) {
            return;
        }
        socketRef.current = new WebSocket(`ws://localhost:8000/ws/game/?token=${token}`);

        // Event handler for receiving messages
        socketRef.current.onmessage = event => {
            const eventData = JSON.parse(event.data)
            console.log("RECEIVED <<<<<<<========", eventData)
            const action = eventData.action

            if (action === ACTION_PLAY) {
                const user = parseInt(eventData.user)

                const userId = parseInt(localStorage.getItem('userId'))
                const pId = getPlayerId(userId)

                let incomingCurrentPlayer

                if (user === 1) {
                    incomingCurrentPlayer = PLAYER_ONE
                }

                if (user === 2) {
                    incomingCurrentPlayer = PLAYER_TWO
                }

                // If the action is coming from the same user, do nothing!
                if (incomingCurrentPlayer === pId) {
                    return;
                }

                const [rowIndex, colIndex] = eventData.payload.toString().split(',')
                setTimeout(() => {
                    tileClicked(rowIndex, colIndex, incomingCurrentPlayer)
                }, 10)
            }

            if (action === ACTION_RESET) {
                resetGame()
            }
        };

        // Clean up the WebSocket connection on component unmount
        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        };
    }, []);

    const getPlayerId = (id) => {
        if (id === 1) {
            return PLAYER_ONE
        }

        if (id === 2) {
            return PLAYER_TWO
        }

        return null
    }
    const broadcast = (action, payload = null) => {
        const data = {
            action, payload
        }
        console.log('SENDING DATA =====>>>>>', data)
        socketRef.current?.send(JSON.stringify(data));
    }


    const eligibleTile = (rowIndex, colIndex) => {
        return !!(LEFT_COORS[`${rowIndex}:${colIndex}`] || RIGHT_COORS[`${rowIndex}:${colIndex}`])
    }

    let cellRefs = Array.from({length: ROWS}, () =>
        Array.from({length: COLS}, () => useRef(null))
    )

    const getDirection = (rowIndex, colIndex) => {
        if (LEFT_COORS[`${rowIndex}:${colIndex}`]) {
            return LEFT
        }

        if (RIGHT_COORS[`${rowIndex}:${colIndex}`]) {
            return RIGHT
        }

        throw new Error('Invalid direction')
    }

    const rowIsNotFull = (rowIndex) => {
        return game[rowIndex].some(tile => tile === null)
    }

    const checkWinner = () => {
        // There should be at least four actions for a winner to happen
        if (gameActions.top < 4) {
            return false
        }

        // Check horizontally
        for (let row = 0; row < ROWS; row++) {
            let startCol = 0
            let endCol = startCol + WINDOW_SIZE - 1

            while (endCol <= COLS - 1) {
                const slice = game[row].slice(startCol, startCol + WINDOW_SIZE)
                const winnerPlayerOne = slice.every(tile => tile === PLAYER_ONE)
                const winnerPlayerTwo = slice.every(tile => tile === PLAYER_TWO)

                if (winnerPlayerOne || winnerPlayerTwo) {
                    if (winnerPlayerOne) {
                        setWinner(PLAYER_ONE)
                    }

                    if (winnerPlayerTwo) {
                        setWinner(PLAYER_TWO)
                    }
                    return true
                }

                startCol += 1
                endCol = startCol + WINDOW_SIZE - 1
            }
        }

        // Check vertically
        for (let col = 0; col < COLS; col++) {
            let startRow = 0
            let endRow = startRow + WINDOW_SIZE - 1

            while (endRow <= ROWS - 1) {
                const tracker = {
                    [PLAYER_ONE]: 0,
                    [PLAYER_TWO]: 0
                }

                for (let r = startRow; r <= endRow; r++) {
                    const cell = game[r][col]
                    if (cell) {
                        tracker[cell] += 1
                    }
                }

                const winnerPlayerOne = tracker[PLAYER_ONE] === WINDOW_SIZE
                const winnerPlayerTwo = tracker[PLAYER_TWO] === WINDOW_SIZE

                if (winnerPlayerOne || winnerPlayerTwo) {
                    if (winnerPlayerOne) {
                        setWinner(PLAYER_ONE)
                    }

                    if (winnerPlayerTwo) {
                        setWinner(PLAYER_TWO)
                    }
                    return true
                }

                startRow += 1
                endRow = startRow + WINDOW_SIZE - 1
            }
        }

        // Check Diagonally
        for (let r = 0; r < ROWS - WINDOW_SIZE - 1; r++) {
            // From top-left to bottom-right
            for (let c = 0; c < COLS - WINDOW_SIZE - 1; c++) {
                const player = game[r][c]
                if (
                    player === game[r + 1][c + 1]
                    && player === game[r + 2][c + 2]
                    && player === game[r + 3][c + 3]
                ) {
                    setWinner(player)
                    return true
                }
            }

            // From top-right to bottom-left
            for (let c = WINDOW_SIZE - 1; c < COLS; c++) {
                const player = game[r][c]
                if (
                    player === game[r + 1][c - 1]
                    && player === game[r + 2][c - 2]
                    && player === game[r + 3][c - 3]
                ) {
                    setWinner(player)
                    return true
                }
            }
        }
        return false
    }

    const resetGame = () => {
        window.location.reload()
    }

    const getWinnerName = () => {
        return winner?.split('_').join(' ')
    }

    const titleClickedAndBroadCast = (rowIndex, colIndex, currentPlayer) => {
        const direction = tileClicked(rowIndex, colIndex, currentPlayer)
        if (direction) {
            broadcast(ACTION_PLAY, `${rowIndex},${colIndex},${direction}`)
        }
    }

    const tileClicked = (rowIndex, colIndex, currentPlayer, automatic = false) => {
        rowIndex = parseInt(rowIndex)
        colIndex = parseInt(colIndex)

        if (!currentPlayer) {
            return
        }

        if (!automatic) {
            if (winner || gameOver) {
                alert('Click `Play Again` to continue.')
                return;
            }

            if (!eligibleTile(rowIndex, colIndex)) {
                alert('Please play from either the left or right');
                return
            }
        }

        // If the row is full we skip the action
        if (!rowIsNotFull(rowIndex)) {
            return
        }

        const direction = getDirection(rowIndex, colIndex)

        if (gameActions.peek) {
            const lastAction = gameActions.peek

            // You have already played
            if (lastAction.player === currentPlayer) {
                !automatic && alert("It's not your turn yet!")
                return
            }
        } else {

        }

        const gameTracker = [...game]

        // Check if the tile is already coloured
        if (game[rowIndex][colIndex]) {
            let columnTracker = colIndex
            while (game[rowIndex][columnTracker]) {
                if (direction === RIGHT) {
                    columnTracker -= 1;
                } else {
                    columnTracker += 1;
                }
            }

            if (direction === RIGHT) {
                for (let i = columnTracker; i < game[rowIndex].length - 1; i++) {
                    // Set the tile colors
                    let tile = cellRefs[rowIndex][i]
                    tile.current.classList.remove('red', 'yellow')
                    tile.current.classList.add(getColor(game[rowIndex][i + 1]))

                    // Set the new players
                    gameTracker[rowIndex][i] = game[rowIndex][i + 1]
                }
            } else {
                for (let i = columnTracker; i >= 1; i--) {
                    // Set the tile colors
                    let tile = cellRefs[rowIndex][i]
                    tile.current.classList.remove('red', 'yellow')
                    tile.current.classList.add(getColor(game[rowIndex][i - 1]))

                    // Set the new players
                    gameTracker[rowIndex][i] = game[rowIndex][i - 1]
                }
            }
        }

        // Set the color of the current tile
        const currentTile = cellRefs[rowIndex][colIndex]
        currentTile.current.classList.remove('red', 'yellow')
        currentTile.current.classList.add(getColor(currentPlayer))

        // Set the player of the current tile
        gameTracker[rowIndex][colIndex] = currentPlayer

        setGame(gameTracker)

        // Update the actions tracker
        gameActions.push({player: currentPlayer, coords: [rowIndex, direction]})
        setGameActions(gameActions)

        if (checkWinner()) {
            // TODO game over
        } else {
            if (gameActions.top === TOTAL_ACTIONS) {
                setGameOver(true)
            }
        }

        return direction
    }
    const buildGame = () => {
        return Array.from({length: ROWS}, (_, index) => (
            <GameRow
                key={`row-${index}`}
                row={index}
                rowRefs={cellRefs[index]}
                titleClick={(rowIndex, colIndex) => {
                    const userId = parseInt(localStorage.getItem('userId'))
                    const currentPlayer = getPlayerId(userId)
                    titleClickedAndBroadCast(rowIndex, colIndex, currentPlayer)
                }}
            />
        ))
    }

    return (
        <div className="flex flex-col justify-center mt-10">
            <h2 className="text-white text-xl my-4">Connect Four</h2>
            {gameOver && <h2 className="text-blue-500 text-xl my-4">GAME OVER!</h2>}
            <div className="my-2 flex flex-row justify-between mx-auto with-width">
                {winner &&
                    <h2
                        className={classNames('text-xl my-4', `${getColor(winner)}-text`)}>
                        {getWinnerName()} has won!
                    </h2>
                }
                {
                    (winner || gameOver) &&
                    <button
                        onClick={() => broadcast(ACTION_RESET)}
                        type="button"
                        className=" inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm "
                    >
                        Play Again
                    </button>
                }
            </div>

            <div className="board">
                <div className="flex flex-col justify-center">
                    {buildGame()}
                </div>
            </div>
        </div>
    )
}
