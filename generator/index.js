let mysql = require('mysql2');
let gimage = require('google-images');
let faker = require('faker');
var http = require("http");

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '1234',
    database: 'db'
});

if (process.argv[2] === 'create-user') {

    for (let i = 0; i < 100; i += 1) {
        connection.query(
            'INSERT INTO users (username, email, first_name, last_name, password)' +
            '   VALUES (?, ?, ?, ?, MD5(?))',
            [faker.internet.userName(), faker.internet.email(), faker.name.firstName(), faker.name.lastName(), faker.internet.password()],
            function (err, results, fields) {
                if (i === 99) {
                    connection.close();
                }
            }
        );
    }

} else if (process.argv[2] === 'add-movies') {
    let request = require('request');

    request('http://www.omdbapi.com/?s=' + process.argv[3] + '&page=&apikey=9194a1a8', (error, response, body) => {

        JSON.parse(body).Search.forEach((elems) => {
            if (elems.Type === 'movie') {
                request('http://www.omdbapi.com/?apikey=9194a1a8&i=' + elems.imdbID, (error, response, body) => {
                    body = JSON.parse(body);
                    connection.query(
                        'INSERT INTO movies (name, release_year, duration, description, awards, picture, production, box_office, website, rated) ' +
                        '   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        [body.Title, parseInt(body.Released, 10) || '', parseInt(body.Runtime, 10) || '', body.Plot, body.Awards, body.Poster,
                        body.Production, parseInt(body.BoxOffice, 10) || 0, body.Website, body.Rated],
                        function (err) {
                            console.log(3);
                            console.log(err);
                        }
                    );
                })
            }
        })

        //   const client = new gimage('004286675445984025592:ypgpkv9fjd4', 'AIzaSyCzb6SI_JRrp6xLLYV617Ary6n59h36ros');
        //   client.search('matt Damon')
        //       .then(images => {
        //           images.some((elem) => {
        //              if (elem.height > elem.width){
        //
        //                  return true;
        //              }
        //              return false;
        //           });
        //       });
        // connection.close();
    });
} else if (process.argv[2] === 'init') {

    // console.log(faker.company.catchPhrase());

    connection.query(
        'INSERT INTO roles (name)' +
        '   VALUES (?), (?), (?)',
        ['actor', 'director', 'writter'],
        function (err, results, fields) {
            connection.close();
        }
    );
}
