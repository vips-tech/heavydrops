const db = require('../config/db');
const queueService = require('../services/queueService');
const trustService = require('../services/trustService');
const { z } = require('zod');

/**
 * Handle Appointment Booking
 * Must link to an ACTIVE block
 */
exports.bookAppointment = async (req, res) => {
    const schema = z.object({
        block_id: z.number(),
        appointment_time: z.string().datetime(),
        liability_accepted: z.boolean().optional()
    });

    try {
        const { block_id, appointment_time, liability_accepted } = schema.parse(req.body);
        const user_id = req.user.id;

        // 1. Validate Block Status and Get Design/Seller info
        const block = await db('blocks')
            .join('designs', 'blocks.design_id', 'designs.design_id')
            .where({ 'blocks.block_id': block_id, 'blocks.user_id': user_id, 'blocks.status': 'active' })
            .select('blocks.*', 'designs.seller_id')
            .first();

        if (!block) {
            return res.status(400).json({ error: 'Cannot book appointment. No active intent block found for this design.' });
        }

        const seller_id = block.seller_id;

        // 2. Check for duplicate appointment for this block
        const existingAppt = await db('appointments')
            .where({ block_id, status: 'requested' })
            .orWhere({ block_id, status: 'confirmed' })
            .first();

        if (existingAppt) {
            return res.status(400).json({ error: 'An appointment is already linked to this intent block.' });
        }

        // 3. Create Appointment Entry
        const [appointmentId] = await db('appointments')
            .insert({
                user_id,
                seller_id,
                block_id,
                appointment_time,
                status: 'requested',
                liability_accepted: !!liability_accepted
            }, ['appointment_id']);

        // Emit Notification
        await queueService.publish('appointment.booked', {
            user_id: user_id,
            design_id: block.design_id,
            time: appointment_time
        });

        res.status(201).json({
            message: 'Appointment requested successfully',
            appointment_id: appointmentId
        });
    } catch (error) {
        console.error('[BRIDGE] Booking failed:', error);
        res.status(500).json({ error: 'Failed to create appointment' });
    }
};

/**
 * Update Appointment Status (Seller/Admin Action)
 */
exports.updateAppointmentStatus = async (req, res) => {
    console.log(`[DEBUG] updateAppointmentStatus Called. Params: ${JSON.stringify(req.params)}, Body: ${JSON.stringify(req.body)}`);
    try {
        const { appointment_id } = req.params;
        const { status } = req.body; // confirmed, attended, no_show, cancelled

        const validStatuses = ['confirmed', 'attended', 'no_show', 'cancelled'];
        if (!validStatuses.includes(status)) {
            return res.status(400).json({ error: 'Invalid status update' });
        }

        await db.transaction(async (trx) => {
            const appt = await trx('appointments').where({ appointment_id }).first();
            if (!appt) throw new Error('Appointment not found');

            // Update Appointment
            await trx('appointments')
                .where({ appointment_id })
                .update({ status, updated_at: trx.fn.now() });

            console.log(`[DEBUG] Status identified: ${status}`);
            // Logic Branch: If ATTENDED, convert block
            if (status === 'attended') {
                console.log(`[DEBUG] Converting block #${appt.block_id}`);
                await trx('blocks')
                    .where({ block_id: appt.block_id })
                    .update({ status: 'converted' });
            }

            // Logic Branch: If NO_SHOW, trigger penalty signal
            if (status === 'no_show') {
                console.log(`[DEBUG] Triggering penalizeNoShow for User #${appt.user_id}`);
                await trustService.penalizeNoShow(appt.user_id, appt.block_id, trx);

                // Emit Notification
                await queueService.publish('appointment.no_show', {
                    user_id: appt.user_id,
                    design_id: appt.design_id,
                    appointment_id: appt.appointment_id
                }, trx);
            }
        });

        res.json({ message: `Appointment status updated to ${status}` });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};
