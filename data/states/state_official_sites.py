import json

# List of states and their official domains
states_and_territories = [
    {"name": "Alabama", "domains": ["alabama.gov", "al.gov"]},
    {"name": "Alaska", "domains": ["alaska.gov"]},
    {"name": "American Samoa", "domains": ["americansamoa.gov"]},
    {"name": "Arizona", "domains": ["arizona.gov", "az.gov"]},
    {"name": "Arkansas", "domains": ["arkansas.gov", "ar.gov"]},
    {"name": "California", "domains": ["ca.gov"]},
    {"name": "Colorado", "domains": ["colorado.gov", "co.gov"]},
    {"name": "Connecticut", "domains": ["ct.gov"]},
    {"name": "Delaware", "domains": ["delaware.gov", "de.gov"]},
    {"name": "District of Columbia", "domains": ["dc.gov"]},
    {"name": "Florida", "domains": ["florida.gov", "fl.gov", "myflorida.gov"]},
    {"name": "Georgia", "domains": ["georgia.gov", "ga.gov"]},
    {"name": "Guam", "domains": ["guam.gov"]},
    {"name": "Hawaii", "domains": ["hawaii.gov", "ehawaii.gov"]},
    {"name": "Idaho", "domains": ["idaho.gov"]},
    {"name": "Illinois", "domains": ["illinois.gov"]},
    {"name": "Indiana", "domains": ["indiana.gov", "in.gov"]},
    {"name": "Iowa", "domains": ["iowa.gov"]},
    {"name": "Kansas", "domains": ["kansas.gov"]},
    {"name": "Kentucky", "domains": ["kentucky.gov", "ky.gov"]},
    {"name": "Louisiana", "domains": ["louisiana.gov", "la.gov"]},
    {"name": "Maine", "domains": ["maine.gov"]},
    {"name": "Maryland", "domains": ["maryland.gov", "md.gov"]},
    {"name": "Massachusetts", "domains": ["massachusetts.gov", "ma.gov", "mass.gov"]},
    {"name": "Michigan", "domains": ["michigan.gov", "mi.gov"]},
    {"name": "Minnesota", "domains": ["minnesota.gov", "mn.gov"]},
    {"name": "Mississippi", "domains": ["mississippi.gov", "ms.gov"]},
    {"name": "Missouri", "domains": ["missouri.gov", "mo.gov"]},
    {"name": "Montana", "domains": ["montana.gov", "mt.gov"]},
    {"name": "Nebraska", "domains": ["nebraska.gov", "ne.gov"]},
    {"name": "Nevada", "domains": ["nevada.gov", "nv.gov"]},
    {"name": "New Hampshire", "domains": ["nh.gov"]},
    {"name": "New Jersey", "domains": ["newjersey.gov", "nj.gov"]},
    {"name": "New Mexico", "domains": ["newmexico.gov", "nm.gov"]},
    {"name": "New York", "domains": ["ny.gov"]},
    {"name": "North Carolina", "domains": ["northcarolina.gov", "nc.gov"]},
    {"name": "North Dakota", "domains": ["northdakota.gov", "nd.gov"]},
    {"name": "Ohio", "domains": ["ohio.gov"]},
    {"name": "Oklahoma", "domains": ["oklahoma.gov", "ok.gov"]},
    {"name": "Oregon", "domains": ["oregon.gov"]},
    {"name": "Pennsylvania", "domains": ["pa.gov"]},
    {"name": "Puerto Rico", "domains": ["pr.gov"]},
    {"name": "Rhode Island", "domains": ["ri.gov"]},
    {"name": "South Carolina", "domains": ["sc.gov"]},
    {"name": "South Dakota", "domains": ["sd.gov"]},
    {"name": "Tennessee", "domains": ["tennessee.gov", "tn.gov"]},
    {"name": "Texas", "domains": ["texas.gov"]},
    {"name": "Utah", "domains": ["utah.gov"]},
    {"name": "Vermont", "domains": ["vermont.gov", "vt.gov"]},
    {"name": "Virgin Islands", "domains": ["vi.gov"]},
    {"name": "Virginia", "domains": ["virginia.gov"]},
    {"name": "Washington", "domains": ["wa.gov"]},
    {"name": "West Virginia", "domains": ["westvirginia.gov", "wv.gov"]},
    {"name": "Wisconsin", "domains": ["wisconsin.gov", "wi.gov"]},
    {"name": "Wyoming", "domains": ["wyoming.gov", "wyo.gov"]}
]

# Example usage: generate main URLs for each state
state_main_sites = []
for state in states_and_territories:
    # Use the first domain as the main site
    main_url = f"https://{state['domains'][0]}"
    state_main_sites.append({"state": state["name"], "url": main_url})

with open("state_main_sites.json", "w", encoding="utf-8") as f:
    json.dump(state_main_sites, f, indent=2, ensure_ascii=False)

# You can now use state_main_sites.json as input for LLM summarization
