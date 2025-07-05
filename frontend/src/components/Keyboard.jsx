const Keyboard = (props) => {


  const key_rows = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'DEL'],
  ];

  return (
    <div className="keyboard">
      {key_rows.map((key_row, rowIndex) => (
        <div key={rowIndex} className="key-row">
          {key_row.map((key) => (
            <button
              key={key}
              className={key === 'Enter' || key === 'Del' ? 'wide' : ''}
              onClick={() => props.handleKeyPress(key)}
            >
              {key}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Keyboard;
