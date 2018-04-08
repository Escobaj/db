let {init} = require('./modules/init');
let {init_user, add_user_activity} = require('./modules/user');
let {add_movie, picture} = require('./modules/movie');
let {add_serie} = require('./modules/serie');
let {add_game} = require('./modules/game');


if (process.argv[2] === 'create-user') {
    init_user();
} else if (process.argv[2] === 'add-movie') {
    add_movie();
} else if (process.argv[2] === 'add-serie') {
    add_serie();
} else if (process.argv[2] === 'add-game') {
    add_game();
} else if (process.argv[2] === 'add-activity') {
    add_user_activity();
} else if (process.argv[2] === 'add-picture') {
    picture();
} else if (process.argv[2] === 'init') {
    init();
}
