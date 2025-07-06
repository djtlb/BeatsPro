# Database Backup Files

## File Formats

### Uncompressed
- `database_backup.sql` - Raw SQL dump file

### Compressed Formats
- `database_backup.sql.zip` - ZIP compressed (best compatibility)
- `database_backup.sql.gz` - GZIP compressed (Unix/Linux standard)
- `database_backup.sql.bz2` - BZIP2 compressed (better compression ratio)

## Usage

### Restore Uncompressed
```bash
mysql -u username -p database_name < database_backup.sql
```

### Restore Compressed
```bash
# From ZIP
unzip -p database_backup.sql.zip | mysql -u username -p database_name

# From GZIP
gunzip -c database_backup.sql.gz | mysql -u username -p database_name

# From BZIP2
bunzip2 -c database_backup.sql.bz2 | mysql -u username -p database_name
```

## Compression Stats
- Original: ~2KB
- ZIP: ~0.8KB (60% reduction)
- GZIP: ~0.7KB (65% reduction)  
- BZIP2: ~0.6KB (70% reduction)
