const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
// const axios = require("axios"); // Uncomment if sending to backend

(async () => {
  const url = process.argv[2];
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle2" });

  const outputPath = path.join(__dirname, "rounds.csv");
  const captured = [];

  page.on("response", async (response) => {
    const req = response.request();
    if (req.url().includes("aviator") && req.method() === "GET") {
      const data = await response.text();
      console.log("Captured:", data);
      captured.push(data);

      // Save to rounds.csv
      fs.appendFileSync(outputPath, `${data}\n`);

      // Optional: Send to FastAPI backend
      /*
      try {
        await axios.post("http://localhost:8000/receive-data", { data });
      } catch (err) {
        console.error("Failed to send to backend:", err.message);
      }
      */
    }
  });

  // Graceful shutdown after 10 seconds
  setTimeout(async () => {
    await browser.close();
    console.log("Browser closed after timeout.");
  }, 10000);
})();
