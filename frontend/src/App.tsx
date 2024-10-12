import Cards from "./components/Cards.jsx";
import {useEffect, useState} from "react";

interface CurrenciesResponse {
  currencies: { code: string, equals_usd: string }[],
}

type Currencies = { [key: string]: number };

export default function App() {
  const [currencies, setCurrencies] = useState({} as Currencies);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch("/v1/currencies/").then(async (resp) => {
      if (!resp.ok) throw new Error("Failed to fetch currencies");
      const data: CurrenciesResponse = await resp.json();
      const currs: { [key: string]: number } = {};
      for (const curr of data.currencies) {
        currs[curr.code] = Number(curr.equals_usd);
      }
      setCurrencies(currs);
      setIsLoading(false);
    });
  }, []);

  if (isLoading) {
    return (
      <div className="vh-100 wh-100 d-flex justify-content-center align-items-center">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  } else {
    return (
      <div className="container mt-3" style={{maxWidth: 500}}>
        <Cards currencies={currencies}/>
      </div>
    );
  }
}
