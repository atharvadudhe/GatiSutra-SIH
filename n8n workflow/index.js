// server.js
import express from "express";

const app = express();
app.use(express.json());

app.post("/vehicle-detection", (req, res) => {
  console.log("Incoming vehicle detection:", req.body);

  fetch("http://localhost:5678/webhook-test/emergency-vehicle", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req.body),
  })
    .then(() => console.log("Forwarded to n8n"))
    .catch((err) => console.error("Error:", err));

  res.json({ status: "Vehicle detection received", data: req.body });
});

app.post("/change-signal", (req, res) => {
  // Example body: { signalId: "junction-12", status: "GREEN" }
  console.log("Traffic signal updated:", req.body);
  res.json({ message: "Signal updated successfully", data: req.body });
});


app.listen(3001, '0.0.0.0', () => {
  console.log("Dummy backend running on port 3001");
});
