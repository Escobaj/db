let gimage = require('google-images');
const mysql = require('mysql2/promise');


async function getAsyncConnection() {
    return await mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: '1234',
        database: 'db'
    })
}

async function addActor(name) {

    let connection = await getAsyncConnection();
    try {
        let [rows] = await connection.execute('SELECT count(*) as count, id FROM characters where fullname = ?', [name]);
        if (rows[0].count === 0) {
            // const client = new gimage('004286675445984025592:ypgpkv9fjd4', 'AIzaSyCzb6SI_JRrp6xLLYV617Ary6n59h36ros');
            // // const client = new gimage('012157162083291474543:u54qkbzekyg', 'AIzaSyCCJzNWDsYMc_NnfrhUGlN7NhmtNpqvV7g');
            // let images = [];
            // try {
            //     images = await client.search(name);
            // } catch (e) {
            //     console.log("erreur");
            // }
            let url = null;
            // images.some((elem) => {
            //     if (elem.height > elem.width) {
            //         url = elem.url;
            //         return false;
            //     }
            //     return true;
            // });
            let insert = await connection.execute('INSERT INTO characters (fullname, picture) VALUES (?, ?)',
                [name, url]);
            await connection.close();
            return insert[0].insertId;
        } else {
            await connection.close();
            return rows[0].id;
        }
    } catch (e) {
        console.log(e);
        await connection.close();
    }

}

async function addGenre(name) {
    let connection = await getAsyncConnection();

    try {
        let [rows] = await connection.execute('SELECT count(*) as count, id FROM genres where name = ?', [name]);
        if (rows[0].count === 0) {
            let insert = await connection.execute('INSERT INTO genres (name) VALUES (?)',
                [name]);
            await connection.close();
            return insert[0].insertId;
        } else {
            await connection.close();
            return rows[0].id;
        }
    } catch (e) {
        console.log(e);
        await connection.close();
    }
}

async function addCountry(name) {
    let connection = await getAsyncConnection();

    try {
        let [rows] = await connection.execute('SELECT count(*) as count, id FROM countries where name = ?', [name]);
        if (rows[0].count === 0) {
            let insert = await connection.execute('INSERT INTO countries (name) VALUES (?)', [name]);
            await connection.close();
            return insert[0].insertId;
        } else {
            await connection.close();
            return rows[0].id;
        }
    } catch (e) {
        console.log(e);
        await connection.close();
    }
}

module.exports = {
    addActor: addActor,
    getAsyncConnection: getAsyncConnection,
    addGenre: addGenre,
    addCountry: addCountry
}