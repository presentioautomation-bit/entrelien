# Entrelien — chaîne de fabrication automatique des Carnets

Référence éditoriale : document « bible-production-video » du projet claude.ai *Entrelien* (direction artistique, voix, anonymisation).

## Installation (session neuve)
```bash
mkdir -p /home/claude/prod && cp -r pipeline/lib /home/claude/prod/ && cp -r pipeline/episodes/* /home/claude/prod/
cd /home/claude/prod/lib && for p in fraunces work-sans caveat; do npm pack @fontsource/$p@5 >/dev/null && mkdir -p node_modules/@fontsource/$p && tar xzf fontsource-$p-*.tgz -C node_modules/@fontsource/$p --strip-components 1; done
pip install --break-system-packages -q soundfile playwright scipy numpy pillow
# polices TTF pour vert.py : /home/claude/test/fonts/{caveat,fraunces,work}.ttf (à recréer depuis les .woff2 si absentes)
```
Chrome attendu en `/usr/bin/google-chrome`, ffmpeg dans le PATH.

## Fabriquer un carnet N (dossier /home/claude/prod/cNN)
1. **Texte source** : page https://entrelien.fr/carnets/<slug> (site rendu côté client : lire la page avec un navigateur).
2. **script.json** : 10 à 12 blocs, accroche à suspense en bloc 01 (nuit), bloc 02 « Carnet numéro N. Titre », bascule (phrase-clé) seule dans un bloc précédé de `gaps: 1.6` et listé dans `hush`, décodage, fin « C'était un Carnet de l'Entremetteur. ».
   Règles : pas de lieu ni de région, pas de mention d'inscription sur un site, pas de Presentio, rien d'inventé (pas de prénom, chiffre ou détail absent du carnet).
3. **Voix** : ElevenLabs `creative_generate_speech`, modèle `eleven_v4`, voix `rlqCQzyNTVyUMPGBqC31` (Yann), `generations_count: 1`, un appel par bloc, tous sur un même flow. Télécharger chaque `content_url` (via `creative_get_flow_run_status`) en `tts/XX.mp3` avec curl. ≈ 1 crédit par caractère.
4. `python3 ../lib/timing.py .` → timing.js + vo.wav
5. **film.html** : un plan `sc(id,[blocs],build,render,opts)` par bloc (voir épisodes existants). `P(k)` = début de la k-ième phrase du plan. Nuit : `{night:true}` ; bascule isolée : `{night:true,lead:1.5}`.
6. `bash ../lib/preview.sh .` → tmp/sheet.jpg (planche-contact à vérifier : chevauchements, textes coupés).
7. `python3 ../lib/music.py .` → mix.wav (-14 LUFS) ; `python3 ../lib/render.py .` → film.mp4 (~30 min) ;
   `python3 ../lib/vert.py . N "ligne1|ligne2|ligne3"` → vertical.mp4.

## Publier (Metricool, marque blogId 8111729, fuseau Europe/Paris)
1. Copier le fichier dans ce dépôt (`v/`), commit + push, lien `https://raw.githubusercontent.com/presentioautomation-bit/entrelien/main/v/<fichier>`.
2. `createScheduledPost` avec ce lien : Metricool recopie la vidéo sur static.metricool.com (vérifier que `media` commence par static.metricool.com).
   - YouTube long : type `video`, public, catégorie PEOPLE_BLOGS, madeForKids false, isAiGeneratedContent true, titre « … | Carnet de l'Entremetteur n°N », description avec lien du carnet.
   - Vertical : TikTok (title obligatoire, isAigc true), Instagram REEL (isAiGenerated true), YouTube `short` (isAiGeneratedContent true) avec le lien de la vidéo longue en description.
3. Retirer le fichier du dépôt (commit + push) dès que Metricool l'a recopié.
4. Rythme : une publication tous les 2 jours à 18 h 30.
