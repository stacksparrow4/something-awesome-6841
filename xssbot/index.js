const express = require("express");
const app = express();

const visit = require("./bot");

const config = require("./config.json");

app.use(express.json());

app.post("/visit", async (req, res) => {
  const { runHash, url } = req.body;

  if (!config.hasOwnProperty(runHash)) {
    res.status(400).json({ message: "Run hash does not exist." });
    return;
  }

  const { baseurl, cookie } = config[runHash];

  const toVisit = baseurl + "/" + url;

  console.log(`Visiting: ${toVisit}`);

  await visit(toVisit, cookie);

  res.json({ success: true });
});

app.listen(1337, "0.0.0.0", () => console.log("Listening on port 1337"));
