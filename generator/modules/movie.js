let request = require('async-request');
let {addActor, addGenre, addCountry, getAsyncConnection} = require('./utilitary')
let gimage = require('google-images');

async function add_movie() {

    let connection = await getAsyncConnection();

    try {
        let response = await request('http://www.omdbapi.com/?s=' + process.argv[3] + '&page=&apikey=9194a1a8')
        let tab = JSON.parse(response.body).Search;
        for (let i = 0; i < tab.length; i += 1) {

            if (tab[i].Type === 'movie') {

                response = await request('http://www.omdbapi.com/?apikey=9194a1a8&i=' + tab[i].imdbID)
                let body = JSON.parse(response.body);
                try {
                    let [rows] = await connection.execute(
                            'INSERT INTO movies (name, release_year, duration, description, awards, picture,' +
                            ' production, box_office, website, rated) ' +
                            '   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            [body.Title, (body.Year === 'N/A') ? null : parseInt(body.Year, 10),
                                (body.Runtime === 'N/A') ? null : parseInt(body.Runtime, 10),
                                (body.Plot === 'N/A') ? null : body.Plot,
                                (body.Awards === 'N/A') ? null : body.Awards,
                                (body.Poster === 'N/A') ? null : body.Poster,
                                (body.Production === 'N/A') ? null : body.Production,
                                parseInt(body.BoxOffice.replace('$', '').split(',').join(''), 10) || 0,
                                (body.Website === 'N/A') ? null : body.Website,
                                (body.Rated === 'N/A') ? null : body.Rated]);

                    let actorList = body.Actors.split(',')
                    for (let i = 0; i < actorList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO character_movie (movies_id, characters_id, roles_id) ' +
                            'SELECT ?, ?, id ' +
                            'FROM roles ' +
                            'WHERE name = ?',
                            [rows.insertId, await addActor(actorList[i].trim()), 'actor']);
                    }

                    let directorList = body.Director.split(',')
                    for (let i = 0; i < directorList.length; i += 1) {
                       let r = await connection.execute(
                        'INSERT INTO character_movie (movies_id, characters_id, roles_id) ' +
                        'SELECT ?, ?, id ' +
                        'FROM roles ' +
                        'WHERE name = ?',
                        [rows.insertId, await addActor(directorList[i].trim()), 'director']);
                    }

                    let writerList = body.Writer.split(',')
                    for (let i = 0; i < writerList.length; i += 1) {
                       let r = await connection.execute(
                        'INSERT INTO character_movie (movies_id, characters_id, roles_id) ' +
                        'SELECT ?, ?, id ' +
                        'FROM roles ' +
                        'WHERE name = ?',
                        [rows.insertId, await addActor(writerList[i].trim()), 'writer']);
                    }

                    let genreList = body.Genre.split(',')
                    for (let i = 0; i < genreList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO genre_movie (movies_id, genres_id) VALUES (?, ?)',
                            [rows.insertId, await addGenre(genreList[i].trim())]);
                    }

                    let countryList = body.Country.split(',')
                    for (let i = 0; i < countryList.length; i += 1) {
                        let r = await connection.execute(
                            'INSERT INTO country_movie (movies_id, countries_id) VALUES (?, ?)',
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

async function picture() {

    let connection = await getAsyncConnection();

    let r = await connection.execute(
                            'SELECT *' +
                            '  FROM characters' +
                            '    WHERE picture IS NULL or picture = \'\'');

    for (let i = 0; i < r[0].length; i += 1) {
        const client = new gimage('004286675445984025592:ypgpkv9fjd4', 'AIzaSyCzb6SI_JRrp6xLLYV617Ary6n59h36ros');
        // const client = new gimage('012157162083291474543:u54qkbzekyg', 'AIzaSyCCJzNWDsYMc_NnfrhUGlN7NhmtNpqvV7g');
        let images = [];
        try {
            images = await client.search(r[0][i].fullname);
        } catch (e) {
            console.log(e);
        }
        images.some((elem) => {
            if (elem.height > elem.width) {
                url = elem.url;
                return false;
            }
            return true;
        });
        await connection.execute('UPDATE characters SET picture = ? WHERE id = ?;', [url, r[0][i].id]);
    }
    await connection.close();
}

module.exports = {
    add_movie: add_movie,
    picture: picture
};