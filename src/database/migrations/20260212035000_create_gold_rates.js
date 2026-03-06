/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable('gold_rates', table => {
        table.increments('id').primary();
        table.string('purity', 10).notNullable(); // 22K, 24K
        table.decimal('rate_per_gram', 14, 2).notNullable();
        table.timestamp('updated_at').defaultTo(knex.fn.now());
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTableIfExists('gold_rates');
};
