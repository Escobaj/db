let request = require('async-request');
let {addGenre, addCountry, getAsyncConnection} = require('./utilitary')

async function add_game() {

    let connection = await getAsyncConnection();

    try {
        let response = await request('http://www.omdbapi.com/?s=' + process.argv[3] + '&page=&apikey=9194a1a8')
        let tab = JSON.parse(response.body).Search;
        for (let i = 0; i < tab.length; i += 1) {

            if (tab[i].Type === 'game') {

                response = await request('http://www.omdbapi.com/?apikey=9194a1a8&i=' + tab[i].imdbID)
                let body = JSON.parse(response.body);
                try {
                    let [rows] = await connection.execute(
                            'INSERT INTO games (name, release_year, description, awards, picture)' +
                            '   VALUES (?, ?, ?, ?, ?)',
                            [body.Title, (body.Year === 'N/A') ? null : parseInt(body.Year, 10),
                                (body.Plot === 'N/A') ? null : body.Plot,
                                (body.Awards === 'N/A') ? null : body.Awards,
                                (body.Poster === 'N/A') ? null : body.Poster]);

                    let genreList = body.Genre.split(',')
                    for (let i = 0; i < genreList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO genre_game (games_id, genres_id) VALUES (?, ?)',
                            [rows.insertId, await addGenre(genreList[i].trim())]);
                    }

                    let countryList = body.Country.split(',')
                    for (let i = 0; i < countryList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO country_game (games_id, countries_id) VALUES (?, ?)',
                            [rows.insertId, await addCountry(countryList[i].trim())]);
                    }
                } catch (e) {
                    console.log(e)
                }
            }
        }
    } catch (e) {
        console.log(e);
    } finally {
        await connection.close();
    }
}

module.exports = {
    add_game: add_game
};