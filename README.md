# TKT20019
HY Tietokannat ja web-ohjelmointi harjoitus
Ravintolasovellusta mukaillen Elokuvasovellus
Sovelluksessa näkyy elokuvia, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.
1. Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
2. Käyttäjä näkee elokuvat listana (tai tuotantomaan mukaan kartalla) ja voi painaa elokuvasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus, kesto, genre, ohjaaja, käsikirjoittaja jne.).
3. Käyttäjä voi antaa arvion (tähdet ja kommentti) elokuvasta ja lukea muiden antamia arvioita.
4. Käyttäjä voi etsiä kaikki elokuvat, joiden kuvauksessa (tai metatiedoissa) on annettu sana.
5. Käyttäjä näkee myös listan, jossa elokuvat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
6. Ylläpitäjä voi lisätä ja poistaa elokuvia sekä määrittää elokuvasta näytettävät tiedot.
7. Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
8. Ylläpitäjä voi luoda ryhmiä, joihin elokuvia voi luokitella. Elokuva voi kuulua yhteen tai useampaan ryhmään.

Tilanne 7.4.2024
Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
Tarkoitus vielä rajoittaa että vain admin-tunnuksella voi luoda uusia tunnuksia.
/admin sivulla voi käydä luomassa itselleen tunnukset, kun niitä ei vielä aluksi ole.

Sovelluksen pohjana on pitkälti käytetty kurssilla esimerkkinä käytettyä kyselysovellusta, ja tämä näkyy vielä räikeästi koodissa, html-sivuissa, taulukoissa jne.

Elokuvia pystyy syöttämään ja antamaan näille tietoja. Näistä muodostuu listaa. Muuten suunnitellut ominaisuudet vielä toteuttamatta tai alkutekijöissä.

Käynnistysohjeet:

Lataa repositorio ja siirry sen juurikansioon. Luo kansioon .env-tiedosto (uusi tyhjä tiedosto ja nimeksi vain .env) ja määritä siihen:
DATABASE_URL= (todennäköisesti muotoa postgresql:///käyttäjänimesi)
SECRET_KEY= 

Ohjelman saat käyntiin näillä komennoilla

cd kansionmissäsijaitsee
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
psql < schema.sql
flask run