const QueryButton = ({ onQueryHandler, disabled }) => (
  <div className="button-container tooltip-wrapper">
    <button className="query-button" onClick={onQueryHandler} disabled={disabled}>
      Ask LexiBot
    </button>
    {disabled && (
      <span className="tooltip-text">Available after the game ends</span>
    )}
  </div>
);

export default QueryButton;
