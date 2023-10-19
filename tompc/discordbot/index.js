const { Client, Events, GatewayIntentBits } = require("discord.js");
const { token, flag } = require("./config.json");

const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database(":memory:");

const AUTHORIZE_KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpIGxvdmUiOiJqd3RzIn0.2l7LGZh6enJW2j-QTHNCJSXWtHoYPF9hoLHnthpyzSw";

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const lastCommandTime = {};

client.once(Events.ClientReady, (c) => {
  console.log(`Ready! Logged in as ${c.user.tag}`);
});

client.on(Events.MessageCreate, (msg) => {
  if (msg.author.bot) return;
  if (!msg.content.startsWith("!")) return;

  const author = msg.author.id;

  if (!author in lastCommandTime) {
    lastCommandTime[author] = Date.now();
  } else {
    if (Date.now() - lastCommandTime[author] < 3000) {
      msg.reply("You are being rate limited");
      return;
    } else {
      lastCommandTime[author] = Date.now();
    }
  }

  const cmds = msg.content.split(" ");

  if (cmds.length === 0) {
    return;
  }

  const table_name = `user_${msg.author.id}`;

  switch (cmds[0]) {
    case "!authorize":
      if (cmds[1] === AUTHORIZE_KEY) {
        db.run(`CREATE TABLE ${table_name} (flag TEXT)`, (err) => {
          if (err) {
            console.error(err);
            msg.reply("An error occurred.");
            return;
          }

          msg.reply("Authorized user!");
        });
      } else {
        msg.reply("Invalid authorization");
      }
      break;

    case "!get":
      if (cmds.length !== 2) {
        msg.reply("usage: !get flag");
        return;
      }

      db.get(
        `SELECT name FROM sqlite_master WHERE type='table' AND name='${table_name}'`,
        (err, row) => {
          if (err || !row) {
            msg.reply("You are not authorized");
          } else {
            db.get(`SELECT ${cmds[1]} FROM ${table_name}`, (err, row) => {
              if (err) {
                msg.reply("An unexpected error occurred");
              } else if (row) {
                msg.reply("Got flag: " + JSON.stringify(row));
              } else {
                msg.reply("Flag is not there");
              }
            });
          }
        }
      );
      break;

    case "!putflag":
      db.run(`INSERT INTO ${table_name} VALUES ('${flag}')`, (err) => {
        if (err) {
          console.error(err);
          msg.reply("An error occurred. Perhaps you are not authorized");
          return;
        }

        msg.reply("Put flag!");
      });

      setTimeout(() => {
        db.run(`DELETE FROM ${table_name}`);
      }, 2000);
      break;
  }
});

client.login(token);
