function init(connection) {
    connection.query(
        'INSERT INTO roles (name)' +
        '   VALUES (?), (?), (?)',
        ['actor', 'director', 'writter'],

        function (err, results, fields) {
            connection.close();
        }
    );
}

module.exports = {
    init: init,
};