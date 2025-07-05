import spinner from '../assets/spinner.png';

const Spinner = ({ loading, wordReveal, word, botSteps, done }) => {
  let utilSpace;
  if (done && botSteps.length > 0) {
    utilSpace = (
      <div>
        <div className="bot-items-heading">{`Lexibot found the answer in ${botSteps.length} tries`}</div>
        <ul className="bot-items">
          {botSteps.map((step, idx) => (
            <li key={step.guess}>
              {idx + 1}: {step.guess}
            </li>
          ))}
        </ul>
      </div>
    );
  } else {
    utilSpace = (
      <>
        <div
          className="word-reveal"
          style={{ display: wordReveal ? 'block' : 'none' }}
        >
          {`The word of the day is: ${word}`}
        </div>
        {!wordReveal && loading && (
          <div className={`spinner visible`}>
            <img
              src={spinner}
              alt="Loading Spinner"
            />
          </div>
        )}
      </>
    );
  }
  return <div className="info-bar show">{utilSpace}</div>;
};

export default Spinner;
