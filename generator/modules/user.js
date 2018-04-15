let faker = require('faker');
let {getAsyncConnection} = require('./utilitary')


async function init_user() {

    let connection = await getAsyncConnection();

    for (let i = 0; i < 1000; i += 1) {
        await connection.query(
            'INSERT INTO users (username, email, first_name, last_name, password)' +
            '   VALUES (?, ?, ?, ?, MD5(?))',
            [faker.internet.userName(), faker.internet.email(), faker.name.firstName(), faker.name.lastName(), faker.internet.password()]);
    }
    await connection.close();
}

async function add_user_activity() {

    let connection = await getAsyncConnection();
    try {
        let users = await connection.execute('SELECT id FROM users');
        users = users[0];

        //add review
        for (let i = 0; i < users.length; i += 1) {
            let movies = (await connection.execute('SELECT id FROM movies WHERE picture is not NULL ORDER BY RAND() LIMIT ?', [Math.round(Math.random() * 30)]))[0];
            for (let j = 0; j < movies.length; j += 1) {
                await connection.execute('INSERT INTO evaluate_movie (users_id, movies_id, comment, rate) VALUE (?, ?, ?, ?);',
                    [users[i].id, movies[j].id, faker.lorem.paragraph(), Math.round(Math.random() * 10)]);
            }
            let series = (await connection.execute('SELECT id FROM series WHERE picture is not NULL ORDER BY RAND() LIMIT ?', [Math.round(Math.random() * 30)]))[0];
            for (let j = 0; j < series.length; j += 1) {
                await connection.execute('INSERT INTO evaluate_serie (users_id, series_id, comment, rate) VALUE (?, ?, ?, ?);',
                    [users[i].id, series[j].id, faker.lorem.paragraph(), Math.round(Math.random() * 10)]);
            }
            let games = (await connection.execute('SELECT id FROM games WHERE picture is not NULL ORDER BY RAND() LIMIT ?', [Math.round(Math.random() * 30)]))[0];
            for (let j = 0; j < games.length; j += 1) {
                await connection.execute('INSERT INTO evaluate_game (users_id, games_id, comment, rate) VALUE (?, ?, ?, ?);',
                    [users[i].id, games[j].id, faker.lorem.paragraph(), Math.round(Math.random() * 10)]);
            }
        }

        //add wishList
        for (let i = 0; i < users.length; i += 1) {
            let movies = (await connection.execute('SELECT id FROM movies WHERE picture is not NULL ORDER BY RAND() LIMIT ?', [Math.round(Math.random() * 30)]))[0];
            for (let j = 0; j < movies.length; j += 1) {
                await connection.execute('INSERT INTO wish_list_movies (users_id, movies_id) VALUE (?, ?);',
                    [users[i].id, movies[j].id]);
            }
            let series = (await connection.execute('SELECT id FROM series WHERE picture is not NULL ORDER BY RAND() LIMIT ?', [Math.round(Math.random() * 30)]))[0];
            for (let j = 0; j < series.length; j += 1) {
                await connection.execute('INSERT INTO wish_list_series (users_id, series_id) VALUE (?, ?);',
                    [users[i].id, series[j].id]);
            }
            let games = (await connection.execute('SELECT id FROM games WHERE picture is not NULL ORDER BY RAND() LIMIT ?', [Math.round(Math.random() * 30)]))[0];
            for (let j = 0; j < games.length; j += 1) {
                await connection.execute('INSERT INTO wish_list_games (users_id, games_id) VALUE (?, ?);',
                    [users[i].id, games[j].id]);
            }
        }
    } catch (e) {
        console.log(e);
    }

    await connection.close();
}


module.exports = {
    init_user: init_user,
    add_user_activity: add_user_activity
};