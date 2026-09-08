# Extraction de documents PNG par vision

## Objectif

Ce dépôt contient des documents administratifs et juridiques numérisés sous
forme d'images PNG. L'extraction consiste à retranscrire fidèlement le contenu
visible de chaque page avec une IA de vision, puis à enregistrer la
transcription dans un fichier texte correspondant.

Cette méthode repose sur la vision : on lit directement chaque image PNG, on
retranscrit exactement ce qui est visible, et on n'utilise pas un OCR
classique pour produire le résultat final. Le but est de conserver la fidélité
du document original sans modifier son contenu ni sa structure.

Ce guide décrit uniquement cette procédure d'extraction. Il permet à une
autre personne de reprendre le travail sans modifier les images originales.

## Organisation des fichiers

Les images à traiter se trouvent dans un dossier `png` organisé par année et
par document. Les transcriptions sont enregistrées dans un dossier `txt` qui
reprend la même organisation.

Exemple :

```text
Image source :
data/sgg/lois/png/2026/loi-2026-05/loi-2026-05-1.png

Résultat :
data/sgg/lois/txt/2026/loi-2026-05/loi-2026-05-1.txt
```

Le principe est toujours le suivant :

```text
.../png/.../nom-du-document/nom-de-page.png
								 devient
.../txt/.../nom-du-document/nom-de-page.txt
```

Seul le dossier `png` est remplacé par `txt` et l'extension `.png` est
remplacée par `.txt`. Le reste du chemin et le nom du fichier restent
identiques.

Pour les arrêtés, par exemple :

```text
data/sgg/arretes/png/arrete-2018-001/arrete-2018-001-1.png
data/sgg/arretes/txt/arrete-2018-001/arrete-2018-001-1.txt
```

## Prompt d'extraction

Utiliser le prompt suivant pour chaque image :

```text
Retranscris exactement tout ce qui est visible dans l'image, en conservant le
texte imprimé, la ponctuation, les accents, les majuscules, les espaces et les
retours à la ligne tels qu'ils apparaissent.

Ne résume pas, n'interprète pas, ne corrige pas l'orthographe, la grammaire ou
la typographie, et n'ajoute aucun texte qui n'est pas visible dans l'image.

Remplace toute signature manuscrite par [signature]. Remplace chaque numéro
de page visible par [pageN], où N est le numéro réellement visible. Si un
passage est impossible à lire, écris [ILLISIBLE].

Pour les tampons, cachets, sceaux, logos ou annotations manuscrites qui ne
sont pas des signatures, retranscris le texte lisible. Si leur contenu est
illisible, écris [ILLISIBLE].

Respecte l'ordre de lecture et les retours à la ligne visibles. Pour un tableau,
une liste ou une mise en page en colonnes, conserve autant que possible leur
structure avec des espaces et des retours à la ligne. Ne transforme pas le
contenu en tableau Markdown.

Retourne uniquement le texte brut, sans bloc de code, sans commentaire et sans
explication.
```

## Procédure page par page

### 1. Choisir un dossier source

Lister les pages du dossier PNG et vérifier leur ordre numérique :

```bash
find data/sgg/lois/png/2026/loi-2026-05 \
	-maxdepth 1 -type f -name '*.png' -print | sort -V
```

Le même principe s'applique aux arrêtés et aux autres catégories de
documents.

### 2. Ouvrir chaque PNG avec la vision

Traiter les pages une par une, dans l'ordre du nom de fichier. Vérifier
visuellement :

- le titre, le numéro et la date du document ;
- les articles, paragraphes, listes et alinéas ;
- les accents, majuscules et signes de ponctuation ;
- les coupures de texte entre deux pages ;
- les signatures manuscrites et les numéros de page ;
- les passages flous ou masqués.

La page suivante doit reprendre exactement à l'endroit où la page précédente
s'arrête. Il ne faut ni répéter un passage déjà retranscrit, ni supprimer un
passage situé au début ou à la fin d'une page.

### 3. Créer le chemin de sortie

