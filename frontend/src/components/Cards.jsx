import { useImmer } from "use-immer";
import Card from "./Card";
import { v4 as uuidv4 } from "uuid";

export default function CardList() {
  const [currencies, setCurrencies] = useImmer([
    { id: uuidv4(), code: "USD", value: 0.0 },
    { id: uuidv4(), code: "UKR", value: 0.0 },
  ]);

  function handleValueChange(currencyId, value) {
    setCurrencies((draft) => {
      const curr = draft.find((curr) => curr.id === currencyId);
      curr.value = value;
    });
  }

  function handleCodeChange(currencyId, code) {
    setCurrencies((draft) => {
      const curr = draft.find((curr) => curr.id === currencyId);
      curr.code = code;
    });
  }

  function handleRemove(currencyId) {
    setCurrencies(currencies.filter((curr) => curr.id !== currencyId));
  }

  function handleAdd() {
    setCurrencies((draft) => {
      draft.push({ id: uuidv4(), code: "USD", value: 0 });
    });
  }

  const cardsListItems = currencies.map((curr) => (
    <div key={curr.id} className="col">
      <Card
        value={curr.value}
        code={curr.code}
        onValueChange={handleValueChange.bind(null, curr.id)}
        onCodeChange={handleCodeChange.bind(null, curr.id)}
        onRemove={handleRemove.bind(null, curr.id)}
      />
    </div>
  ));
  return (
    <div className="row row-cols-1 gap-3">
      {cardsListItems}
      <div className="col d-flex justify-content-center">
        <button className="btn border" onClick={handleAdd}>
          <i className="bi bi-plus text-secondary" />
        </button>
      </div>
    </div>
  );
}
