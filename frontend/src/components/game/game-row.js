import {COLS} from "@/components/Board";

export default function GameRow({row, rowRefs, titleClick}) {
    return (
        <div className="flex flex-row" id={row}>
            {
                Array.from(
                    {length: COLS},
                    (_, colIndex) => (
                        <div
                            className="tile"
                            key={`col-${row}-${colIndex}`}
                            ref={rowRefs[colIndex]}
                            onClick={() => titleClick(row, colIndex)}
                        />
                    )
                )
            }
        </div>
    )
}