import React from "react";
import { useEffect, useState } from "react";
function App() {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    fetch("https://us-central1-aicis-control.cloudfunctions.net/api/api/trades", {
        method: "GET",
        headers: {
            "Cache-Control": "no-cache",  // Prevent cached response
            "Pragma": "no-cache"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Fetched Trades:", data);
        setTrades(data);
    })
    .catch(error => console.error("Error fetching trades:", error));
}, []);
  return (
    <div>
      <h1>🔥 AICIS Control Panel 🔥</h1>
      <h2>Trade Data</h2>
      {trades.length === 0 ? (
        <p>No trade data available.</p>
      ) : (
        <ul>
          {trades.map((trade, index) => (
            <li key={index}>
              <strong>{trade.pair}</strong> - {trade.action} at ${trade.price} (Profit: {trade.profit})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}  
export default App;

