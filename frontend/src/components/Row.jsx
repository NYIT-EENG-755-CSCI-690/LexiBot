
import Tile from './Tile';

const Row = ({ letters, statuses, id, invalid }) => {
    return (
        <div className={`scoreboard-row scoreboard-row${id} ${invalid ? 'mark-invalid': ''}`}>
          {letters.map((letter, idx) => (
              <Tile key={idx} letter={letter} status={statuses[idx]} />
          ))}
        </div>
    );
};

export default Row;