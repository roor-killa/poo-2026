

Pour executer le code dans rci_scraper : utilise python -m scrapers.rci_scraper dans le dossier src



Structure :

Scrap "https://rci.fm/deuxiles/infos/toutes-les-infos" 

et https://rci.fm/deuxiles/infos/Caraibes/[L'article concerner] de tous les articles dans la premiere page du scrap


Pour recuperer le lien d'un article : 
Chercher les div avec le role = 'article' et le lien relatif a https://rci.fm/ est dans l'attribut about



Pour le titre:
h1 : itemprop="name"

Pour l'info / petit description :
p : class="infi"


Pour le contenu de l'article : 
div : id="contenu-article" itemprop="articleBody description"






INTEGRER LES DONNEES DANS UNE BASE POSTGRESQL