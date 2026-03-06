/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.alterTable('designs', table => {
        table.integer('view_count').defaultTo(0);
        table.integer('like_count_snapshot').defaultTo(0);
        table.integer('block_count_snapshot').defaultTo(0);
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.alterTable('designs', table => {
        table.dropColumn('view_count');
        table.dropColumn('like_count_snapshot');
        table.dropColumn('block_count_snapshot');
    });
};
