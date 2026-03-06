/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return knex.schema
        .alterTable('designs', table => {
            table.index(['category', 'availability_status', 'created_at'], 'idx_design_discovery');
        })
        .alterTable('blocks', table => {
            table.index(['user_id', 'status'], 'idx_block_limit_check');
            table.index(['status', 'expiry_time'], 'idx_block_expiry_worker');
        })
        .alterTable('appointments', table => {
            table.index(['block_id', 'status'], 'idx_appt_bridge_integrity');
        })
        .alterTable('wallet_transactions', table => {
            table.index(['wallet_id', 'created_at'], 'idx_wallet_history');
        });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return knex.schema
        .alterTable('designs', table => table.dropIndex(null, 'idx_design_discovery'))
        .alterTable('blocks', table => {
            table.dropIndex(null, 'idx_block_limit_check');
            table.dropIndex(null, 'idx_block_expiry_worker');
        })
        .alterTable('appointments', table => table.dropIndex(null, 'idx_appt_bridge_integrity'))
        .alterTable('wallet_transactions', table => table.dropIndex(null, 'idx_wallet_history'));
};
