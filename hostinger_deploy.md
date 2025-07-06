# Hostinger Deployment Guide

## Recommended Approach for Hostinger

### 1. File Manager Upload
- Use `.sql.zip` format (max 50MB on shared hosting)
- Upload via Hostinger File Manager or FTP
- Store in `/domains/yourdomain.com/private_html/backups/`

### 2. phpMyAdmin Import
- Hostinger provides phpMyAdmin access
- Import uncompressed `.sql` files (max 2MB)
- For larger files, use the PHP script method

### 3. Automated Backups
```php
// Add to your cron jobs in Hostinger panel
// Schedule: 0 2 * * * (daily at 2 AM)
/usr/bin/php /home/u123456789/domains/yourdomain.com/public_html/hostinger_backup.php
```

## File Naming for Hostinger
- `database_backup.sql` - Direct import via phpMyAdmin  
- `database_backup.sql.zip` - Compressed for file manager
- `backup_2024-01-01_02-00-00.sql.gz` - Automated timestamped backups

## Storage Locations
- `/public_html/admin/backups/` - Web accessible (password protect)
- `/private_html/backups/` - Private storage (recommended)
- External: Google Drive integration via Hostinger tools
