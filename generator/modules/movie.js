let request = require('request');

function add_movie(connection) {
    request('http://www.omdbapi.com/?s=' + process.argv[3] + '&page=&apikey=9194a1a8', (error, response, body) => {
        let tab = JSON.parse(body);
        tab.Search.forEach(async (elems, i) => {
            if (elems.Type === 'movie') {
                request('http://www.omdbapi.com/?apikey=9194a1a8&i=' + elems.imdbID, (error, response, body) => {
                    body = JSON.parse(body);
                    connection.query(
                        'INSERT INTO movies (name, release_year, duration, description, awards, picture,' +
                        ' production, box_office, website, rated) ' +
                        '   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        [body.Title, (body.Released === 'N/A') ? undefined : parseInt(body.Released, 10),
                            (body.Released === 'N/A') ? undefined : parseInt(body.Released, 10),
                            body.Plot, body.Awards, body.Poster, body.Production,
                            parseInt(body.BoxOffice.replace('$', '').split(',').join(''), 10) || 0,
                            body.Website, body.Rated],
                        function (err) {
                            console.log(err);
                        }
                    );
                }
            )
            }
        })
    });
}

module.exports = {
    add_movie: add_movie
};