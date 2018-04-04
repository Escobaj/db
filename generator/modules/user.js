let faker = require('faker');

function init_user(connection) {
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
}

module.exports = {
    init_user: init_user
};