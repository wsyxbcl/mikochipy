from calcmass.mass import massof
# draft of the data structure

def ideal_cap(molar_mass, num_electron):
    """
    Calculate theoretical capacity of material based on 
    molar mass and number of available electrons
    """
    ideal_cap = (num_electron * 96485 * 1000) / (3600 * molar_mass) # mAh/g
    return ideal_cap

active_material = {
    "id": "test_am",
    "comment": "none",
    "formula": "Li2RuO3",
    "electrons": 2 # available electrons
}

slurry = {
    "id": "test_slurry",
    "am": {
        "id": "test_am",
        "mass": 0.05 # unit: g
    },
    "binder":{
        "type": "pvdf/nmp",
        "c": 1 / 11, # mass concentration
        "mass": 0.06875 # unit: g
    },
    "conduct":{
        "type": "acetylene black",
        "mass": 0.00625 # unit: g
    }
}

electrode = {
    "id": "test_electrode",
    "slurry": "test_slurry",
    "current_collector":{
        "type": "Al",
        "mass": 0.0418 # unit:g
    },
    "mass": 0.0435 # unit: g
}

am_ratio = 0.8
# c_rate = 0.1 # h^-1
current_density = 50 # mA/g
mass_am = (electrode['mass'] - electrode['current_collector']['mass']) * am_ratio
# amp_rate = ideal_cap(massof(active_material["formula"]), active_material['electrons']) * c_rate * mass_am * 0.001 # A
charge_current = current_density * 0.001 * mass_am
# print(amp_rate)
print(charge_current)