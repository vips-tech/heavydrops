const knex = require('knex');
const config = require('../../knexfile');

const db = knex({
    ...config.development,
    pool: {
        afterCreate: (conn, cb) => {
            conn.run('PRAGMA journal_mode = WAL', cb);
        }
    }
});

module.exports = db;
