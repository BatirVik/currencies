import Card from "./Card";
import {v4 as uuidv4} from "uuid";
import {useImmer} from "use-immer";
import {useState, FormEvent, ChangeEvent} from "react";

interface Props {
  currencies: { [key: string]: number }
}

export default function CardList({currencies}: Props) {
  const [usdValue, setUsdValue] = useState(1 as number | null);
  if (isNaN(Number(currencies["USD"]))) {
    throw new Error("Currencies must have at least a number value for 'USD'");
  }
  const [cardCurrencies, setCardCurrencies] = useImmer([
    {id: uuidv4(), code: "USD", value: String(usdValue)},
  ]);

  function handleValueChange(currencyId: string, event: FormEvent<HTMLInputElement>): void {
    setCardCurrencies((draft) => {
      const card = draft.find((card) => card.id === currencyId);
      if (card === undefined) {
        throw new Error("Currency " + currencyId + " not found!")
      }
      if (event.currentTarget.value === "") {
        setUsdValue(null);
      } else {
        setUsdValue(
          calculateUsdValueFrom(card.code, Number(card.value))
        );
      }
    });
  }

  function handleCodeChange(currencyId: string, event: ChangeEvent<HTMLSelectElement>): void {
    setCardCurrencies((draft) => {
      const card = draft.find((card) => card.id === currencyId);
      if (card === undefined) {
        throw new Error("Currency " + currencyId + " not found!")
      }
      card.code = event.target.value;
    });
  }

  function handleRemove(currencyId: string): void {
    setCardCurrencies(cardCurrencies.filter((curr) => curr.id !== currencyId));
  }

  function handleAdd(): void {
    setCardCurrencies((draft) => {
      draft.push({id: uuidv4(), code: "USD", value: String(usdValue)});
    });
  }

  function roundValue(num: number): number {
    if (
      num.toString().includes(".") &&
      num.toString().split(".")[1].length > 2
    ) {
      return parseFloat(num.toFixed(2));
    }
    return num;
  }

  function calculateValue(code: string): string {
    if (usdValue === null) return "";
    const equals_usd = currencies[code];
    return String(roundValue(usdValue / equals_usd));
  }

  function calculateUsdValueFrom(code: string, value: number): number {
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
          <i className="bi bi-plus text-secondary"/>
        </button>
      </div>
    </div>
  );
}
