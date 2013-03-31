#Files erased by `make clean`
CLEANABLE = db.sql graph.*

#Layout for visual representation
DOTLAYOUT = circo

db.sql: graph/models.py
	./manage.py syncdb

graph.dot : db.sql
	./manage.py graphviz > graph.dot

%.png : %.dot
	${DOTLAYOUT} -Tpng $< > $@

%.svg : %.dot
	${DOTLAYOUT} -Tsvg $< > $@

populate: db.sql graph/management/commands/populate.py
	./manage.py flush --noinput
	./manage.py populate

.PHONY : clean test
clean:
	rm -f ${CLEANABLE}

test:
	./manage.py test graph