const Parser = require("./usbdescreqparser.js");
const fs = require("fs");

const stddescHex = fs.readFileSync("testdata/stddesc-hex.txt", "utf-8");
const stddescExpected = fs
  .readFileSync("testdata/stddesc-expected.txt", "utf-8")
  .trimEnd();

describe("best_guess", () => {
  test("stddesc", () => {
    const parser = new Parser();

    console.log(stddescHex);

    expect(parser.best_guess(stddescHex)).toBe(stddescExpected);
  });
});
