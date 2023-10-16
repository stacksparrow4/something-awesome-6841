const express = require("express");
const app = express();
const port = 3000;

app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.render("pages/index");
});

app.get("/secretnotes", (req, res) => {
  res.render("pages/secretnotes");
});

app.get("/welcomer", (req, res) => {
  res.render("pages/welcomer", {
    name: req.query.name.toUpperCase() || "UNNAMED",
  });
});

app.use(express.static("static"));

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
