
DB := cached.db

all:
	echo not clear what this should do yet

initdb: seed.csv
	rm -f -- $(DB)
	sqlite3 $(DB) < schema.sql
	sqlite3 -init init.sql $(DB) ".import $^ cases_log"

clean:
	rm -f -- $(DB)

