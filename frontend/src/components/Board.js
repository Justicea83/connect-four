import {useRef, useState} from "react";
import GameRow from "@/components/game/game-row";
import GameActions from "@/utils/GameActions";

export const COLS = 7
const ROWS = 7

const gameCell = {
    value: ''
}

export const initialGame = Array.from({length: ROWS}, () =>
    Array.from({length: COLS}, () => ({...gameCell}))
)


export default function Board() {
    const gameActions = new GameActions()

    const game = useState(initialGame)

    const cellRefs = Array.from({length: ROWS}, () =>
        Array.from({length: COLS}, () => useRef(null))
    )

    const tileClicked = (rowIndex, colIndex) => {
        console.log(`row: ${rowIndex}, col: ${colIndex}`)

        const tile = cellRefs[rowIndex][colIndex]
        console.log(tile?.current?.classList)
        if (tile) {
            tile.current.classList.add('red-piece')
        }
    }
    const buildGame = () => {
        return Array.from({length: ROWS}, (_, index) => (
            <GameRow
                key={`row-${index}`}
                row={index}
                rowRefs={cellRefs[index]}
                titleClick={(rowIndex, colIndex) => tileClicked(rowIndex, colIndex)}
            />
        ))
    }

    return (
        <div className="flex flex-col justify-center mt-10">
            <h2 className="text-white text-xl my-4">Connect Four</h2>
            <div className="board">
                <div className="flex flex-col justify-center">
                    {buildGame()}
                </div>
            </div>
        </div>
    )
}
