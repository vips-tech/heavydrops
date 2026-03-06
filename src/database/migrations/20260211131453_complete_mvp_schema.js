/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema
        .createTable('design_media', table => {
            table.increments('media_id').primary();
            table.integer('design_id').unsigned().references('design_id').inTable('designs').onDelete('CASCADE');
            table.string('url').notNullable();
            table.string('type').defaultTo('image');
            table.boolean('is_primary').defaultTo(false);
            table.timestamps(true, true);
        })
        .createTable('likes', table => {
            table.increments('like_id').primary();
            table.integer('user_id').unsigned().references('user_id').inTable('users').onDelete('CASCADE');
            table.integer('design_id').unsigned().references('design_id').inTable('designs').onDelete('CASCADE');
            table.unique(['user_id', 'design_id']);
            table.timestamps(true, true);
        })
        .createTable('seller_metrics', table => {
            table.increments('metric_id').primary();
            table.integer('seller_id').unsigned().references('seller_id').inTable('sellers').onDelete('CASCADE');
            table.integer('total_designs').defaultTo(0);
            table.integer('active_blocks').defaultTo(0);
            table.integer('monthly_conversions').defaultTo(0);
            table.float('average_trust_score').defaultTo(100);
            table.timestamp('snapshot_date').defaultTo(knex.fn.now());
        });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema
        .dropTableIfExists('seller_metrics')
        .dropTableIfExists('likes')
        .dropTableIfExists('design_media');
};
