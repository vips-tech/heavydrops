const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BACKUP_DIR = path.join(__dirname, '../../backups');
const DB_PATH = path.join(__dirname, '../../platform.db'); // Assumed SQLite path

/**
 * Create a timestamped snapshot of the database
 */
exports.createSnapshot = () => {
    console.log('[BACKUP] Initiating database snapshot...');

    if (!fs.existsSync(BACKUP_DIR)) {
        fs.mkdirSync(BACKUP_DIR, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(BACKUP_DIR, `snapshot_${timestamp}.db`);

    try {
        // For SQLite, a simple file copy is often sufficient if the DB is not under heavy write.
        // However, using the '.backup' command via sqlite3 CLI is safer for consistency.
        execSync(`sqlite3 ${DB_PATH} ".backup '${backupPath}'"`);

        console.log(`[BACKUP] Snapshot successfully created: ${backupPath}`);
        return backupPath;
    } catch (error) {
        console.error('[BACKUP] Snapshot failed:', error.message);
        throw error;
    }
};

/**
 * Basic pruning script - Keep last 7 days of snapshots
 */
exports.pruneOldBackups = () => {
    const files = fs.readdirSync(BACKUP_DIR);
    const now = Date.now();
    const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;

    files.forEach(file => {
        const filePath = path.join(BACKUP_DIR, file);
        const stats = fs.statSync(filePath);
        if (now - stats.mtimeMs > SEVEN_DAYS_MS) {
            fs.unlinkSync(filePath);
            console.log(`[BACKUP] Pruned old snapshot: ${file}`);
        }
    });
};
