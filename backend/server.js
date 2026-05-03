const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();

app.use(cors());
app.use(express.json());

app.post("/api/query", async (req, res) => {
  try {
    console.log("REQ BODY:", req.body);

    const response = await axios.post(
      "http://127.0.0.1:8000/analyze",
      req.body
    );

    console.log("PYTHON RESPONSE SUCCESS");

    res.json(response.data); // ✅ IMPORTANT
  } catch (error) {
    console.error("ERROR:", error.message);
    res.status(500).json({ error: "Backend failed" });
  }
});

app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});