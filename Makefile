
DB := cached.db
SEED := seed.csv

all:
	echo not clear what this should do yet

initdb: $(SEED)
	rm -f -- $(DB)
	sqlite3 $(DB) < schema.sql
	sqlite3 -init init.sql $(DB) ".import $^ cases_log"

clean:
	rm -f -- $(DB)

reseed:
	sqlite3 -init init.sql $(DB) \
		'select day, cases from cases_log order by day;' \
	| tr -d '\r' > $(SEED)
