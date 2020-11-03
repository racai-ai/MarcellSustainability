#!/bin/sh

curl -X POST \
    -F 'text=Ovaj tekst treba anotirati.' \
    -F 'metadata={"id":"identifikator", "year": "2020", "title": "Testni dokument", "type": "odluka", "entype": "decision", "descriptors": [{"descriptor": "testni deskriptor", "tld": "36"}, {"descriptor": "drugi testni deskriptor", "tld": "36"}], "url": "https://marcell-project.eu", "in_effect_since": "2020"}' \
    http://127.0.0.1:8008/annotate
