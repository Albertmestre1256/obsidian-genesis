---
level: protocol-shell
tipo: extraction
descripcion: Extracción estructurada de información de fuentes
---

# Protocol Shell: /extract.information

Plantilla para pedirle a una IA que extraiga información de una fuente (un PDF, una página, un chat) de forma ordenada. Copiala, completá `source`, `schema` y `focus_areas`, y pegala en el chat.

    /extract.information{
        intent="Extraer información estructurada de una fuente",
        input={
            source="<texto|url|archivo>",
            schema="<esquema_esperado>",
            focus_areas=["<area1>", "<area2>"]
        },
        process=[
            /analyze.structure{identify=["sections", "arguments", "evidence"]},
            /extract.entities{types=["people", "organizations", "dates", "metrics"]},
            /extract.claims{require_evidence=true},
            /validate.consistency{cross_reference=true}
        ],
        output={
            structured_data="<JSON segun schema>",
            confidence_scores="<por campo>",
            gaps="<lista de info faltante>"
        }
    }
