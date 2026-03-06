// Basic Maintenance State - In a real app, this would be in Redis or DB config
let isMaintenanceMode = false;

module.exports = {
    /**
     * Toggle maintenance mode
     */
    setMaintenanceMode: (status) => {
        isMaintenanceMode = status;
        console.log(`[SYSTEM] Maintenance Mode: ${status ? 'ENABLED' : 'DISABLED'}`);
    },

    /**
     * Middleware to block requests if maintenance is active
     */
    maintenanceGate: (req, res, next) => {
        if (isMaintenanceMode) {
            return res.status(503).json({
                error: 'Platform Emergency Freeze Active',
                message: 'System is undergoing data integrity restoration. Intent signaling is temporarily disabled.',
                status: 'maintenance'
            });
        }
        next();
    }
};
