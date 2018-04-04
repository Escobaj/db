let mysql = require('mysql2');


let {init} = require('./modules/init');
let {init_user} = require('./modules/user');
let {add_movie} = require('./modules/movie');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '1234',
    database: 'db'
});

if (process.argv[2] === 'create-user') {
    init_user(connection);
} else if (process.argv[2] === 'add-movie') {
    add_movie(connection);
} else if (process.argv[2] === 'init') {
    init(connection);
}
