# Painojenkirjaussovellus

### Ongelma

Kuntosalilla monet kirjaavat mitä liikkeitä tekee, millä painolla, monellako toistolla ja monellako sarjalla. Tästä saa nopeasti epäselvän kirjauksen, tai vähintäänkin alkaa ärsyttää, kun joka kerta joutuu kirjoittamaan uudestaan, mitä liikkeitä aikoo tehdä.

### Ratkaisu

Koodataan webapp, joka helpottaa ja suoraviivaistaa tämän prosessin seuraavasti.

### Tarkemmin

  * Sovelluksessa lista liikkeitä, joita admin voi lisätä (Nämä näkyy kaikille)
  * Käyttäjä voi lisätä itselleen omia liikkeitä (Nämä näkyy vain käyttäjälle)
  * Käyttäjä voi tehdä erilaisia sarjayhdistelmiä ("presettejä") (esim vetävät, työntävät, jalat tms)
  * Salilla valitsee yhden näistä preseteistä, jonka jälkeen liikkeet tulevat kirjattavaksi tässä järjestyksessä
  * Järjestystä voi muuttaa kesken treenin (Jos joku laite esim varattu)
  * Liikkeitä voi lisätä tähän treeniin (vaikuttamatta presettiin) kesken treenin
  * Kun kirjataan liikettä:
    * Jokainen sarja erikseen (vaikka nappi, jossa "seuraava sarja")
    * Sarjaan kirjataan paino (oletuksena edellisen sarjan paino) ja toistojen määrä (määrä voi tulla presetistä myös ehkä)
    * Sarjasta voi myös siirtyä seuraavaan liikkeeseen
  * Sovelluksen tulee olla mobiiliystävällinen
  * Kun liike vaihtuu, niin näkyy edellisen kerran painot ja toistot ja sarjat

### Heroku

Testaamaan pääsee tästä linkistä [gymapp-l](http://gymapp-l.herokuapp.com)

### Työn edistyminen

Työn alku on edistynyt kohtuu hitaasti, koska python on täysin vieras kieli. Tällä hetkellä pystyy rekisteröityä käyttäjäksi ja pystyy lisäämään liikkeitä ja niitä pystyy katselemaan. Myöskin sisään pystyy kirjautumaan. Myöskin eri taulut on suunniteltu. Ilmeisesti tähän asti tehdyt SQL kyselyt on injection-proof. Koska python on niin vieras kieli, niin kaikki moneen fileen refaktorointi ym. tulee menemään varmaankin kurssin loppupuolelle. Priorisoituna nyt käytettävyys ja toimmallisuus.