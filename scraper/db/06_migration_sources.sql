-- =============================================================================
-- Migration : étendre les contraintes CHECK pour pawolotek, potomitan, conte
-- À exécuter manuellement sur une base déjà initialisée :
--   psql -h localhost -p 5431 -U postgres -d poo_db -f db/06_migration_sources.sql
-- =============================================================================

ALTER TABLE documents
    DROP CONSTRAINT IF EXISTS chk_source,
    ADD  CONSTRAINT chk_source
         CHECK (source IN ('bizouk','kiprix','madiana','rci','kreyol','pawolotek','potomitan'));

ALTER TABLE documents
    DROP CONSTRAINT IF EXISTS chk_doc_type,
    ADD  CONSTRAINT chk_doc_type
         CHECK (doc_type IN ('annonce','produit','film','actualite','mot','conte'));
