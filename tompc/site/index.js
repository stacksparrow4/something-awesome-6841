const express = require("express");
const cookieParser = require("cookie-parser");
const fs = require("fs");

const app = express();
const port = 3000;

app.use(cookieParser());
app.use(express.json());

app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.render("pages/index");
});

app.get("/secretnotes", (req, res) => {
  res.render("pages/secretnotes");
});

app.get("/welcomer", (req, res) => {
  const n = (req.query.name || "UNNAMED").toUpperCase();

  if (n.indexOf("SCRIPT") >= 0 || n.length > 180) {
    res.send("Hacking detected: either request too long or script tags");
    return;
  }

  res.render("pages/welcomer", {
    name: n,
  });
});

const checkAdmin = (req, res, next) => {
  if (
    req.cookies["admin_secret"] !== "secret_admin_token_that_gives_admin_access"
  ) {
    res.status(403);
    res.send("Unauthorized. You need to be admin to view this page");
    return;
  }
  next();
};

app.get("/admin", checkAdmin, (req, res) => {
  res.render("pages/admin");
});

app.post("/debug", checkAdmin, (req, res) => {
  if (req.body.name.indexOf('"') >= 0) {
    res.json({
      message: "Hacking attempt detected!",
    });
    return;
  }

  const filePath = __dirname + "/temp.js";

  fs.writeFileSync(
    filePath,
    `module.exports = {
      "name": "${req.body.name}",
      "${req.body.name}": {
        "status": 1
      }
    }`
  );

  const rendered = require(filePath);

  res.json(rendered);
});

app.get("/view_source", checkAdmin, (req, res) => {
  res
    .type("text/plain")
    .send(fs.readFileSync(__filename, { encoding: "utf8" }));
});

app.use(express.static("static"));

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
