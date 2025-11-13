const puppeteer = require("puppeteer");

(async () => {
  const url = process.argv[2];
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle2" });

  page.on("response", async (response) => {
    const req = response.request();
    if (req.url().includes("aviator") && req.method() === "GET") {
      const data = await response.text();
      console.log("Captured:", data);
      // TODO: Save to rounds.csv or send to backend
    }
  });
})();
