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
  res.render("pages/welcomer", {
    name: (req.query.name || "UNNAMED").toUpperCase(),
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

  const filePath = __dirname + "/temp.json";

  fs.writeFileSync(
    filePath,
    `{
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
