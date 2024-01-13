# Risultati

Legenda: 
- 0: Non supera il validation test
- 1: Solo compilazione valida
- 2: Plan valido
- 3: codice sintatticamente corretto ma validate faila per colpa di un attributo
- 4: Plan valido solo se subset
- ?: Da rivedere
- *: vedi se cambiare il prompt.
## Codeonly-T06

- *apigatewayv2_api: 11001211010111101021
- *dynamodb_table:  00000000000000000000
- iam_role:         22222222202222222202
- instance:         22200202220022000002; Gli "0" sono per la presenza di soli '# Hello world'.
- lambda:           RIFAI TEST SENZA L'USO DI CACHE E modifica prompt: Anziché 'Also provide the aws provider' sostituisci 'provide' con 'set up'.
- lambda_hard:      42002002022202000022
- lb:               11111111111111111111
- lb_hard:          33311111123331112000; Gli zeri sono solo perché scrive 'type' anziché 'load_balancer_type' e per 'Hello world'.
- aws_provider:     022202222000020222202; Ci sono molti zeri perché il modello non produceva letteralmente nulla. Dovrei togliere l'uso della cache.
- s3_bucket:        0000000002-----; Cose a caso, sai senza senza cache e cambia prompt.
- vpc:              22222222220222222222;
- function_app_hard:01000000000000000000; Scriveva site_config { {} } anziché site_config {}
- provider_block_azure: 00022021111111200000; Non mette "features {}".
- resource_group:   11111111200020200000; Zeri: "# Hello world".
- security_group:   00000022220102122122; Zeri: "# Hello world" e provider azure senza features {}.
- storage_account:  00022002020202000200; Zeri: "# Hello world". Rifai senza cache.
- subnet:           02000000000000020200; Zeri: "# Hello world". Vedi se rifare senza cache.
- virtual_network:  02222202202211112121; Zeri: Due/tre hello world, più provider senza features {}.
- cloudfunctions2_function: 22111111111111111211; Infenta parametri che non esistono.
- compute_firewall: 22111212222202122222; Zeri: hello world.
- compute_instance: 22222020202222222222; Zeri: hello world.
- compute_subnetworks:   11111111111111111112; Uni: Scriveva google compute network come data block anziché resource -> Vedi se rifare senza cache. 
- google_prov_block:22022022202022222220: Zeri: non scriveva letteralmente nulla.
- sql_database:     RIFAI CON NUOVO PROMPT
- storage_bucket:   22212222202220020222; Zeri: hello world e cose a caso.
- storage_bucket_website:   00000000000100000000; Zeri: hello world, vedi se rifare senza cache.


## Mix-T06
- *apigatewayv2_api: 3333322333332323331; Se il codice contiene un attributo "provider" non funziona nemmeno validate, ma il codice è sintatticamente corretto.
- dynamodb_table:   21221022222222122222
- iam_role:         22212222222222222112
- instance:         22124241412222431122
- lambda:           RIFAI TEST SENZA L'USO DI CACHE E modifica prompt: Anziché 'Also provide the aws provider' sostituisci 'provide' con 'set up'.
- lambda_hard:      01220111011111411111
- lb:               22222222202202224222
- lb_hard:          32223332322233233323
- aws_provider:     00000000000000000000; Produceva output a caso, cambia prompt.
- s3_bucket:        0000000002-----; Cose a caso, fai senza cache e con prompt diverso.
- vpc:              24222222222210222224
- function_app_hard:00000000000000000000; Zeri: come in codeonly.
- provider_block_azure: 00000220022042200000; Scrive cose a caso negli stippet hcl ma senza senso.
- resource_group:   22222222222222222222;
- security_group:   22222222222222222222;
- storage_account:  22222222222242222220;
- subnet:           11111111111111111112; Zeri: Scrive address_prefix = VALORE, anziché address_prefixes = [VALORE]
- virtual_network:  22222222222212222221: Zeri: provider senza features {}.
- cloudfunctions2_function: 111111111111111111111; Scrive parametri max_instance_count e altri come parametri sfusi, anziché in service_config {}.
- compute_firewall: 22224221222222242222. Solo 1 di questi test ha l'attributo "name" settato correttamente. L'ha generato a caso.
- compute_instance: 22222222222222222222;
- compute_subnetworks:   22211122212211211221; Uni: scrive "google_compute_network.vpc.self_link" anziché "google_compute_network.vpc.id".
- google_prov_block:00000000000000000000; Scrive cose a caso prima dell'effettivo codice, tipo ' nobody knows what you're doing. 
 Please provide a full example of your code. 
 The provider block alone is not enough to create a Terraform configuration.'.
- sql_database:    RIFAI CON NUOVO PROMPT.
- storage_bucket:  22212222222222222222
- storage_bucket_website:   12211111112212210121; Uni: scriveva '"*"' anziché '["*"]'.

# Considerazioni
- Alcuni test fallivano perché il prompt non era costruito in modo perfetto: ad esempio in aws_lb veniva erroneamente generato l'attributo "type" e non load_balancer_type
- Per funzionare è stato necessario mettere le credenziali dei provider che li richiedevano nelle variabili d'ambiente.
- Modificare la tesi nel capitolo 3 dove parlo di validate e sostituisci con 'fmt', altrimenti i risultati di compile_check e functional_correctness saranno uguali.
- I modelli, tendenzialmente, non riescono a capire se un attributo(o risorsa) non specificata nel prompt dipende da un altro, e quindi sarebbe necessario crearla. Inoltre non riesce sempre a capire che un attributo vada all'interno di una struttura struct { } a meno che non lo si specifichi nel prompt. Altre volte riescono capire che per alcuni attributi, tipo la regione/zona, crea un blocco provider anziché mettere quei dati negli attributi della risorsa/e (plus).
- A volte i modelli si inventano gli attributi se trovano delle keyword particolari nel prompt: come scrivere "google_compute_network.vpc.self_link" anziché "google_compute_network.vpc.id" se nel prompt c'è scritto '[...] and its network is linked to the vpc id.'
- A volte il modello mix, specialmente per i test relativi ai blocchi provider, scrive cose senza senso prima della definizione del codice del provider(che è corretto), facendo fallire i test. Tuttavia molti test dove è stato necessario il blocco provider sono stato compiuti senza questi problemi. Vedi provider_block_google/generated/mix_T06/output_1.

# Test corretti e non
Se il controllo del plan non avveniva con successo (fallimenti), i test venivano comunque considerati corretti se:
- Alcuni attributi, tipo la regione/zona, crea un blocco provider anziché mettere quei dati negli attributi della risorsa/e (plus).
- Se un attributo doveva essere "X", il codice generato prevedeva l'uso di una variabile, comunque inizializzata con il valore corretto ("X").
- Negli attributi tipo "name" compariva un suffisso/prefisso generato automaticamente, per dargli un id randomico. Tipo: 'name = "my-instance-${local.name_suffix}"'
- Un test è considerato corretto per il compile check se `terraform fmt` non da errori.