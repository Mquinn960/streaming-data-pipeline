\c menustats

ALTER USER menustatsuser PASSWORD 'examplepw';
GRANT ALL PRIVILEGES ON DATABASE menustats TO menustatsuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO menustatsuser;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO menustatsuser;
