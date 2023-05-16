# Genelex
Au
lieu de développer l'ensemble des variantes à partir d'un dictionnaire
de base pour créer un dictionnaire étendu, nous allons chercher à
appliquer des règles de variation aux mots du texte qui n'ont pas été
reconnus par un dictionnaire de base lors du processus d'étiquetage (a)
pour générer (b) uniquement les formes nécessaires.

Nous utilisons Corpindex, un outil que nous avons développé et qui
permet de projetter (i) des dictionnaires (ii) des règles de
transduction sur du texte brut.

## Discussion

L'objectif est double : associer à une forme inconnue des informatons
morpho syntaxique et sémantique.

Le principe qui consiste à essayer de rapprocher une forme inconnue,
mais localement régulière, permet de produire une liste ordonnée de
proposition. Quelque soit l'algorithme utilisé les propositions ne sont
par obligatoirement valides. Le classement effectué permet de faire une
proposition mais sans aucune garantie de la justesse du résultat. .

La prerformance de ce type de méthode dépend donc de l'algorithme mais
également de la mesure de similarité associée. A ces deux paramètres il
faut également ajouter la source à partir de laquelle on cherche des
similarités.

La plupart des correcteurs orthographiques fonctionnent par distance
d'édition, c'est-à-dire par calcul du nombre de modification à affectuer
pour aller d'une forme initiale à une forme finale. Ce passage se fait
par insertion, suppression ou remplacement de caractère.

Le calcul similarité peut être ajusté et il est possible d'avoir deux
mesures identiques pour deux formes candidates diffrentes. Dans ce cas
là il n'est pas possible de choisir.

Les résultats obtenus ici se base donc sur les paramètres suivants :

-   Dictionnaires : l'objectif est d'identifier le plus de mots, nous
    utilisons donc des dictionnaires de formes de français moderne et de
    français médiéval. Plus on ajoute de dictionnaires plus les
    candidats sont éparpillés

## Ressources

Les dictionnaires ont donc une hiérarchie, nous appellerons
*dictionnaires de base* les ressources les plus générales et les plus
normatives. Ce sont elles qui contiendront ce que nous avons appelé les
*hyperlemmes*. Ils sont constitués des trois ressources distincts :

-   un dictionnaire général en langue moderne ;

-   un dictionnaire de langue médiévale (lemmes) ;

-   un dictionnaire de langue médiévale (formes fléchies).

Notre objectif est d'avoir un ensemble le plus restreint possible, les
variantes étant générées par des règles (cf. infra). Nous avons donc
ajouté, dans la nomenclature, une étiquette « *Dictionnaire* ».

Dans la perspective de devoir lever les ambiguïtés après projection de
la ressource, il ne nous semble pas anodin de pouvoir déterminer si une
forme est présente dans les deux lexiques, ou bien dans un seul des deux
et de savoir dans lequel. Les dictionnaires comportent donc les
informations suivantes : forme, lemme, catégorie morpho-syntaxique,
identifiant du dictionnaire.

#### Dictionnaire général

Il s'agit d'un dictionnaire de langue moderne[^12] auquel nous
appliquons un certain nombre de modifications :

1.  suppression des diacritiques ;

2.  suppression des formes anachroniques.

Le résultat obtenu est un dictionnaire de $270~834$ formes ;
l'identifiant du dictionnaire est `Dg`.

#### Sacregraal

Ce dictionnaire se compose de la réunion des deux lexiques de
l'ancien-français : le Tobler-Lommatzsch, Altfranzösisches Wörterbuch et
le Dictionnaire de l'ancien français de Godefroy. La nomenclature de
l'ouvrage de Frédéric Godefroy qui ouvre plus de $160~000$ entrées
empruntées à tous les dialectes et tous les vocabulaires de l'ancienne
langue. Le lexique Tobler, Lommatszch et Christman dans la version
révisée par les éditeurs de la version électronique intègre dans les
entrées plus de $30~000$ variantes renvoyant à d'autres entrées. Tout
comme le dictionnaire général nous supprimons les diacritiques et nous
regroupons sous une seule étiquette les identifiants de dictionnaire
(« `T` », « `G` », « `T:G` » resp. Tobler-Lommatzsch, Godefroy et les
deux).

#### Verbes

Nous avons, dans un premier temps extrait des deux précédentes
ressources les verbes du premier groupe (sélectionnés à partir de la
terminaison en *-er*). Nous utilisons ensuite
Proteus [@art_FabIss2015a], un moteur de flexion pouvant manipuler les
caractères d'une chaîne via un *code proteus*. Celui-ci intègre les
différentes variantes du français entre le 9$^e$ et le 13$^e$ siècle
pour le présent. les résultats sont de la forme :

    aacieies   aacier
    aacieit    aacier
    aaciiiens  aacier
    aaciiiez   aacier
    aacieient  aacier
    aacioie    aacierx

Nous obtenons une liste de $565~876$ flexions verbales ; l'identifiant
du dictionnaire est `Pr`.

#### Variantes phonologique

Cette ressource va permettre d'effectuer des transformations sur des
mots pour obtenir des variantes *possibles* par rapport à des variations
phonologiques. Ces règles sont de la forme :

::: center
`motif de caractères` $\rightarrow$
`liste de chaînes de caractères de remplacement`
:::

Le *motif de caractères* est exprimé sous forme d'une expression
régulière, les différents éléments de la liste de remplacement sont
séparés par le caractère « `|` ». il est possible d'utiliser la totalité
du langage des expressions régulières, cela signifie qu'il est par
exemple possible d'indiquer un contexte, droit ou gauche, d'application
de la règle. La règle :

    (ch|w|qu?|c?[cq]|k)(?=[a-tv-z]) ch|q|w|qu|c|cq|cc|k

permet ainsi d'obtenir un ensemble de variantes quand sont reconnus *ch*
ou *w* ou *qu* *q* ou *c* ou *cq* ou *k* suivis par un caractère qui
n'est pas un *u*. Cette méthode permet d'exprimer un grand nombre de
règles sous une forme compacte. L'application de cette règle sur le mot
*cheval* donne le résultat suivant.

::: center
  mot      sous-règle          variante générée
  -------- ------------------- ------------------
  cheval   ch -> k    keval
  cheval   ch -> w    weval
  cheval   ch -> c    ceval
  cheval   c -> cc    ccheval
  cheval   l -> ll    chevall
  cheval   ch -> cc   cceval
  cheval   ch -> q    qeval
  cheval   ch -> qu   queval
  cheval   ch -> cq   cqeval
:::

Notre ressource comporte à ce jour $44$ méta-règles plus les règles
concernant le doublement de consonnes.
