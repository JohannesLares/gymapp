# Tietokantakuvaus

## Käyttäjä

* username
* password
* user_id
* email
* created_on
* last_login
* admin

## Liike

* name
* id
* public
* user_id (FK user.id)
* description

## Setti

* id
* user_id (FK user.id)
* preset_id (FK preset.id)
* description ym
* order
* liike_id
* paino
* time
* toistojen_määrä

## Preset

* id
* name
* description
* user_id (FK user.id)
* 