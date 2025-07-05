import Row from './Row';

const Grid = ({ grid, invalid, currentRow }) => {
  return (
    <div className="scoreboard">
      {grid.map((row, idx) => (
        <Row
          key={idx}
          id={idx}
          currentRow={currentRow}
          letters={row.letters}
          statuses={row.statuses}
          invalid={invalid && idx === currentRow}
        />
      ))}
    </div>
  );
};

export default Grid;
