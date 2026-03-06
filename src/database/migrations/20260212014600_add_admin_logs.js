/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable('admin_logs', table => {
        table.increments('log_id').primary();
        table.integer('admin_id').unsigned().references('user_id').inTable('users');
        table.string('action').notNullable(); // adjust_wallet, update_status, etc.
        table.string('target_entity').notNullable(); // user, seller, design
        table.integer('target_id').notNullable();
        table.text('description');
        table.string('ip_address');
        table.timestamp('created_at').defaultTo(knex.fn.now());
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTableIfExists('admin_logs');
};
