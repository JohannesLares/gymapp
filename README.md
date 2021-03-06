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

### Mitä tuli/ei tullut tehtyä

  * Ylläolevan listan asiat poislukien:
    * Kesken treenin voi lisätä lisää liikkeitä
    * Järjestystä voi muuttaa kesken treenin
    * Mobiiliystävällisyys
  * Treenihistorian näkee sovelluksesta

### Heroku ja sielä testaaminen

Testaamaan pääsee tästä linkistä [gymapp-l](http://gymapp-l.herokuapp.com)

Luo käyttäjä, kirjaudu sisään. Voit lisätä liikkeitä kohdassa Liikkeet => Luo uusi. Voit lisätä treenisuunnitelmia kohdasta Treenisuunnitelmat => Luo uusi. Sovellus kyllä ilmoittaa, jos jotain puuttuu (paitsi treenisuunnitelmaa luodessa ei ilmoityeta mahd puuttuvista liikkeistä, koska on jo joitain julkisia liikkeitä)

## Vaatimukset

  * Sovellus toimii vain HTML5:llä
  * Sovellus vaatii javascriptin

## Työn edistyminen

#### 2. palautus

Työn alku on edistynyt kohtuu hitaasti, koska python on täysin vieras kieli. Tällä hetkellä pystyy rekisteröityä käyttäjäksi ja pystyy lisäämään liikkeitä ja niitä pystyy katselemaan. Myöskin sisään pystyy kirjautumaan. Myöskin eri taulut on suunniteltu. Ilmeisesti tähän asti tehdyt SQL kyselyt on injection-proof. Koska python on niin vieras kieli, niin kaikki moneen fileen refaktorointi ym. tulee menemään varmaankin kurssin loppupuolelle. Priorisoituna nyt käytettävyys ja toimmallisuus.

#### 3. palautus

Työhön on lisätty loputkin tietokantataulut ja näitä hyödyntäviä toiminnallisuuksia on lisätty. Ohjelmaa on myös rikottu selkeämpiin osiin, kuten html templateen ja python tiedostoja on rikottu yhtä asiaa hoitaviin tiedostoihin. Nyt siis voi tehdä erilaisia sarjayhdistelmiä, eli enää vain treenin aikana oleva toiminnallisuus. Myös lomakkeisiin pitäisi lisätä CSRF- haavoittuvuutta estävä toiminnallisuus. 