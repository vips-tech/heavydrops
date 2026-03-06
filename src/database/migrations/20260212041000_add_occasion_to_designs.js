/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.alterTable('designs', table => {
        table.string('occasion_tag').index(); // e.g., Wedding, Engagement, Festive, Daily Wear
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.alterTable('designs', table => {
        table.dropColumn('occasion_tag');
    });
};
