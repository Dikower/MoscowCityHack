'use strict';

const {DialogManger} = require("dialute");
const express = require("express");
const chalk = require("chalk");
const fs = require("fs");

function choice(choices) {
  const index = Math.floor(Math.random() * choices.length);
  return choices[index];
}


function* script(r) {
  yield 'Приветствуем в мультичатах'
  // let rsp = r.buildRsp()
  // if ('отправить' ===r.nlu.lemmas[0]){
  //   rsp.data = {"text": r.msg}
  //
  // }
}


const dm = new DialogManger(script);
const app = express();
const port = 8000;


app.use((req, res, next) => {
  console.info(`${chalk.cyanBright(new Date().toUTCString())} - ${chalk.green(req.method)}:`, chalk.cyan(req.path));
  next();
});
app.use(express.json());
// app.use(express.static('../frontend/public'))
app.use(express.static('public'))
//
app.post('/log', (request, response) => {
  // console.log(request.body);
  response.send('ok')
})

app.post('/app-connector/', (request, response) => {
  const body = dm.process(request.body);
  response.send(body);
});

app.listen(port, () => console.log(chalk.blue(`Start server on http://localhost:${port}/`)));
