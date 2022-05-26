def strip_bbr_tag(tag: str) -> str:
    return tag.replace("{http://data.gov.dk/schemas/bbr}", "")


def format_bbr_tag(tag: str) -> str:
    """
    """
    return "{http://data.gov.dk/schemas/bbr}" + tag


USEFUL_COLS = [
    "{http://data.gov.dk/schemas/bbr}husnummer",
    "{http://data.gov.dk/schemas/bbr}byg021BygningensAnvendelse",
    "{http://data.gov.dk/schemas/bbr}byg056Varmeinstallation",
    "{http://data.gov.dk/schemas/bbr}byg057Opvarmningsmiddel",
    "{http://data.gov.dk/schemas/bbr}byg404Koordinat",
    "{http://data.gov.dk/schemas/bbr}byg406Koordinatsystem",
    "{http://data.gov.dk/schemas/bbr}byg134KvalitetAfKoordinatsæt",
    "{http://data.gov.dk/schemas/bbr}virkningFra",
    "{http://data.gov.dk/schemas/bbr}registreringFra",
    "{http://data.gov.dk/schemas/bbr}byg094Revisionsdato",
    "{http://data.gov.dk/schemas/bbr}byg024AntalLejlighederMedKøkken",
    "{http://data.gov.dk/schemas/bbr}byg025AntalLejlighederUdenKøkken",
    "{http://data.gov.dk/schemas/bbr}kommunekode",
    "{http://data.gov.dk/schemas/bbr}ejerlejlighed",
]

CLEAN_USEFUL = [strip_bbr_tag(col) for col in USEFUL_COLS]
