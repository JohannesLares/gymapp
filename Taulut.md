# Tietokantakuvaus

## Käyttäjä

* username
* password
* user_id
* email
* created_on
* last_login

## Liike

* name
* id
* public
* user_id (FK user.id)
* description

## Toisto

* id
* liike_id (FK liike.id)
* paino
* setti_id (FK setti.id)
* time

## Setti

* id
* user_id (FK user.id)
* preset_id (FK preset.id)
* description ym
* order

## Preset

* id
* name
* description
* user_id (FK user.id)
* 