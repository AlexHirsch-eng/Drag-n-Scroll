# Generated manually to fix Render database schema

from django.db import migrations, models


def force_add_video_fields(apps, schema_editor):
    """
    Force add video_file and thumbnail columns to video_video table.
    This migration uses ALTER TABLE IF EXISTS to ensure columns are added even if
    Django's migration system thinks they already exist.
    """
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            # Add video_file column - use IF NOT EXISTS to be safe
            # FileField stores as VARCHAR(100) by default
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'video_video'
                        AND column_name = 'video_file'
                    ) THEN
                        ALTER TABLE video_video
                        ADD COLUMN video_file VARCHAR(100) NULL;
                        COMMENT ON COLUMN video_video.video_file IS 'Uploaded video file';
                    END IF;
                END $$;
            """)

            # Add thumbnail column - use IF NOT EXISTS to be safe
            # ImageField stores as VARCHAR(100) by default
            cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'video_video'
                        AND column_name = 'thumbnail'
                    ) THEN
                        ALTER TABLE video_video
                        ADD COLUMN thumbnail VARCHAR(100) NULL;
                        COMMENT ON COLUMN video_video.thumbnail IS 'Video thumbnail image';
                    END IF;
                END $$;
            """)

            # Verify columns were added
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'video_video'
                AND column_name IN ('video_file', 'thumbnail')
                ORDER BY column_name;
            """)
            result = cursor.fetchall()
            print(f"Video fields after migration: {result}")


def reverse_migration(apps, schema_editor):
    """Reverse the migration - remove the columns"""
    pass  # We don't want to drop columns on reverse


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_add_missing_fields_safely'),
    ]

    operations = [
        migrations.RunPython(force_add_video_fields, reverse_migration),
    ]
