export default function Card({
  code,
  onCodeChange,
  value,
  onValueChange,
  onRemove,
}) {
  return (
    <div className="d-flex p-1 border gap-1 rounded flex">
      <select
        className="form-select w-auto"
        onChange={(e) => onCodeChange(e.target.value)}
      >
        <option>{code}</option>
      </select>
      <input
        type="number"
        className="form-control"
        onChange={(e) => onValueChange(e.target.value)}
        value={value}
      />
      <button className="btn border text-secondary" onClick={onRemove}>
        <i className="bi-x bi" />
      </button>
    </div>
  );
}
