const Parser = require("./usbdescreqparser.js");

const fs = require("fs");
const args = process.argv.slice(2);

var command;
var filename;

if (args.length < 2) {
  command = "--best-guess";
  filename = args[0];
} else {
  command = args[0];
  filename = args[1];
}

const inTxt = fs.readFileSync(filename, "utf8");
const parser = new Parser();

var outTxt;

if (command == "--best-guess") {
  outTxt = parser.best_guess(inTxt);
} else if (command == "--hidrepdesc") {
  outTxt = parser.go_parse_hidrepdesc(inTxt);
} else if (command == "--stddesc") {
  outTxt = parser.go_parse_stddesc(inTxt);
} else if (command == "--stdrequest") {
  outTxt = parser.go_parse_stdrequest(inTxt);
} else {
  console.log("ERROR: unknown command " + command);
}

console.log(outTxt);
