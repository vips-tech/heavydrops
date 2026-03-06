/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema
        .createTable('notifications', table => {
            table.increments('notification_id').primary();
            table.integer('user_id').unsigned().references('user_id').inTable('users');
            table.string('type').notNullable(); // block_confirmation, expiry_warning, etc.
            table.string('channel').notNullable(); // sms, email, in_app
            table.string('status').defaultTo('pending'); // pending, sent, failed
            table.text('payload').notNullable(); // JSON payload
            table.integer('retry_count').defaultTo(0);
            table.timestamps(true, true);
        })
        .createTable('notification_queue', table => {
            table.increments('job_id').primary();
            table.string('event_type').notNullable();
            table.text('payload').notNullable();
            table.string('status').defaultTo('pending'); // pending, processing, completed, failed
            table.integer('attempts').defaultTo(0);
            table.timestamp('next_attempt_at').defaultTo(knex.fn.now());
            table.timestamps(true, true);
        });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema
        .dropTableIfExists('notification_queue')
        .dropTableIfExists('notifications');
};
