const Tile = ({ letter, status }) => {
  return <div className={`scoreboard-letter ${status || ''}`}>{letter}</div>;
};

export default Tile;
