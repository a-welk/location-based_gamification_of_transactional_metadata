const fs = require('fs');
const csv = require('csv-parser');
const bcrypt = require('bcryptjs');
const util = require('util');

const hashAsync = util.promisify(bcrypt.hash);

if (process.argv.length !== 3) {
  console.error('Run with node bcrypt.js <input_file.csv>');
  process.exit(1);
}

const inputFile = process.argv[2];
const outputFile = 'outputfile.csv';
const searchColumn = 'Person'; //can be changed to process another file
const newColumn = 'Password'; // along with this
const saltRounds = 12;
const results = [];

function processRow(row) {
  return new Promise(async (resolve, reject) => {
    const fullName = row[searchColumn];
    if (fullName) {
      const [firstName, lastName] = fullName.split(' ');
      const password = `${firstName}${lastName}123`;
      try {
        const hash = await hashAsync(password, saltRounds);
        row[newColumn] = hash;
        results.push(row);
        resolve();
      } catch (err) {
        console.error(err.message);
        reject(err);
      }
    } else {
      console.log('Unable to find the column to process');
      resolve();
    }
  });
}

const processingPromises = [];
fs.createReadStream(inputFile)
  .pipe(csv())
  .on('data', (row) => {
    const processingPromise = processRow(row);
    processingPromises.push(processingPromise);
  })
  .on('end', () => {
    Promise.all(processingPromises)
      .then(() => {
        if (results.length > 0) {
          const ws = fs.createWriteStream(outputFile);
          ws.write(Object.keys(results[0]).join(',') + '\n');
          results.forEach((row) => {
            ws.write(Object.values(row).join(',') + '\n');
          });
          ws.end();
        } else {
          console.log('Results array returned to process came back empty');
        }
      })
      .catch((err) => {
        console.error(err);
      });
  });
