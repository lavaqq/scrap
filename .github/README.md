### how to use

```sh
py scraping.py
```

packages: `requests`, `beautifulsoup4`, `progressbar`, `regex`

### output example

```sh
{
  "Lorem ipsum": {
    "Numéro d'entreprise": "0101.010.101",
    "Sécurité sociale": "0101010-10",
    "Numéro de TVA": "BE0101010101",
    "Type d'entité": "Personne morale",
    "Situation": "Lorem ipsum",
    "Capital": "0 EUR",
    "Forme juridique": "Lorem ipsum",
    "Effectif": "Entre 1 et 4 personnes",
    "Adresse": "Lorem ipsum, 01 0000 cerdid",
    "Téléphone": "010 10 10 10",
    "Equipe": {
      "John Doe": "Gérant",
	  # ...
    }
  }
  # ...
}
```
