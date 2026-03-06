/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema
        .alterTable('users', table => {
            table.boolean('is_demo').defaultTo(false);
        })
        .alterTable('sellers', table => {
            table.boolean('is_demo').defaultTo(false);
        })
        .alterTable('designs', table => {
            table.boolean('is_demo').defaultTo(false);
        })
        .alterTable('design_media', table => {
            table.boolean('is_demo').defaultTo(false);
        });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema
        .alterTable('users', table => {
            table.dropColumn('is_demo');
        })
        .alterTable('sellers', table => {
            table.dropColumn('is_demo');
        })
        .alterTable('designs', table => {
            table.dropColumn('is_demo');
        })
        .alterTable('design_media', table => {
            table.dropColumn('is_demo');
        });
};
