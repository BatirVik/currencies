import Cards from "./components/Cards.jsx";
import { useEffect, useState } from "react";

export default function App() {
  const [currencies, setCurrencies] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const url = new URL("/v1/currencies", import.meta.env.VITE_API_URL);
    fetch(url).then(async (resp) => {
      if (!resp.ok) throw new Error("Failed to fetch currencies");
      const data = await resp.json();
      const currs = {};
      for (const curr of data.currencies) {
        currs[curr.code] = curr.equals_usd;
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
      <div className="container mt-3" style={{ maxWidth: 500 }}>
        <Cards currencies={currencies} />
      </div>
    );
  }
}
