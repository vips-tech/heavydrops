/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema.createTable('design_media', table => {
        table.increments('media_id').primary();
        table.integer('design_id').unsigned().references('design_id').inTable('designs').onDelete('CASCADE');
        table.string('uri').notNullable();
        table.string('media_type').defaultTo('image');
        table.string('shot_type').nullable(); // master, closeup, worn
        table.string('status').defaultTo('pending_review'); // pending_review, approved, rejected
        table.timestamps(true, true);
    });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema.dropTableIfExists('design_media');
};
