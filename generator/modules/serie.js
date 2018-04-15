let request = require('async-request');
let {addActor, addGenre, addCountry, getAsyncConnection} = require('./utilitary')

async function add_serie() {

    let connection = await getAsyncConnection();

    try {
        let response = await request('http://www.omdbapi.com/?s=' + process.argv[3] + '&page=&apikey=9194a1a8')
        let tab = JSON.parse(response.body).Search;
        for (let i = 0; i < tab.length; i += 1) {
            if (tab[i].Type === 'series') {

                response = await request('http://www.omdbapi.com/?apikey=9194a1a8&i=' + tab[i].imdbID)
                let body = JSON.parse(response.body);
                try {
                    let [rows] = await connection.execute(
                        'INSERT INTO series (name, `release`, end, duration, nb_saison, description, picture, awards) ' +
                        '   VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        [body.Title, (body.Year === 'N/A') ? null : parseInt(body.Year, 10),
                            (body.Year.split('–')[1] === '' || body.Year.split('-')[1] == null ) ?
                                null : parseInt(body.Year.split('–')[1], 10),
                            (body.Runtime === 'N/A') ? null : parseInt(body.Runtime, 10),
                            parseInt(body.totalSeasons, 10),
                            (body.Plot === 'N/A') ? null : body.Plot,
                            (body.Poster === 'N/A') ? null : body.Poster,
                            (body.Awards === 'N/A') ? null : body.Awards]);

                    let actorList = body.Actors.split(',')
                    for (let i = 0; i < actorList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO character_serie (series_id, characters_id, roles_id) VALUES (?, ?, 4)',
                            [rows.insertId, await addActor(actorList[i].trim())]);
                    }

                    let directorList = body.Director.split(',')
                    for (let i = 0; i < directorList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO character_serie (series_id, characters_id, roles_id) VALUES (?, ?, 5)',
                            [rows.insertId, await addActor(directorList[i].trim())]);
                    }

                    let writerList = body.Writer.split(',')
                    for (let i = 0; i < writerList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO character_serie (series_id, characters_id, roles_id) VALUES (?, ?, 6)',
                            [rows.insertId, await addActor(writerList[i].trim())]);
                    }

                    let genreList = body.Genre.split(',')
                    for (let i = 0; i < genreList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO genre_serie (series_id, genres_id) VALUES (?, ?)',
                            [rows.insertId, await addGenre(genreList[i].trim())]);
                    }

                    let countryList = body.Country.split(',')
                    for (let i = 0; i < countryList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO country_serie (series_id, countries_id) VALUES (?, ?)',
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
    add_serie: add_serie
};