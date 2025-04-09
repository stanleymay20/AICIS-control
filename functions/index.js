const functions = require("firebase-functions");
const express = require("express");
const cors = require("cors");

// Initialize Express App
const app = express();
app.use(cors({ origin: true }));

// Test Route
app.get("/", (req, res) => {
  res.json({ message: "AICIS API is running!" });
});

// Trade Route
app.get("/api/trades", (req, res) => {
  res.json([
    { pair: "BTC/USD", action: "BUY", price: 45000, profit: "+5%" },
    { pair: "ETH/USD", action: "SELL", price: 3000, profit: "-2%" },
  ]);
});

// Export Function
exports.api = functions.https.onRequest(app);
