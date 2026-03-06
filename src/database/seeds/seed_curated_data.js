/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> } 
 */
exports.seed = async function (knex) {
  // Deletes ALL existing entries
  await knex('wallet_transactions').del();
  await knex('violations').del();
  await knex('appointments').del();
  await knex('blocks').del();
  await knex('wallets').del();
  await knex('designs').del();
  await knex('sellers').del();
  await knex('users').del();

  // Seed Sellers
  const [seller1, seller2] = await knex('sellers').insert([
    {
      business_name: 'Vedic Jewels',
      email: 'onboarding@vedicjewels.com',
      city: 'Mumbai',
      trust_score: 98,
      membership_status: 'active'
    },
    {
      business_name: 'Royal Heritage',
      email: 'admin@royalheritage.com',
      city: 'Mumbai',
      trust_score: 95,
      membership_status: 'active'
    }
  ], ['seller_id']);

  // Seed Designs
  await knex('designs').insert([
    {
      seller_id: 1,
      category: 'Necklace',
      purity: '22K',
      weight: 45.5,
      gold_rate_snapshot: 6200,
      making_charge_snapshot: 850,
      media_quality_status: 'approved',
      availability_status: 'available'
    },
    {
      seller_id: 1,
      category: 'Rings',
      purity: '18K Diamond',
      weight: 4.2,
      gold_rate_snapshot: 6200,
      making_charge_snapshot: 1200,
      media_quality_status: 'approved',
      availability_status: 'available'
    },
    {
      seller_id: 2,
      category: 'Bangle',
      purity: '22K',
      weight: 22.0,
      gold_rate_snapshot: 6200,
      making_charge_snapshot: 600,
      media_quality_status: 'approved',
      availability_status: 'available'
    }
  ]);

  // Seed User
  const [user] = await knex('users').insert({
    phone: '9876543210',
    role: 'buyer',
    intent_score: 100,
    strike_count: 0
  }, ['user_id']);

  // Seed Wallet
  await knex('wallets').insert({
    user_id: 1,
    balance: 5001
  });

  console.log('[SEED] Curated data injected successfully.');
};
