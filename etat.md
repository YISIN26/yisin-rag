# État de l’extraction par vision

Ce fichier suit uniquement l’extraction des images PNG vers des fichiers TXT
par retranscription avec la vision.

## Règle de correspondance

Un fichier source :

```text
data/<categorie>/png/<annee>/<document>/<page>.png
```

produit une transcription ici :

```text
data/<categorie>/txt/<annee>/<document>/<page>.txt
```

Pour les dossiers sans année :

```text
data/<categorie>/png/<document>/<page>.png
→ data/<categorie>/txt/<document>/<page>.txt
```

Un dossier est considéré comme **traité** lorsque chaque PNG possède son TXT
correspondant.

## Structure du projet

```text
data/
├── inclu/
│   ├── accords/
│   └── decisions/
├── legis/
└── sgg/
    ├── arretes/
    │   ├── png/
    │   └── txt/
    ├── cm/
    │   ├── png/
    │   └── txt/
    ├── decrets/
    ├── lois/
    │   ├── png/
    │   └── txt/
    └── ordonnances/
```

## Dossiers traités

### `data/sgg/arretes/`

```text
arretes/
├── png/
│   ├── arrete-2018-001/
│   └── arrete-2018-002/
└── txt/
    ├── arrete-2018-001/
    └── arrete-2018-002/
```

| Dossier | PNG | TXT | État |
|---|---:|---:|---|
| `arrete-2018-001` | 2 | 2 | Traité |
| `arrete-2018-002` | 2 | 2 | Traité |

### `data/sgg/lois/`

#### Année 2025

```text
lois/
├── png/
│   └── 2025/
│       ├── loi-2025-04/
│       ├── loi-2025-07/
│       ├── loi-2025-08/
│       ├── loi-2025-11/
│       ├── loi-2025-12/
│       ├── loi-2025-13/
│       ├── loi-2025-15/
│       ├── loi-2025-17/
│       └── loi-2025-18/
└── txt/
    └── 2025/
        ├── loi-2025-04/
        ├── loi-2025-07/
        ├── loi-2025-08/
        ├── loi-2025-11/
        ├── loi-2025-12/
        ├── loi-2025-13/
        ├── loi-2025-15/
        ├── loi-2025-17/
        └── loi-2025-18/
```

| Dossier | PNG | TXT | État |
|---|---:|---:|---|
| `loi-2025-04` | 2 | 2 | Traité |
| `loi-2025-07` | 3 | 3 | Traité |
| `loi-2025-08` | 3 | 3 | Traité |
| `loi-2025-11` | 3 | 3 | Traité |
| `loi-2025-12` | 2 | 2 | Traité |
| `loi-2025-13` | 2 | 2 | Traité |
| `loi-2025-15` | 6 | 6 | Traité |
| `loi-2025-17` | 4 | 4 | Traité |
| `loi-2025-18` | 5 | 5 | Traité |

**Total 2025 traité : 30 PNG et 30 TXT.**

#### Année 2026

```text
lois/
├── png/
│   └── 2026/
│       ├── loi-2026-01/
│       ├── loi-2026-04/
│       ├── loi-2026-05/
│       ├── loi-2026-12/
│       ├── loi-2026-13/
│       └── loi-2026-14/
└── txt/
    └── 2026/
        ├── loi-2026-01/
        ├── loi-2026-04/
        ├── loi-2026-05/
        ├── loi-2026-12/
        ├── loi-2026-13/
        └── loi-2026-14/
```

| Dossier | PNG | TXT | État |
|---|---:|---:|---|
| `loi-2026-01` | 18 | 18 | Traité |
| `loi-2026-04` | 2 | 2 | Traité |
| `loi-2026-05` | 4 | 4 | Traité |
| `loi-2026-12` | 2 | 2 | Traité |
| `loi-2026-13` | 3 | 3 | Traité |
| `loi-2026-14` | 2 | 2 | Traité |

**Total 2026 traité : 31 PNG et 31 TXT.**

## Synthèse générale

| Catégorie | Dossiers traités | PNG traités | TXT produits |
|---|---:|---:|---:|
| `sgg/arretes` | 2 | 4 | 4 |
| `sgg/lois/2025` | 9 | 30 | 30 |
| `sgg/lois/2026` | 6 | 31 | 31 |
| **Total** | **17** | **65** | **65** |

## Dossiers restant à traiter

### Lois 2025

Les dossiers PNG suivants existent, mais ne possèdent pas encore de TXT
correspondant :

| Dossier | PNG à traiter |
|---|---:|
| `loi-2025-01` | 20 |
| `loi-2025-02` | 25 |
| `loi-2025-03` | 11 |
| `loi-2025-05` | 34 |
| `loi-2025-06` | 18 |
| `loi-2025-09` | 17 |
| `loi-2025-14` | 58 |
| `loi-2025-16` | 142 |
| `loi-2025-19` | 25 |
| `loi-2025-20` | 10 |

**Total restant 2025 : 360 PNG.**

### Lois 2026

| Dossier | PNG à traiter |
|---|---:|
| `loi-2026-15` | 31 |
| `loi-2026-16` | 72 |

**Total restant 2026 : 103 PNG.**

### Autres catégories

Les catégories suivantes possèdent des sources PNG, mais aucun dossier TXT
correspondant dans le suivi de cette extraction vision :

- `data/sgg/cm/png/`
- `data/sgg/lois/png/` pour les dossiers listés comme restant à traiter
- `data/sgg/ordonnances/png/`
- `data/legis/png/`

Le dossier `data/sgg/cm/txt/` contient déjà des sorties TXT pour certains
comptes rendus, mais elles ne sont pas incluses dans les totaux de cette
extraction vision des arrêtés et des lois.

## Vérifier l’état d’un dossier

```bash
document='loi-2026-05'
annee='2026'

png_count=$(find "data/sgg/lois/png/$annee/$document" \
  -maxdepth 1 -type f -name '*.png' | wc -l)

txt_count=$(find "data/sgg/lois/txt/$annee/$document" \
  -maxdepth 1 -type f -name '*.txt' | wc -l)

printf 'PNG : %s\nTXT : %s\n' "$png_count" "$txt_count"
```

Pour identifier une page manquante :

```bash
for image in data/sgg/lois/png/2026/loi-2026-05/*.png; do
  base=$(basename "$image" .png)
  test -f "data/sgg/lois/txt/2026/loi-2026-05/$base.txt" || \
    printf 'TXT manquant : %s\n' "$base"
done
```

Mettre à jour ce fichier après chaque dossier terminé en reportant le nombre
de PNG et de TXT, puis en actualisant les totaux.
