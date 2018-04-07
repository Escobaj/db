let {getAsyncConnection} = require('./utilitary')

async function init() {
    let connection = await getAsyncConnection();
    await connection.execute(
        'INSERT INTO roles (name)' +
        '   VALUES (?), (?), (?)',
        ['actor', 'director', 'writer']);
    await connection.close();
}

module.exports = {
    init: init,
};