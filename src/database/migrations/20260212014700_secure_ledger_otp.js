/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema
        .alterTable('otp_codes', table => {
            table.timestamp('verified_at');
        })
        .alterTable('wallet_transactions', table => {
            table.string('reference_id').index(); // Link to block_id or gateway_txid
        });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema
        .alterTable('otp_codes', table => {
            table.dropColumn('verified_at');
        })
        .alterTable('wallet_transactions', table => {
            table.dropColumn('reference_id');
        });
};
