/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.alterTable('users', table => {
        table.string('name').nullable();
        table.string('email').unique().nullable();
        table.string('status').defaultTo('active'); // active, restricted
        table.integer('active_block_count').defaultTo(0);
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.alterTable('users', table => {
        table.dropColumn('name');
        table.dropColumn('email');
        table.dropColumn('status');
        table.dropColumn('active_block_count');
    });
};
