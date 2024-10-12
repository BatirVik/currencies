export default function Card({
  code,
  onCodeChange,
  value,
  onValueChange,
  onRemove,
  availableCodes,
}) {
  return (
    <div className="d-flex p-1 border gap-1 rounded flex">
      <select
        className="form-select w-auto"
        onChange={onCodeChange}
        defaultValue={code}
      >
        {availableCodes.map((c) => {
          return <option key={c}>{c}</option>;
        })}
      </select>
      <input
        type="number"
        className="form-control"
        onChange={onValueChange}
        value={value}
      />
      <button className="btn border text-secondary" onClick={onRemove}>
        <i className="bi-x bi" />
      </button>
    </div>
  );
}
