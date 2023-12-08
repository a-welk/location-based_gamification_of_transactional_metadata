const fs = require('fs');
const csv = require('csv-parser');

// How to run this script
if (process.argv.length !== 3) {
  console.error('Run with node userparser.js <input_file.csv>');
  process.exit(1);
}

const inputFile = process.argv[2];
const outputFile = 'outputfile.csv';
const person = 'Person'; //can be changed to process another file
const email = 'Email'; //along with this
const results = [];

fs.createReadStream(inputFile)
  .pipe(csv())
  .on('data', (row) => {
    const fullName = row[person];
    const [firstName, lastName] = fullName.split(' ');
    row[email] = `${firstName}.${lastName}@gmail.com`;
    results.push(row);
  })
  .on('end', () => {
    const ws = fs.createWriteStream(outputFile);
    ws.write(Object.keys(results[0]).join(',') + '\n');
    results.forEach((row) => {
      ws.write(Object.values(row).join(',') + '\n');
    });
    ws.end();
  });