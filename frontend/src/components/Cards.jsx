import Card from "./Card";
import { v4 as uuidv4 } from "uuid";
import { useImmer } from "use-immer";
import { useState } from "react";
import { useEffect } from "react";

export default function CardList({ currencies }) {
  const [usdValue, setUsdValue] = useState(1);
  if (isNaN(Number(currencies["USD"]))) {
    throw new Error("Currencies must have at least a number value for 'USD'");
  }
  const [cardCurrencies, setCardCurrencies] = useImmer([
    { id: uuidv4(), code: "USD", value: usdValue },
  ]);

  function handleValueChange(currencyId, event) {
    setCardCurrencies((draft) => {
      const curr = draft.find((curr) => curr.id === currencyId);
      curr.value = event.target.value;
      if (curr.value === "") {
        setUsdValue(null);
      } else {
        setUsdValue(calculateUsdValueFrom(curr.code, curr.value));
      }
    });
  }

  function handleCodeChange(currencyId, event) {
    setCardCurrencies((draft) => {
      const curr = draft.find((curr) => curr.id === currencyId);
      curr.code = event.target.value;
    });
  }

  function handleRemove(currencyId) {
    setCardCurrencies(cardCurrencies.filter((curr) => curr.id !== currencyId));
  }

  function handleAdd() {
    setCardCurrencies((draft) => {
      draft.push({ id: uuidv4(), code: "USD", value: usdValue });
    });
  }

  function roundValue(num) {
    if (
      num.toString().includes(".") &&
      num.toString().split(".")[1].length > 2
    ) {
      return parseFloat(num.toFixed(2));
    }
    return num;
  }

  function calculateValue(code) {
    if (usdValue === null) return "";
    const equals_usd = currencies[code];
    return roundValue(usdValue / equals_usd);
  }

  function calculateUsdValueFrom(code, value) {
    const equals_usd = currencies[code];
    return value * equals_usd;
  }

  const cardsListItems = cardCurrencies.map((curr) => {
    const value = calculateValue(curr.code);
    return (
      <div key={curr.id} className="col">
        <Card
          value={value}
          code={curr.code}
          availableCodes={Object.keys(currencies)}
          onValueChange={handleValueChange.bind(null, curr.id)}
          onCodeChange={handleCodeChange.bind(null, curr.id)}
          onRemove={handleRemove.bind(null, curr.id)}
        />
      </div>
    );
  });

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
