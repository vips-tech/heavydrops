/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema
        .createTable('users', table => {
            table.increments('user_id').primary();
            table.string('phone').unique().notNullable();
            table.string('role').defaultTo('buyer');
            table.integer('intent_score').defaultTo(0);
            table.integer('strike_count').defaultTo(0);
            table.timestamp('last_login');
            table.timestamps(true, true);
        })
        .createTable('sellers', table => {
            table.increments('seller_id').primary();
            table.string('business_name').notNullable();
            table.string('email').unique().notNullable();
            table.string('city').notNullable();
            table.integer('trust_score').defaultTo(100);
            table.string('membership_status').defaultTo('applicant'); // applicant, active, suspended
            table.timestamps(true, true);
        })
        .createTable('designs', table => {
            table.increments('design_id').primary();
            table.integer('seller_id').unsigned().references('seller_id').inTable('sellers');
            table.string('category').notNullable();
            table.string('purity').notNullable();
            table.float('weight').notNullable();
            table.float('gold_rate_snapshot').notNullable();
            table.float('making_charge_snapshot').notNullable();
            table.string('media_quality_status').defaultTo('pending'); // pending, approved, rejected
            table.string('availability_status').defaultTo('available'); // available, blocked, sold
            table.timestamps(true, true);
        })
        .createTable('wallets', table => {
            table.increments('wallet_id').primary();
            table.integer('user_id').unsigned().references('user_id').inTable('users');
            table.float('balance').defaultTo(0);
            table.timestamp('last_updated').defaultTo(knex.fn.now());
        })
        .createTable('blocks', table => {
            table.increments('block_id').primary();
            table.integer('user_id').unsigned().references('user_id').inTable('users');
            table.integer('design_id').unsigned().references('design_id').inTable('designs');
            table.float('price_snapshot').notNullable();
            table.string('status').defaultTo('active'); // active, expired, converted
            table.timestamp('expiry_time').notNullable();
            table.timestamps(true, true);
        })
        .createTable('appointments', table => {
            table.increments('appointment_id').primary();
            table.integer('user_id').unsigned().references('user_id').inTable('users');
            table.integer('seller_id').unsigned().references('seller_id').inTable('sellers');
            table.integer('block_id').unsigned().references('block_id').inTable('blocks');
            table.string('status').defaultTo('requested'); // requested, confirmed, attended, no_show, cancelled
            table.timestamp('appointment_time');
            table.boolean('liability_accepted').defaultTo(false);
            table.timestamps(true, true);
        })
        .createTable('violations', table => {
            table.increments('violation_id').primary();
            table.string('entity_type').notNullable(); // buyer, seller
            table.integer('entity_id').notNullable();
            table.string('type').notNullable();
            table.string('level').defaultTo('warning'); // warning, suspension, removal
            table.text('reason');
            table.timestamps(true, true);
        })
        .createTable('wallet_transactions', table => {
            table.increments('transaction_id').primary();
            table.integer('wallet_id').unsigned().references('wallet_id').inTable('wallets');
            table.float('amount').notNullable();
            table.string('type').notNullable(); // credit, debit
            table.string('source_type').notNullable(); // block_payment, forfeit, correction
            table.text('description');
            table.timestamps(true, true);
        });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema
        .dropTableIfExists('wallet_transactions')
        .dropTableIfExists('violations')
        .dropTableIfExists('appointments')
        .dropTableIfExists('blocks')
        .dropTableIfExists('wallets')
        .dropTableIfExists('designs')
        .dropTableIfExists('sellers')
        .dropTableIfExists('users');
};