Le dossier TXT correspondant doit reprendre l'arborescence du dossier PNG.
Créer le dossier du document s'il n'existe pas, puis enregistrer un fichier TXT
par page.

Exemple :

```text
PNG : data/sgg/lois/png/2025/loi-2025-15/loi-2025-15-3.png
TXT : data/sgg/lois/txt/2025/loi-2025-15/loi-2025-15-3.txt
```

Le contenu du fichier TXT doit être du texte brut uniquement. Ne pas ajouter
de bloc Markdown, de titre explicatif, de commentaire ou de métadonnées.

### 4. Appliquer les remplacements obligatoires

- Signature manuscrite : `[signature]`
- Numéro de page visible `1` : `[page1]`
- Numéro de page visible `2` : `[page2]`
- Numéro de page visible `N` : `[pageN]`
- Passage impossible à lire : `[ILLISIBLE]`

Le nom imprimé situé sous une signature reste retranscrit. Seule la partie
manuscrite est remplacée par `[signature]`.

### 5. Vérifier le résultat

Après l'extraction, comparer le nombre de PNG et de TXT :

```bash
document='loi-2026-05'
annee='2026'

png_count=$(find "data/sgg/lois/png/$annee/$document" \
	-maxdepth 1 -type f -name '*.png' | wc -l)

txt_count=$(find "data/sgg/lois/txt/$annee/$document" \
	-maxdepth 1 -type f -name '*.txt' | wc -l)

printf 'PNG : %s\nTXT : %s\n' "$png_count" "$txt_count"
test "$png_count" -eq "$txt_count"
```

Vérifier aussi les noms manquants :

```bash
for image in data/sgg/lois/png/2026/loi-2026-05/*.png; do
	base=$(basename "$image" .png)
	test -f "data/sgg/lois/txt/2026/loi-2026-05/$base.txt" || \
		printf 'Transcription manquante : %s\n' "$base"
done
```

Lire ensuite les fichiers TXT dans l'ordre :

```bash
for file in data/sgg/lois/txt/2026/loi-2026-05/*.txt; do
	printf '\n===== %s =====\n' "$file"
	sed -n '1,240p' "$file"
done
```

## Règles de qualité

- Ne jamais modifier, renommer ou écraser les PNG sources.
- Créer un TXT pour chaque PNG, même si la page est presque vide.
- Conserver le même identifiant de page dans le nom du TXT que dans le nom du
	PNG.
- Ne pas fusionner plusieurs pages dans un seul fichier TXT.
- Ne pas ajouter de numéros de page qui ne sont pas visibles.
- Ne pas inventer un mot illisible : utiliser `[ILLISIBLE]`.
- Ne pas corriger le texte juridique, même s'il semble comporter une faute.
- Conserver les coupures de page et la continuité entre les fichiers.
- Vérifier chaque page avec l'image, pas uniquement avec le texte d'une page
	voisine ou d'un document similaire.

## Reprendre un travail existant

Avant de commencer un nouveau dossier, compter les PNG et les TXT :

```bash
find data/sgg/lois/png/2025/loi-2025-15 \
	-maxdepth 1 -name '*.png' | wc -l

find data/sgg/lois/txt/2025/loi-2025-15 \
	-maxdepth 1 -name '*.txt' | wc -l
```

Si les nombres sont différents, rechercher les pages manquantes avec la
commande de comparaison ci-dessus. Relire également les fichiers déjà
présents avant de poursuivre, car une transcription peut exister tout en
contenant une coupure de page incorrecte ou un passage oublié.

## Exemple complet

Pour extraire la page :

```text
data/sgg/lois/png/2026/loi-2026-05/loi-2026-05-1.png
```

1. Ouvrir l'image avec la vision.
2. Envoyer le prompt d'extraction.
3. Copier uniquement la réponse texte dans :

```text
data/sgg/lois/txt/2026/loi-2026-05/loi-2026-05-1.txt
```

4. Vérifier la transcription contre l'image.
5. Recommencer avec `loi-2026-05-2.png`, puis avec les pages suivantes.
6. Comparer finalement le nombre total de PNG et de TXT.
