# velo-france

Jeu de données de l'étude **« Construire des pistes cyclables ne suffit pas »** : pour chaque commune de France métropolitaine, le linéaire d'aménagements cyclables (Géovélo / OpenStreetMap), la part des actifs qui vont travailler à vélo (Insee) et, pour les 2 626 communes qualifiées, la note du Baromètre vélo 2025 de la FUB. Un second jeu détaille les 20 arrondissements de Paris.

Article : [Construire des pistes cyclables ne suffit pas](https://xj1.fr/blog/construire-des-pistes-cyclables-ne-suffit-pas-2600-communes-et-vingt-arrondissements) (xj1.fr).

Dernière mise à jour des données : octobre 2026.

## Fichiers

| Fichier | Contenu |
|---|---|
| `data/communes-velo.csv` | 34 875 communes : population, km par type d'aménagement (2025), km 2022, km pour 1 000 habitants, part du vélo dans les trajets domicile-travail, notes FUB 2025 |
| `data/paris-arrondissements.csv` | 20 arrondissements : km d'aménagements dédiés (2019, 2022, 2026), population, revenu médian, part du vélo, notes FUB brutes |
| `data/paris-lineaire-annuel.csv` | Km d'aménagements dédiés par arrondissement et par instantané annuel de la Ville de Paris, 2015 à 2026 |
| `scripts/export-communes.sql` | Requête DuckDB qui produit `communes-velo.csv` à partir des fichiers sources |
| `scripts/graphiques.py` | Génération des trois graphiques de l'étude |

## Colonnes de `communes-velo.csv`

| Colonne | Description |
|---|---|
| `code_insee` | Code commune (texte, zéros initiaux conservés) |
| `nom` | Nom de la commune |
| `population` | Population municipale utilisée par Géovélo |
| `km_total_2025` | Total des aménagements cyclables, tous types (km) |
| `km_pistes`, `km_voies_vertes`, `km_bandes`, `km_double_sens`, `km_voies_bus`, `km_mixtes`, `km_autre` | Km par type d'aménagement, 2025 |
| `km_total_2022` | Total en 2022 (km) |
| `km_pour_1000_hab` | `km_total_2025` pour 1 000 habitants |
| `km_proteges_pour_1000_hab` | Pistes cyclables + voies vertes pour 1 000 habitants |
| `part_velo_domicile_travail_pct` | Part des actifs occupés qui vont travailler à vélo (%) |
| `fub_categorie`, `fub_score`, `fub_classe` | Catégorie, note globale sur 5 et classe (A+ à G) du Baromètre 2025 |
| `fub_ressenti`, `fub_securite`, `fub_confort`, `fub_efforts`, `fub_services` | Sous-notes du Baromètre 2025 |
| `fub_score_2019`, `fub_score_2021` | Notes des éditions précédentes quand elles existent |
| `fub_evolution_2021_2025` | Évolution de la note entre 2021 et 2025 (calculée par la FUB) |

Les colonnes `fub_*` sont vides pour les communes non qualifiées par la FUB.

Pour Paris (75056), Lyon (69123) et Marseille (13055), l'Insee publie par arrondissement : la part du vélo est calculée en additionnant les arrondissements.

## Sources

- **Géovélo**, « Linéaire cyclable pour 1000 habitants » (data.gouv.fr, tableau de bord des mobilités durables), ODbL, millésime octobre 2026, d'après OpenStreetMap.
- **FUB**, Baromètre vélo 2025, fichiers « résultats des communes classées » par région publiés sur opendata.parlons-velo.fr, ODbL.
- **Insee**, recensement de la population, mobilités professionnelles (modes de transport des actifs occupés), Licence Ouverte.
- **Ville de Paris**, « Linéaires d'aménagement cyclable » (opendata.paris.fr), ODbL, instantanés annuels 2015-2026.

## Limites

- **Le Baromètre est un sondage de volontaires**, pas un échantillon représentatif. Seules les communes qualifiées par la FUB ont une note.
- **Les kilomètres viennent d'OpenStreetMap.** Une partie de la hausse entre 2022 et 2025 reflète un meilleur relevé. Géovélo a modifié sa méthode de qualification en octobre 2026 (plus de 3 000 km re-typés) : à prendre en compte avant de comparer avec des millésimes antérieurs.
- **`km_autre` représente environ 20 % du linéaire** national et n'est pas un type d'aménagement défini.
- **Les km pour 1 000 habitants pénalisent les villes denses** dont le réseau déborde sur les communes voisines.
- **Part du vélo** : recensement, domicile-travail uniquement, bruité sous 1 000 habitants.
- **Paris par arrondissement** : « aménagements dédiés » = pistes cyclables, voies vertes, vélorues et bandes cyclables, hors bois de Boulogne et de Vincennes. Les notes FUB par arrondissement sont des **moyennes brutes des réponses** (7 791 réponses avec arrondissement) : la moyenne parisienne brute est 3,47 alors que la note officielle de la FUB est 3,67. La colonne `moitie` sépare les dix arrondissements dont le centre est le plus à l'ouest des dix autres ; elle est fortement liée au revenu médian (corrélation de −0,65).
- Deux communes notées par la FUB ont changé de code (49069 Orée d'Anjou, 93059 Pierrefitte-sur-Seine) et ne sont pas rattachées.

## Licence

Ce jeu de données dérive de bases publiées sous **ODbL 1.0** : il est lui-même publié sous [ODbL 1.0](LICENSE). Merci de citer les sources ci-dessus et ce dépôt. Les scripts sont libres de réutilisation.
