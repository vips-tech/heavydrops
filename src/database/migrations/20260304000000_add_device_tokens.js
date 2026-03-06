/**
 * Migration: Add device_tokens table for FCM push notifications
 */

exports.up = function(knex) {
    return knex.schema.createTable('device_tokens', (table) => {
        table.increments('token_id').primary();
        table.integer('user_id').unsigned().nullable();
        table.string('fcm_token', 500).notNullable().unique();
        table.string('platform', 20).defaultTo('web'); // web, android, ios
        table.boolean('is_active').defaultTo(true);
        table.timestamp('created_at').defaultTo(knex.fn.now());
        table.timestamp('last_used_at').defaultTo(knex.fn.now());
        
        table.foreign('user_id').references('users.user_id').onDelete('CASCADE');
        table.index(['user_id', 'is_active']);
    });
};

exports.down = function(knex) {
    return knex.schema.dropTableIfExists('device_tokens');
};
