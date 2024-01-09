# Plan generation
- Comandi del tipo `terraform -chdir=terraform/ plan -input=false -out=plan.tfplan` non producono proprio plan.tfplan in caso di errori, quindi non c'è la possibilità di capire se un errore è stato generato.
- - **UPDATE**: se si genera il piano con l'opzione `-json` è possibile avete un output contenga la presenza di errori:
```json
{
  "@level": "info",
  "@message": "Terraform 1.6.6",
  "@module": "terraform.ui",
  "@timestamp": "2023-12-27T16:07:08.536482+01:00",
  "terraform": "1.6.6",
  "type": "version",
  "ui": "1.2"
}
{
  "@level": "error",
  "@message": "Error: Missing required argument",
  "@module": "terraform.ui",
  "@timestamp": "2023-12-27T16:07:11.836901+01:00",
  "diagnostic": {
    "severity": "error",
    "summary": "Missing required argument",
    "detail": "\"instance_type\": one of `instance_type,launch_template` must be specified",
    "address": "aws_instance.my_instance",
    "range": {
      "filename": "main.tf",
      "start": {
        "line": 9,
        "column": 39,
        "byte": 131
      },
      "end": {
        "line": 9,
        "column": 40,
        "byte": 132
      }
    },
    "snippet": {
      "context": "resource \"aws_instance\" \"my_instance\"",
      "code": "resource \"aws_instance\" \"my_instance\" {",
      "start_line": 9,
      "highlight_start_offset": 38,
      "highlight_end_offset": 39,
      "values": []
    }
  },
  "type": "diagnostic"
}
```

# Plan validation
- Togliere i nomi dei blocchi prima di comparare i piani potrebbe essere una buona soluzione
- Magari non fare controllo 1:1 -> Per ogni oggetto del plan_target['configuration'] controllare che ci sia un corrispettivo nel piano generato.


# In generale
Molti test di azure probabilmente falliranno dato che molte risorse, anche quelle "semplici", richiedono una o più dipendenze verso altre risorse.